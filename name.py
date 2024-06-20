from keys import api_key, api_secret
from pybit.unified_trading import HTTP
from decimal import Decimal
from datetime import datetime
from pprint import pprint

session = HTTP(
    demo=True,
    api_key=api_key,
    api_secret=api_secret
)

# Получение баланса
def get_balance():
    response = session.get_wallet_balance(accountType='UNIFIED', coin='USDT')
    balance = response['result']['list'][0]['coin'][0]['walletBalance']
    return balance
    
# Получение информации о текущей последней цене
def get_last_price(symbol):
    response = session.get_tickers(category='linear', symbol=symbol)
    mark_price = float(response['result']['list'][0]['lastPrice'])
    return mark_price

# Получение информации о лотсайзфильтре ордера
def get_roundQty(symbol):
    mark_price = get_last_price(symbol)
    data_minroundQty = session.get_instruments_info(category='linear', symbol=symbol)
    data_minroundQty_2 = data_minroundQty['result']['list'][0]['lotSizeFilter']['minOrderQty']
    roundQty_forTPSL = len(str(mark_price).split('.')[-1]) if '.' in str(data_minroundQty) else 0
    roundQty_forOrder = len(str(data_minroundQty_2).split('.')[-1]) if '.' in str(data_minroundQty_2) else 0
    return roundQty_forTPSL, roundQty_forOrder

# Публикация ордера
def place_order(symbol, side, mark_price, roundQty, balanceWL, tp, sl):
    try:
        if len(session.get_open_orders(category='linear', settleCoin='USDT')['result']['list']) < 8:
            qty = round(balanceWL / mark_price, roundQty[1])
            if side == 'Sell':
                tp_priceL = round(Decimal(1 - tp) * mark_price, roundQty[0])
                sl_price = round(Decimal(1 + sl) * mark_price, roundQty[0])
            elif side == 'Buy':
                tp_priceL = round(Decimal(1 + tp) * mark_price, roundQty[0])
                sl_price = round(Decimal(1 - sl) * mark_price, roundQty[0])
        
            # Выставление маркет ордера
            resp = session.place_order(
                category='linear',
                symbol=symbol,
                qty=qty,
                marketUnit='baseCoin',
                side=side,
                orderType='Market',
                takeProfit=tp_priceL,
                stopLoss=sl_price,
                isLeverage=12,
                tpTriggerBy='LastPrice',
                slTriggerBy='LastPrice'
            )
            pprint(resp)

            # Более точное выставление тп и сл ордеров
            entryPrice = round(Decimal(session.get_positions(
                category='linear',
                symbol=symbol
            )['result']['list'][0]['avgPrice']), roundQty[0])
            if side == 'Sell':
                tp_priceL = round(Decimal(1 - tp) * Decimal(entryPrice), roundQty[0])
                sl_price = round(Decimal(1 + sl) * Decimal(entryPrice), roundQty[0])
            elif side == 'Buy':
                tp_priceL = round(Decimal(1 + tp) * Decimal(entryPrice), roundQty[0])
                sl_price = round(Decimal(1 - sl) * Decimal(entryPrice), roundQty[0])
            try:
                print(session.set_trading_stop(
                    category='linear',
                    symbol=symbol,
                    tpslMode='Full',
                    takeProfit=tp_priceL,
                    stopLoss=sl_price,
                    positionIdx=0
                ))
            except:
                print('тп не установлен потому что и так все хорошо')
    except Exception as er:
        print(er, 'Place order')
        with open('errors', 'a', encoding='utf-8') as f:
            f.write(f'ошибка в Place Order: \n\n{er}\n {datetime.now()}')


# resp = session.place_order(
#     category='linear',
#     symbol='ETHUSDT',
#     qty=0.03,
#     marketUnit='baseCoin',
#     side='Buy',
#     orderType='Market',
#     takeProfit='5000',
#     stopLoss='2000',
#     isLeverage=23,
#     tpTriggerBy='LastPrice',
#     slTriggerBy='LastPrice'
#     )


