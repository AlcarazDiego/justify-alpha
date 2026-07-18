# justify-alpha

[![PyPI version](https://badge.fury.io/py/justify-alpha.svg)](https://badge.fury.io/py/justify-alpha)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python library that translates a target Bayes Factor into an exact frequentist alpha ($\alpha$) threshold. This allows researchers to maintain strict evidence standards and avoid the **Lindley Paradox** in large sample sizes, while still reporting traditional $p$-values. Useful tool for justifying alpha values and 



## The Problem: The Lindley Paradox
Under traditional frequentist testing, the significance threshold ($\alpha$) is kept fixed (usually at 0.05). However, as your sample size ($N$) grows, your statistical power increases and the standard error shrinks. Eventually, even a microscopic, practically meaningless effect size will easily yield a $p$-value less than 0.05. 

This creates a paradox (i.e., Lindley paradox; Lindley, 1957). Such "paradox" occurs when a frequentist test claims overwhelming evidence against the null (i.e., $p < 0.05$), while a Bayesian analysis of the exact same data shows that the null hypothesis is actually far more likely.

## The Solution: A Hybrid Bridge
While researchers like Maier & Lakens (2022) advocate for justifying alpha levels, implementing their frameworks usually requires complex numerical integration or R programming.

This package provides an elegant Python-native solution using the **BIC (Bayesian Information Criterion) Approximation** formalized by Wagenmakers (2007). By treating hypothesis testing as a model-selection competition, the BIC approximation imposes a logarithmic penalty for sample size ($\ln N$). 

Instead of guessing an expected effect size or setting arbitrary statistical power, you simply define the level of evidence you want (e.g., a Bayes Factor of $BF_{10} = 3.0$ for "moderate evidence" or $10.0$ for "strong evidence"). The package calculates the exact frequentist $\alpha$ required to achieve that target Bayes Factor given your sample size ($N$). 

As your sample size grows, the required $\alpha$ threshold automatically tightens, thus preventing the Lindley paradox from triggering on trivial effects.

## How the Package Calculates the Maths
This package uses the **Bayesian Information Criterion (BIC)** approximation to calculate your alpha threshold. 

Instead of picking an arbitrary alpha (like 0.05), the package determines the exact critical test statistic ($t_{crit}$) needed to achieve your target Bayes Factor ($BF_{10}$) given your sample size ($N$):

$$t_{crit} = \sqrt{\ln(N) + 2\ln(BF_{10})}$$

Once the package calculates this $t_{crit}$, it uses `scipy.stats` to find the matching $p$-value (based on your specific test type and degrees of freedom). That $p$-value becomes your **justified alpha threshold ($\alpha$)**.

## Installation
You can install the package directly from PyPI using pip:

```bash
pip install justify-alpha 
```

## Quickstart & Usage

### 1. Import
To use the calculator, simply import the package and pass your research parameters into the `bayes_alpha` function:

```python
from justify_alpha import calculator
```

### 2. Run the calculation and generate the graph
```
calculator.bayes_alpha(
    test_type='two-sample',   # Options: 'one-sample', 'paired', or 'two-sample'
    alternative='two-sided',  # Options: 'two-sided', 'larger', or 'smaller'
    target_bf10=3,            # Target Bayes Factor (e.g., 3 for moderate evidence)
    target_total_n=100        # Your total sample size across all groups
)
```
 .

**Parameter** *options* and *descriptions* are detailed below:

| Parameter | Type | Options / Description |
| :--- | :--- | :--- |
| `test_type` | `str` | `'one-sample'`, `'paired'`, or `'two-sample'` |
| `alternative` | `str` | `'two-sided'`, `'larger'`, or `'smaller'` |
| `target_bf10` | `float`/`int`| Your target Bayes Factor (e.g., `3` for moderate evidence, `10` for strong evidence). |
| `target_total_n`| `int` | The total number of participants or observations across *all* experimental groups. |

## What Happens When You Run the Package?
When you execute the function, the package performs the following actions automatically:

1. **Console Output:** Prints a clear text summary in your terminal showing exact alpha ($\alpha$) threshold required to maintain your target Bayes Factor given your sample size ($N$).


2. **Visualization:** Produces a Matplotlib window displaying a live-rendered curve, illustrating how the required alpha threshold varies across different sample sizes (ranging from 20 up to your target $N$ (```target_total_n```), or 1000). The graph also highlights your specific study's ```target_total_n``` and its corresponding calculated alpha ($\alpha$) threshold, showing the precise point where your selected sample size ($N$) on the curve.


## Dependencies

This package relies on standard scientific Python libraries, which are installed automatically alongside it:
* `numpy`
* `scipy`
* `matplotlib`

## License

This project is open-source and available under the **MIT License**
