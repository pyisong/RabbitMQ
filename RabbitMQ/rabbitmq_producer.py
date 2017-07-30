import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()  # 生成一个管道

# 在管道里声明一个queue
# durable=True 使队列持久化，但消息丢失了
channel.queue_declare(queue='hello', durable=True)

channel.basic_publish(exchange='',
                      routing_key='hello',  # queue名字
                      body='Hello World!',
                      properties=pika.BasicProperties(
                          delivery_mode=2,  # make message persistent 持久化
                        )
                      )

print("[x] Sent 'Hell World!'")
connection.close()
