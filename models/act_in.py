"""
This model tries to demonstrate how patterns forms in a closed system
"""

import lib.actions as acts
from lib.agent import Agent
from lib.display_methods import RED, BLUE
from lib.model import Model, NUM_MBRS, MBR_ACTION, NUM_MBRS_PROP, COLOR
from lib.utils import Debug
from registry.registry import save_reg

DEBUG = Debug()

MODEL_NAME = "act_in"
DEF_INACTIVE_MBRS = 2
DEF_ACTIVE_MBRS = 2


def act_in_action(agent, **kwargs):
    """
    We're going to use this agent action to test the new get_neighbors()
    func in space.py.
    """
    if DEBUG.debug:
        print("Agent {} is located at {}".format(agent.name,
                                                 agent.get_pos()))
    for neighbor in acts.get_neighbors(agent):
        print(f"{str(agent)} has neighbor {str(neighbor)}")
    return acts.DONT_MOVE


def create_agent(name, i, exec_key=None, action=act_in_action):
    """
    Create a agent
    """
    return Agent(name + str(i),
                 action=action, exec_key=exec_key)


act_in_grps = {
    "active": {
        MBR_ACTION: act_in_action,
        NUM_MBRS: DEF_ACTIVE_MBRS,
        NUM_MBRS_PROP: "num_active",
        COLOR: BLUE
    },
    "inactive": {
        MBR_ACTION: act_in_action,
        NUM_MBRS: DEF_INACTIVE_MBRS,
        NUM_MBRS_PROP: "num_inactive",
        COLOR: RED
    },
}


class ActIn(Model):
    """
    Activation-inhibition model.
    """


def create_model(serial_obj=None, props=None, create_for_test=False,
                 exec_key=None):
    """
    This is for the sake of the API server.
    """
    if serial_obj is not None:
        return ActIn(serial_obj=serial_obj)
    else:
        return ActIn(MODEL_NAME, grp_struct=act_in_grps, props=props,
                     create_for_test=create_for_test)


def main():
    model = create_model()
    model.run()
    return 0


if __name__ == "__main__":
    main()
