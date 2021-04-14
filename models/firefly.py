"""
This model illustrates the spontaneous synronization of large crowds without a
central central clock or synronization tool. In this model, the agents
(fireflies) start chaning color (blinkin) at random frequencies. However, at
each simulation run, the agents increase or decrease the frequencies based on
the average ofneighborung agents' blinkin frequencies. After a certain number
of simulation runs, we see that all of the agents are blinking at the pretty
much same frequency.

A related video that explains this phenomena:
https://www.youtube.com/watch?v=t-_VPRCtiUg

Another good website to understand this model:
https://1000fireflies.net/about
"""

from lib.agent import MOVE
from lib.display_methods import LIMEGREEN
from lib.model import Model, NUM_MBRS, MBR_ACTION, NUM_MBRS_PROP, COLOR
from lib.utils import Debug
from registry.registry import save_reg, TEST_EXEC_KEY

DEBUG = Debug()

MODEL_NAME = "firefly"
DEF_FIREFLY_MBRS = 2
DEF_FIREFLY_GROUP_NAME = "Firefly"
DEF_NUM_MBRS_PROP = "num_firefly"
num_firefly = 0


def firefly_action(agent, **kwargs):
    """
    A simple default agent action.
    """
    if DEBUG.debug:
        print("Agent {} is located at {}".format(agent.name, agent.get_pos()))
    return MOVE


firefly_grps = {
    DEF_FIREFLY_GROUP_NAME: {
        MBR_ACTION: firefly_action,
        NUM_MBRS: DEF_FIREFLY_MBRS,
        NUM_MBRS_PROP: DEF_NUM_MBRS_PROP,
        COLOR: LIMEGREEN,
    },
}


class Firefly(Model):
    """
    This class should just create a Firefly model that runs, has
    some agents that move around, and allows us to test if
    the system as a whole is working.
    It turns out that so far, we don't really need to subclass anything!
    """


def create_model_for_test(props=None):
    """
    This set's up the Firefly model at exec_key 0 for testing.
    This method is to be called from registry only. Props may be
    overridden here for testing but the conventional api would be the correct
    way to do that.
    :param props: None
    :return: Firefly
    """
    return Firefly(
        MODEL_NAME, grp_struct=firefly_grps, props=props, create_for_test=True
    )


def create_model(serial_obj=None, props=None):
    """
    This is for the sake of the API server:
    """
    if serial_obj is not None:
        return Firefly(serial_obj=serial_obj)
    else:
        return Firefly(MODEL_NAME, grp_struct=firefly_grps, props=props)


def setup_test_model():
    """
    Set's up the Firefly model at exec_key = 0 for testing purposes.
    :return: None
    """
    create_model_for_test(props=None)
    save_reg(TEST_EXEC_KEY)


def main():
    model = create_model()
    model.run()
    return 0


if __name__ == "__main__":
    main()
