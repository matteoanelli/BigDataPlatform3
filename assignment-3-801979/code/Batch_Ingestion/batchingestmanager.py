import os
import time
import json
from os.path import isfile, join


with open('./config_user.json', "r") as read_file:
    config = json.load(read_file)
tenants = config['tenants']
while True:
    time.sleep(30)
    clientInputDir = "/home/matteo/Desktop/BigDataPlatform2/assignment-2-801979/data/StagingData"
    # TODO: relative path
    tenantsappdir = "/home/matteo/Desktop/BigDataPlatform2/assignment-2-801979/code/Batch_Ingestion/clientbatchingestapps/"
    files = []
    for dir in os.walk(clientInputDir):
        if dir[0] != clientInputDir:
            if os.listdir(dir[0]):
                tenant = os.path.basename(os.path.normpath(dir[0]))
                for client in tenants:
                    if client['tenant_id'] == tenant:
                        mongo_url = client['MONGO_URL']
                for file in os.listdir(dir[0]):
                    files.append(dir[0] + '/'+ file)
                    os.system('python ' + tenantsappdir + 'clientbatchingestapp_' + os.path.basename(os.path.normpath(dir[0])) + '.py "' + dir[0] + '/' + file + '" "' + mongo_url + '"')

# TODO: multitreading
# TODO: logging and test
# TODO: microbatching    done but final test neded
# TODO: Config file done
# TODO: second client app