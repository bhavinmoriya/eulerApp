# ==========================================================
# FULL OPTION PRICING LAB
# Black–Scholes | Heston | FFT | Jumps | Calibration | GPU MC
# ==========================================================

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.integrate import quad
from scipy.optimize import minimize
import torch

st.set_page_config(page_title="Advanced Option Pricing Lab", layout="wide")
st.title("🚀 Advanced Option Pricing & Volatility Lab")
st.caption("Black–Scholes, Heston, FFT (Carr–Madan), Jumps, Calibration, GPU Monte Carlo")

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
    pdf = norm.pdf(d1)
    delta = norm.cdf(d1) if option == "call" else norm.cdf(d1) - 1
    gamma = pdf / (S * sigma * np.sqrt(T))
    vega = S * pdf * np.sqrt(T)
    return delta, gamma, vega

# ==========================================================
# Heston characteristic function
# ==========================================================

def heston_cf(phi, S, T, r, kappa, theta, sigma, rho, v0):
    i = 1j
    a = kappa * theta
    b = kappa
    d = np.sqrt((rho * sigma * phi * i - b)**2 + sigma**2 * (phi**2 + i * phi))
    g = (b - rho * sigma * phi * i + d) / (b - rho * sigma * phi * i - d)
    C = r * phi * i * T + a / sigma**2 * ((b - rho * sigma * phi * i + d) * T - 2 * np.log((1 - g * np.exp(d * T)) / (1 - g)))
    D = (b - rho * sigma * phi * i + d) / sigma**2 * ((1 - np.exp(d * T)) / (1 - g * np.exp(d * T)))
    return np.exp(C + D * v0 + i * phi * np.log(S))

# ==========================================================
# Carr–Madan FFT pricing
# ==========================================================

def carr_madan_fft(S, T, r, cf, alpha=1.5, N=4096, eta=0.25):
    lambd = 2 * np.pi / (N * eta)
    b = np.log(S) - N * lambd / 2
    u = np.arange(N) * eta
    k = b + np.arange(N) * lambd

    psi = np.exp(-r * T) * cf(u - (alpha + 1) * 1j) / (alpha**2 + alpha - u**2 + 1j * (2 * alpha + 1) * u)
    fft_vals = np.real(np.fft.fft(psi * np.exp(1j * u * b) * eta)) / np.pi
    strikes = np.exp(k)
    calls = np.exp(-alpha * k) * fft_vals
    return strikes, calls

# ==========================================================
# Jump Diffusion (Merton)
# ==========================================================

def merton_cf(phi, S, T, r, sigma, lam, mu_j, sig_j):
    i = 1j
    jump = lam * T * (np.exp(i * phi * mu_j - 0.5 * sig_j**2 * phi**2) - 1)
    return np.exp(i * phi * (np.log(S) + (r - 0.5 * sigma**2) * T) - 0.5 * sigma**2 * phi**2 * T + jump)

# ==========================================================
# GPU Monte Carlo (Heston)
# ==========================================================

def heston_mc_gpu(S, K, T, r, kappa, theta, sigma, rho, v0, paths=200_000, steps=200):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    dt = T / steps
    S_t = torch.full((paths,), S, device=device)
    v_t = torch.full((paths,), v0, device=device)

    for _ in range(steps):
        z1 = torch.randn(paths, device=device)
        z2 = rho * z1 + torch.sqrt(torch.tensor(1 - rho**2, device=device)) * torch.randn(paths, device=device)
        v_t = torch.clamp(v_t + kappa * (theta - v_t) * dt + sigma * torch.sqrt(v_t * dt) * z2, min=0)
        S_t = S_t * torch.exp((r - 0.5 * v_t) * dt + torch.sqrt(v_t * dt) * z1)

    payoff = torch.clamp(S_t - K, min=0)
    return torch.exp(torch.tensor(-r * T, device=device)) * payoff.mean()

# ==========================================================
# Calibration (Heston to market data)
# ==========================================================

def calibrate_heston(strikes, prices, S, T, r):
    def objective(params):
        kappa, theta, sigma, rho, v0 = params
        model = [heston_price(S, k, T, r, kappa, theta, sigma, rho, v0) for k in strikes]
        return np.mean((np.array(model) - prices)**2)

    x0 = [2, 0.04, 0.5, -0.7, 0.04]
    bounds = [(0.1, 5), (0.01, 0.2), (0.1, 1), (-0.9, 0), (0.01, 0.2)]
    return minimize(objective, x0, bounds=bounds)

# ==========================================================
# Sidebar
# ==========================================================

st.sidebar.header("Option")
S = st.sidebar.slider("Spot", 50.0, 150.0, 100.0)
T = st.sidebar.slider("Maturity", 0.2, 3.0, 1.0)
r = st.sidebar.slider("Rate", 0.0, 0.1, 0.05)

st.sidebar.header("Heston")
kappa = st.sidebar.slider("κ", 0.1, 5.0, 2.0)
theta = st.sidebar.slider("θ", 0.01, 0.2, 0.04)
sigma_h = st.sidebar.slider("σ", 0.1, 1.0, 0.5)
rho = st.sidebar.slider("ρ", -0.9, 0.0, -0.7)
v0 = st.sidebar.slider("v₀", 0.01, 0.2, 0.04)

# ==========================================================
# FFT pricing display
# ==========================================================

st.subheader("⚡ Carr–Madan FFT Pricing")
cf = lambda u: heston_cf(u, S, T, r, kappa, theta, sigma_h, rho, v0)
K_fft, C_fft = carr_madan_fft(S, T, r, cf)

fig = plt.figure()
plt.plot(K_fft, C_fft)
plt.xlim(50, 150)
plt.xlabel("Strike")
plt.ylabel("Call Price")
st.pyplot(fig)

# ==========================================================
# Volatility surface (synthetic)
# ==========================================================

st.subheader("🌈 Volatility Surface (Heston)
")
strikes = np.linspace(70, 130, 20)
maturities = np.linspace(0.3, 2.0, 10)
vol_surface = np.zeros((len(maturities), len(strikes)))

for i, T_ in enumerate(maturities):
    for j, K_ in enumerate(strikes):
        price = heston_price(S, K_, T_, r, kappa, theta, sigma_h, rho, v0)
        vol = 0.2
        for _ in range(10):
            vol -= (bs_price(S, K_, T_, r, vol) - price) / max(1e-4, bs_greeks(S, K_, T_, r, vol)[2])
        vol_surface[i, j] = vol

fig2 = plt.figure()
plt.imshow(vol_surface, aspect='auto', origin='lower', extent=[strikes[0], strikes[-1], maturities[0], maturities[-1]])
plt.colorbar(label="Implied Vol")
plt.xlabel("Strike")
plt.ylabel("Maturity")
st.pyplot(fig2)

# ==========================================================
# GPU Monte Carlo
# ==========================================================

st.subheader("🔥 GPU Monte Carlo (Heston)")
mc_gpu = heston_mc_gpu(S, 100, T, r, kappa, theta, sigma_h, rho, v0)
st.write("GPU Monte Carlo Price:", mc_gpu.item())
