from smq import smq_get_data, smq
from get import get_round_qty, get_get_data
from set import *
from keys import session
from asyncio import to_thread, gather, run
from settings__ import files_content
from itertools import count
from datetime import datetime
from pprint import pprint

data_update = 60
tp = None
sl = float(files_content['STOPLOSS'])
counter = count(start=0, step=1)

async def in_cycle_funcs(result):
    positions = result[0]['result']['list']
    if positions:
        position = positions[-1]
        symbol = position['symbol']
        avg_price = float(position['avgPrice'])
        round_qty = get_round_qty(symbol)
        tasks_2 = [
            to_thread(TP, position, symbol, round_qty, avg_price, tp),
            to_thread(SL, position, symbol, round_qty, avg_price, sl)
        ]
        await gather(*tasks_2)

async def cycle(data_update):
    data_old = smq_get_data()
    start_time = time.time()
    while True:
        if time.time() - start_time >= data_update:
            print('data collected')
            data_old = smq_get_data()
            start_time = time.time()
        print(next(counter), datetime.now())
        tasks_1 = [
        to_thread(session.get_positions, category='linear', settleCoin='USDT'),
        to_thread(smq, data_old)
        ]
        result = await gather(*tasks_1)
        signal = result[1]
        await in_cycle_funcs(result)

        if signal:
            return signal

# @time_measurements
def post_cycle(signal):
    data = run(get_get_data(signal[0]))
    if not data[-1]['result']['list']:
        qty = round(
            ((data[0] * 10) / float(files_content['BALANCE_DIVIDER'])) / data[1], 
            data[2][0]
        )
        global tp
        tp = 1 - ((signal[1] - 1) / 2.5)
        place_order(signal[0], qty)

def main():
    while True:
        try:
            '''CYCLE ⭣
            '''
            signal = run(cycle(data_update))
            print(signal)
            
            '''MAIN ⭣
            '''
            post_cycle(signal)
        except:
            traceback.print_exc()
            cancel_position()

if __name__ == '__main__':
    s_leverage_and_margin_mode()
    main() #⭠⭡⭢⭣⭤ ⭥⮂⮃