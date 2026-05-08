
def put_credit_spread_pnl(participation, premium_received, K1, K2, S):
    # K1 < K2 typically, K1 is the short put strike, K2 is the long put strike
    # PnL = Premium received + Payoff at maturity
    payoff = max(0, K1 - S) - max(0, K2 - S)
    
    current_pnl = premium_received + payoff * participation
    max_profit = premium_received  # Max profit occurs if both options expire worthless
    max_loss = (K2 - K1) * participation - premium_received  # Max loss occurs if S <= K1
    
    #k1 < S < k2 -> payoff = 0 - max(0, K2 - S) = -(K2 - S) -> loss but limited
    
    
    return current_pnl, max_profit, max_loss

