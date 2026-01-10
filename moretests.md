---

# 1) TWO-SAMPLE t-TEST — ONE-SIDED VS TWO-SIDED

## 🎯 Story: Fertilizer A vs Fertilizer B

You measure plant growth (cm):

**A:** [10, 12, 9, 11, 10]
**B:** [13, 14, 12, 15, 13]

Question:

> Does Fertilizer B produce **larger** plants than A?

---

## Step 1 — Hypotheses

### Two-sided version

H₀: mean(A) = mean(B)
H₁: mean(A) ≠ mean(B)

### One-sided version (direction chosen in advance!)

H₀: mean(A) ≥ mean(B)
H₁: mean(A) < mean(B)

(We test whether A < B)

---

## Step 2 — Compute t-statistic

Same formula always:

[
t = \frac{\bar A - \bar B}{\sqrt{s_A^2/n_A + s_B^2/n_B}}
]

Only the **decision rule** changes.

---

## Step 3 — Decision rules

| Hypothesis type   | Reject H₀ if   |   |               |
| ----------------- | -------------- | - | ------------- |
| Two-sided         |                | t | > t_{α/2, df} |
| One-sided (A < B) | t < −t_{α, df} |   |               |
| One-sided (A > B) | t > t_{α, df}  |   |               |

The t-statistic is identical — only which tail we look at changes.

---

## Step 4 — Python

```python
from scipy.stats import ttest_ind

A = [10,12,9,11,10]
B = [13,14,12,15,13]

t_stat, p_two = ttest_ind(A, B, equal_var=False)

# one-sided p-value for H1: A < B
p_one = p_two / 2 if t_stat < 0 else 1 - p_two/2

t_stat, p_two, p_one
```

---

# 2) PAIRED t-TEST (BEFORE / AFTER)

## 🎯 Story: Same plants before and after treatment

Before: [10, 11, 9, 10, 12]
After:  [13, 14, 11, 13, 15]

Question:

> Did treatment increase growth?

---

## Step 1 — Compute differences

d = After − Before
→ [3,3,2,3,3]

Now it becomes a **one-sample t-test** on d.

H₀: mean(d) = 0
H₁: mean(d) > 0

---

## Step 2 — t-statistic

[
t = \frac{\bar d - 0}{s_d/\sqrt{n}}
]

---

## Step 3 — Python

```python
from scipy.stats import ttest_rel

before = [10,11,9,10,12]
after  = [13,14,11,13,15]

t_stat, p_two = ttest_rel(after, before)

# one-sided p-value (after > before)
p_one = p_two/2 if t_stat > 0 else 1 - p_two/2

t_stat, p_one
```

---

# 3) POWER CALCULATION — TWO-SAMPLE t-TEST

## 🎯 Question

> How many samples do I need to detect a mean difference δ?

---

## Key formula (balanced groups)

[
n \approx
\frac{2 (z_{α/2} + z_{β})^2 σ^2}{δ^2}
]

---

## Python tool

```python
from statsmodels.stats.power import TTestIndPower

analysis = TTestIndPower()

# effect size = delta / sigma
effect_size = 0.5   # medium effect
n = analysis.solve_power(effect_size, power=0.8, alpha=0.05)
n
```

Meaning:

* You need ~n per group

---

# 4) NONPARAMETRIC ALTERNATIVE — MANN–WHITNEY U

## When to use

* Data not normal
* Heavy tails / outliers
* Ordinal data

## 🎯 Story

Same fertilizer data, but maybe growth ranks matter more than exact cm.

---

## Test idea

Instead of comparing means:

> Compare **ranks**

H₀: Distributions identical
H₁: One tends to have larger values

---

## Python

```python
from scipy.stats import mannwhitneyu

A = [10,12,9,11,10]
B = [13,14,12,15,13]

u_stat, p = mannwhitneyu(A, B, alternative="less")
u_stat, p
```

---

# MEMORY SUMMARY

| Problem                    | Test           | Measures            |
| -------------------------- | -------------- | ------------------- |
| Two independent means      | Two-sample t   | Mean difference     |
| Same subjects before/after | Paired t       | Mean of differences |
| Non-normal continuous      | Mann–Whitney   | Rank shift          |
| Planning sample size       | Power analysis | Detectable effect   |

---

# FINAL MENTAL MODEL

> **t-test = compare means**
> **paired t-test = compare within-subject changes**
> **power = how big n to see effect**
> **Mann-Whitney = compare distributions without normality**


