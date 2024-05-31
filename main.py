import requests
from bs4 import BeautifulSoup
from name import get_balance, get_tickers, set_mode, place_order_market

headers = {'User-Agent': 'Opera/9.80 (Windows NT 6.2; WOW64) Presto/2.12.388 Version/12.17'}
url_count = 706

# Инструменты для торговли
tp = 0.005
sl = 0.005
qty = 300

# Отсчет времени и количества запросов
import time
start_time = time.time()
i = 0

run = True
while run:
    elapsed_time = time.time() - start_time
    url = 'https://t.me/pump_dump_screener_demo/' + str(url_count)

    # Получаем данные из http запроса
    try:
        response = requests.get(url, headers)
    except:
        print('ошибка. повторение запроса')
        response = requests.get(url, headers)
    soup = BeautifulSoup(response.text, 'lxml')
    data = soup.find_all('meta')

    # Исходя из данных принимаем решение на сторону ставки
    for content in data:
        if str(content).count('🔴') == 1 or str(content).count('🟢') == 1:
            elements = str(content).split()
            ticker = str(elements[1][11:-1] + 'USDT')
            # set_mode(ticker)
            url_count += 1
            if str(content).count('🔴') == 1:
                print('long')
                tickers = get_tickers()
                balance_usdt = get_balance()
                if ticker in tickers:
                    if balance_usdt != 0:
                        place_order_market(ticker, 1, ((int(float(get_balance()))-5)*10), tp, sl)
            else:
                print('short')
                tickers = get_tickers()
                balance_usdt = get_balance()
                if ticker in tickers:
                    if balance_usdt != 0:
                        place_order_market(ticker, 0, ((int(float(get_balance()))-5)*10), tp, sl)
            break
    
    i += 1
    print(i, int(elapsed_time))
