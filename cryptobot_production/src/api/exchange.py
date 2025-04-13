import ccxt
import asyncio
import numpy as np
from typing import Tuple, List, Dict
from utils.logger import get_logger
from dataclasses import dataclass

logger = get_logger(__name__)

@dataclass
class Order:
    symbol: str
    side: str  # 'buy' or 'sell'
    price: float
    amount: float
    type: str = 'limit'

class PionexClient:
    def __init__(self):
        self.api = ccxt.pionex({
            'apiKey': os.getenv("PIONEX_API_KEY"),
            'secret': os.getenv("PIONEX_API_SECRET"),
            'enableRateLimit': True,
            'options': {
                'defaultType': 'spot'
            }
        })
        
    async def get_market_data(self, symbol: str) -> Tuple[float, float]:
        """Returns (price, volatility)"""
        try:
            # Get ticker and OHLCV data
            ticker = await self.api.fetch_ticker(symbol)
            ohlcv = await self.api.fetch_ohlcv(symbol, '1h', limit=24)
            
            # Calculate volatility (std of hourly returns)
            closes = [x[4] for x in ohlcv]
            returns = np.diff(closes) / closes[:-1]
            volatility = np.std(returns)
            
            return ticker['last'], volatility
            
        except Exception as e:
            logger.error(f"Market data error: {e}")
            raise
            
    async def execute_orders(self, orders: List[Order]) -> List[str]:
        """Execute batch orders, returns order IDs"""
        try:
            tasks = [self._place_order(order) for order in orders]
            return await asyncio.gather(*tasks)
        except ccxt.RateLimitExceeded:
            logger.warning("Rate limit exceeded, backing off...")
            await asyncio.sleep(5)
            return await self.execute_orders(orders)
            
    async def _place_order(self, order: Order) -> str:
        """Place single order"""
        try:
            response = await self.api.create_order(
                symbol=order.symbol,
                type=order.type,
                side=order.side,
                amount=order.amount,
                price=order.price
            )
            return response['id']
        except Exception as e:
            logger.error(f"Order failed: {e}")
            raise