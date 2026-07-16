"""Select put credit spreads using Yahoo Finance option data."""

from __future__ import annotations

import argparse
import datetime
import math
import sys
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

try:
    import yfinance as yf
except ImportError:  # pragma: no cover
    yf = None


@dataclass
class PutOption:
    strike: float
    bid: float
    ask: float
    last_price: float
    implied_vol: Optional[float]
    delta: Optional[float]
    open_interest: Optional[int]
    in_the_money: bool
    contract_symbol: str


def norm_cdf(x: float) -> float:
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def approximate_put_delta(
    underlying: float,
    strike: float,
    days_to_expiry: int,
    implied_vol: Optional[float],
    annual_rate: float = 0.03,
    dividend_yield: float = 0.0,
) -> Optional[float]:
    if implied_vol is None or implied_vol <= 0 or days_to_expiry <= 0:
        return None

    T = days_to_expiry / 365.0
    sigma = implied_vol
    if sigma <= 0:
        return None

    try:
        d1 = (
            math.log(underlying / strike)
            + (annual_rate - dividend_yield + 0.5 * sigma**2) * T
        ) / (sigma * math.sqrt(T))
    except ValueError:
        return None

    return norm_cdf(d1) - 1.0


def load_put_chain(
    ticker: str,
    expiration: str,
    underlying_price: float,
    days_to_expiry: int,
    dividend_yield: float,
    annual_rate: float = 0.03,
) -> List[PutOption]:
    if yf is None:
        raise RuntimeError(
            'yfinance is required for option chain lookup. Install with `pip install yfinance`.'
        )

    ticker_obj = yf.Ticker(ticker)
    chain = ticker_obj.option_chain(expiration)
    puts = []

    for _, row in chain.puts.iterrows():
        strike = float(row['strike'])
        bid = float(row['bid'] or 0.0)
        ask = float(row['ask'] or 0.0)
        last_price = float(row['lastPrice'] or 0.0)
        implied_vol = float(row['impliedVolatility']) if row['impliedVolatility'] not in (None, float('nan')) else None
        delta = None

        if 'delta' in row.index and row['delta'] not in (None, float('nan')):
            delta = float(row['delta'])
        else:
            delta = approximate_put_delta(
                underlying_price,
                strike,
                days_to_expiry,
                implied_vol,
                annual_rate=annual_rate,
                dividend_yield=dividend_yield,
            )

        puts.append(
            PutOption(
                strike=strike,
                bid=bid,
                ask=ask,
                last_price=last_price,
                implied_vol=implied_vol,
                delta=delta,
                open_interest=int(row['openInterest']) if row['openInterest'] not in (None, float('nan')) else None,
                in_the_money=bool(row['inTheMoney']),
                contract_symbol=str(row['contractSymbol']),
            )
        )

    return puts


