from keys import session
import time
import traceback
from settings__ import files_content
from pprint import pprint

'''CYCLE ⭣
'''
def cancel_position():
    try:
        order = session.get_order_history(category='linear')['result']['list'][0]
        side = 'Buy' if order['side'] == 'Sell' else 'Sell'
        session.place_order(
            category='linear',
            symbol=order['symbol'],
            side=side,
            orderType='Market',
            qty=0,
            reduceOnly=True
        )
    except:
        traceback.print_exc()

def TP(position, symbol, round_qty, avg_price, tp):
    if tp:
        tp_price_position = position['takeProfit'].rstrip('0')
        tp_price_position_rounded = tp_price_position[:int(round_qty[2])]
        tp_price = str(round(avg_price * tp, int(round_qty[1]))).rstrip('0')
        tp_price_rounded = tp_price[:round_qty[2]]
        if (
            tp_price_position != tp_price and 
            tp_price_position_rounded != tp_price_rounded
        ):
            session.set_trading_stop(
                category='linear', 
                symbol=symbol, 
                tpslMode='Full', 
                takeProfit=tp_price, 
                positionIdx=0
            )

def SL(position, symbol, round_qty, avg_price, sl):
    sl_price_position = position['stopLoss'].rstrip('0')
    sl_price_position_rounded = sl_price_position[:round_qty[2]]
    sl_price = str(round(avg_price * sl, int(round_qty[1]))).rstrip('0')
    sl_price_rounded = sl_price[:round_qty[2]]
    if (
        sl_price_position != sl_price and 
        sl_price_position_rounded != sl_price_rounded
    ):
        print(f'sl_position: {sl_price_position_rounded} sl: {sl_price_rounded}')
        session.set_trading_stop(
            category='linear', 
            symbol=symbol, 
            tpslMode='Full', 
            stopLoss=sl_price, 
            positionIdx=0
        )

'''MAIN ⭣
'''
def place_order(symbol, qty):
    pprint(session.place_order(
        category='linear',
        symbol=symbol,
        qty=qty, 
        marketUnit='baseCoin',
        side='Sell',
        orderType='Market',
        isLeverage=10,
        tpTriggerBy='LastPrice', 
        slTriggerBy='LastPrice'
    ))

def s_leverage_and_margin_mode():
    for value in session.get_tickers(
        category='linear'
    )['result']['list']:
        if files_content['MODE'].upper() == 'DEMO':
            try:
                symbol = value['symbol']
                print(symbol)
                session.set_leverage(
                    category='linear', 
                    symbol=symbol,
                    buyLeverage='10',
                    sellLeverage='10'
                )
            except:
                pass
        else:
            try:
                symbol = value['symbol']
                print(symbol)
                session.switch_margin_mode(
                    category='linear', 
                    symbol=symbol, 
                    tradeMode=1,
                    buyLeverage='10',
                    sellLeverage='10'
                )
            except:
                pass

def time_measurements(func):
    def wrapper(*args):
        start = time.perf_counter() 
        result = func(*args)
        print(time.perf_counter() - start)
        return result
    return wrapper

if __name__ == '__main__':
    s_leverage_and_margin_mode()