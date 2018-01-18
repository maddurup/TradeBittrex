import cmd, json
from bittrex.bittrex import Bittrex, API_V2_0
from bittrex.bittrex import *
from beautifultable import BeautifulTable
import pprint, time
import json
from pandas.io.json import json_normalize
import pandas as pd
pd.set_option('display.width', 1000)
import operator
pp = pprint.PrettyPrinter(indent=4)
from pandasql import sqldf

self.my_bittrex = Bittrex("Key", "Secert")


def get_balance(my_bittrex):
    pysqldf = lambda q: sqldf(q, globals())
    res = my_bittrex.get_balances()
    res = res['result']
    btc_value = 0

    if res:

    #     table.numeric_precision = 10
        column_headers = ["Index","CurrencyLong","Currency","Available","Balance","Pending","TxFee","Last","btc_value"]
    #     table = pd.DataFrame(columns = column_headers)
        table = list()
        index = 1
        for order in res:
            # print(order)
            try:
                if order['BitcoinMarket'] is not None:
                    if int(order['Balance']['Balance']) != 0:
                        # print("here")
                        table.append([
                            index,
                            order['Currency']['CurrencyLong'],
                            order['Currency']['Currency'],
                            order['Balance']['Available'],
                            order['Balance']['Balance'],
                            order['Balance']['Pending'],
                            order['Currency']['TxFee'],
                            float(order['BitcoinMarket']['Last']),
                            float(order['BitcoinMarket']['Last']) * float(order['Balance']['Balance'])
                        ])
                        index += 1
            except Exception as e:
                print(str(e))

    res = pd.DataFrame(table,columns = column_headers)
    res['Currency'] = res['Currency'].apply(lambda x: 'BTC-'+str(x))
    balance = res
    return balance

pysqldf = lambda q: sqldf(q, globals())
order_res = my_bittrex.get_order_history()
order_res = order_res['result']
order_res = pd.DataFrame(order_res)
order_res = pysqldf("select Closed, Exchange, PricePerUnit, Price as btc_value_actual, Quantity - QuantityRemaining as total_quantity \
                        FROM order_res where OrderType = 'LIMIT_BUY' ")
order_history = order_res


balance = get_balance(my_bittrex)

print(pysqldf("select CurrencyLong, Currency, Available, Balance,\
            PricePerUnit,btc_value_actual, Last, btc_value, coalesce(round((Last - PricePerUnit)*100/PricePerUnit,2) || '%','check') as Percent_pl  \
            FROM balance b \
                left join order_history o \
                    on b.Currency = o.Exchange \
                    and b.Balance = o.total_quantity \
        "))