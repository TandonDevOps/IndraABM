import os

INDRA_HOME_VAR = "INDRA_HOME"
PA_INDRA_HOME = "/home/IndraABM/IndraABM"

class Env:
  def __init__(self):
    self.indra_dir = os.getenv(INDRA_HOME_VAR, PA_INDRA_HOME)

env = Env()