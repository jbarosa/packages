import StructuredProducts as sp
import DerivativesStrategies as ds

def price_cp(S, K, T, r, q, sigma, participation, protection, cap=0):
    return sp.capital_protection_price(S, K, T, r, q, sigma, participation, protection, cap)

cp_silver = price_cp(79.7961,63,2,0.03,0,0.2,1,90,cap=160)
print(cp_silver)

