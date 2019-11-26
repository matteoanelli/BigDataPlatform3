# Consumer Deamon that listen from rabbit and ingest data
import pika, os, json
import pymongo

client = pymongo.MongoClient(os.environ.get('MONGO_URL'))
db = client.get_database('test')
records = db.documents

url = os.environ.get('CLOUDAMQP_URL')
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel() # start a channel
channel.queue_declare(queue='user') # Declare a queue

def callback(ch, method, properties, body):
    data = json.loads(body)
    records.insert(data)

channel.basic_consume('user',
                      callback,
                      auto_ack=True)
print(' [*] Waiting for messages:')
channel.start_consuming()

