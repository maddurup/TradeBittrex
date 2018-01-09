import cmd, json
from bittrex.bittrex import Bittrex, API_V2_0
from bittrex.bittrex import *
from beautifultable import BeautifulTable
import pprint, time
pp = pprint.PrettyPrinter(indent=4)

class BittrexShell(cmd.Cmd):
    intro = 'Welcome to the Bittrex shell. Type help or ? to list commands.\n'
    prompt = '> '
    my_bittrex = Bittrex(None, None)  # or defaulting to v1.1 as Bittrex(None, None)
	# print(my_bittrex.get_markets())
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.my_bittrex = Bittrex("Key", "Secert")


    def do_sl(self, arg):
        'Sell stock s <symbol> <quantity> <price_to_sell> <executing_price>'
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
        print(res)
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
                    "{:.6f}".format(float(order['Price'])),
                    # str(order['Price']*1.05) + "," + str(order['Price']*1.10 )+  "," + str(order['Price']*1.15)
                ])
                index += 1

            print(table)
            # return table
        else:
            print("No Open Orders")
        print('done')

    def do_l(self, arg):
        res = self.my_bittrex.get_order_history()
        res = res['result']
        print(res)
        # pp.pprint(res['result'])
        if res:
            table = BeautifulTable(max_width=150)
            table.column_headers = ["Index","AccountId","Available", "Balance", "Currency", "Pending", "Requested", "Uuid"]

            index = 1
            for order in res:
                table.append_row([
                    index,
                    order['Balance']['AccountId'],
                    order['Balance']['Available'],
                    order['Balance']['Balance'],
                    order['Balance']['Currency'],
                    order['Balance']['Pending'],
                    order['Balance']['Requested'],
                    order['Balance']['Uuid']
                ])
                index += 1

            print(table)
            # return table
        else:
            print("No Open Orders")
        print('done')

if __name__ == '__main__':
    BittrexShell().cmdloop()
