from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
import json
import os
import pika

#from producer import producer

def checkID(tenant):
    with open('./config_user.json', "r") as read_file:
        config = json.load(read_file)
    tenants = config['tenants']
    for client in tenants:
        if client['tenant_id'] == tenant:
            return True
    return False

def producer(new_records):
    # Access the CLODUAMQP_URL environment variable and parse it (fallback to localhost)
    url = os.environ.get('CLOUDAMQP_URL')
    params = pika.URLParameters('amqp://lglizjgp:ZHTrNmxKUo5sjiTgux_OOvmvSfnJUvao@moose.rmq.cloudamqp.com/lglizjgp')
    connection = pika.BlockingConnection(params)
    channel = connection.channel() # start a channel
    channel.queue_declare(queue=new_records['tenant_id']) # Declare a queue
    channel.basic_publish(exchange='',
                          routing_key=new_records['tenant_id'],
                          body=json.dumps(new_records))
    connection.close()
    return 'message sent'

# ------------------------------------ Application -----------------------------------------------
app = Flask(__name__)

@app.route('/insert',methods=['POST'])
def insert():

    if not request.is_json:
        return jsonify({'message': '400 : Request not valid json'})
    id = request.json['tenant_id']
    if not id:
        return jsonify({'message': '400 : Missing tenant ID '})
    if checkID(id) == False:
        return jsonify({'message': '400 : Tenant ID not valid '})

    message = producer(request.get_json())
    return message


if __name__ == '__main__':
    app.run(debug=True)

