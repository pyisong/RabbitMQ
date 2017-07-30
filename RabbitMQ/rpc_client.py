import pika
import uuid
import time


class FibonacciRpcClient(object):
    def __init__(self):
        self.corr_id = str(uuid.uuid4())
        self.response = None
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(self.on_response,  # 收到消息调用on_response
                                   no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue',
                                   properties=pika.BasicProperties(
                                       reply_to=self.callback_queue,
                                       correlation_id=self.corr_id
                                   ),
                                   body=str(n))

        while self.response is None:
            # 非阻塞的start_consuming
            self.connection.process_data_events()
            print('no msg......')
            time.sleep(0.5)
        return int(self.response)


if __name__ == '__main__':
    fibonacci_rpc = FibonacciRpcClient()
    print(" [x] Requesting fib(30)")
    response = fibonacci_rpc.call(30)
    print(" [.] Got %r" % response)
