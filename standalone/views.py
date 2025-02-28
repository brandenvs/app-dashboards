from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime

from .services.books import (
    get_binance_btc_usdt,
    get_valr_btc_zar,
    get_exchangerateapi_usd_zar,
    fetch_binance_order_book,
    fetch_valr_order_book
)
from .services.calculators import (
    convert_usd_to_zar, 
    convert_zar_to_usd,
    determine_optimal_trade
)
from .services.volumes import get_binance_btc_volume, get_valr_btc_volume

from decouple import config

API_KEY = config('API_KEY')

def get_exchange_data():
    """Fetches exchange data and computes key metrics for arbitrage opportunities."""
    try:
        # Fetch prices
        binance_btc_usdt = get_binance_btc_usdt()
        valr_btc_zar = get_valr_btc_zar()
        usd_zar = get_exchangerateapi_usd_zar(API_KEY)

        # Convert prices
        binance_btc_zar = binance_btc_usdt * usd_zar
        valr_btc_usd = valr_btc_zar / usd_zar

        # Fetch order books
        valr_bids, valr_asks = fetch_valr_order_book('BTCZAR')
        binance_bids, binance_asks = fetch_binance_order_book('BTCUSDT')

        # Ensure order books exist
        valr_bids = valr_bids[:10] if valr_bids else []
        valr_asks = valr_asks[:10] if valr_asks else []
        binance_bids = binance_bids[:10] if binance_bids else []
        binance_asks = binance_asks[:10] if binance_asks else []

        # Convert Binance order book prices to ZAR
        binance_bids_zar = [(float(bid[0]) * usd_zar, float(bid[1])) for bid in binance_bids]
        binance_asks_zar = [(float(ask[0]) * usd_zar, float(ask[1])) for ask in binance_asks]

        # Get market volumes
        valr_btc_vol = get_valr_btc_volume()
        binance_btc_vol = get_binance_btc_volume()

        # Live Gross Premium Calculation
        binance_best_bid = float(binance_bids[0][0]) if binance_bids else 0
        valr_best_ask = float(valr_asks[0][0]) / usd_zar if valr_asks else 0

        binance_to_valr_lgp = (
            ((valr_best_ask - binance_best_bid) / binance_best_bid) * 100
            if binance_best_bid > 0 else 0
        )

        valr_best_bid = float(valr_bids[0][0]) / usd_zar if valr_bids else 0
        binance_best_ask = float(binance_asks[0][0]) if binance_asks else 0

        valr_to_binance_lgp = (
            ((binance_best_ask - valr_best_bid) / valr_best_bid) * 100
            if valr_best_bid > 0 else 0
        )

        # Determine optimal trade
        lgp_result = determine_optimal_trade(
            binance_btc_usdt, valr_btc_usd, binance_btc_vol, valr_btc_vol
        )

        return {
            'binance_btc_usdt': binance_btc_usdt,
            'valr_btc_zar': valr_btc_zar,
            'usd_zar': usd_zar,
            'binance_btc_zar': binance_btc_zar,
            'valr_btc_usd': valr_btc_usd,
            'valr_bids': valr_bids,
            'valr_asks': valr_asks,
            'binance_bids': binance_bids,
            'binance_asks': binance_asks,
            'binance_bids_zar': binance_bids_zar,
            'binance_asks_zar': binance_asks_zar,
            'binance_to_valr_lgp': round(binance_to_valr_lgp, 2),
            'valr_to_binance_lgp': round(valr_to_binance_lgp, 2),
            'lgp_result': lgp_result,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

    except Exception as e:
        return {'error': str(e)}

def bt_bot(request):
    """Renders arbitrage trading dashboard."""
    exchange_data = get_exchange_data()
    return render(request, 'partials/bt_bot.html', {'exchange_data': exchange_data})

def exchange_data_api(request):
    """API endpoint for real-time exchange data."""
    exchange_data = get_exchange_data()
    return JsonResponse(exchange_data)
