# Grid Trading Bot

This project implements a grid trading strategy for the Pionex exchange. The bot is designed to manage risk, analyze market sentiment, and place buy/sell orders based on the grid strategy.

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Set up your API keys in `config.py`.

3. Run the bot:
   ```
   python main.py
   ```

## Features

- Dynamic grid size adjustment based on market sentiment
- Risk management (Stop-Loss, Take-Profit)
- Backtesting functionality
- Real-time alerts via Telegram
