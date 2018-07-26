import pika
import json
from pprint import pprint
import pandas as pd
import json

connection = pika.BlockingConnection(pika.ConnectionParameters(host = 'localhost'))
channel = connection.channel()

channel.queue_declare(queue = 'rhdata')

data_json = []
stock_prices = []

first_iter = True
buy_signal = False
sell_signal = False
prev_flag = False
now_flag = False

def callback(ch, method, properties, body):
    global first_iter
    global buy_signal
    global sell_signal
    global prev_flag
    global now_flag

    print(first_iter)
    data_json.append(json.loads(body))
    pprint(data_json)

    stock_prices.append(float(data_json[len(data_json)-1][0]['bid_price']))
    # print(stock_prices)
    stock_prices_df = pd.Series(stock_prices)
    # print(stock_prices_df)
    # print(len(stock_prices_df))
    ma20 = stock_prices_df.rolling(20).mean().iloc[-1]
    ma100 = stock_prices_df.rolling(20).mean().iloc[-1]

    if ma20 > ma100:
        now_flag = True
    else:
        now_flag = False

    if now_flag != prev_flag:
        if now_flag == True:
            buy_signal = True
        else:
            sell_signal = True

    if first_iter == True:
        buy_signal = False
        sell_signal = False
        first_iter = False

    prev_flag = now_flag

    if buy_signal == True:
        #Connect to RabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters(host = 'localhost'))
        channel = connection.channel()

        #Create queue
        channel.queue_declare(queue = 'order_signal')
        message = 'buy'
        channel.basic_publish(exchange = '', routing_key = 'order_signal', body = json.dumps(message))
        connection.close()

    elif sell_signal == True:
        #Connect to RabbitMQ
        connection2 = pika.BlockingConnection(pika.ConnectionParameters(host = 'localhost'))
        channel2 = connection2.channel()

        #Create queue
        channel2.queue_declare(queue = 'order_signal')
        message = 'sell'
        channel2.basic_publish(exchange = '', routing_key = 'order_signal', body = json.dumps(message))
        connection2.close()

    '''Moving average crossover strategy: When the shorter-term MA crosses above the longer-term MA, it's a buy signal.
    Meanwhile, when the shorter-term MA crosses below the longer-term MA, it's a sell signal'''

channel.basic_consume(callback, queue = 'rhdata', no_ack = True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
