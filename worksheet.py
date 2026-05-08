import StructuredProducts as sp
import DerivativesStrategies as ds

def price_cp(S, K, T, r, q, sigma, participation, protection, cap=0):
    return sp.capital_protection_price(S, K, T, r, q, sigma, participation, protection, cap)

cp_silver = price_cp(79.7961,63,2,0.03,0,0.2,1,90,cap=160)
print(cp_silver)

# Example usage of put credit spread payoff and price
spot=100

put2_strike = 80
put2_bid = 0.5
put2_ask = 0.6

put1_strike = 50
put1_bid = 0.2
put1_ask = 0.7

participation = 1  # Number of spreads
premium_received = put2_bid - put1_ask  # Net premium received from selling the spread
current_liquidation = premium_received - put2_ask + put1_bid # Current liquidation value if we were to close the position now (buy back the short put at ask, sell the long put at bid)

print(f"Premium received: {participation*premium_received}")
print(f"Current liquidation value: {participation*current_liquidation}")
