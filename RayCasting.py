import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
plt.style.use("ggplot")
st.set_page_config(page_title="Ray Casting Algorithm", layout="centered")
def is_inside(polygon, point):
    """
    Ray casting algorithm to check if a point is inside a polygon.
    polygon: List of (x, y) tuples
    point: (x, y) tuple
    """
    x, y = point
    n = len(polygon)
    inside = False
    p1x, p1y = polygon[0]
    for i in range(n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xints = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

def polygon(n):
    # Generate a simple polygon (convex hull for simplicity)
    polygon = []
    for i in range(n):
        x = np.random.randint(1, 10)
        y = np.random.randint(1, 10)
        polygon.append((x, y))
    # Sort points to avoid self-intersections (simplistic approach)
    polygon.sort()
    return polygon

# Streamlit app
st.title("Polygon Point Checker")

# Generate polygon
n = st.slider("Number of vertices", 3, 10, 5)
poly = polygon(n)
poly_closed = poly + [poly[0]]  # Close the polygon

# Generate a random point
point = (random.randint(1, 10), random.randint(1, 10))

# Plot
fig, ax = plt.subplots()
x, y = zip(*poly_closed)
ax.plot(x, y, marker='o', label="Polygon")
ax.scatter(*point, marker='*', color='red', label="Point")
ax.scatter(*poly_closed[0], marker='x', color='green', label="Start/End")
ax.set_title("Polygon and Point")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.legend()

st.pyplot(fig)

# Check if point is inside
inside = is_inside(poly, point)
st.write(f"Point {point} is {'inside' if inside else 'outside'} the polygon.")
st.write("Polygon vertices:", poly)
