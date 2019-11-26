import json, os, sys, signal
import subprocess

command = sys.argv[1]
# if command == 'run_all':
#     with open('assignment-2-801979/code/Near-realtime_ingestion/clientstreamingingestapp', "r") as read_file:
#         config = json.load(read_file)
#     tenants = config['tenants']
#
#     tenantsappdir = "assignment-2-801979/code/Near-realtime_ingestion/clientstreamingingestapp/"
#     for tenant in tenants:
#         os.system('python ' + tenantsappdir + 'clientstreamingestapp_' + tenant['tenant_id'] + '.py ' + tenant['MONGO_URL'])

if command == 'run':
    new_pid = 0
    tenant = sys.argv[2]
    with open('/home/matteo/Desktop/BigDataPlatform2/assignment-2-801979/code/Near-realtime_ingestion/API/config_user.json', "r") as read_file:
        config = json.load(read_file)
    tenants =  config['tenants']
    print(tenants)
    tenantsappdir = "assignment-2-801979/code/Near-realtime_ingestion/clientstreamingingestapp/"
    mongo_uri = None
    for temp in tenants:
        if temp['tenant_id'] == tenant:
            mongo_uri = temp['MONGO_URL']
    if(mongo_uri):
        pid = subprocess.Popen(['python',tenantsappdir + 'clientstreamingestapp_' + tenant + '.py ',mongo_uri], shell=True)
        new_pid = pid.pid
        print('New app running with PID: {}'.format(new_pid))
        print(new_pid)
    exit(1111)

elif command == 'stop':
    pid = sys.argv[2]
    os.kill(int(pid), signal.SIGSTOP)
    print('App killed:{}'.format(pid))
    exit(0)

else:
    exit(1)
#TODO: fix path problem porco dio