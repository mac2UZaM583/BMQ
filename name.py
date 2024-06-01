from keys import api_key, api_secret
from pybit.unified_trading import HTTP
import asyncio
from datetime import datetime

session = HTTP(
    demo=True,
    api_key=api_key,
    api_secret=api_secret
)

async def get_balance():
    try:
        response = await asyncio.to_thread(session.get_wallet_balance, accountType='UNIFIED', coin='USDT')
        minOrderQty = response['result']['list'][0]['coin'][0]['walletBalance']
        return minOrderQty
    except Exception as er:
        print(er, 'гет баланс')

async def get_tickers():
    try:
        data = await asyncio.to_thread(session.get_tickers, category='linear')
        minOrderQty = data['result']['list']
        tickers = [ticker['symbol'] for ticker in minOrderQty if 'USDT' in ticker['symbol'] and not 'USDC' in ticker['symbol']]
        return tickers
    except Exception as er:
        print(er, 'get tickers')
        return []

async def get_precisions(symbol):
    try:
        response = await asyncio.to_thread(session.get_instruments_info, category='inverse', symbol=symbol)
        minOrderQty = response['result']['list'][0]['lotSizeFilter']['minOrderQty']
        roundQty = len(minOrderQty.split('.')[-1])
        return minOrderQty, roundQty
    except Exception as er:
        print(er, 'get_precisions')
        return None, None

async def get_mark_price(symbol):
    try:
        response = await asyncio.to_thread(session.get_tickers, category='linear', symbol=symbol)
        mark_price = float(response['result']['list'][0]['markPrice'])
        return mark_price
    except Exception as er:
        print(er)

async def place_order(symbol, side, qty, tp, sl):
    try:
        precisions = await get_precisions(symbol)
        mark_price = await get_mark_price(symbol)
        mark_price = float(mark_price)
        order_qty = round(qty / mark_price, precisions[1])
        print(f'Placing {side} order for ' + symbol, datetime.now())
        tp_price, sl_price = None, None

        if side == 0:
            tp_price = mark_price - (mark_price * tp)
            sl_price = mark_price + (mark_price * sl)
        else:
            tp_price = mark_price + (mark_price * tp)
            sl_price = mark_price - (mark_price * sl)

        resp = await asyncio.to_thread(session.place_order,
            category='linear',
            symbol=symbol,
            side='Sell' if side == 0 else 'Buy',
            orderType='market',
            qty=order_qty,
            takeProfit=tp_price,
            stopLoss=sl_price,
            tpTriggerBy='LastPrice',
            slTriggerBy='LastPrice',
            marketUnit='quoteCoin'
        )
        print(resp)
    except Exception as er:
        print(er, 'place order')
