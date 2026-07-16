
from python.pricing.Derivatives import black_scholes_call, black_scholes_put

# Payoff and price functions for structured products:
    # Capital Protection: long call option + long zero-coupon bond
    # Discount certificate: long stock + short call option or bond + short put option
    # Reverse convertible: bond + short put option
    # Counditional Coupon Barrier Reverse Convertible: bond + coupons + short put option with barrier (down-and-in put)
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
    # Structured deposit:

def capital_protection_payoff(S, K, T, r, q, sigma, participation, protection, cap=0):
    #long call option + long zero-coupon bond
    payoff = min(protection + participation * max(0, S - K), cap) if cap > 0 else protection + participation * max(0, S - K) 
    return payoff

def capital_protection_price(S, K, T, r, q, sigma, participation, protection, cap=0):
    #long call option + long zero-coupon bond  
    call_price = black_scholes_call(S, K, T, r, q, sigma)
    zero_cupon_bond_price = protection * (1 + r) ** (-T)
    return zero_cupon_bond_price + call_price * participation

def discount_certificate_payoff(S, K, T, r, q, sigma, participation):
    #long stock + short call option or bond + short put option
    payoff = S + participation * max(0, K - S)  # Payoff from the stock plus the payoff from the short call option
    return payoff

def discount_certificate_price(S, K, T, r, q, sigma, participation):
    #long stock + short call option or bond + short put option
    call_price = black_scholes_call(S, K, T, r, q, sigma)
    return S - call_price * participation  # Price of the stock minus the price of the short call option 

def reverse_convertible_payoff(S, K, T, r, q, sigma, participation, notional, coupon):
    #bond + short put option
    payoff = notional + coupon - participation * max(0, K - S)  # Payoff from the bond plus coupons minus the payoff from the short put option
    #if S<K and notional = K -> payoff = S + coupon 
    return payoff

def reverse_convertible_price(S, K, T, r, q, sigma, participation, notional, coupon):
    #bond + short put option
    put_price = black_scholes_put(S, K, T, r, q, sigma)
    zero_cupon_bond_price = notional * (1 + r) ** (-T)
    return zero_cupon_bond_price + coupon * (1 - (1 + r) ** (-T)) / r - put_price * participation  # Price of the bond plus the present value of coupons minus the price of the short put option

def barrier_reverse_convertible_payoff(S, K, H, T, r, q, sigma, participation, notional, coupon):
    #bond + coupons + short put option with barrier (down-and-in put)
    if S <= H:
        payoff = notional + coupon - participation * max(0, K - S)# payoff = S+coupon if K=notional  # Payoff from the bond plus coupons minus the payoff from the short put option
    else:
        payoff = notional + coupon  # Payoff from the bond plus coupons (short put option expires worthless)
    return payoff

def barrier_reverse_convertible_price(S, K, H, T, r, q, sigma, participation, notional, coupon):
    #bond + coupons + short put option with barrier (down-and-in put)
    down_and_in_put_price = black_scholes_put(S, K, T, r, q, sigma) - black_scholes_put(S, K, T, r, q, sigma) * (H / S) ** (2 * (r - q + 0.5 * sigma**2) / sigma**2)
    zero_cupon_bond_price = notional * (1 + r) ** (-T)
    return zero_cupon_bond_price + coupon * (1 - (1 + r) ** (-T)) / r - down_and_in_put_price * participation  # Price of the bond plus the present value of coupons minus the price of the short put option with barrier