import pika
import json
from pprint import pprint
import pandas as pd
import json

connection = pika.BlockingConnection(pika.ConnectionParameters(host = 'localhost'))
channel = connection.channel()
channel.queue_declare(queue = 'order_signal')

def callback(ch, method, properties, body):
        data_json.append(json.loads(body))
        pprint(data_json)

channel.basic_consume(callback, queue = 'rhdata', no_ack = True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
