def calculate_volatility(prices):
    # Calculate market volatility based on historical prices
    volatility = max(prices) - min(prices)
    return volatility
