# %% [markdown]
# # Cypto-bot Initial Build
# 
# > 04 Jan 2025 | Branden van Staden
# 
# ## Objectives
# 
# - Get BTC: USDT (**Binance**)
# - GET BTC: ZAR (**VALR**)
# - GET USD: ZAR (**Yahoo Finance**)

# %%
import requests
from datetime import datetime, timedelta


# %% [markdown]
# ### BTC: USDT

# %%
def get_binance_btc_usdt():
    url = 'https://api.binance.com/api/v3/ticker/price'
    params = {'symbol': 'BTCUSDT'}
    response = requests.get(url, params=params)
    data = response.json()
    return float(data['price'])

def fetch_binance_order_book(symbol, limit=100):
    url = f'https://api.binance.com/api/v3/depth'
    params = {'symbol': symbol, 'limit': limit}

    response = requests.get(url, params=params)
    data = response.json()

    # Extracting bids and asks
    bids = [(float(bid[0]), float(bid[1])) for bid in data['bids']]
    asks = [(float(ask[0]), float(ask[1])) for ask in data['asks']]

    return bids, asks


# %% [markdown]
# ### BTC: ZAR

# %%
def get_valr_btc_zar():
    url = 'https://api.valr.com/v1/public/BTCZAR/marketsummary'
    response = requests.get(url)
    data = response.json()
    return float(data['lastTradedPrice'])

def fetch_valr_order_book(currency_pair):
    url = f'https://api.valr.com/v1/public/{currency_pair}/orderbook'
    response = requests.get(url)
    data = response.json()

    # Check if 'Asks' and 'Bids' are in the response
    if 'Asks' in data and 'Bids' in data:
        # Extracting bids and asks
        bids = [(float(bid['price']), float(bid['quantity'])) for bid in data['Bids']]
        asks = [(float(ask['price']), float(ask['quantity'])) for ask in data['Asks']]

    else:
        # If 'Asks' and 'Bids' are not present, process the combined list
        bids = [(float(order['price']), float(order['quantity'])) for order in data if order['side'] == 'buy']
        asks = [(float(order['price']), float(order['quantity'])) for order in data if order['side'] == 'sell']

    return bids, asks



# %% [markdown]
# ### USD: ZAR

# %%
def get_usd_to_zar_exchange_rate(api_key, date=None):
    """
    Fetches the USD to ZAR exchange rate from ExchangeRate-API.
    If a date is provided, fetches the historical rate for that date.
    """
    base_url = f'https://v6.exchangerate-api.com/v6/{api_key}'
    if date:
        url = f'{base_url}/history/USD/{date}'
    else:
        url = f'{base_url}/pair/USD/ZAR'
    
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        if date:
            # For historical data, navigate to the specific date and currency pair
            try:
                return float(data['rates']['ZAR'])
            except KeyError:
                raise Exception(f"Historical data for {date} not available.")
        else:
            return float(data['conversion_rate'])
    else:
        raise Exception(f"Error fetching data: {data.get('error-type', 'Unknown error')}")

def get_exchangerateapi_usd_zar(api_key):
    url = f'https://v6.exchangerate-api.com/v6/{api_key}/pair/USD/ZAR'
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        return float(data['conversion_rate'])
    else:
        raise Exception(f"Error fetching data: {data.get('error-type', 'Unknown error')}")
