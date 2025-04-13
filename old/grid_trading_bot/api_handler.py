
import ccxt
import time

class PionexAPI:
    def __init__(self):
        self.api_key = 'your_api_key'
        self.api_secret = 'your_api_secret'
        self.exchange = ccxt.pionex({
            'apiKey': self.api_key,
            'secret': self.api_secret
        })
    
    def safe_api_call(self, func, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"API call failed: {e}")
            time.sleep(5)
            return self.safe_api_call(func, *args, **kwargs)
    
    def get_market_data(self, symbol):
        return self.safe_api_call(self.exchange.fetch_ticker, symbol)
    
    def place_orders(self, current_price, grid_size):
        # Example: Place a series of buy and sell orders based on the grid size
        buy_price = current_price - grid_size
        sell_price = current_price + grid_size
        self.safe_api_call(self.exchange.create_limit_buy_order, 'BTC/USDT', 0.01, buy_price)
        self.safe_api_call(self.exchange.create_limit_sell_order, 'BTC/USDT', 0.01, sell_price)
    
    def place_stop_loss_order(self):
        # Example: Place stop-loss order
        stop_price = self.get_market_data('BTC/USDT')['price'] * 0.95
        self.safe_api_call(self.exchange.create_stop_limit_order, 'BTC/USDT', 'sell', 0.01, stop_price, stop_price)
