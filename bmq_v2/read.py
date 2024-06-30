import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bmq_v2.keys import session
import numpy as np
from decimal import Decimal as D
from datetime import datetime
import time
from pprint import pprint


'''POSITION ↓
'''     
def get_balance():
    return D(session.get_wallet_balance(accountType='UNIFIED', coin='USDT')['result']['list'][0]['coin'][0]['walletBalance'])
    
def get_last_price(symbol):
    return D(session.get_tickers(category='linear', symbol=symbol)['result']['list'][0]['lastPrice'])

def get_roundQty(symbol):
    data_minroundQty = session.get_instruments_info(category='linear', symbol=symbol)['result']['list'][0]['lotSizeFilter']['minOrderQty']
    data_minroundPrice = session.get_instruments_info(category='linear', symbol=symbol)['result']['list'][0]['priceFilter']['minPrice'].rstrip('0')
    tick_minround_price = session.get_instruments_info(category='linear', symbol=symbol)['result']['list'][0]['priceFilter']['tickSize'].rstrip('0')
    roundForQty = (len(data_minroundQty) - 2) if D(data_minroundQty) < 1 else 0
    roundForTPSL = (len(data_minroundPrice) - 2) if D(data_minroundPrice) < 1 else 0
    round_for_tpsl2 = (len(tick_minround_price) - 1) if D(tick_minround_price) < 1 else len(tick_minround_price)
    return roundForTPSL, roundForQty, round_for_tpsl2

if __name__ == '__main__':
    time_now = time.time()
    time.sleep(60)