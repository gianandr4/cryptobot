
import time
from api_handler import PionexAPI
from risk_management import RiskManager
from sentiment_analysis import MarketSentiment
from backtesting import Backtester
from logging_and_alerts import Logger

# Initialize components
api = PionexAPI()
risk_manager = RiskManager()
sentiment_analyzer = MarketSentiment()
logger = Logger()

def main():
    while True:
        # Fetch market data
        market_data = api.get_market_data("BTC/USDT")
        current_price = market_data['price']
        
        # Analyze market sentiment
        sentiment = sentiment_analyzer.analyze_sentiment()
        logger.log(f"Market sentiment: {sentiment}")
        
        # Adjust grid strategy based on sentiment
        grid_size = sentiment_analyzer.adjust_grid(sentiment)
        
        # Handle risk management
        if risk_manager.check_stop_loss():
            api.place_stop_loss_order()
        
        # Execute grid trading logic
        api.place_orders(current_price, grid_size)
        
        time.sleep(60)  # Wait for next iteration

if __name__ == "__main__":
    main()
