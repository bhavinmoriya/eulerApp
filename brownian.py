import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Brownian Motion Simulator", layout="wide")  # Unique browser tab title
# App title
st.title("Brownian Motion Simulator")
st.write(
    r"""
    This app simulates **Brownian Motion (Wiener Process)**:
    \[
    dW_t \sim \mathcal{N}(0, dt)
    \]
    where:
    - \( W_t \): Position at time \( t \)
    - \( dW_t \): Increment (normally distributed with mean 0 and variance \( dt \))
    """
)

# Sidebar for user inputs
st.sidebar.header("Simulation Parameters")
T = st.sidebar.number_input("Time horizon (T)", value=1.0)
steps = st.sidebar.slider("Number of steps", 100, 10000, 1000)
num_simulations = st.sidebar.slider("Number of simulations", 1, 100, 5)

# Simulate Brownian Motion
def simulate_brownian_motion(T, steps, num_simulations):
    dt = T / steps
    t = np.linspace(0, T, steps + 1)
    W = np.zeros((num_simulations, steps + 1))

    for i in range(num_simulations):
        for j in range(1, steps + 1):
            dW = np.random.normal(0, np.sqrt(dt))
            W[i, j] = W[i, j - 1] + dW

    return t, W

# Run simulation
t, W = simulate_brownian_motion(T, steps, num_simulations)

# Plot results
st.subheader("Simulated Paths")
fig, ax = plt.subplots(figsize=(10, 6))
for i in range(num_simulations):
    ax.plot(t, W[i], lw=1, label=f"Simulation {i+1}" if i < 3 else "")
ax.set_xlabel("Time (t)")
ax.set_ylabel("Position (Wₜ)")
ax.set_title("Brownian Motion (Wiener Process) Simulations")
ax.grid(True)
st.pyplot(fig)

# Show summary statistics
st.subheader("Summary Statistics")
st.write(f"**Final Positions**: {W[:, -1]}")
st.write(f"**Mean Final Position**: {np.mean(W[:, -1]):.2f}")
st.write(f"**Standard Deviation**: {np.std(W[:, -1]):.2f}")
