👉 **Simple story first → then numbers → then statistic → then general form**

No abstraction first. Only intuition. Just like coin and χ².

---

# 🎯 STORY: Which coffee makes people faster?

A company claims:

> Coffee A and Coffee B give the same average reaction time.

You test:

* 6 people drink **Coffee A**
* 6 people drink **Coffee B**

Reaction times (seconds):

**A:**
[0.31, 0.35, 0.30, 0.33, 0.36, 0.34]

**B:**
[0.28, 0.27, 0.26, 0.29, 0.25, 0.27]

Question:

> Is there evidence Coffee B leads to faster reaction time?

---

# Step 1 — Hypotheses

Null hypothesis (boring world):

> **H₀: average reaction time of A = average reaction time of B**

Alternative:

> **H₁: averages differ**
> (or one-sided: B < A if chosen beforehand)

---

# Step 2 — Compute sample averages

[
\bar A = 0.3317
]
[
\bar B = 0.2700
]

Difference = 0.0617 seconds.

Looks big — but is it **big compared to random variability**?

---

# Step 3 — Measure variability

Sample standard deviations:

[
s_A \approx 0.022
]
[
s_B \approx 0.015
]

---

# Step 4 — Build the t-statistic

[
t = \frac{\bar A - \bar B}{\sqrt{s_A^2/n_A + s_B^2/n_B}}
]

Plug in:

[
t \approx \frac{0.0617}{\sqrt{0.022^2/6 + 0.015^2/6}}
\approx 5.6
]

---

# Step 5 — Convert t → p-value

Degrees of freedom ≈ 9 (Welch formula)

p ≈ 0.0004

---

# Step 6 — Decision

α = 0.05

Since p ≪ α:

👉 **Reject H₀**

---

# Step 7 — Plain English conclusion

> “Reaction times under Coffee B are significantly faster than under Coffee A.”

---

# Step 8 — Python reproduction

```python
import numpy as np
from scipy.stats import ttest_ind

A = np.array([0.31,0.35,0.30,0.33,0.36,0.34])
B = np.array([0.28,0.27,0.26,0.29,0.25,0.27])

t_stat, p = ttest_ind(A, B, equal_var=False)
t_stat, p
```

---

# Step 9 — Connect to earlier tests

| Test            | Data type  | Question           |
| --------------- | ---------- | ------------------ |
| Coin (binomial) | Counts     | Fair?              |
| One-sample t    | Numbers    | Mean correct?      |
| Two-sample t    | Numbers    | Means equal?       |
| χ²              | Categories | Frequencies match? |

Same logic every time.

---

# Step 10 — Memory hook

> **Two-sample t-test = “Is the difference between two averages too large to be explained by random variation?”**


