from enum import Enum, auto
from APIServer.model_api import create_model
import lib.model as mdl
import lib.agent as agt
from model_generator.model_generator import create_group

import models.basic as bsc

# All the function that can be run on a model to get info must be defined here
class CommunicationType(Enum):
  RUN_MODEL = auto()
  AGENT_INFO = auto()
  GET_MODEL = auto()
  CREATE_GROUP = auto()

class Message:
  def __init__(self, communication_type, data=None):
    self.type = communication_type
    self.data = data

def listenForMessages(conn, model):
  while True:                                 # The process then goes into an infinite loop listening on the pipe
      message = conn.recv()
      if message.type == CommunicationType.RUN_MODEL:
        periods = message.data['runtime']
        model.runN(int(periods))
        conn.send(model)
      elif message.type == CommunicationType.GET_MODEL:
        conn.send(model)
      elif message.type == CommunicationType.AGENT_INFO:
        agent = model.get_agent(message.data['agent_name'])
        conn.send(agent)
      elif message.type == CommunicationType.CREATE_GROUP:
        new_group = create_group(message.data['jrep'], message.data['group_color'], message.data['group_num_of_members'], message.data['group_name'])
        agt.join(model.env, new_group[0])
        conn.send(model)
      

""" 
  Each process spawned holds the model
  The process then waits on the parent process to send messages with a communication type
  and responds correspondingly
"""
def createModelProcess(conn, model_id, payload, is_test):
  if(is_test):
    model = bsc.create_model(create_for_test=True)
  else:
    model = create_model(model_id, payload) #This uses the child process

  conn.send(model)  # The first time a process is created, it send back the model was created
  listenForMessages(conn, model)

def createNewModel(conn, model_name):
  model = mdl.Model(model_name, grp_struct={}, props={})
  conn.send(model)
  listenForMessages(conn, model)

