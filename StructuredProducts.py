
from Derivatives import black_scholes_call, black_scholes_put

# Payoff and price functions for structured products:
    # Capital Protection: long call option + long zero-coupon bond
    # Discount certificate:
    # Reverse convertible:
    # Counditional Coupon Barrier Reverse Convertible:
    # Autocallable:
    # Tracker certificate:
    # Outperformance certificate:
    # Bonus certificate:
    # Bonus Outperformance certificate:
    # Twin win certificate:
    # Warrant:
    # Spread warrant:
    # Warrant with knock-out:
    # Mini-Future:
    # Constant leverage certificate:

def capital_protection_payoff(S, K, T, r, q, sigma, participation, protection, cap=0):
    #long call option + long zero-coupon bond
    payoff = min(protection + participation * max(0, S - K), cap) if cap > 0 else protection + participation * max(0, S - K) 
    return payoff

def capital_protection_price(S, K, T, r, q, sigma, participation, protection, cap=0):
    #long call option + long zero-coupon bond  
    call_price = black_scholes_call(S, K, T, r, q, sigma)
    zero_cupon_bond_price = protection * (1 + r) ** (-T)
    return zero_cupon_bond_price + call_price * participation
