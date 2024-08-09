import time
import numpy as np
import asyncio
from keys import session
from settings__ import files_content
from pprint import pprint

def get_balance():
    return float(
        session.get_wallet_balance(
            accountType=files_content['ACCOUNT_TYPE'].upper(), coin='USDT'
        )['result']['list'][0]['coin'][0]['availableToWithdraw']
    )

def get_last_price(symbol):
    return float(
        session.get_tickers(
            category='linear', symbol=symbol
        )['result']['list'][0]['lastPrice']
    )

def get_round_qty(symbol):
    data = session.get_instruments_info(category='linear', symbol=symbol)['result']['list'][0]
    data_minroundQty = data['lotSizeFilter']['minOrderQty']
    data_minroundPrice = data['priceFilter']['minPrice'].rstrip('0')
    tick_minround_price = data['priceFilter']['tickSize'].rstrip('0')
    roundForQty = (len(data_minroundQty) - 2) if float(data_minroundQty) < 1 else 0
    roundForTPSL = (len(data_minroundPrice) - 2) if float(data_minroundPrice) < 1 else 0
    round_for_tpsl2 = (len(tick_minround_price) - 1) if float(tick_minround_price) < 1 else len(tick_minround_price)
    return np.array((roundForQty, roundForTPSL, round_for_tpsl2))

'''MAIN ⭣
'''
async def get_get_data(symbol):
    tasks = [
        asyncio.to_thread(get_balance),  
        asyncio.to_thread(get_last_price, symbol),
        asyncio.to_thread(get_round_qty, symbol),
        asyncio.to_thread(session.get_positions, category='linear', settleCoin='USDT')
    ]
    return await asyncio.gather(*tasks)
    