import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs', type='fanout')

message = ' '.join(sys.argv[1:]) or "info: Hello world!"

channel.basic_publish(exchange='logs', routing_key='', body=message)

print(" [x] Sent %r " % message)
connection.close()
