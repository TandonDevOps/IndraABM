from lru import LRU
from multiprocessing import Process, Pipe, cpu_count
import werkzeug.exceptions as wz
from APIServer.model_process import createModelProcess, Message, CommunicationType, createNewModel

from db.model_db import get_model_by_id

TEST_MODEL_ID = 0

class ModelProcessAttrs:
    #New model is being created, once the endpoint is done we call spawn_model within ModelManager
    def __init__(self, process, parent_conn, model_id):
        self.process = process 
        self.parent_conn = parent_conn
        self.model_id = model_id

class ModelManager:

    def __init__(self):
        print("Creating new model manager")
        self.maxSize = cpu_count() * 5 + 1       #Max number of process to run at parallel, can be used to check before caching a process
        self.processes = LRU(self.maxSize) # Not too many processes but also not too little, this is the total amount we're permitted to have
        self.spawn_model(isTest=True)

    def terminate_model(self, exec_key=None):
        modelProcess = None
        if(exec_key == None):
            model_tuple = self.processes.peek_last_item()
            modelProcess = model_tuple[1]
        else:
            modelProcess = self.get_process(exec_key)
            del self.processes[exec_key]
        modelProcess.process.terminate()
        modelProcess.process.join()
        modelProcess.process.close()

    #First step to occur after model is initialized, when we start the server we don't have child processes until we get requests
    #model_id is used as a username for that model to identify it
    def spawn_model(self, model_id=None, payload=None, model_name=None, isTest=False):
        if(len(self.processes.items()) == self.maxSize):
            self.terminate_model()
        parent_conn, child_conn = Pipe() #we use pipe to communicate between parent and child; child process runs the actual model
        if(model_name == None):
            new_process = Process(target=createModelProcess, args=(child_conn, model_id, payload, isTest)) #each model runs in a process of its own
        else:
            new_process = Process(target=createNewModel, args=(child_conn, model_name))
        mp = ModelProcessAttrs(new_process, parent_conn, model_id if not isTest else TEST_MODEL_ID)
        new_process.start()
        model = parent_conn.recv()
        self.processes[model.exec_key] = mp
        return model

    def get_process(self, exec_key):
        if(not self.processes.has_key(exec_key)):
            raise wz.NotFound(f"Model Key: {exec_key}, not found.")
        return self.processes[exec_key]

    def run_model(self, exec_key, runtime):
        modelProcess = self.get_process(exec_key)
        message = Message(CommunicationType.RUN_MODEL, {'runtime': runtime})
        modelProcess.parent_conn.send(message)
        model = modelProcess.parent_conn.recv()
        return model

    def get_model(self, exec_key): 
        modelProcess = self.get_process(exec_key)
        message = Message(CommunicationType.GET_MODEL)
        modelProcess.parent_conn.send(message)
        model = modelProcess.parent_conn.recv()
        return model

    def get_agent(self, exec_key, agent_name):
        modelProcess = self.get_process(exec_key)
        message = Message(CommunicationType.AGENT_INFO, {'agent_name': agent_name})
        modelProcess.parent_conn.send(message)
        agent = modelProcess.parent_conn.recv()
        return agent

    def create_group(self, exec_key, jrep, group_color, group_num_of_members, group_name):
        modelProcess = self.get_process(exec_key)
        message = Message(CommunicationType.CREATE_GROUP, {'jrep': jrep, 
                                                            'group_color': group_color, 
                                                            'group_num_of_members': group_num_of_members, 
                                                            'group_name' : group_name})
        modelProcess.parent_conn.send(message)
        model = modelProcess.parent_conn.recv()
        return model
    
    def to_json(self):
        ret_json = {}
        for key,val in self.processes.items():
            ret_json[key] = get_model_by_id(val.model_id).name
        return ret_json

modelManager = ModelManager()