import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.integrate import quad

st.set_page_config(page_title="Black–Scholes & Heston Option Lab", layout="wide")
st.title("📊 Black–Scholes & Heston Option Pricing Lab")
st.caption("Pricing, Greeks, Monte Carlo, and volatility smiles")

# ==========================================================
# Black–Scholes
# ==========================================================

def bs_price(S, K, T, r, sigma, option="call"):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if option == "call":
        return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:
        return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)


def bs_greeks(S, K, T, r, sigma, option="call"):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    pdf = norm.pdf(d1)

    delta = norm.cdf(d1) if option == "call" else norm.cdf(d1) - 1
    gamma = pdf / (S * sigma * np.sqrt(T))
    vega = S * pdf * np.sqrt(T)
    theta = (
        - (S * pdf * sigma) / (2 * np.sqrt(T))
        - r * K * np.exp(-r * T) * (norm.cdf(d2) if option == "call" else norm.cdf(-d2))
    )

    return delta, gamma, vega, theta

# ==========================================================
# Heston model
# ==========================================================

def heston_cf(phi, S, T, r, kappa, theta, sigma, rho, v0, j):
    i = 1j
    u = 0.5 if j == 1 else -0.5
    b = kappa - rho * sigma if j == 1 else kappa
    a = kappa * theta

    d = np.sqrt((rho * sigma * phi * i - b)**2 - sigma**2 * (2 * u * phi * i - phi**2))
    g = (b - rho * sigma * phi * i + d) / (b - rho * sigma * phi * i - d)

    C = r * phi * i * T + a / sigma**2 * ((b - rho * sigma * phi * i + d) * T - 2 * np.log((1 - g * np.exp(d * T)) / (1 - g)))
    D = (b - rho * sigma * phi * i + d) / sigma**2 * ((1 - np.exp(d * T)) / (1 - g * np.exp(d * T)))

    return np.exp(C + D * v0 + i * phi * np.log(S))


def heston_prob(j, S, K, T, r, kappa, theta, sigma, rho, v0):
    integrand = lambda phi: np.real(np.exp(-1j * phi * np.log(K)) * heston_cf(phi, S, T, r, kappa, theta, sigma, rho, v0, j) / (1j * phi))
    val, _ = quad(integrand, 0, 100)
    return 0.5 + val / np.pi


def heston_price(S, K, T, r, kappa, theta, sigma, rho, v0, option="call"):
    P1 = heston_prob(1, S, K, T, r, kappa, theta, sigma, rho, v0)
    P2 = heston_prob(2, S, K, T, r, kappa, theta, sigma, rho, v0)
    call = S * P1 - K * np.exp(-r * T) * P2
    return call if option == "call" else call - S + K * np.exp(-r * T)

# ==========================================================
# Heston Monte Carlo
# ==========================================================

def heston_mc(S, K, T, r, kappa, theta, sigma, rho, v0, paths=5000, steps=200, option="call"):
    dt = T / steps
    S_t = np.full(paths, S)
    v_t = np.full(paths, v0)

    for _ in range(steps):
        z1 = np.random.normal(size=paths)
        z2 = rho * z1 + np.sqrt(1 - rho**2) * np.random.normal(size=paths)

        v_t = np.maximum(v_t + kappa * (theta - v_t) * dt + sigma * np.sqrt(v_t * dt) * z2, 0)
        S_t *= np.exp((r - 0.5 * v_t) * dt + np.sqrt(v_t * dt) * z1)

    payoff = np.maximum(S_t - K, 0) if option == "call" else np.maximum(K - S_t, 0)
    return np.exp(-r * T) * payoff.mean()

# ==========================================================
# Sidebar inputs
# ==========================================================

st.sidebar.header("Option")
S = st.sidebar.slider("Spot", 50.0, 150.0, 100.0)
K = st.sidebar.slider("Strike", 50.0, 150.0, 100.0)
T = st.sidebar.slider("Maturity (years)", 0.1, 3.0, 1.0)
r = st.sidebar.slider("Rate", 0.0, 0.1, 0.05)
option = st.sidebar.selectbox("Type", ["call", "put"])

st.sidebar.header("Black–Scholes")
sigma_bs = st.sidebar.slider("Volatility", 0.05, 0.6, 0.2)

st.sidebar.header("Heston")
kappa = st.sidebar.slider("κ", 0.1, 5.0, 2.0)
theta = st.sidebar.slider("θ", 0.01, 0.2, 0.04)
sigma_h = st.sidebar.slider("σ (vol of vol)", 0.1, 1.0, 0.5)
rho = st.sidebar.slider("ρ", -0.9, 0.0, -0.7)
v0 = st.sidebar.slider("v₀", 0.01, 0.2, 0.04)

# ==========================================================
# Pricing results
# ==========================================================

bs = bs_price(S, K, T, r, sigma_bs, option)
heston = heston_price(S, K, T, r, kappa, theta, sigma_h, rho, v0, option)
mc = heston_mc(S, K, T, r, kappa, theta, sigma_h, rho, v0, option=option)

st.subheader("💰 Prices")
st.metric("Black–Scholes", f"{bs:.4f}")
st.metric("Heston (closed form)", f"{heston:.4f}")
st.metric("Heston (Monte Carlo)", f"{mc:.4f}")

# ==========================================================
# Greeks
# ==========================================================

delta, gamma, vega, theta_g = bs_greeks(S, K, T, r, sigma_bs, option)

st.subheader("🧮 Black–Scholes Greeks")
st.write({"Delta": delta, "Gamma": gamma, "Vega": vega, "Theta": theta_g})

# ==========================================================
# Plots
# ==========================================================

st.subheader("📈 Price vs Strike")
strikes = np.linspace(60, 140, 40)
bs_curve = [bs_price(S, k, T, r, sigma_bs, option) for k in strikes]
h_curve = [heston_price(S, k, T, r, kappa, theta, sigma_h, rho, v0, option) for k in strikes]

fig1 = plt.figure()
plt.plot(strikes, bs_curve, label="Black–Scholes")
plt.plot(strikes, h_curve, label="Heston")
plt.legend()
st.pyplot(fig1)

st.subheader("🌈 Implied Vol Smile (Heston)")

ivs = []
for k in strikes:
    price = heston_price(S, k, T, r, kappa, theta, sigma_h, rho, v0, option)
    vol = sigma_bs
    for _ in range(20):
        vol -= (bs_price(S, k, T, r, vol, option) - price) / max(1e-5, bs_greeks(S, k, T, r, vol, option)[2])
    ivs.append(vol)

fig2 = plt.figure()
plt.plot(strikes, ivs)
st.pyplot(fig2)
