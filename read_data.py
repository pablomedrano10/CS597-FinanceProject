#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 18:53:00 2018

@author: pablo
"""

import schedule
import time
from Robinhood import Robinhood

"""Robinhood example

#Setup
my_trader = Robinhood()
#login
my_trader.login(username="pablomedrano", password="Ronda$36192506")

#Get stock information
#Note: Sometimes more than one instrument may be returned for a given stock symbol
#stock_instrument = my_trader.instruments("GEVO")[0]

#print(stock_instrument)

##Get a stock's quote
my_trader.print_quote("AAPL")
print(my_trader.quote_data("AAPL"))

#Prompt for a symbol
my_trader.print_quote()

#Print multiple symbols
my_trader.print_quotes(stocks=["BBRY", "FB", "MSFT"])

#View all data for a given stock ie. Ask price and size, bid price and size, previous close, adjusted previous close, etc.
quote_info = my_trader.quote_data("GEVO")
print(quote_info)

Place a buy order (uses market bid price)
buy_order = my_trader.place_buy_order(stock_instrument, 1)

Place a sell order
sell_order = my_trader.place_sell_order(stock_instrument, 1)
"""

#Setup
my_trader = Robinhood()
#login
my_trader.login(username="pablomedrano", password="Ronda$36192506")

symbols = ["AAPL", "MSFT", "FB"]

def job():
    for stock in symbols:
        my_trader.print_quote(stock)

schedule.every(10).seconds.do(job)
#schedule.every().hour.do(job)
#schedule.every().day.at("10:30").do(job)

#while 1:
#    schedule.run_pending()
#    time.sleep(1)

try:
    while True:
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
    print('End')
    
    