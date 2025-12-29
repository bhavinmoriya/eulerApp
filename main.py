import streamlit as st
import matplotlib.pyplot as plt

def euler_method(f, t0, y0, t_end, step_size):
    """
    Solve a first-order ODE using the Euler method.

    Parameters:
    - f: Function representing dy/dt = f(t, y)
    - t0: Initial time
    - y0: Initial value of y at t0
    - t_end: End time for the solution
    - step_size: Step size for the Euler method

    Returns:
    - Lists of t and y values
    """
    t_values = [t0]
    y_values = [y0]
    t = t0
    y = y0

    while t < t_end:
        y += step_size * f(t, y)
        t += step_size
        t_values.append(t)
        y_values.append(y)

    return t_values, y_values

# Example: Solve dy/dt = -2ty with y(0) = 1
def f(t, y):
    return -2 * t * y

# Streamlit UI
st.title("Euler Method for ODEs")
st.write("This app solves the ODE \( \frac{dy}{dt} = -2ty \) with \( y(0) = 1 \) using the Euler method.")

step_size = st.number_input("Enter the step size (e.g., 0.1):", min_value=0.001, max_value=1.0, value=0.1)

t0 = 0
y0 = 1
t_end = 1

t, y_euler = euler_method(f, t0, y0, t_end, step_size)

# Exact solution for comparison: y(t) = exp(-t^2)
t_exact = [ti for ti in t]
y_exact = [y0 * (1 - ti**2) for ti in t_exact]  # Approximate exact solution for this ODE

# Plot the results
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(t, y_euler, 'bo-', label='Euler Approximation')
ax.plot(t_exact, y_exact, 'r-', label='Exact Solution')
ax.set_xlabel('t')
ax.set_ylabel('y')
ax.set_title('Euler Method Approximation vs Exact Solution')
ax.legend()
ax.grid(True)

st.pyplot(fig)
