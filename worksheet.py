import StructuredProducts as sp
import DerivativesStrategies as ds
import PnLCalc as pnl

def price_cp(S, K, T, r, q, sigma, participation, protection, cap=0):
    return sp.capital_protection_price(S, K, T, r, q, sigma, participation, protection, cap)

cp_silver = price_cp(79.7961,63,2,0.03,0,0.2,1,90,cap=160)
print(cp_silver)

s=12.0
k1=10.5
k2=11.0
participation=4
t=30
k1_bid=0.04
k1_ask=0.05
k2_bid=0.10
k2_ask=0.11

premium_received_test = (k2_bid - k1_ask)*participation*100  # Net premium received from selling the spread
print(f"Premium received: {premium_received_test}€")

current_pnl, max_profit, max_loss, max_cover = pnl.put_credit_spread_pnl(participation, premium_received_test, k1, k2, s)
print(f"Current PnL: {current_pnl}€")
print(f"Max margin required: {max_loss}€")
print(f"Max profit: {max_profit}€")
print(f"Max cover: {max_cover}€")

s=739
k1=670
k2=675
participation=1
t=30
k1_bid=1.65
k1_ask=1.67
k2_bid=1.86
k2_ask=1.88

premium_received_test = (k2_bid - k1_ask)*participation*100  # Net premium received from selling the spread
print(f"Premium received: {premium_received_test}€")

current_pnl, max_profit, max_loss, max_cover = pnl.put_credit_spread_pnl(participation, premium_received_test, k1, k2, s)
print(f"Current PnL: {current_pnl}€")
print(f"Max margin required: {max_loss}€")
print(f"Max profit: {max_profit}€")
print(f"Max cover: {max_cover}€")