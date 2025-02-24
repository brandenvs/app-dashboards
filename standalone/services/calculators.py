import requests

def calculate_live_gross_premium(price_binance, price_valr):
    """Calculate the Live Gross Premium between two exchanges."""
    premium = price_valr - price_binance
    percentage_premium = (premium / price_binance) * 100
    return premium, percentage_premium


def determine_optimal_trade(price_binance, price_valr, volume_a, volume_b):
    """Determine the ideal buy order on Exchange A that can be sold on Exchange B."""
    premium, percentage_premium = calculate_live_gross_premium(price_binance, price_valr)
    
    if premium <= 0:
        return "No arbitrage opportunity."
    
    # The maximum BTC that can be traded is limited by the lower of the available volumes
    tradeable_volume = min(volume_a, volume_b)
    
    potential_profit = tradeable_volume * premium
    
    return {
        "Live Gross Premium ($)": round(premium, 2),
        "Live Gross Premium (%)": round(percentage_premium, 2),
        "Tradeable Volume (BTC)": tradeable_volume,
        "Potential Profit ($)": round(potential_profit, 2),
    }


def convert_usd_to_zar(amount, api_key):
    """
    Converts USD to ZAR using the ExchangeRate-API.
    """
    api_url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/USD"
    response = requests.get(api_url)
    
    print(response)
    if response.status_code == 200:
        data = response.json()
        exchange_rate = data["conversion_rates"]["ZAR"]
        converted_amount = amount * exchange_rate
        return converted_amount
    else:
        print("Failed to retrieve exchange rate.")
        return None


def convert_zar_to_usd(amount, api_key):
    """
    Converts USD to ZAR using the ExchangeRate-API.
    """
    api_url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/ZAR"
    response = requests.get(api_url)
    
    print(response)
    if response.status_code == 200:
        data = response.json()
        exchange_rate = data["conversion_rates"]["USD"]
        converted_amount = amount * exchange_rate
        return converted_amount
    else:
        print("Failed to retrieve exchange rate.")
        return None


def allocate_order_book_depth(desired_dollar_value, order_book):
    """
    Allocates a trade across order book levels based on available liquidity.

    Returns:
        list of dict: Each dict details the 'price', 'btc_volume', and 'dollar_value' to trade at that level.
    """
    orders = []
    remaining_value = desired_dollar_value
    for price, available_btc in order_book:
        available_dollar = price * available_btc
        if available_dollar <= remaining_value:
            # Use up the full depth at this level.
            orders.append({
                'price': price,
                'btc_volume': available_btc,
                'dollar_value': available_dollar
            })
            remaining_value -= available_dollar
        else:
            # Only part of this level is needed.
            btc_needed = remaining_value / price
            orders.append({
                'price': price,
                'btc_volume': btc_needed,
                'dollar_value': remaining_value
            })
            remaining_value = 0
            break

    if remaining_value > 0:
        print(f"Warning: Order book depth insufficient. Still need ${remaining_value:.2f}.")
    return orders


'''
Bot sells r100K of BTC (Valr)
    Convert R100k to USDT

-- Never transact
-- Group order book instead of ticker
-- Determine the spread (profit)


Bot buys R100K(in UDST) of BTC (Binance)
Instantly Bot sells BTC back into USDT 
'''

