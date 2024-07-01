import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from smq import smq, fetch_data
from bmq_v2.keys import session
from bmq_v2.read import (
    get_balance as gb, 
    get_roundQty as gr, 
    get_last_price as gl,
)
from bmq_v2.write import (
    switch_margin_mode as smm, 
    place_order as po, 
    TP,
    SL,
    cancel_position
)
from decimal import Decimal as D
import time
import traceback

print(f'\n\nSTART-V1-V2\n\n')
data_update = 60
tp = D(0.030)
sl = D(0.050)

'''PRE ↓
'''
def pre_main1():
    data_old = fetch_data()
    prices_old = {price['symbol']: D(price['lastPrice']) for price in data_old}
    start_time = time.time()
    while True:
        positions = session.get_positions(category='linear', settleCoin='USDT')['result']['list']
        if positions:
            TP(position=positions[-1], tp=tp)
            SL(position=positions[-1], sl=sl)

        if time.time() - start_time >= data_update:
            data_old = fetch_data()
            prices_old = {price['symbol']: D(price['lastPrice']) for price in data_old}
            start_time = time.time()
        signal = smq(prices_old=prices_old)
        if signal != None:
            print(signal)
            return signal, positions

'''POST ↓
'''
def pre_main2(signal, positions):
    balanceWL = gb() * 9.99
    roundQty =  gr(signal[0])
    if not positions:
        smm(symbol=signal[0])
        mark_price = gl(signal[0])
        qty = round(balanceWL / mark_price, roundQty[1])
        po(symbol=signal[0], side=signal[0], qty=qty)

def main():
    while True:
        try:
            '''PRE ↓
            '''
            signal, positions = pre_main1()
            
            '''POST ↓
            '''
            pre_main2(signal=signal, positions=positions)
        except:
            cancel_position()
            er = traceback.format_exc()
            # with open('/CODE_PROJECTS/SMQ-N & Python/signal.txt', 'w', encoding='utf-8') as f:
            #     f.write(f'{er}\n\ntime: {time.time()}')

if __name__ == '__main__':
    main()