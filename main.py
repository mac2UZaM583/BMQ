from smq import smq
from name import get_balance, place_order, get_last_price, get_roundQty
from pprint import pprint
from decimal import Decimal

tp = 0.004
sl = 0.006

def main():
    global headers, tp, sl
    while True:
        try:
            while True:
                try:
                    print(f'\n\nstart/time - плдюююююю\n\n')                    
                    signal = smq()
                    print(signal)
                            
                    balance_usdt = get_balance()
                    balanceWL = Decimal(balance_usdt)
                    mark_price = Decimal(get_last_price(signal[0]))
                    roundQty =  get_roundQty(signal[0])
                    if signal[1] < 0:
                        place_order(signal[0], 'Buy', mark_price, roundQty, balanceWL, tp, sl)
                    if signal[1] > 0:
                        place_order(signal[0], 'Sell', mark_price, roundQty, balanceWL, tp, sl)
                    break
                except Exception as er:
                    pprint(er)
        except Exception as er:
            pprint(er)

if __name__ == '__main__':
    main()
