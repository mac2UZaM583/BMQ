from pybit.unified_trading import HTTP
import numpy as np
from settings__ import files_content
from time import sleep
from pprint import pprint

THRESHOLD_PERCENT = float(files_content['THRESHOLD_PERCENT'])
LIMIT_PERCENT = float(files_content['LIMIT_PERCENT'])
print(THRESHOLD_PERCENT)
session = HTTP()

'''GET ⭣
'''
def unpacking_data(data):
    return (
        np.array(tuple(
            info['symbol'] 
            for info in data 
            if 'USDT' in info['symbol'] and 'USDC' not in info['symbol']
        )),
        np.array(tuple(
            float(info['lastPrice']) 
            for info in data 
            if 'USDT' in info['symbol'] and 'USDC' not in info['symbol']
        ))
    )

def smq_get_data():
    return unpacking_data(
        np.array(session.get_tickers(category='linear')['result']['list'])
    )

def g_percent_change(symbols_old, prices_old, symbols_new, prices_new):
    where = prices_new / prices_old
    indeces = np.where((where >= THRESHOLD_PERCENT) & (where <= LIMIT_PERCENT))
    if np.size(indeces) > 0:
        symbol = symbols_new[indeces]
        if np.all(symbols_old[indeces] == symbol):
            return (
                next(iter(symbol)),
                next(iter(prices_new[indeces] / prices_old[indeces]))
            )
    
'''SET ⭣
'''
def smq(data_old):    
    return g_percent_change(*data_old, *smq_get_data())