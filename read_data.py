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

STARTING_TRADING_HOUR = 8
STARTING_TRADING_MIN = 30
ENDING_TRADING_HOUR = 22
ENDING_TRADING_MIN = 30

def Trading_hours():
    if (((datetime.datetime.now().hour == 8 and datetime.datetime.now().minute > 30) or datetime.datetime.now().hour > 9) and datetime.datetime.now().hour < 15):
        return True
    else:
        return False

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

    if Trading_hours() == False:
        for stock in symbols:
            message = []
            message.append(my_trader.quote_data(stock))
            pprint(message)
        channel.basic_publish(exchange = '', routing_key = 'rhdata', body = json.dumps(message))
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
