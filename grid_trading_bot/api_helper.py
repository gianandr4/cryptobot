import ccxt
import logging

def get_market_data(api_key, api_secret, trading_pair):
    exchange = ccxt.pionex({
        'apiKey': api_key,
        'secret': api_secret,
    })
    market_data = exchange.fetch_ticker(trading_pair)
    return market_data

def execute_order(api_key, api_secret, order_params):
    exchange = ccxt.pionex({
        'apiKey': api_key,
        'secret': api_secret,
    })
    response = exchange.create_order(order_params)
    return response
