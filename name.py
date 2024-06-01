from keys import api_key, api_secret
from pybit.unified_trading import HTTP

session = HTTP(
    # testnet=True,
    demo=True,
    api_key=api_key,
    api_secret=api_secret
)

# Получаем баланс единого торгового аккаунта
def get_balance():
    try:
        minOrderQty = session.get_wallet_balance(accountType='UNIFIED', coin='USDT')['result']['list'][0]['coin'][0]['walletBalance']
        return minOrderQty
    except Exception as er:
        print(er)

# print('USDT Balance: ' + get_balance())

# Получаем все тикеры
def get_tickers():
    try:
        minOrderQty = session.get_tickers(category='linear')['result']['list']
        tickers = []
        for ticker in minOrderQty:
            if 'USDT' in ticker['symbol'] and not 'USDC' in ticker['symbol']:
                tickers.append(ticker['symbol'])
        return tickers
    except Exception as er:
        print(er)

# print(get_tickers())

# Сетируем режим для фьючерсной торговли
def set_mode(symbol):
    try:
        print(session.switch_margin_mode(
            category="inverse",
            symbol=symbol,
            tradeMode=1,
            buyLeverage=10,
            sellLeverage=10
        ), 'cok')
    except Exception as er:
        print(er)
# set_mode('BTCUSDT')

# Получаем информацию для возможности открытия\закрытия сделки
def get_precisions(symbol):
    try:
        minOrderQty = session.get_instruments_info(
        category='inverse',
        symbol=symbol,
        )['result']['list'][0]['lotSizeFilter']['minOrderQty']
        roundQty = len(minOrderQty) - 2
        return minOrderQty, roundQty
    except Exception as er:
        print(er)

# print(get_precisions('ARKMUSDT'))

# Создание инструментов для создания ордера и создание ордера
def place_order_market(symbol, side, qty, tp, sl):
    mark_price = session.get_tickers(
        category='linear',
        symbol=symbol
    )['result']['list'][0]['markPrice']
    mark_price = float(mark_price)
    print(f'Placing {side} order for ' + symbol)
    order_qty = round(qty/mark_price, get_precisions(symbol)[1])

    if side == 0:
        try:
            if get_precisions(symbol)[1] <= 0:
                tp_price = (mark_price - (mark_price * tp))
                sl_price = (mark_price + (mark_price * sl))
            else:       
                tp_price = round(mark_price - (mark_price * tp), get_precisions(symbol)[1])
                sl_price = round(mark_price + (mark_price * sl), get_precisions(symbol)[1])
            print(tp_price, sl_price, get_precisions(symbol)[0], get_precisions(symbol)[1])
            
            # Создание ордера
            resp = session.place_order(
                category='linear',
                symbol=symbol,
                side='Sell',
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
            print(er)

    if side == 1:
        try:
            if get_precisions(symbol)[1] <= 0:
                tp_price = (mark_price + (mark_price * tp))
                sl_price = (mark_price - (mark_price * sl))
            else:       
                tp_price = round(mark_price + (mark_price * tp), get_precisions(symbol)[1])
                sl_price = round(mark_price - (mark_price * sl), get_precisions(symbol)[1])
            print(tp_price, sl_price, get_precisions(symbol)[0], get_precisions(symbol)[1])
            

            # Создание ордера
            resp = session.place_order(
                category='linear',
                symbol=symbol,
                side='Buy',
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
            print(er)