"""
This model tries to demonstrate how patterns forms in a closed system
"""

from lib.agent import MOVE
from lib.display_methods import RED, BLUE
from lib.model import Model, NUM_MBRS, MBR_ACTION, NUM_MBRS_PROP, COLOR
from lib.space import get_neighbors
from lib.utils import Debug
from registry.registry import save_reg

DEBUG = Debug()

MODEL_NAME = "basic"
DEF_RED_MBRS = 2
DEF_BLUE_MBRS = 2
num_blue = 0
TEST_EXEC_KEy = 0
DEF_STATE = 1
STATE = "agent state"


def env_action(agent, **kwargs):
    """
    Just to see if this works!
    """
    print("The environment does NOT look perilous: you can relax.")


def basic_action(agent, **kwargs):
    """
    We're going to use this agent action to test the new get_neighbors()
    func in space.py.
    """
    if DEBUG.debug:
        print("Agent {} is located at {}".format(agent.name,
                                                 agent.get_pos()))
    neighbors = get_neighbors(agent)
    for neighbor in neighbors:
        print(f"{str(agent)} has neighbor {str(neighbor)}")
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


def create_model(serial_obj=None, props=None, create_for_test=False,
                 use_exec_key=None):
    """
    This is for the sake of the API server.
    """
    if create_for_test:
        """
        This set's up the Basic model for testing.
        Props may be overridden here for testing but
        the conventional api would be the correct way to do that.
        """
        if use_exec_key is None:
            return Basic(MODEL_NAME, grp_struct=basic_grps, props=props,
                         create_for_test=True)
        else:
            return Basic(MODEL_NAME, grp_struct=basic_grps, props=props,
                         create_for_test=True, exec_key=use_exec_key)
    if serial_obj is not None:
        return Basic(serial_obj=serial_obj)
    else:
        return Basic(MODEL_NAME, grp_struct=basic_grps, props=props,
                     env_action=env_action)


def setup_test_model():
    """
    Set's up the basic model at exec_key = 0 for testing purposes.
    :return: None
    """
    basic = create_model(serial_obj=None, props=None, create_for_test=True,
                         use_exec_key=TEST_EXEC_KEy)
    save_reg(basic.exec_key)


def main():
    model = create_model()
    model.run()
    return 0


if __name__ == "__main__":
    main()
