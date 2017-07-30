import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# durable=True 使队列持久化
channel.queue_declare(queue='hello', durable=True)


def callback(ch, method, properties, body):
    # print(ch)
    # print(method)
    print(properties)
    print("[x] Received %r : %r" % (method.routing_key, body.decode()))
    # 如果no_ack=FALSE 加上下面的code 手动确认收到消息
    # ch.basic_ack(delivery_tag=method.delivery_tag)

# 消费者消费这条消息以后，生产者才会再次发消息(权重设置)，
# 消费者端只要存在一条消息就不会再发(与计算机的处理速度有关)
channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue='hello', no_ack=True)  # 不确认消息是否收到

print('[*] Waiting for messages. To exit press Ctrl+C')
channel.start_consuming()
