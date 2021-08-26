"""
This module is intended to hold the various functions an agent might call
in the course of acting.
"""
from math import pi, sin

import lib.agent as agt
import lib.space as spc
import lib.utils as utl
import registry.registry as reg

DEBUG = utl.Debug()

MOVE = agt.MOVE
DONT_MOVE = agt.DONT_MOVE


def get_model(agent):
    return reg.get_model(agent.exec_key)


def get_group(agent, grp_nm):
    return reg.get_group(grp_nm, agent.exec_key)


def create_agent(name, i, action=None, **kwargs):
    """
    Create an agent that does almost nothing.
    """
    return agt.Agent(name + str(i), action=action, **kwargs)


def def_action(agent, **kwargs):
    """
    A simple default agent action.
    """
    if DEBUG.debug_lib:
        print("Agent {} is acting".format(agent.name))
    return agt.DONT_MOVE


def add_switch(agent, old_group, new_group):
    """
    Switch an agent between groups.
    """
    model = get_model(agent)
    assert model is not None
    model.add_switch(str(agent),
                     old_group,
                     new_group)


def get_prop(exec_key, prop_nm, default=None):
    model = reg.get_model(exec_key)
    assert model is not None
    return model.get_prop(prop_nm, default=None)


def prob_state_trans(curr_state, states):
    return agt.prob_state_trans(curr_state, states)


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
    return spc.neighbor_ratio(agent, pred_one, pred_two=pred_two, size=size,
                              region_type=region_type, **kwargs)


def ratio_to_sin(ratio):
    """
    Take a ratio of y to x and turn it into a sine.
    """
    return sin(ratio * pi / 2)
