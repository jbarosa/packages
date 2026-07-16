import python.pricing.StructuredProducts as sp
import python.pricing.DerivativesStrategies as ds


def put_credit_spread_pnl(participation, premium_received, K1, K2, S):
    # K1 < K2 typically, K1 is the short put strike, K2 is the long put strike
    # PnL = Premium received + Payoff at maturity
    payoff = max(0, K1 - S) - max(0, K2 - S)
    
    current_pnl = premium_received + payoff * participation*100  # PnL in euros, considering participation and contract size (100)
    max_profit = premium_received  # Max profit occurs if both options expire worthless
    max_loss = (K2 - K1) * participation*100  # Max margin is the maximum loss potential of the spread
    max_cover = K2 * participation*100  # Max cover is the maximum amount that can be lost if the underlying price drops to ~k2, which is the strike of the long put times participation and contract size  
    #k1 < S < k2 -> payoff = 0 - max(0, K2 - S) = -(K2 - S) -> loss but limited
   
    return current_pnl, max_profit, max_loss, max_cover

def put_credit_spread_delta(participation, delta_k1, delta_k2):
    # Delta of a long put option is negative, delta of a short put option is positive
    spread_delta = delta_k1 + delta_k2
    return spread_delta * participation*100  # Adjusting for participation and contract size

