#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 18:53:00 2018
@author: pablo
"""

import schedule
import time
from Robinhood import Robinhood
from pprint import pprint
import pika
import json
import datetime
from os import environ

starting_trading_hour = 8
starting_trading_minute = 30
ending_trading_hour = 22
ending_trading_minute = 30

#Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host = 'localhost'))
channel = connection.channel()

#Create queue
channel.queue_declare(queue = 'rhdata')

#Setup
my_trader = Robinhood()
#login
my_trader.login(username = environ.get('RH_USER'), password = environ.get('RH_PASSWORD'))

symbols = ["AAPL"]

def job():
    print(type(datetime.datetime.now().hour))

    for stock in symbols:
        message = []
        message.append(my_trader.quote_data(stock))
        pprint(message)
    channel.basic_publish(exchange='',
                      routing_key = 'rhdata',
                      body = json.dumps(message))
    print("-------------")
    print("Message Sent!")
    print("-------------")

    # connection.close()

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
