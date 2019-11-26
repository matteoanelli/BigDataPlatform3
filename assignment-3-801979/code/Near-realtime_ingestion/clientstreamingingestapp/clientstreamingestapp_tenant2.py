# Tenant2 Deamon that listen from rabbit and ingest data
import pika, os, json, sys
import pymongo

client = pymongo.MongoClient(sys.argv[1])
db = client.get_database('test_tenant2')
records = db.documents_tenant2

url = 'amqp://lglizjgp:ZHTrNmxKUo5sjiTgux_OOvmvSfnJUvao@moose.rmq.cloudamqp.com/lglizjgp'
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel() # start a channel
channel.queue_declare(queue='tenant2') # Declare a queue

def callback(ch, method, properties, body):
    payload = json.loads(body)
    data = payload['data']
    records.insert(data)

channel.basic_consume('tenant2',
                      callback,
                      auto_ack=True)
print(' [*] Waiting for messages:')
channel.start_consuming()