from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse

from hyperion.models import StudentProgress

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
    determine_optimal_trade,
    allocate_order_book_depth
)
from .services.volumes import get_binance_btc_volume, get_valr_btc_volume

from decouple import config
from pathlib import Path
import os
import json
from datetime import datetime

app_label = 'standalone'

BASE_DIR = Path(__file__).resolve().parent.parent

'''Load environment variables'''
ENV_PATH = os.path.join(BASE_DIR, '.env')
config._find_file(ENV_PATH)

API_KEY = config('API_KEY')

def index(request):
    return render(request, 'partials/standalone_home.html')


def progression_tracker(request):
    db_students = StudentProgress.objects.all()
    view_dict = {}
    chart_data = {
        'students': [],
        'level1': [],
        'level2': [],
        'level3': []
    }

    for student in db_students:
        if student.fullname not in chart_data['students']:
            chart_data['students'].append(student.fullname)
            _records = {}

        if student.level == 'Level 1':              
            progress_lvl1 = int(student.completed)  
            resubmission_lvl1 = int(student.resubmitted)
            incomplete_lvl1 = int(student.incomplete)
            below100_lvl1 = int(student.below_100)

            _records['lvl1_progress'] = progress_lvl1
            _records['lvl1_resubmission'] = resubmission_lvl1
            _records['lvl1_incomplete'] = incomplete_lvl1
            _records['lvl1_below100'] = below100_lvl1
            chart_data['level1'].append(progress_lvl1)

        elif student.level == 'Level 2':
            progress_lvl2 = int(student.completed)  
            resubmission_lvl2 = int(student.resubmitted)
            incomplete_lvl2 = int(student.incomplete)
            below100_lvl2 = int(student.below_100)

            _records['lvl2_progress'] = progress_lvl2
            _records['lvl2_resubmission'] = resubmission_lvl2
            _records['lvl2_incomplete'] = incomplete_lvl2
            _records['lvl2_below100'] = below100_lvl2
            chart_data['level2'].append(progress_lvl2)

        elif student.level == 'Level 3':
            progress_lvl3 = int(student.completed)  
            resubmission_lvl3 = int(student.resubmitted)
            incomplete_lvl3 = int(student.incomplete)
            below100_lvl3 = int(student.below_100)

            _records['lvl3_progress'] = progress_lvl3
            _records['lvl3_resubmission'] = resubmission_lvl3
            _records['lvl3_incomplete'] = incomplete_lvl3
            _records['lvl3_below100'] = below100_lvl3
            chart_data['level3'].append(progress_lvl3)

        view_dict[student.fullname] = _records

    return render(request, 'partials/student_progression.html', {
        'chart_data': chart_data,
        'records': view_dict
    })


def get_exchange_data():
    """Get fresh exchange data for each request"""
    binance_btc_usdt = get_binance_btc_usdt()  # Binance
    valr_btc_zar = get_valr_btc_zar()  # VALR
    usd_zar = get_exchangerateapi_usd_zar(API_KEY)  # Exchange rate

    binance_btc_zar = convert_usd_to_zar(binance_btc_usdt, API_KEY)
    valr_btc_usd = convert_zar_to_usd(valr_btc_zar, API_KEY)

    valr_btc_vol = get_valr_btc_volume()
    binance_btc_vol = get_binance_btc_volume()

    valr_bids, valr_asks = fetch_valr_order_book('BTCZAR')
    binance_bids, binance_asks = fetch_binance_order_book('BTCUSDT')
    
    # Convert binance bids/asks to ZAR
    binance_bids_zar = [(float(bid[0]) * usd_zar, float(bid[1])) for bid in binance_bids[:10]]
    binance_asks_zar = [(float(ask[0]) * usd_zar, float(ask[1])) for ask in binance_asks[:10]]
    
    # Calculate LGP (Live Gross Premium)
    binance_best_bid = float(binance_bids[0][0]) if binance_bids else 0
    valr_best_ask = float(valr_asks[0][0]) / usd_zar if valr_asks else 0
    binance_to_valr_lgp = ((valr_best_ask - binance_best_bid) / binance_best_bid) * 100 if binance_best_bid > 0 else 0
    
    valr_best_bid = float(valr_bids[0][0]) / usd_zar if valr_bids else 0
    binance_best_ask = float(binance_asks[0][0]) if binance_asks else 0
    valr_to_binance_lgp = ((binance_best_ask - valr_best_bid) / valr_best_bid) * 100 if valr_best_bid > 0 else 0
    
    lgp_result = determine_optimal_trade(
        binance_btc_usdt, 
        valr_btc_usd, 
        binance_btc_vol, 
        valr_btc_vol
    )
    
    return {
        'binance_btc_usdt': binance_btc_usdt,
        'valr_btc_zar': valr_btc_zar,
        'usd_zar': usd_zar,
        'binance_btc_zar': binance_btc_zar,
        'valr_btc_usd': valr_btc_usd,
        'valr_bids': valr_bids[:10],
        'valr_asks': valr_asks[:10],
        'binance_bids': binance_bids[:10],
        'binance_asks': binance_asks[:10],
        'binance_bids_zar': binance_bids_zar,
        'binance_asks_zar': binance_asks_zar,
        'binance_to_valr_lgp': round(binance_to_valr_lgp, 2),
        'valr_to_binance_lgp': round(valr_to_binance_lgp, 2),
        'lgp_result': lgp_result,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }


def bt_bot(request):
    exchange_data = get_exchange_data()
    return render(request, 'partials/bt_bot.html', {
        'exchange_data': exchange_data
    })


def exchange_data_api(request):
    """API endpoint to refresh exchange data"""
    exchange_data = get_exchange_data()
    return JsonResponse(exchange_data)