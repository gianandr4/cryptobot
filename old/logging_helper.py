import logging

def setup_logging():
    logging.basicConfig(
        filename='grid_trading_bot.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logging.info("Logging initialized for Grid Trading Bot")
