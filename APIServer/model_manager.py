from lru import LRU
from multiprocessing import Process, Pipe, cpu_count
from APIServer.model_process import createModelProcess, Message, CommunicationType

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
        model = None
        if(exec_key == None):
            model = self.processes.peek_last_item()
        else:
            model = self.processes[exec_key]
            del self.processes[exec_key]
        model.process.terminate()
        model.process.close()

    #First step to occur after model is initialized, when we start the server we don't have child processes until we get requests
    #model_id is used as a username for that model to identify it
    def spawn_model(self, model_id=None, payload=None, isTest=False):
        if(len(self.processes.items()) == self.maxSize):
            self.terminate_model()
        parent_conn, child_conn = Pipe() #we use pipe to communicate between parent and child; child process runs the actual model
        new_process = Process(target=createModelProcess, args=(child_conn, model_id, payload, isTest)) #each model runs in a process of its own
        mp = ModelProcessAttrs(new_process, parent_conn, model_id if not isTest else TEST_MODEL_ID)
        new_process.start()
        model = parent_conn.recv()
        self.processes[model.exec_key] = mp
        return model

    def run_model(self, exec_key, runtime):
        modelProcess = self.processes[exec_key] #Uses the child process
        if(modelProcess is None):
            return None
        message = Message(CommunicationType.RUN_MODEL, {'runtime': runtime})
        modelProcess.parent_conn.send(message)
        model = modelProcess.parent_conn.recv()
        return model

    def get_model(self, exec_key): 
        modelProcess = self.processes[exec_key]
        if(modelProcess is None):
            return None
        message = Message(CommunicationType.GET_MODEL)
        modelProcess.parent_conn.send(message)
        model = modelProcess.parent_conn.recv()
        return model

    def get_agent(self, exec_key, agent_name):
        modelProcess = self.processes[exec_key]
        if(modelProcess is None):
            return None
        message = Message(CommunicationType.AGENT_INFO, {'agent_name': agent_name})
        modelProcess.parent_conn.send(message)
        agent = modelProcess.parent_conn.recv()
        return agent
    
    def kill_model(self, exec_key):
        if(not self.processes.has_key(exec_key)):
            raise KeyError()
        self.terminate_model(exec_key)
    
    def to_json(self):
        ret_json = {}
        for key,val in self.processes.items():
            ret_json[key] = get_model_by_id(val.model_id).name
        return ret_json

modelManager = ModelManager()