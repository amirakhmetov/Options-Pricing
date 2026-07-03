# Options Pricing Engine & Market Validation

An institutional-grade derivatives analytics platform that bridges theoretical option pricing models with empirical market data extraction. The system implements closed-form Black-Scholes pricing, computes risk-management Greeks, constructs Cox-Ross-Rubinstein (CRR) binomial trees, and resolves market-implied volatilities using numerical root-finding methods.

---

## Features

* **Analytical Pricing Core:** Full European call and put evaluation incorporating continuous dividend yields ($q$).
* **Risk Greeks Engine:** Sensitivity modules calculating first and second-order risk measures: Delta ($\Delta$), Gamma ($\Gamma$), Vega ($\mathcal{V}$), Theta ($\Theta$), and Rho ($\rho$).
* **Numerical Lattice Engine:** Discrete-time Cox-Ross-Rubinstein binomial tree framework to analyze numerical pricing convergence behaviors.
* **Implied Volatility Solver:** A robust root-finding module utilizing a numerical bisection algorithm to invert market midpoint prices into volatility metrics.
* **Live Ingestion Pipeline:** Automated data ingestion via `yfinance` to track live option chains, contract spreads, and historical underlying price series.

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
