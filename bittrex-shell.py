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
        self.my_bittrex = Bittrex("key", "secert")
        # self.trader.login(username=USERNAME, password=PASSWORD)
	# my_bittrex = 

	# print(my_bittrex.buy_limit('BTC-RCN',100,0.00001943))
	# pprint(my_bittrex.get_open_orders())
    def do_b(self, arg):
        'Buy stock b <symbol> <quantity> <price>'
        parts = arg.split()
        if len(parts) >= 2 and len(parts) <= 3:
            symbol = parts[0]
            quantity = parts[1]
            if len(parts) == 3:
                price = float(parts[2])
            else:
                price = 0.0
            print(price)    
            # stock_instrument = self.my_bittrex.buy_limit('BTC-RCN',100,0.00001943)
            res = self.my_bittrex.buy_limit(symbol,quantity,price)
            pp.pprint(res)
            # if not (res.status_code == 200 or res.status_code == 201):
            #     print("Error executing order")
            #     try:
            #         data = res.json()
            #         if 'detail' in data:
            #             print(data['detail'])
            #     except:
            #         print(data['detail'])
            # else:
            #     print("Done\nTrailing stoploss code:- " + "p " + symbol + " " + str(quantity) + " " + str(price) + " 0.0")
            #     print(      "Sell code             :- " + "s " + symbol + " " + str(quantity) + " " + str(price))
        else:
            print("Bad Order")
    
    def do_s(self, arg):
        'Sell stock s <symbol> <quantity> <?price>'
        parts = arg.split()
        if len(parts) >= 2 and len(parts) <= 3:
            symbol = parts[0]
            quantity = parts[1]
            if len(parts) == 3:
                price = float(parts[2])
            else:
                price = 0.0

            res = self.my_bittrex.sell_limit(symbol,quantity,price)
            pp.pprint(res)
        else:
            print("Bad Order")

    def do_o(self, arg):
        'List open orders'
        open_orders = self.my_bittrex.get_open_orders()
        # pp.pprint(open_orders)
        if open_orders:
            table = BeautifulTable(max_width=150)
            table.column_headers = ["Index","Exchange", "ImmediateOrCancel", "IsConditional", "Limit", "OrderType", "Opened","OrderUuid","Quantity","QuantityRemaining"]

            index = 1
            for order in open_orders['result']:
                table.append_row([
                    index,
                    order['Exchange'],
                    order['ImmediateOrCancel'],
                    order['IsConditional'],
                    float(order['Limit']),
                    order['OrderType'],
                    order['Opened'],
                    order['OrderUuid'],
                    # int(float(order['quantity'])),
                    order['Quantity'],
                    order['QuantityRemaining'],
                ])
                index += 1

            print(table)
            return table
        else:
            print("No Open Orders")

    def do_ca(self, arg):
        'Cancel all open orders'
        # open_orders = self.trader.get_open_orders()
        # for order in open_orders:
        #     try:
        #         self.trader.cancel_order(order['id'])
        #     except Exception as e:
        #         pass
        try:
            open_orders = BittrexShell.do_o(self,arg)
            for i in open_orders['OrderUuid']:
                self.my_bittrex.cancel(i)
        except Exception as e:
            print("Error cancelling - could be no Open Orders " + str(e))
        print("Done")

    

if __name__ == '__main__':
    BittrexShell().cmdloop()
