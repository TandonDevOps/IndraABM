
"""
This module is intended to hold the various functions an agent might call
in the course of acting.
"""

import lib.agent as agt
import lib.space as spc
import lib.utils as utl

DEBUG = utl.Debug()


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


def get_neighbors(agent, pred=None, exclude_self=True, size=1,
                  region_type=None):
    """
    Get the Moore neighbors for an agent.
    We might expand this in the future to allow von Neumann hoods!
    """
    return spc.get_neighbors(agent, pred=pred, exclude_self=exclude_self,
                             size=size, region_type=region_type)
