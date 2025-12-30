import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Geometric Brownian Motion Simulator", layout="wide")  # Unique browser tab title
# App title
st.title("Geometric Brownian Motion Simulator")
st.write(
    r"""
    This app simulates **Geometric Brownian Motion (GBM)**:
    \[
    dS_t = \mu S_t \, dt + \sigma S_t \, dW_t
    \]
    where:
    - \( S_t \): Asset price at time \( t \)
    - \( \mu \): Drift coefficient
    - \( \sigma \): Volatility
    - \( dW_t \): Wiener process (Brownian motion)
    """
)

# Sidebar for user inputs
st.sidebar.header("Simulation Parameters")
mu = st.sidebar.number_input("Drift coefficient (μ)", value=0.1)
sigma = st.sidebar.number_input("Volatility (σ)", value=0.2)
S0 = st.sidebar.number_input("Initial price (S₀)", value=100.0)
T = st.sidebar.number_input("Time horizon (T)", value=1.0)
steps = st.sidebar.slider("Number of steps", 100, 10000, 1000)
num_simulations = st.sidebar.slider("Number of simulations", 1, 100, 5)

# Simulate GBM
def simulate_gbm(mu, sigma, S0, T, steps, num_simulations):
    dt = T / steps
    t = np.linspace(0, T, steps + 1)
    S = np.zeros((num_simulations, steps + 1))
    S[:, 0] = S0

    for i in range(num_simulations):
        for j in range(1, steps + 1):
            dW = np.random.normal(0, np.sqrt(dt))
            S[i, j] = S[i, j - 1] * (1 + mu * dt + sigma * dW)

    return t, S

# Run simulation
t, S = simulate_gbm(mu, sigma, S0, T, steps, num_simulations)

# Plot results
st.subheader("Simulated Paths")
fig, ax = plt.subplots(figsize=(10, 6))
for i in range(num_simulations):
    ax.plot(t, S[i], lw=1, label=f"Simulation {i+1}" if i < 3 else "")
ax.set_xlabel("Time (t)")
ax.set_ylabel("Price (Sₜ)")
ax.set_title("Geometric Brownian Motion (GBM) Simulations")
ax.grid(True)
st.pyplot(fig)

# Show summary statistics
st.subheader("Summary Statistics")
st.write(f"**Final Prices**: {S[:, -1]}")
st.write(f"**Mean Final Price**: {np.mean(S[:, -1]):.2f}")
st.write(f"**Standard Deviation**: {np.std(S[:, -1]):.2f}")
