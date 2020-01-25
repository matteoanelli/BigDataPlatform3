import sys
import pika
from time import sleep
from datetime import datetime

# Using Rabbit running locally

# RABBITMQ_URI = 'amqp://guest:guest@localhost/'

'''
Producer that read the input file and push line by line the records inside the message broker.
The actual implementation is meant to use rubbitMQ as a service using the CLOUDAMQP service. 
It aim to simulate a client that interact with the big data platform throughout the message broker.
'''

# Using rabbit as a service
RABBITMQ_URI = CLOUDAMQP_URL
queue = 'customer1queue'

params = pika.URLParameters(RABBITMQ_URI)
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue=queue, durable=True)  # the 'durable' param guarantees at-least-once

file_path = "../../data/2018_Yellow_Taxi.csv"

with open(file_path) as file:
    for line in file:
        sleep(0.01)
        # sleep(0.001)
        record = line.strip()
        channel.basic_publish(exchange='', routing_key=queue, body=record)
        print("record sent {}: ".format(record))


