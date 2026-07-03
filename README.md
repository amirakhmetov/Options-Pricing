# Options Pricing Engine & Market Validation

An institutional-grade derivatives analytics platform that bridges theoretical option pricing models with empirical market data extraction. The system implements closed-form Black-Scholes pricing, computes risk-management Greeks, constructs Cox-Ross-Rubinstein (CRR) binomial trees, and resolves market-implied volatilities using numerical root-finding methods.

---

## Features

* **Analytical Pricing Core:** Full European call and put evaluation incorporating continuous dividend yields.
* **Risk Greeks Engine:** Sensitivity modules calculating first and second-order risk measures: Delta, Gamma, Vega, Theta, and Rho.
* **Numerical Lattice Engine:** Discrete-time Cox-Ross-Rubinstein binomial tree framework to analyze numerical pricing convergence behaviors.
* **Implied Volatility Solver:** A robust root-finding module utilizing a numerical bisection algorithm to invert market midpoint prices into volatility metrics.
* **Live Ingestion Pipeline:** Automated data ingestion via yfinance to track live option chains, contract spreads, and historical underlying price series.

---

## Repository Structure

```text
├── pricing_engine/
│   ├── __init__.py
│   ├── black_scholes.py   # Analytical pricing and closed-form Greeks
│   ├── binomial_tree.py   # CRR discrete-time lattice engine
│   └── iv_solver.py       # Numerical bisection root-finding algorithm
├── data/
│   └── pipeline.py        # yfinance ingestion and data cleaning
├── main.py                # Pipeline orchestrator and validation entry point
├── requirements.txt       # Scientific computing dependencies
└── README.md
```

---

## Installation

Ensure you have Python 3.8+ installed, then clone this repository and install the mandatory scientific computing and data tracking packages:

```bash
git clone [https://github.com/amirakhmetov/options-pricing-engine.git](https://github.com/amirakhmetov/options-pricing-engine.git)
cd options-pricing-engine
pip install -r requirements.txt
```

### `requirements.txt`
```text
numpy
pandas
matplotlib
yfinance
scipy
```

---

## Quick Start & Usage

To run the complete data-mining, pricing verification, and volatility smile extraction pipeline seamlessly from scratch, execute:

```bash
python main.py
```

### Programmatic Example
```python
from pricing_engine.black_scholes import BlackScholesEngine

# Initialize engine for an Equity Option
option = BlackScholesEngine(S=100, K=100, T=1.0, r=0.05, sigma=0.20, q=0.0)
call_price = option.calc_price(contract_type="call")
greeks = option.get_greeks()

print(f"Theoretical Call Price: {call_price:.4f}")
print(f"Delta: {greeks['delta']:.4f} | Gamma: {greeks['gamma']:.4f}")
```

---

## Quantitative Validation & Results

### 1. Model Verification (Put-Call Parity)
The analytical framework was structurally validated by testing put-call parity constraints via continuous pricing variables. The mathematical difference resolved to ~0 within absolute numerical precision, verifying code structure accuracy.

| Metric | Valuation Baseline |
| :--- | :--- |
| **Call Price** | 10.4506 |
| **Put Price** | 5.5735 |
| **Parity Divergence** | ~0 |

### 2. Discrete-Time Convergence (Binomial vs. Analytical)
To evaluate the stability of the numerical lattice engine, a standard at-the-money contract (S=100, K=100, volatility=20%, risk-free rate=5%, maturity=1 year) was priced across expanding tree steps to witness asymptotic convergence toward the Black-Scholes limits.

| Binomial Tree Steps | Absolute Pricing Error |
| :--- | :--- |
| 10 | 0.197 |
| 50 | 0.040 |
| 100 | 0.020 |
| 500 | 0.004 |
| 1000 | 0.002 |
| 2000 | 0.001 |

### 3. Empirical Market Studies (AAPL Volatility Smile)
The numerical framework was stress-tested against live Apple Inc. (AAPL) option chain distributions, applying an institutional liquid-contract moneyness constraint (0.8 <= K/S <= 1.2) to eliminate structural out-of-the-money anomalies.

* **The Volatility Smile Phenomenon:** Plotting strike dimensions against numerical implied volatility metrics mapped out a classic U-shaped "volatility smile". This directly demonstrates that real-world volatility varies across strike configurations, capturing a fundamental empirical limitation of the baseline Black-Scholes constant-volatility assumption.
* **Vendor Calibration Offset:** While the recovered implied volatility path closely tracked vendor curves, a persistent parallel level shift was identified. This empirical divergence points directly to distinct data-feed assumptions regarding dividend curves, underlying cost-of-carry parameters, or commercial interpolation routines.

---

## Author
* **Amir Akhmetov** – *Computational Finance & Computer Science Joint Degree Student*
