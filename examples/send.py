import pika

#Establish connection
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

#Create a queue
channel.queue_declare(queue='hello')

#Specify exchange type ' ' for default, queue and message
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='tu vieja')
print(" [x] Sent 'Hello World!'")

#Close connection to make sure buffer was flushed and delivered
connection.close()
