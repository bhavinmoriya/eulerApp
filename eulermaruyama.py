import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Euler-Maruyama SDE Simulator",
    layout="wide"
)

def euler_maruyama(mu, sigma, x0, t0, t_end, step_size, num_simulations=1):
    """
    Solve an SDE using the Euler-Maruyama method.

    Parameters:
    - mu: Drift coefficient
    - sigma: Diffusion coefficient
    - x0: Initial value
    - t0: Initial time
    - t_end: End time
    - step_size: Step size
    - num_simulations: Number of simulations (paths)

    Returns:
    - Lists of t and X values for each simulation
    """
    num_steps = int((t_end - t0) / step_size)
    t = np.linspace(t0, t_end, num_steps + 1)
    X = np.zeros((num_simulations, num_steps + 1))
    X[:, 0] = x0

    for i in range(num_simulations):
        for j in range(num_steps):
            dW = np.random.normal(0, np.sqrt(step_size))
            X[i, j + 1] = X[i, j] + mu * X[i, j] * step_size + sigma * X[i, j] * dW

    return t, X

# Streamlit UI
st.title("Euler-Maruyama Method for SDEs")
# st.write(r"This app solves the SDE $\( dX_t = \mu X_t \, dt + \sigma X_t \, dW_t \)$ using the Euler-Maruyama method.")
st.latex(r"\text{This app solves the SDE }\left( dX_t = \mu X_t \, dt + \sigma X_t \, dW_t \right) \mbox{using the Euler-Maruyama method.}")

# User inputs
col1, col2 = st.columns(2)
with col1:
    mu = st.number_input("Drift coefficient (mu):", value=1.0)
    x0 = st.number_input("Initial value (X0):", value=1.0)
    t_end = st.number_input("End time (t_end):", value=1.0)

with col2:
    sigma = st.number_input("Diffusion coefficient (sigma):", value=0.1)
    step_size = st.number_input("Step size (e.g., 0.01):", min_value=0.001, max_value=0.1, value=0.01)
    num_simulations = st.number_input("Number of simulations (paths):", min_value=1, max_value=10, value=3)

t0 = 0

# mu, sigma, x0, t_end, step_size, num_simulations=1,.1,1,1,.001,5
# Solve SDE
t, X = euler_maruyama(mu, sigma, x0, t0, t_end, step_size, num_simulations)

# Plot the results
fig, ax = plt.subplots(figsize=(12, 6))
for i in range(num_simulations):
    ax.plot(t, X[i], label=f'Simulation {i+1}')
ax.set_xlabel('t')
ax.set_ylabel('X(t)')
ax.set_title('Euler-Maruyama Method: Simulated Paths')
ax.legend()
ax.grid(True)

st.pyplot(fig)
