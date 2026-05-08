import StructuredProducts as sp
import DerivativesStrategies as ds


def put_credit_spread_pnl(participation, premium_received, K1, K2, S):
    # K1 < K2 typically, K1 is the short put strike, K2 is the long put strike
    # PnL = Premium received + Payoff at maturity
    payoff = max(0, K1 - S) - max(0, K2 - S)
    
    current_pnl = premium_received + payoff * participation
    max_profit = premium_received  # Max profit occurs if both options expire worthless
    max_loss = (K2 - K1) * participation - premium_received  # Max loss occurs if S <= K1
    
    #k1 < S < k2 -> payoff = 0 - max(0, K2 - S) = -(K2 - S) -> loss but limited
    
    
    return current_pnl, max_profit, max_loss


# Example usage of put credit spread payoff and price
spot=16

put2_strike = 14
put2_bid = 0.11
put2_ask = 0.38

put1_strike = 13.5
put1_bid = 0.04
put1_ask = 0.7

participation = 1  # Number of spreads
premium_received = put2_bid - put1_ask  # Net premium received from selling the spread
current_liquidation = premium_received - put2_ask + put1_bid # Current liquidation value if we were to close the position now (buy back the short put at ask, sell the long put at bid)

print(f"Premium received: {participation*premium_received}")
print(f"Current liquidation value: {participation*current_liquidation}")