def select_put_credit_spreads(
    ticker: str,
    min_dte: int,
    max_dte: int,
    target_delta: float,
    max_loss: float,
    max_profit: Optional[float] = None,
    max_spread: float = 0.25,
    min_open_interest: int = 1,
    top_n: int = 10,
) -> List[Dict[str, Any]]:
    if yf is None:
        raise RuntimeError('yfinance must be installed to run this selector.')

    ticker_obj = yf.Ticker(ticker)
    today = datetime.date.today()
    expirations = list(ticker_obj.options)
    if not expirations:
        raise RuntimeError(f'No option expirations found for {ticker}')

    expirations_with_dte: List[tuple[str, int]] = []
    for expiration in expirations:
        exp_date = datetime.date.fromisoformat(expiration)
        dte = (exp_date - today).days
        if min_dte <= dte <= max_dte:
            expirations_with_dte.append((expiration, dte))

    if not expirations_with_dte:
        raise RuntimeError(
            f'No expirations found for {ticker} between {min_dte} and {max_dte} DTE.'
        )

    history = ticker_obj.history(period='5d')
    if history.empty:
        raise RuntimeError(f'Unable to fetch historical price data for {ticker}')

    underlying_price = float(history['Close'].iloc[-1])
    dividend_yield = float(
        ticker_obj.info.get('dividendYield', 0.0) or 0.0
    )

    candidates: List[Dict[str, Any]] = []
    for expiration, dte in expirations_with_dte:
        put_chain = load_put_chain(
            ticker,
            expiration,
            underlying_price,
            dte,
            dividend_yield,
        )

        put_chain = [put for put in put_chain if put.bid > 0 and put.ask > 0]
        put_chain.sort(key=lambda o: o.strike)

        for i, short_put in enumerate(put_chain):
            if short_put.open_interest is not None and short_put.open_interest < min_open_interest:
                continue
            if short_put.delta is None:
                continue
            if abs(abs(short_put.delta) - target_delta) > 0.15:
                continue
            if short_put.ask - short_put.bid > max_spread:
                continue

            for long_put in put_chain[:i]:
                if long_put.ask <= 0:
                    continue
                if long_put.open_interest is not None and long_put.open_interest < min_open_interest:
                    continue
                if long_put.ask - long_put.bid > max_spread:
                    continue

                credit = short_put.bid - long_put.ask
                if credit <= 0:
                    continue

                width = short_put.strike - long_put.strike
                if width <= 0:
                    continue

                max_loss_calc = width * 100 - credit * 100
                max_profit_calc = credit * 100
                if max_loss_calc > max_loss:
                    continue
                if max_profit is not None and max_profit_calc > max_profit:
                    continue

                candidates.append(
                    {
                        'expiration': expiration,
                        'dte': dte,
                        'short_strike': short_put.strike,
                        'long_strike': long_put.strike,
                        'credit': round(credit, 4),
                        'max_profit': round(max_profit_calc, 2),
                        'max_loss': round(max_loss_calc, 2),
                        'spread_width': round(width, 2),
                        'short_delta': round(short_put.delta, 4),
                        'short_bid': round(short_put.bid, 4),
                        'long_ask': round(long_put.ask, 4),
                        'short_oi': short_put.open_interest,
                        'long_oi': long_put.open_interest,
                        'short_symbol': short_put.contract_symbol,
                        'long_symbol': long_put.contract_symbol,
                        'prob_close_to_delta': abs(abs(short_put.delta) - target_delta),
                    }
                )

    candidates.sort(key=lambda x: (x['max_loss'], -x['max_profit'], x['prob_close_to_delta']))
    return candidates[:top_n]


def print_spreads(spreads: List[Dict[str, Any]], ticker: str) -> None:
    if not spreads:
        print('No candidate put credit spreads found.')
        return

    print(f'Candidate put credit spreads for {ticker}:')
    print('-' * 82)
    print(
        'Exp   DTE  Short  Long   Credit   MaxProfit  MaxLoss  Delta   ShortOI  LongOI'
    )
    print('-' * 82)
    for spread in spreads:
        print(
            f"{spread['expiration']} {spread['dte']:4d} "
            f"{spread['short_strike']:6.2f} {spread['long_strike']:6.2f} "
            f"{spread['credit']:7.3f}  {spread['max_profit']:9.2f} "
            f"{spread['max_loss']:8.2f}  {spread['short_delta']:6.3f} "
            f"{(spread['short_oi'] or 0):8d} {(spread['long_oi'] or 0):7d}"
        )
    print('-' * 82)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Find put credit spread candidates using Yahoo Finance option chains.'
    )
    parser.add_argument('ticker', help='Underlying ticker symbol, e.g. SPY')
    parser.add_argument('--min-dte', type=int, default=30, help='Minimum DTE to consider.')
    parser.add_argument('--max-dte', type=int, default=45, help='Maximum DTE to consider.')
    parser.add_argument('--delta', type=float, default=0.4, help='Target short put absolute delta.')
    parser.add_argument('--max-loss', type=float, default=300.0, help='Maximum allowed loss per spread in dollars.')
    parser.add_argument('--max-profit', type=float, default=None, help='Maximum allowed profit per spread in dollars. Leave unset to ignore this filter.')
    parser.add_argument('--top', type=int, default=10, help='Number of candidate spreads to show.')
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        spreads = select_put_credit_spreads(
            args.ticker,
            args.min_dte,
            args.max_dte,
            args.delta,
            args.max_loss,
            args.max_profit,
            top_n=args.top,
        )
        print_spreads(spreads, args.ticker)
        return 0
    except Exception as exc:
        print('Error:', exc, file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())

