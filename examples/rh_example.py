import schedule
import time
from Robinhood import Robinhood
import pprint
import pika
import json
from os import environ

#Robinhood example
#Setup
my_trader = Robinhood()
#login
my_trader.login(username = environ.get('RH_USER'), password = environ.get('RH_PASSWORD'))
#Get a stock's quote
my_trader.print_quote("AAPL")
print(my_trader.quote_data("AAPL"))
