<h1>Cryptobot Technical Documentation</h1>

<p>This section provides technical documentation for each of the scripts in the Cryptobot project. The documentation includes an overview, functionality, and usage instructions for each script.</p>

<h2>1. <code>main.py</code></h2>
<h3>Overview</h3>
<p>The <code>main.py</code> script is the entry point of the bot. It initializes the bot, sets up the trading environment, and starts the trading loop.</p>

<h3>Functionality</h3>
<ul>
    <li>Initializes the Pionex API connection using provided credentials.</li>
    <li>Sets up the trading parameters like the trading pair, grid size, and stop-loss limits.</li>
    <li>Starts the main loop that continuously monitors the market and places trades based on market conditions and sentiment analysis.</li>
</ul>

<h3>Usage</h3>
<pre>
    python main.py --api-key <your-api-key> --api-secret <your-api-secret> --symbol <trading-pair>
</pre>
<p><code>--api-key</code> and <code>--api-secret</code> are required for Pionex API authentication. <code>--symbol</code> specifies the trading pair (e.g., BTC/USDT).</p>

<h2>2. <code>api.py</code></h2>
<h3>Overview</h3>
<p>The <code>api.py</code> script contains functions to handle API calls to Pionex using the <code>ccxt</code> library. This script is responsible for executing trades, retrieving portfolio data, and interacting with the exchange's API.</p>

<h3>Functionality</h3>
<ul>
    <li>Connects to Pionex API using provided credentials.</li>
    <li>Handles basic trading operations like fetching market prices, portfolio balances, and placing buy/sell orders.</li>
    <li>Includes error handling for failed API calls and rate-limiting compliance.</li>
</ul>

<h3>Usage</h3>
<pre>
    from api import PionexAPI

    api = PionexAPI(api_key="<your-api-key>", api_secret="<your-api-secret>")
    market_price = api.get_market_price("BTC/USDT")
    balance = api.get_balance()
    api.place_order("BTC/USDT", "buy", 0.01, market_price)
</pre>

<h2>3. <code>risk_management.py</code></h2>
<h3>Overview</h3>
<p>The <code>risk_management.py</code> script handles the risk management aspects of the bot. It includes logic for stop-loss and take-profit orders, as well as drawdown protection.</p>

<h3>Functionality</h3>
<ul>
    <li>Sets stop-loss and take-profit orders based on market conditions.</li>
    <li>Monitors the portfolio for drawdown, stopping trading if the balance drops below a specified threshold.</li>
    <li>Integrates with the <code>api.py</code> script to place orders when risk conditions are met.</li>
</ul>

<h3>Usage</h3>
<pre>
    from risk_management import RiskManager

    risk_manager = RiskManager(api)
    risk_manager.monitor_risk()
</pre>
<p><code>monitor_risk()</code> continuously checks if the portfolio exceeds the drawdown limit or triggers a stop-loss or take-profit order.</p>

<h2>4. <code>grid_trading.py</code></h2>
<h3>Overview</h3>
<p>The <code>grid_trading.py</code> script is responsible for placing and managing grid orders. It defines the grid strategy, including the placement of buy and sell orders at various price levels.</p>

<h3>Functionality</h3>
<ul>
    <li>Calculates the grid levels (buy and sell orders) based on market prices and grid size.</li>
    <li>Places orders at predetermined price levels, updating them as market conditions change.</li>
    <li>Logs every order placed, including the amount gained or lost after fees.</li>
</ul>

<h3>Usage</h3>
<pre>
    from grid_trading import GridTrader

    grid_trader = GridTrader(api, symbol="BTC/USDT", grid_size=0.5)
    grid_trader.place_grid_orders()
</pre>
<p><code>place_grid_orders()</code> calculates the buy and sell levels and places orders accordingly. The <code>grid_size</code> defines the spacing between the levels.</p>

<h2>5. <code>sentiment_analysis.py</code></h2>
<h3>Overview</h3>
<p>The <code>sentiment_analysis.py</code> script uses OpenAI's GPT-4 API to analyze market sentiment and adjust the grid strategy accordingly.</p>

<h3>Functionality</h3>
<ul>
    <li>Uses the OpenAI GPT-4 API to perform sentiment analysis based on the current market conditions.</li>
    <li>Adjusts the grid strategy (grid size and spacing) based on the market sentiment (bullish, bearish, or neutral).</li>
</ul>

<h3>Usage</h3>
<pre>
    from sentiment_analysis import SentimentAnalyzer

    sentiment_analyzer = SentimentAnalyzer(api_key="<your-openai-api-key>")
    sentiment = sentiment_analyzer.get_market_sentiment("BTC/USDT")
    sentiment_analyzer.adjust_grid(sentiment)
</pre>
<p><code>get_market_sentiment()</code> uses GPT-4 to analyze sentiment, and <code>adjust_grid()</code> dynamically adjusts the grid strategy based on the sentiment.</p>

<h2>6. <code>monitoring.py</code></h2>
<h3>Overview</h3>
<p>The <code>monitoring.py</code> script continuously monitors the bot's performance, logs key events, and sends real-time alerts via Telegram.</p>

<h3>Functionality</h3>
<ul>
    <li>Monitors the bot's balance, trading activity, and risk events.</li>
    <li>Sends real-time Telegram alerts for events such as trade execution, stop-loss triggers, and drawdown limits.</li>
    <li>Logs all important events for transparency and troubleshooting.</li>
</ul>

<h3>Usage</h3>
<pre>
    from monitoring import BotMonitor

    bot_monitor = BotMonitor(api, telegram_bot_token="<your-telegram-bot-token>")
    bot_monitor.start_monitoring()
</pre>
<p><code>start_monitoring()</code> initiates the monitoring loop and sends Telegram alerts for significant events like trades and risk events.</p>

<h2>7. <code>backtesting.py</code></h2>
<h3>Overview</h3>
<p>The <code>backtesting.py</code> script provides a basic backtesting feature that simulates the trading strategy using historical data. It allows the user to test the grid trading strategy before deploying it live.</p>

<h3>Functionality</h3>
<ul>
    <li>Simulates grid trading using historical price data.</li>
    <li>Logs every trade and calculates the profit/loss based on the backtested trades.</li>
    <li>Compares the backtest results with actual market data to evaluate performance.</li>
</ul>

<h3>Usage</h3>
<pre>
    from backtesting import Backtester

    backtester = Backtester(api, symbol="BTC/USDT", grid_size=0.5, historical_data="historical_data.csv")
    backtester.run_backtest()
</pre>
<p><code>run_backtest()</code> runs the backtest on the provided historical data and logs the results for analysis.</p>

<h2>Conclusion</h2>
<p>This documentation provides an overview of the key scripts that make up the Cryptobot. Each script is modular and can be adjusted for specific needs, from API integration to risk management and sentiment-based trading strategies. Use these scripts to configure and customize your trading bot for different market conditions.</p>
