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



class BittrexShell(cmd.Cmd):
    intro = 'Welcome to the Bittrex shell. Type help or ? to list commands.\n'
    prompt = '> '
    my_bittrex = Bittrex(None, None)  # or defaulting to v1.1 as Bittrex(None, None)
	# print(my_bittrex.get_markets())
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.my_bittrex = Bittrex("Key", "Secert")


    def do_sl(self, arg):
        'Sell stock sl <symbol> <quantity> <price_to_sell> <executing_price>'
        parts = arg.split()
        if len(parts) >= 3 and len(parts) <= 4:
            symbol = parts[0]
            quantity = parts[1]
            if len(parts) == 3:
                price = float(parts[2])
                executing_price = float(str(parts[2]) + '9')
            else:
                price = float(parts[2])
                executing_price = float(str(parts[3]))

            res = self.my_bittrex.trade_sell(symbol, 'LIMIT', quantity , price, 
            	'GOOD_TIL_CANCELLED','LESS_THAN', executing_price) # sell_limit(symbol,quantity,price)
            pp.pprint(res)
        else:
            print("Bad Order")

    def do_oh(self, arg):
        res = self.my_bittrex.get_order_history()
        res = res['result']
        # print(res)
        # pp.pprint(res['result'])
        if res:
            table = BeautifulTable(max_width=170)
            table.numeric_precision = 10
            # table._width_exceed_policy = BeautifulTable.WEP_WRAP
            table.column_headers = ["Index","Exchange"
            # ,"TimeStamp"
            , "OrderType", "Quantity", "PricePerUnit","%5","%10","%15","%20","%30","%50", "Commission", "Price"
            # ,"Btcmults"
            ]

            index = 1
            for order in res:
                table.append_row([
                    index,
                    order['Exchange'],
                    # order['TimeStamp'],
                    order['OrderType'],
                    order['Quantity'],
                    order['PricePerUnit'],
                    order['PricePerUnit'] * 1.05,
                    order['PricePerUnit'] * 1.10,
                    order['PricePerUnit'] * 1.15,
                    order['PricePerUnit'] * 1.20,
                    order['PricePerUnit'] * 1.30,
                    order['PricePerUnit'] * 1.50,
                    # "{:.8f}".format(float(self.my_bittrex.get_ticker(order['Exchange'])['result']['Last'])),
                    "{:.6f}".format(float(order['Commission'])),
                    "{:.6f}".format(float(order['Price']))
                    # str(order['Price']*1.05) + "," + str(order['Price']*1.10 )+  "," + str(order['Price']*1.15)
                ])
                index += 1

            print(table)
            # return table
        else:
            print("No Open Orders")
        print('done')

    def do_oo(self, arg):
        pysqldf = lambda q: sqldf(q, locals())
        res = self.my_bittrex.get_order_history()
        res = res['result']
        # print(res)
        # pp.pprint(res['result'])
        res = pd.DataFrame(res)
        # res = res[['Exchange','TimeStamp','Quantity','QuantityRemaining']]
        # res = res[(res.OrderType == 'LIMIT_BUY' and re)]
        res = pysqldf("select * FROM res where OrderType = 'LIMIT_BUY' ")
        print(res)
        # if res:
        #     table = BeautifulTable(max_width=170)
        #     table.numeric_precision = 10
        #     # table._width_exceed_policy = BeautifulTable.WEP_WRAP
        #     table.column_headers = ["Index","Exchange"
        #     # ,"TimeStamp"
        #     , "OrderType", "Quantity", "PricePerUnit","%5","%10","%15","%20","%30","%50", "Commission", "Price"
        #     # ,"Btcmults"
        #     ]

        #     index = 1
        #     for order in res:
        #         table.append_row([
        #             index,
        #             order['Exchange'],
        #             # order['TimeStamp'],
        #             order['OrderType'],
        #             order['Quantity'],
        #             order['PricePerUnit'],
        #             order['PricePerUnit'] * 1.05,
        #             order['PricePerUnit'] * 1.10,
        #             order['PricePerUnit'] * 1.15,
        #             order['PricePerUnit'] * 1.20,
        #             order['PricePerUnit'] * 1.30,
        #             order['PricePerUnit'] * 1.50,
        #             # "{:.8f}".format(float(self.my_bittrex.get_ticker(order['Exchange'])['result']['Last'])),
        #             "{:.6f}".format(float(order['Commission'])),
        #             "{:.6f}".format(float(order['Price']))
        #             # str(order['Price']*1.05) + "," + str(order['Price']*1.10 )+  "," + str(order['Price']*1.15)
        #         ])
        #         index += 1

        #     print(table)
        #     # return table
        # else:
        #     print("No Open Orders")
        # print('done')

    def do_l(self, arg):
        res = self.my_bittrex.get_balances()
        res = res['result']
        btc_value = 0
        if arg:
            parts = arg.split()
            btc_value = parts[0]
        print("btc value is " + str(btc_value))
        # data = json.dumps(res)
        # print(type(res))
        # # data = json.load(res)
        # print(type(data))
        # df = pd.DataFrame(data) 
        # print(df)
        # print(res)
        # pp.pprint(res['result'])


        if res:
            table = BeautifulTable(max_width=150)
            table.numeric_precision = 10
            table.column_headers = ["Index","CurrencyLong","Currency","Available","Balance","Pending","TxFee","Last","btc_value"]

            index = 1
            for order in res:
                # print(order)
                if order['BitcoinMarket'] is not None and order['Balance']['Balance'] != 0:
                    # print("here")
                    table.append_row([
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

            print(table)
            # return table
        else:
            print("No Open Orders")
        print('done')

if __name__ == '__main__':
    BittrexShell().cmdloop()
