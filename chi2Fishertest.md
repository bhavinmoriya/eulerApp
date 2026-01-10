Perfect — we now complete the categorical side of hypothesis testing.

👉 **Simple real story → numbers → test → Python → intuition**

No abstract formulas first.

---

# PART 1 — χ² INDEPENDENCE TEST

## 🎯 STORY: Does coffee type affect sleep quality?

You survey 40 people:

|          | Slept Well | Slept Poorly | Total |
| -------- | ---------- | ------------ | ----- |
| Coffee A | 12         | 8            | 20    |
| Coffee B | 6          | 14           | 20    |
| Total    | 18         | 22           | 40    |

Question:

> Is sleep quality **independent** of coffee type?

---

## Step 1 — Hypotheses

**H₀:** coffee type and sleep quality are independent
**H₁:** they are associated

---

## Step 2 — Expected counts under H₀

If independent:

[
E_{row,col} = \frac{(\text{row total})(\text{col total})}{\text{grand total}}
]

Compute expected:

|          | Slept Well     | Slept Poorly    |
| -------- | -------------- | --------------- |
| Coffee A | (20×18)/40 = 9 | (20×22)/40 = 11 |
| Coffee B | 9              | 11              |

---

## Step 3 — Measure deviation

[
\chi^2 = \sum \frac{(O - E)^2}{E}
]

[
= \frac{(12-9)^2}{9} + \frac{(8-11)^2}{11}

* \frac{(6-9)^2}{9} + \frac{(14-11)^2}{11}
  ]

[
\chi^2 = 1 + 0.818 + 1 + 0.818 = 3.636
]

---

## Step 4 — Convert χ² → p-value

Degrees of freedom:

[
df = (rows-1)(cols-1) = 1
]

χ² = 3.636 with df=1 → p ≈ 0.056

---

## Step 5 — Decision

α = 0.05

Since p ≈ 0.056 > 0.05:

👉 **Fail to reject H₀**

---

## Step 6 — Plain English

> “The observed association is suggestive but not strong enough to rule out chance at the 5% level.”

---

## Step 7 — Python reproduction

```python
import numpy as np
from scipy.stats import chi2_contingency

table = np.array([[12,8],
                  [6,14]])

chi2, p, df, expected = chi2_contingency(table)
chi2, p, expected
```

---

## Step 8 — Intuition

If coffee truly had no effect:

* Tables like this appear ~5% of the time
* This one is right on the borderline

---

# PART 2 — FISHER EXACT TEST (SMALL SAMPLES)

Now suppose you only had **8 people**:

|          | Slept Well | Slept Poorly |
| -------- | ---------- | ------------ |
| Coffee A | 3          | 1            |
| Coffee B | 0          | 4            |

Question:

> Same — independent or not?

Expected counts are below 5 → χ² approximation breaks.

We use **Fisher’s Exact Test**.

---

## Step 1 — Hypotheses

Same as before.

---

## Step 2 — Exact probability

Fisher computes the **exact probability** of getting a table this extreme under H₀.

No approximations.

---

## Step 3 — Python

```python
from scipy.stats import fisher_exact

table = np.array([[3,1],
                  [0,4]])

oddsratio, p = fisher_exact(table)
oddsratio, p
```

Typical p ≈ 0.028

---

## Step 4 — Decision

p < 0.05 → Reject H₀

---

## Step 5 — Plain English

> “With such an extreme table, independence is very unlikely. Coffee type and sleep appear associated.”

---

# WHEN TO USE WHICH

| Situation             | Test                 |
| --------------------- | -------------------- |
| Expected counts ≥ 5   | χ² independence test |
| Any expected cell < 5 | Fisher exact test    |

---

# MEMORY HOOK

> **χ² = approximate large-sample test**
> **Fisher = exact small-sample test**

---

# BIG PICTURE CONNECTION

| Problem              | Test   | Data type           |
| -------------------- | ------ | ------------------- |
| Mean equality        | t-test | continuous          |
| Category frequencies | χ²     | categorical         |
| Small categorical    | Fisher | categorical small n |


