import math
from scipy.stats import norm

def black_scholes_call(S, K, T, r, q, sigma):
    """
    S: preço atual do ativo
    K: strike (preço de exercício)
    T: tempo até maturidade (em anos)
    r: taxa de juros livre de risco (decimal, ex: 0.05)
    q: dividend yield (decimal, ex: 0.02)
    sigma: volatilidade (decimal, ex: 0.2)
    """

    d1 = (math.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)

    call_price = S * math.exp(-q * T) * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    return call_price


def black_scholes_put(S, K, T, r, q, sigma):
    """
    S: preço atual do ativo
    K: strike (preço de exercício)
    T: tempo até maturidade (em anos)
    r: taxa de juros livre de risco (decimal, ex: 0.05)
    q: dividend yield (decimal, ex: 0.02)
    sigma: volatilidade (decimal, ex: 0.2)
    """

    d1 = (math.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)

    put_price = - S * norm.cdf(-d1) * math.exp(-q * T) + K * math.exp(-r * T) * norm.cdf(-d2) 
    return put_price


# --- Down-and-Out Call (closed-form, simplified) ---
def down_and_out_call(S, K, B, T, r, q, sigma):
    if S <= B:
        return 0.0  # already knocked out

    lambda_ = (r - q + 0.5 * sigma**2) / (sigma**2)

    x1 = (math.log(S / K) / (sigma * math.sqrt(T))) + lambda_ * sigma * math.sqrt(T)
    y1 = (math.log(B**2 / (S * K)) / (sigma * math.sqrt(T))) + lambda_ * sigma * math.sqrt(T)

    A = S * norm.cdf(x1) - K * math.exp(-r * T) * norm.cdf(x1 - sigma * math.sqrt(T))
    B_term = S * math.exp(-q * T)*(B / S)**(2 * lambda_) * norm.cdf(y1) \
           - K * math.exp(-r * T) * (B / S)**(2 * lambda_ - 2) * norm.cdf(y1 - sigma * math.sqrt(T))

    return A - B_term


# --- Down-and-In Call ---
def down_and_in_call(S, K, B, T, r, q, sigma):
    vanilla = black_scholes_call(S, K, T, r, q, sigma)
    down_out = down_and_out_call(S, K, B, T, r, q, sigma)

    return vanilla - down_out


def down_and_out_put(S, K, H, T, r, q, sigma):
    """
    Down-and-Out Put (continuous barrier, no rebate)
    H < S, H < K typically
    """
    if S <= H:
        return 0.0  # already knocked out

    if T <= 0:
        return max(K - S, 0.0) if S > H else 0.0

    lam = (r - q + 0.5 * sigma**2) / sigma**2
    x1 = math.log(S / K) / (sigma * math.sqrt(T)) + (lam + 1) * sigma * math.sqrt(T)
    x2 = math.log(S / H) / (sigma * math.sqrt(T)) + (lam + 1) * sigma * math.sqrt(T)
    y1 = math.log(H**2 / (S * K)) / (sigma * math.sqrt(T)) + (lam + 1) * sigma * math.sqrt(T)
    y2 = math.log(H / S) / (sigma * math.sqrt(T)) + (lam + 1) * sigma * math.sqrt(T)

    A = black_scholes_put(S, K, T, r, q, sigma)

    B = (
        S * math.exp(-q * T) * (H / S) ** (2 * lam) * norm.cdf(y2)
        - K * math.exp(-r * T) * (H / S) ** (2 * lam - 2) * norm.cdf(y1)
    )

    return A - B


def down_and_in_put(S, K, H, T, r, q, sigma):
    """
    Down-and-In Put via in-out parity
    DIP = Vanilla Put - Down-and-Out Put
    """
    vanilla = black_scholes_put(S, K, T, r, q, sigma)
    dout = down_and_out_put(S, K, H, T, r, q, sigma)

    return vanilla - dout


# Exemplo de uso
S = 100     # preço do ativo
K = 100     # strike
T = 1       # 1 ano
r = 0.05    # 5% taxa de juros
q = 0.02    # 2% dividend yield
sigma = 0.2 # 20% volatilidade
B = K - 10 # barreira para o down-and-out call (ex: 10% abaixo do strike)
H = K - 10 # barreira para o down-and-out put (ex: 10% abaixo do strike)

call_price = black_scholes_call(S, K, T, r, q, sigma)
put_price = black_scholes_put(S, K, T, r, q, sigma)
dic_price = down_and_in_call(S, K, B, T, r, q, sigma)
dip_price = down_and_in_put(S, K, H, T, r, q, sigma)

#print(f"Preço da Call: {round(call_price,2)}")
#print(f"Preço da Put: {round(put_price,2)}")
#print(f"Down-and-In Call Price: {round(dic_price,2)}")
#print(f"Down-and-In Put Price: {round(dip_price,2)}")