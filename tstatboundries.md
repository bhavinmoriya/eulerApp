---

# The ONE rule that generates everything

> **The sign of the t-statistic tells you the direction.**
> **The alternative hypothesis tells you which direction you care about.**

That’s it.

---

# Step 1 — Fix how you compute t

Always compute:

[
t = \frac{\bar A - \bar B}{\text{standard error}}
]

So:

* t > 0  → A > B
* t < 0  → A < B

Memorize:

> **“t points from B to A.”**

---

# Step 2 — Draw the picture in your head

Number line:

```
<----------|----------|---------->

        negative      0      positive
```

Left side = A < B
Right side = A > B

---

# Step 3 — Decision rules by story

### Case 1 — Two-sided

> “Are they different at all?”

Reject if:

[
|t| \text{ is big}
]

→ either far left or far right

---

### Case 2 — One-sided: “Is A smaller than B?”

Alternative:

[
H_1: A < B
]

You only care about **left tail**.

Reject if:

[
t \text{ is very negative}
]

---

### Case 3 — One-sided: “Is A larger than B?”

Alternative:

[
H_1: A > B
]

You only care about **right tail**.

Reject if:

[
t \text{ is very positive}
]

---

# Decision table (minimal)

| Alternative | Reject when    |   |             |
| ----------- | -------------- | - | ----------- |
| A ≠ B       |                | t | > threshold |
| A < B       | t < −threshold |   |             |
| A > B       | t > threshold  |   |             |

Threshold = critical t-value for α (or equivalently p < α)

---

# p-value version (even easier)

SciPy gives **two-sided p-value** by default.

Let:

* p₂ = two-sided p-value
* t = test statistic

Then:

### Two-sided

Reject if:

[
p_2 < \alpha
]

---

### One-sided: A < B

Reject if:

[
t < 0 \quad \text{and} \quad p_2/2 < \alpha
]

---

### One-sided: A > B

Reject if:

[
t > 0 \quad \text{and} \quad p_2/2 < \alpha
]

---

# Ultra-simple mnemonic

> **Two-sided → absolute value**
> **One-sided → sign + half the p-value**

---

# Tiny Python helper (for your brain)

```python
def decide(t, p_two, alpha, alternative):
    if alternative == "two-sided":
        return p_two < alpha
    if alternative == "less":   # A < B
        return t < 0 and p_two/2 < alpha
    if alternative == "greater":  # A > B
        return t > 0 and p_two/2 < alpha
```

---

# Visual memory trick

Imagine:

* A hill centered at 0
* You fall off:

  * both sides → two-sided
  * left only → A < B
  * right only → A > B

---

# Final 10-second recall

1. Compute t = (A − B)/SE
2. Look at sign of t
3. Ask what H₁ says
4. Compare p appropriately


