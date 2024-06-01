import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
from name import get_balance, get_tickers, place_order
import asyncio

headers = {'User-Agent': 'Opera/9.80 (Windows NT 6.2; WOW64) Presto/2.12.388 Version/12.17'}
url_count = 718

# Инструменты для торговли
tp = 0.005
sl = 0.005

# Отсчет времени и количества запросов
start_time = time.time()
i = 0

async def main():
    global url_count, i
    while True:
        try:

            while True:
                try:
                    elapsed_time = time.time() - start_time
                    url = 'https://t.me/pump_dump_screener_demo/' + str(url_count)

                    # Получаем данные из http запроса
                    try:
                        response = requests.get(url, headers)
                    except:
                        print('ошибка. повторение запроса/время: ', datetime.now())
                        response = requests.get(url, headers)
                    soup = BeautifulSoup(response.text, 'lxml')
                    data = soup.find_all('meta')

                    # Исходя из данных принимаем решение на сторону ставки
                    for content in data:
                        if '🔴' in str(content) or '🟢' in str(content):
                            elements = str(content).split()
                            ticker = str(elements[1][11:-1] + 'USDT')
                            url_count += 1
                            tickers = await get_tickers()
                            balance_usdt = await get_balance()
                            print(balance_usdt)

                            if str(content).count('🔴') == 1:
                                if ticker in tickers and balance_usdt != 0:
                                    await place_order(ticker, 1, int((float(balance_usdt) - 5) * 10), tp, sl)
                                    print(datetime.now())

                            if str(content).count('🟢') == 1:
                                if ticker in tickers and balance_usdt != 0:
                                    await place_order(ticker, 0, int((float(balance_usdt) - 5) * 10), tp, sl)
                                    print(datetime.now())

                            break
                    i += 1
                    print(i, int(elapsed_time))
                except Exception as er:
                    print(er, datetime.now())
        
        except Exception as er:
            print(er)

if __name__ == "__main__":
    asyncio.run(main())
