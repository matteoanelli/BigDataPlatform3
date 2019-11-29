import pika, os

def producer(new_records):
    # Access the CLODUAMQP_URL environment variable and parse it (fallback to localhost)
    url = os.environ.get('CLOUDAMQP_URL')
    params = pika.URLParameters(url)
    print(params)
    connection = pika.BlockingConnection(params)
    channel = connection.channel() # start a channel
    channel.queue_declare(queue='user') # Declare a queue
    channel.basic_publish(exchange='',
                          routing_key='user',
                          body=new_records)
    connection.close()
    return 'message sent'