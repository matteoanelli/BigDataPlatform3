import sys
import pika
from time import sleep
import csv
from datetime import datetime

# RABBITMQ_URI = 'amqp://guest:guest@localhost/'
RABBITMQ_URI = 'amqp://lglizjgp:ZHTrNmxKUo5sjiTgux_OOvmvSfnJUvao@moose.rmq.cloudamqp.com/lglizjgp'
queue = 'customer1queue'

params = pika.URLParameters(RABBITMQ_URI)
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue=queue, durable=True)  # the 'durable' param guarantees at-least-once

file_path = "../../data/2018_Yellow_Taxi.csv"

with open(file_path) as file:
    for line in file:
        sleep(0.001)
        record = line.strip()
        channel.basic_publish(exchange='', routing_key=queue, body=record)
        print("record sent {}: ".format(record))


