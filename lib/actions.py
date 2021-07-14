
"""
This module is intended to hold the various functions an agent might call
in the course of acting.
"""

import lib.agent as agt
import lib.utils as utl

DEBUG = utl.Debug()


def def_action(agent, **kwargs):
    """
    A simple default agent action.
    """
    if DEBUG.debug_lib:
        print("Agent {} is acting".format(agent.name))
    return agt.DONT_MOVE
