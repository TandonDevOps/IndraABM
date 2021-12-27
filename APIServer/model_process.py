from enum import Enum, auto
from APIServer.model_api import create_model

import models.basic as bsc

# All the function that can be run on a model to get info must be defined here
class CommunicationType(Enum):
  RUN_MODEL = auto()
  AGENT_INFO = auto()
  GET_MODEL = auto()

class Message:
  def __init__(self, communication_type, data):
    self.type = communication_type
    self.data = data

""" 
  Each process spawned holds the model
  The process then waits on the parent process to send messages with a communication type
  and responds correspondingly
"""
def createModelProcess(conn, model_id, payload, is_test=False):
  if(is_test):
    model = bsc.create_model(create_for_test=True)
  else:
    model = create_model(model_id, payload) #This uses the child process

  conn.send(model)  # The first time a process is created, it send back the model was created
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
