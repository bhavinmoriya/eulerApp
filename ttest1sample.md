You’ll see exactly *what problem a t-test solves*.

---

# 🎯 The Story: Are my dice rolls fair?

But instead of heads/tails, we’ll measure **waiting time**.

## Step 1 — The setup

Suppose a game designer claims:

> “On average, players finish level 1 in **10 seconds**.”

You test 8 players and record their times:

```
[12, 9, 11, 13, 8, 10, 12, 14]
```

Question:

> Is the true average really 10 seconds?
> Or is the claim wrong?

This is **exactly** the same logic as the fair-coin question, but now data are real numbers instead of counts.

---

# Step 2 — Define hypotheses

Null hypothesis (boring world):

> **H₀: average time = 10 seconds**

Alternative:

> **H₁: average time ≠ 10 seconds**

---

# Step 3 — Look at the data

Compute sample mean:

[
\bar x = 11.125
]

So players seem slower than claimed.
But: maybe this happened by chance. Small samples fluctuate.

---

# Step 4 — Measure “surprise”

If H₀ were true (mean = 10), how surprising is seeing a sample mean of 11.125?

But we must scale by variability — some players differ more than others.

Compute sample standard deviation:

[
s \approx 2.03
]

Standard error of mean:

[
SE = s / \sqrt{8} \approx 0.718
]

Now form the **t-statistic**:

[
t = \frac{11.125 - 10}{0.718} \approx 1.57
]

This says:

> “The observed mean is 1.57 standard-errors away from the null claim.”

---

# Step 5 — Convert t → p-value

For 7 degrees of freedom:

[
p \approx 0.16
]

---

# Step 6 — Make decision

Choose α = 0.05.

Since:

[
p = 0.16 > 0.05
]

👉 **Fail to reject H₀**

---

# Step 7 — Plain English conclusion

> “With only 8 players, the observed average of 11.1 seconds is not unusual enough to contradict the claim of 10 seconds.”

We do **not** say:

* “The claim is true”
* or “Players are slower”

We only say:

* **Not enough evidence**

---

# Step 8 — Python reproduction

```python
import numpy as np
from scipy.stats import ttest_1samp

times = np.array([12,9,11,13,8,10,12,14])
t_stat, p = ttest_1samp(times, 10)

t_stat, p
```

---

# Step 9 — Connect back to coin

| Coin problem       | Time problem      |
| ------------------ | ----------------- |
| Heads count        | Sample mean       |
| Binomial noise     | Measurement noise |
| Binomial test      | t-test            |
| p-value = surprise | same              |

**Same logic. Different data type.**

---

# Step 10 — Key memory hook

> **t-test = “Is my sample average unusually far from the claimed average, relative to natural variability?”**


