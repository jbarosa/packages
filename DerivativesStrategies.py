from Derivatives import black_scholes_call, black_scholes_put
# Payoff and price functions for options strategies:
    # Covered Call: long stock + short call
    # Protective Put: long stock + long put
    # Collar: long stock + short call + long put
    # Straddle: long call + long put
    # Iron Condor: short call + long call + short put + long put
    # Butterfly Spread: long call + short call + long call (or put version) 
    # Put credit spread: short put + long put
    # Call credit spread: short call + long call
    
    
def covered_call_payoff(S, K):
    # long stock + short call
    return max(0, S - K)

def covered_call_price(S, K, T, r, sigma):
    #long stock + short call
    call_price = black_scholes_call(S, K, T, r, sigma)
    return S - call_price

def protective_put_payoff(S, K):
    #long stock + long put
    return max(0, K - S)

def protective_put_price(S, K, T, r, sigma):
    #long stock + long put
    put_price = black_scholes_put(S, K, T, r, sigma)
    return S + put_price

def put_credit_spread_payoff(S, K1, K2):
    # short put + long put
    # K1 < K2 typically, K1 is the short put strike, K2 is the long put strike
    return max(0, K1 - S) - max(0, K2 - S)

def put_credit_spread_price(S, K1, K2, T, r, sigma):
    # short put + long put
    # K1 < K2 typically, K1 is the short put strike, K2 is the long put strike
    put1_price = black_scholes_put(S, K1, T, r, sigma)
    put2_price = black_scholes_put(S, K2, T, r, sigma)
    return put2_price - put1_price