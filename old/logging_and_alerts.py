
import logging
import telegram

class Logger:
    def __init__(self):
        logging.basicConfig(filename="bot.log", level=logging.INFO)
        self.telegram_bot = telegram.Bot(token="your_telegram_bot_token")
        self.chat_id = "your_chat_id"
    
    def log(self, message):
        logging.info(message)
        self.send_telegram_alert(message)
    
    def send_telegram_alert(self, message):
        self.telegram_bot.send_message(chat_id=self.chat_id, text=message)
