from telegram import Bot
from telegram.error import TelegramError
import asyncio
import os
from utils.logger import get_logger

logger = get_logger(__name__)

class TelegramNotifier:
    def __init__(self):
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self.bot = Bot(token) if token else None
        
    async def send_message(self, text: str) -> bool:
        if not self.bot:
            logger.warning("Telegram not configured")
            return False
            
        try:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=text,
                parse_mode='Markdown'
            )
            return True
        except TelegramError as e:
            logger.error(f"Telegram error: {e}")
            return False
            
    async def notify_trade(self, order: dict) -> bool:
        """Format and send trade notification"""
        side = "🟢 BUY" if order['side'] == 'buy' else "🔴 SELL"
        text = (
            f"*Trade Executed*\n"
            f"Pair: `{order['symbol']}`\n"
            f"Side: {side}\n"
            f"Price: `{order['price']}`\n"
            f"Amount: `{order['amount']}`\n"
            f"Value: `{order['price'] * order['amount']:.2f}`"
        )
        return await self.send_message(text)