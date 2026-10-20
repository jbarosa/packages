# Structured Products & Options Calculator

A Python-based toolkit for pricing vanilla and barrier options, modeling structured product payoffs, and screening simple options strategies.

This project is designed for research, educational use, and quick prototyping of option and structured product ideas. It includes a set of pricing functions and helper utilities for common derivatives and structured product constructions.

## Features

- Black-Scholes option pricing for calls and puts
- Barrier option pricing using simplified down-and-in / down-and-out formulas
- Structured product payoff and price helpers
  - capital protection
  - discount certificate
  - reverse convertible
  - barrier reverse convertible
- Basic strategy formulas for covered calls, protective puts, and put credit spreads
- PnL / hedge helper utilities
- Yahoo Finance option-chain candidate screening for put credit spreads

## Project structure

- `HedgeOpenPosition.py` — simple hedge / PnL helper examples
- `src/Derivatives.py` — vanilla and barrier option pricing formulas
- `src/StructuredProducts.py` — structured product payoff and pricing functions
- `src/DerivativesStrategies.py` — common options strategy payoff / pricing functions
- `src/PnLCalc.py` — PnL-related calculations
- `src/SelectionCriteria.py` — option-chain screening for put credit spreads
- `notebooks/worksheet.py` — exploratory notebook-style calculations

## Requirements

This project uses Python 3 and depends on:

- `scipy`
- `yfinance` (only required for option-chain lookup / screening features)

## Installation

Create a virtual environment and install the dependencies:

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
pip install scipy yfinance
```

On macOS/Linux:

```bash
source .venv/bin/activate
pip install scipy yfinance
```

## Quick start

### Black-Scholes example

```python
from src.Derivatives import black_scholes_call, black_scholes_put

S = 100
K = 100
T = 1
r = 0.05
q = 0.02
sigma = 0.20

call_price = black_scholes_call(S, K, T, r, q, sigma)
put_price = black_scholes_put(S, K, T, r, q, sigma)

print(round(call_price, 4))
print(round(put_price, 4))
```

### Barrier option example

```python
from src.Derivatives import down_and_in_call, down_and_in_put

S = 100
K = 100
B = 90
T = 1
r = 0.05
q = 0.02
sigma = 0.20

print(down_and_in_call(S, K, B, T, r, q, sigma))
print(down_and_in_put(S, K, B, T, r, q, sigma))
```

### Structured product example

```python
from src.StructuredProducts import capital_protection_price, reverse_convertible_payoff

price = capital_protection_price(
    S=100,
    K=100,
    T=1,
    r=0.05,
    q=0.02,
    sigma=0.20,
    participation=1.0,
    protection=100,
    cap=0,
)

payoff = reverse_convertible_payoff(
    S=95,
    K=100,
    T=1,
    r=0.05,
    q=0.02,
    sigma=0.20,
    participation=1.0,
    notional=100,
    coupon=5,
)

print(round(price, 4))
print(payoff)
```

### Option spread screening example

```bash
python src/SelectionCriteria.py SPY --min-dte 30 --max-dte 45 --delta 0.4 --max-loss 300 --top 10
```

This command fetches option-chain data for SPY and prints candidate put credit spreads based on your filters.

## Notes

- Many functions in this project are educational approximations and may not be production-grade pricing models.
- Barrier pricing formulas in this repository are simplified and meant for quick analysis.
- The option screening logic depends on live market data from Yahoo Finance and may require internet access.
- This project is not financial advice and should be used only for educational and analytical purposes.

## License

This project does not currently include a formal license file. If you are using it in a production or commercial environment, confirm the legal constraints with the repository owner before distribution or reuse.
