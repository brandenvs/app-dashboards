import requests


def get_valr_btc_volume():
    """
    Fetches the current 24-hour trading volume of BTC from VALR exchange.
    """
    try:
        url = 'https://api.valr.com/v1/public/BTCZAR/marketsummary'
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            volume = float(data['baseVolume'])
            return volume
        else:
            raise Exception(f"Error fetching data from VALR: {data.get('error', 'Unknown error')}")

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def get_binance_btc_volume():
    """
    Fetches the current 24-hour trading volume of BTC from Binance exchange.
    """
    try:
        url = 'https://api.binance.com/api/v3/ticker/24hr'
        params = {'symbol': 'BTCUSDT'}
        response = requests.get(url, params=params)
        data = response.json()
        if response.status_code == 200:
            volume = float(data['volume'])
            return volume
        else:
            raise Exception(f"Error fetching data from Binance: {data.get('msg', 'Unknown error')}")

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
