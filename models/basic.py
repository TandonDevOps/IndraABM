"""
This is a minimal model that inherits from model.py
and just sets up a couple of agents in two groups that
do nothing except move around randomly.
"""

from lib.agent import MOVE
from lib.display_methods import RED, BLUE
from lib.model import Model, NUM_MBRS, MBR_ACTION, NUM_MBRS_PROP, COLOR
from lib.utils import Debug

DEBUG = Debug()

MODEL_NAME = "basic"
DEF_RED_MBRS = 2
DEF_BLUE_MBRS = 2
num_blue = 0


def basic_action(agent, **kwargs):
    """
    A simple default agent action.
    """
    if DEBUG.debug:
        print("Agent {} is located at {}".format(agent.name,
                                                 agent.get_pos()))
    return MOVE


basic_grps = {
    "blue_grp": {
        MBR_ACTION: basic_action,
        NUM_MBRS: DEF_BLUE_MBRS,
        NUM_MBRS_PROP: "num_blue",
        COLOR: BLUE
    },
    "red_grp": {
        MBR_ACTION: basic_action,
        NUM_MBRS: DEF_RED_MBRS,
        NUM_MBRS_PROP: "num_red",
        COLOR: RED
    },
}


class Basic(Model):
    """
    This class should just create a basic model that runs, has
    some agents that move around, and allows us to test if
    the system as a whole is working.
    It turns out that so far, we don't really need to subclass anything!
    """


def create_model_for_test(props=None):
    """
    This set's up the Basic model at exec_key 0 for testing.
    This method is to be called from registry only. Props may be
    overridden here for testing but the conventional api would be the correct
    way to do that.
    :param props: None
    :return: Basic
    """
    return Basic(MODEL_NAME, grp_struct=basic_grps, props=props,
                 create_for_test=True)


def create_model(serial_obj=None, props=None):
    """
    This is for the sake of the API server:
    """
    if serial_obj is not None:
        return Basic(serial_obj=serial_obj)
    else:
        return Basic(MODEL_NAME, grp_struct=basic_grps, props=props)


def main():
    model = create_model()
    model.run()

    return 0


if __name__ == "__main__":
    main()
