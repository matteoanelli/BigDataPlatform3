import json, os, time
import subprocess
from multiprocessing import Process, Queue

class streamingestmanager():
    def __init__(self,tenants):
        self.tenants = tenants
        tenantsappdir = "assignment-2-801979/code/Near-realtime_ingestion/clientstreamingingestapp/"
        for tenant in self.tenants:
            os.system('python ' + tenantsappdir + 'clientstreamingestapp_' + tenant['tenant_id'] + '.py ' + tenant['MONGO_URL'])




if __name__ == '__main__':
    #tenantsappdir = "./assignment-2-801979/code/Near-realtime_ingestion/clientstreamingingestapp/"
    tenants = ['tenant1','tenant2']
    proc = []
    print('python ' + 'BasicStreamingongestmanager.py ' + 'run ' + 'tenant1')
    pid = os.system('python ' + 'BasicStreamingongestmanager.py ' + 'run ' + 'tenant1')
    print('PID: {}'.format(pid))
    time.sleep(20)
    exit = os.system('python ' + 'BasicStreamingongestmanager.py ' + 'stop ' + str(pid))
    print(exit)


