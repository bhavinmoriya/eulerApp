👉 **Simple story first → then statistic → then general form**

No abstraction before intuition.

---

# 🎯 STORY: Is my die fair?

This is the **categorical version** of the coin problem.

## Step 1 — The setup

You have a die.
You roll it 60 times and get:

| Face | Observed count |
| ---- | -------------- |
| 1    | 8              |
| 2    | 9              |
| 3    | 10             |
| 4    | 11             |
| 5    | 12             |
| 6    | 10             |

Question:

> Is the die fair?

---

# Step 2 — Hypotheses

**H₀:** the die is fair
(each face has probability 1/6)

**H₁:** the die is not fair

---

# Step 3 — Expected counts under H₀

60 rolls / 6 faces = 10 expected per face.

So:

| Face | Observed (O) | Expected (E) |
| ---- | ------------ | ------------ |
| 1    | 8            | 10           |
| 2    | 9            | 10           |
| 3    | 10           | 10           |
| 4    | 11           | 10           |
| 5    | 12           | 10           |
| 6    | 10           | 10           |

---

# Step 4 — Measure surprise

We compute how far O deviates from E:

[
\chi^2 = \sum \frac{(O - E)^2}{E}
]

Compute:

[
\chi^2 =
\frac{(8-10)^2}{10} +
\frac{(9-10)^2}{10} +
... +
\frac{(10-10)^2}{10}
]

Numerically:

[
\chi^2 = 0.4 + 0.1 + 0 + 0.1 + 0.4 + 0 = 1.0
]

---

# Step 5 — Convert χ² → p-value

Degrees of freedom:

[
df = k - 1 = 6 - 1 = 5
]

Look up χ²=1.0 in χ²(5) distribution:

[
p \approx 0.96
]

---

# Step 6 — Decision

α = 0.05

Since p ≫ α:

👉 **Fail to reject H₀**

---

# Step 7 — Plain English

> “These roll counts are extremely typical of a fair die. No evidence of bias.”

---

# Step 8 — Python reproduction

```python
import numpy as np
from scipy.stats import chisquare

observed = np.array([8,9,10,11,12,10])
expected = np.ones(6)*10

chi2, p = chisquare(observed, expected)
chi2, p
```

---

# Step 9 — Connect to coin and t-test

| Test          | Data type   | Question                 |
| ------------- | ----------- | ------------------------ |
| Binomial test | Heads/tails | Is coin fair?            |
| t-test        | Numbers     | Is mean correct?         |
| χ² test       | Categories  | Are frequencies correct? |

**Same logic every time:**

1. Assume H₀
2. Compute expected behavior
3. Measure deviation
4. Convert to probability under H₀
5. Decide

---

# Step 10 — Important assumptions

* Expected counts ≥ 5 (rule of thumb)
* Independent trials

---

# Step 11 — Memory hook

> **χ² test = “Are my category counts too far from expectation to blame on randomness?”**


