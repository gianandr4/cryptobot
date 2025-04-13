import ccxt
import pandas as pd
import time
import numpy as np
import datetime
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt

# Function to fetch historical market data (OHLCV)
def fetch_historical_data(symbol, timeframe, limit=1000):
    exchange = ccxt.pionex()  # Assuming Pionex is supported via CCXT (replace with appropriate exchange)
    
    since = exchange.parse8601((datetime.datetime.now() - relativedelta(days=365)).isoformat())  # Last year of data
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since=since, limit=limit)
    ohlcv_df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
    ohlcv_df["timestamp"] = pd.to_datetime(ohlcv_df["timestamp"], unit='ms')
    return ohlcv_df

# Backtest the grid strategy
def backtest_grid_strategy(symbol, timeframe='1h', grid_size=0.005, initial_balance=1000, max_drawdown=0.10):
    # Fetch historical data
    data = fetch_historical_data(symbol, timeframe)
    
    # Initial conditions
    balance = initial_balance
    positions = []
    last_order_price = None
    profits = []
    drawdown_limit = initial_balance * (1 - max_drawdown)

    for index, row in data.iterrows():
        current_price = row['close']
        
        # Calculate grid levels
        if last_order_price is None:
            last_order_price = current_price
        
        buy_grid_level = last_order_price * (1 - grid_size)
        sell_grid_level = last_order_price * (1 + grid_size)
        
        # Simulate buy order if price drops below the buy grid level
        if current_price <= buy_grid_level:
            buy_amount = balance / current_price  # Assuming we're spending all balance in the buy order
            positions.append((buy_amount, current_price))  # Store the position (amount, price)
            last_order_price = buy_grid_level  # Update last order price
            print(f"Buy: {buy_amount} at {current_price}")
        
        # Simulate sell order if price rises above the sell grid level
        elif current_price >= sell_grid_level and positions:
            sell_amount, buy_price = positions.pop(0)  # Sell the first position in the list
            sell_value = sell_amount * current_price
            profit = sell_value - (buy_amount * buy_price)
            balance += profit
            profits.append(profit)
            last_order_price = sell_grid_level  # Update last order price
            print(f"Sell: {sell_amount} at {current_price}, Profit: {profit}")

        # Track balance and drawdown
        if balance <= drawdown_limit:
            print(f"Drawdown limit reached. Stopping backtest. Final balance: {balance}")
            break

    # Results
    total_profit = sum(profits)
    final_balance = balance
    print(f"Backtest completed. Final balance: {final_balance}")
    print(f"Total profit: {total_profit}")
    return total_profit, final_balance, profits

# Plotting the backtest performance
def plot_performance(profits):
    plt.figure(figsize=(10, 6))
    plt.plot(np.cumsum(profits))
    plt.title("Cumulative Profits from Backtest")
    plt.xlabel("Trades")
    plt.ylabel("Cumulative Profit")
    plt.show()

# Main function to run backtest
def run_backtest():
    symbol = 'BTC/USDT'  # Define your trading pair
    timeframe = '1h'  # 1-hour candles
    grid_size = 0.005  # 0.5% grid size
    initial_balance = 1000  # Initial portfolio balance
    max_drawdown = 0.10  # 10% max drawdown
    
    print("Running backtest...")
    total_profit, final_balance, profits = backtest_grid_strategy(symbol, timeframe, grid_size, initial_balance, max_drawdown)
    
    print(f"Final balance: {final_balance}")
    print(f"Total profit: {total_profit}")
    plot_performance(profits)

if __name__ == "__main__":
    run_backtest()
