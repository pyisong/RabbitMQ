import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='topic_logs', type='topic')  # 类型变成topic

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue


binding_keys = sys.argv[1:]
if not binding_keys:
    sys.stderr.write("Usage: %s [binding_keys]...\n" % sys.argv[0])
    sys.exit(1)

print(binding_keys)
for binding_key in binding_keys:
    channel.queue_bind(exchange='topic_logs',
                       queue=queue_name,
                       routing_key=binding_key)

print(" [*] Waiting for logs. To exit press Ctrl+C")


def callback(ch, method, properties, body):
    print(ch)
    print(properties)
    print(" [x] %r:%r" % (method.routing_key, body))

channel.basic_consume(callback, queue=queue_name, no_ack=True)
channel.start_consuming()
