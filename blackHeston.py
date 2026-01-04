import streamlit as st
import numpy as np
from scipy.stats import norm
from scipy.integrate import quad

st.set_page_config(page_title="Option Pricing: Black–Scholes & Heston", layout="centered")

st.title("📈 Option Pricing Models")
st.write("Black–Scholes and Heston model pricing for European options")

# -----------------------------
# Black–Scholes Model
# -----------------------------

def black_scholes_price(S, K, T, r, sigma, option_type="call"):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == "call":
        return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:
        return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

# -----------------------------
# Heston Model (Semi-closed form)
# -----------------------------

def heston_char_func(phi, S, K, T, r, kappa, theta, sigma, rho, v0, j):
    i = complex(0, 1)
    a = kappa * theta
    u = 0.5 if j == 1 else -0.5
    b = kappa - rho * sigma if j == 1 else kappa

    d = np.sqrt((rho * sigma * phi * i - b)**2 - sigma**2 * (2 * u * phi * i - phi**2))
    g = (b - rho * sigma * phi * i + d) / (b - rho * sigma * phi * i - d)

    C = r * phi * i * T + (a / sigma**2) * ((b - rho * sigma * phi * i + d) * T - 2 * np.log((1 - g * np.exp(d * T)) / (1 - g)))
    D = ((b - rho * sigma * phi * i + d) / sigma**2) * ((1 - np.exp(d * T)) / (1 - g * np.exp(d * T)))

    return np.exp(C + D * v0 + i * phi * np.log(S))


def heston_probability(j, S, K, T, r, kappa, theta, sigma, rho, v0):
    integrand = lambda phi: np.real(
        np.exp(-complex(0, 1) * phi * np.log(K))
        * heston_char_func(phi, S, K, T, r, kappa, theta, sigma, rho, v0, j)
        / (complex(0, 1) * phi)
    )
    integral, _ = quad(integrand, 0, 100)
    return 0.5 + (1 / np.pi) * integral


def heston_price(S, K, T, r, kappa, theta, sigma, rho, v0, option_type="call"):
    P1 = heston_probability(1, S, K, T, r, kappa, theta, sigma, rho, v0)
    P2 = heston_probability(2, S, K, T, r, kappa, theta, sigma, rho, v0)

    call = S * P1 - K * np.exp(-r * T) * P2
    if option_type == "call":
        return call
    else:
        return call - S + K * np.exp(-r * T)

# -----------------------------
# Sidebar Inputs
# -----------------------------

st.sidebar.header("Option Parameters")
S = st.sidebar.number_input("Spot Price (S)", value=100.0)
K = st.sidebar.number_input("Strike (K)", value=100.0)
T = st.sidebar.number_input("Maturity (years)", value=1.0)
r = st.sidebar.number_input("Risk-free rate", value=0.05)
option_type = st.sidebar.selectbox("Option Type", ["call", "put"])

st.sidebar.header("Black–Scholes")
sigma_bs = st.sidebar.number_input("Volatility (σ)", value=0.2)

st.sidebar.header("Heston Model")
kappa = st.sidebar.number_input("κ (mean reversion)", value=2.0)
theta = st.sidebar.number_input("θ (long-run variance)", value=0.04)
sigma_h = st.sidebar.number_input("σ (vol of vol)", value=0.5)
rho = st.sidebar.number_input("ρ (correlation)", value=-0.7)
v0 = st.sidebar.number_input("v₀ (initial variance)", value=0.04)

# -----------------------------
# Pricing
# -----------------------------

if st.button("Price Option"):
    bs_price = black_scholes_price(S, K, T, r, sigma_bs, option_type)
    h_price = heston_price(S, K, T, r, kappa, theta, sigma_h, rho, v0, option_type)

    st.subheader("Results")
    st.write(f"**Black–Scholes price:** {bs_price:.4f}")
    st.write(f"**Heston price:** {h_price:.4f}")
