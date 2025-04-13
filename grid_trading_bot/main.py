import time
import logging
from api_helper import get_market_data, execute_order
from sentiment_analysis import analyze_sentiment
from grid_trading import GridTrader
from risk_management import RiskManager
from backtest import Backtest
from logging_helper import setup_logging

# Setup logging
setup_logging()

# Configure API keys and settings
API_KEY = 'your_api_key'
API_SECRET = 'your_api_secret'
TRADING_PAIR = 'BTC_USDT'
GRID_SIZE = 0.002  # 0.2% grid size
STOP_LOSS_PERCENTAGE = 0.05  # 5% stop loss
TAKE_PROFIT_PERCENTAGE = 0.05  # 5% take profit

# Initialize grid trader and risk manager
grid_trader = GridTrader(API_KEY, API_SECRET, TRADING_PAIR, GRID_SIZE)
risk_manager = RiskManager(STOP_LOSS_PERCENTAGE, TAKE_PROFIT_PERCENTAGE)

# Main loop
while True:
    try:
        market_data = get_market_data(API_KEY, API_SECRET, TRADING_PAIR)
        sentiment = analyze_sentiment(market_data['price'])
        grid_trader.adjust_grid_based_on_sentiment(sentiment)

        # Execute orders based on the grid strategy
        grid_trader.place_orders()

        # Handle risk management
        risk_manager.monitor_risk()

        time.sleep(10)  # Wait for the next market check
    except Exception as e:
        logging.error(f"Error in main loop: {e}")
        time.sleep(60)  # Wait before retrying
