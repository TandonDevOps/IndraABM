"""
This module is intended to hold contants, classes, and
various functions an agent might call
in the course of acting.

To use the elements, import them from lib.actions and call by names.

@Author: Kefan Yang, Wenbo Nan, Jiawei He, Zilong Wang
@Date: 11/17/2021
"""

import lib.agent as agt
import lib.display_methods as disp
import lib.group as grp
import lib.space as spc
import lib.utils as utl
import registry.registry as reg

DEBUG = utl.Debug()

MOVE = agt.MOVE
DONT_MOVE = agt.DONT_MOVE
AgentEncoder = agt.AgentEncoder
Agent = agt.Agent
X = agt.X
Y = agt.Y
NEUTRAL = agt.NEUTRAL

PURPLE = disp.PURPLE
NAVY = disp.NAVY
BLUE = disp.BLUE
CYAN = disp.CYAN
GREEN = disp.GREEN
SPRINGGREEN = disp.SPRINGGREEN
LIMEGREEN = disp.LIMEGREEN
YELLOW = disp.YELLOW
TAN = disp.TAN
ORANGE = disp.ORANGE
ORANGERED = disp.ORANGERED
TOMATO = disp.TOMATO
RED = disp.RED
DARKRED = disp.DARKRED
MAGENTA = disp.MAGENTA
WHITE = disp.WHITE
GRAY = disp.GRAY
BLACK = disp.BLACK

DEF_HEIGHT = spc.DEF_HEIGHT
DEF_WIDTH = spc.DEF_WIDTH

Group = grp.Group


"""
APIs to get/register model
"""


def get_model(agent):
    """
    Get the model which is a special singleton member of the registry.
    """
    return reg.get_model(agent.exec_key)


def reg_model(model, exec_key):
    """
    The model is a special singleton member of the registry.
    """
    return reg.reg_model(model, exec_key)


def get_prop(exec_key, prop_nm, default=None):
    """
    Have a way to get a prop through the model to hide props structure.
    """
    model = reg.get_model(exec_key)
    assert model is not None
    return model.get_prop(prop_nm, default)


"""
APIs to get group
"""


def get_group(agent, grp_nm):
    """
    Groups *are* agents, so:
    It's a separate func for clarity and in case one day things change.
    """
    return reg.get_group(grp_nm, agent.exec_key)


"""
APIs to get/create agent
"""


def get_agent(agt_nm, exec_key):
    """
    Fetch an agent from the registry based on agent name.
    Return: The agent object, or None if not found.
    """
    return reg.get_agent(agt_nm, exec_key)


def get_agent_at(self, x, y):
    """
    Return agent at cell x,y
    If cell is empty return None.
    Always make location a str for serialization.
    """
    if self.is_empty(x, y):
        return None
    agent_nm = self.locations[str((x, y))]
    return reg.get_agent(agent_nm, self.exec_key)


def create_agent(name, i, action=None, **kwargs):
    """
    Create an agent that does almost nothing.
    """
    return agt.Agent(name + str(i), action=action, **kwargs)


"""
APIs dealing with execution environment
"""


def create_exec_env(save_on_register=True,
                    create_for_test=False, exec_key=None):
    """
    Create a new execution environment and return its key.
    """
    return reg.create_exec_env(save_on_register, create_for_test, exec_key)


"""
agent operations
"""


def def_action(agent, **kwargs):
    """
    A simple default agent action.
    """
    if DEBUG.debug_lib:
        print("Agent {} is acting".format(agent.name))
    return agt.DONT_MOVE


def prob_state_trans(curr_state, states):
    """
    Do a probabilistic state transition.
    """
    return agt.prob_state_trans(curr_state, states)


def join(agent1, agent2):
    """
    Create connection between agent1 and agent2.
    agent1 should be a group.
    """
    return agt.join(agent1, agent2)


"""
model operations
"""


def get_periods(agent):
    """
    Get the pophist (timeline) period from the model's env
    """
    mdl = get_model(agent)
    return mdl.get_periods()


"""
APIs dealing with group switching
"""


def switch(agent_nm, old_group, new_group, exec_key):
    """
    Move agent from grp1 to grp2.
    We first must recover agent objects from the registry.
    """
    return agt.switch(agent_nm, old_group, new_group, exec_key)


def add_switch(agent, old_group, new_group):
    """
    Switch an agent between groups.
    """
    model = get_model(agent)
    assert model is not None
    model.add_switch(str(agent), old_group, new_group)


"""
APIs dealing with neighbors and spacial relations
"""


def exists_neighbor(agent, pred=None, exclude_self=True, size=1,
                    region_type=None, **kwargs):
    """
    Does a neighbor exists within `size` matching `pred`?
    Returns True or False.
    """
    return spc.exists_neighbor(agent, pred=pred, exclude_self=exclude_self,
                               size=size, region_type=region_type, **kwargs)


def get_neighbors(agent, pred=None, exclude_self=True, size=1,
                  region_type=spc.MOORE, model_name=None):
    """
    Get the Moore neighbors for an agent.
    We might expand this in the future to allow von Neumann hoods!
    """
    return spc.get_neighbors(agent, pred=pred, exclude_self=exclude_self,
                             size=size, region_type=region_type,
                             model_name=model_name)


def neighbor_ratio(agent, pred_one, pred_two=None, size=1, region_type=None,
                   **kwargs):
    """
    Returns the ratio of neighbors of one type (specified by pred_one)
    to all neighbors.
    If pred_two is passed, it will return ratio of pred_one to pred_two.
    """
    return spc.neighbor_ratio(agent, pred_one, pred_two=pred_two, size=size,
                              region_type=region_type, **kwargs)


def get_neighbor(agent, pred=None, exclude_self=True, size=1,
                 region_type=None, **kwargs):
    """
    Get one neighbor who passes pred
    """
    return spc.get_neighbor(agent, pred, exclude_self, size, region_type,
                            **kwargs)


def get_num_of_neighbors(agent, exclude_self=False, pred=None, size=1,
                         region_type=None, **kwargs):
    """
    Gen number of neighbors filtered by pred
    """
    return spc.get_num_of_neighbors(agent, exclude_self, pred, size,
                                    region_type, **kwargs)


def in_hood(agent, other, hood_sz):
    """
    Check whether agent and other are within a certain distance
    of each other.
    """
    return spc.in_hood(agent, other, hood_sz)


"""
util functions
"""


def get_user_type(user_api=None):
    """
    Retrieve user type from env
    """
    return utl.get_user_type(user_api)


def init_props(module, props=None, model_dir=None, skip_user_questions=False):
    """
    initilize props
    """
    return utl.init_props(module, props, model_dir, skip_user_questions)


def ratio_to_sin(ratio):
    """
    Take a ratio of y to x and turn it into a sine.
    """
    return utl.ratio_to_sin(ratio)
