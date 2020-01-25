import pika, os, json, sys
'''
Consumer de
'''

# Connection to CloudAMQP service
url = CLOUDAMQP_URL
# local testing
# url = 'amqp://guest:guest@localhost/'
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel() # start a channel
channel.queue_declare(queue='result1') # Declare a queue

def callback(ch, method, properties, body):
    print('Analytics results: {}'.format(body))

channel.basic_consume('result1',
                      callback,
                      auto_ack=True)
channel.start_consuming()
