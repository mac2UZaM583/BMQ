from keys import api_key, api_secret
from pybit.unified_trading import HTTP
import asyncio
from datetime import datetime

session = HTTP(
    demo=True,
    api_key=api_key,
    api_secret=api_secret
)

# Получаем баланс единого торгового аккаунта
async def get_balance():
    try:
        response = await asyncio.to_thread(session.get_wallet_balance, accountType='UNIFIED', coin='USDT')
        balance = response['result']['list'][0]['coin'][0]['walletBalance']
        return balance
    except Exception as er:
        print(er, 'гет баланс')

# Получаем все тикеры
async def get_tickers():
    try:
        data = await asyncio.to_thread(session.get_tickers, category='linear')
        minOrderQty = data['result']['list']
        tickers = [ticker['symbol'] for ticker in minOrderQty if 'USDT' in ticker['symbol'] and not 'USDC' in ticker['symbol']]
        return tickers
    except Exception as er:
        print(er, 'get tickers')
        return []

# Получаем информацию о текущей цене
async def get_last_price(symbol):
    try:
        response = await asyncio.to_thread(session.get_tickers, category='linear', symbol=symbol)
        mark_price = float(response['result']['list'][0]['lastPrice'])
        return mark_price
    except Exception as er:
        print(er)

# Получаем информацию о лотсайзфильтре ордера
async def get_roundQty(symbol):
    try:
        mark_price = await get_last_price(symbol)
        data_minroundQty = await asyncio.to_thread(session.get_instruments_info, category='linear', symbol=symbol)
        data_minroundQty_2 = data_minroundQty['result']['list'][0]['lotSizeFilter']['minOrderQty']
        roundQty_forTPSL = len(str(mark_price).split('.')[-1]) if '.' in str(data_minroundQty) else 0
        roundQty_forOrder = len(str(data_minroundQty_2).split('.')[-1]) if '.' in str(data_minroundQty_2) else 0
        return roundQty_forTPSL, roundQty_forOrder
    except Exception as er:
        print(er, 'get_precisions')
        return None   

# Публикуем ордер
async def place_order(symbol, side, balance, tp, sl):
    try:
        mark_price = await get_last_price(symbol)
        roundQty =  await get_roundQty(symbol)
        qty = round(balance / mark_price, roundQty[1])
        tp_priceL = round((1 + tp) * mark_price, roundQty[0])
        sl_priceL = round((1 - sl) * mark_price, roundQty[0])
        print(f'Placing {side} order for ' + symbol, 'tp price', tp_priceL, 'sl price', sl_priceL, 'qty', qty, 'roundQty', roundQty, datetime.now())

        resp = await asyncio.to_thread(session.place_order,
            category='linear',
            symbol=symbol,
            qty=qty,
            marketUnit='baseCoin',
            side='Sell' if side == 0 else 'Buy',
            orderType='Market',
            takeProfit=sl_priceL if side == 0 else tp_priceL,
            stopLoss=tp_priceL if side == 0 else sl_priceL,
            isLeverage=10,
            tpTriggerBy='LastPrice',
            slTriggerBy='LastPrice'
        )
        print(resp)
    except Exception as er:
        print(er, 'place order')
