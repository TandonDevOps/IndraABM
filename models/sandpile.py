"""
This is a minimal model that inherits from model.py
and just sets up a couple of agents in two groups that
do nothing except move around randomly.
"""

# remove if it turns out it's not needed:
import lib.actions as acts
import lib.display_methods as disp
import lib.agent as agt
import lib.model as mdl

from lib.agent import X, Y
from lib.utils import Debug
from registry.registry import save_reg

DEBUG = Debug()

MODEL_NAME = "sandpile"
NUM_GRAINS = "# grains"

DEF_RED_MBRS = 2
DEF_BLUE_MBRS = 2
num_blue = 0
TEST_EXEC_KEY = 0

GRP0 = "0 group"
GRP1 = "1 group"
GRP2 = "2 group"
GRP3 = "3 group"
GRP4 = "4 group"

MAX_GRAINS = 4


def drop_sand(env, **kwargs):
    """
    Just to see if this works!
    """
    center_loc = env.get_center()
    center_agent = env.get_agent_at(center_loc[X], center_loc[Y])
    print(f"Going to drop grain on: {center_agent} at {center_loc}")
    add_grain(center_agent)


def add_grain(agent):
    agent[NUM_GRAINS] += 1
    if check_topple(agent):
        topple(agent)
    """
    old_member = agent.group_name()
    new_member = old_group
    if old_member == GRP4:
        acts.add_switch(agent, old_member, new_member)
        """


def topple(agent):
    agent[NUM_GRAINS] = 0
    print("Calling add_grain() on neighbors.")
    # get von neumann hood and add grain to those neighbors.
    agent.neighbors = acts.get_neighbors(agent, region_type=acts.spc.VON_N)
    print(agent.neighbors)
    for neighbor in agent.neighbors:
        print("the loop is reading")
        add_grain(agent.neighbors[neighbor])


def check_topple(agent):
    """
    We're going to use this agent action to test the new get_neighbors()
    func in space.py.
    """
    if agent[NUM_GRAINS] >= MAX_GRAINS:
        print(f"I am toppling! {agent[NUM_GRAINS]=}")
        return True
    else:
        print(f"I am not toppling! {agent[NUM_GRAINS]=}")
        return False


def create_cell(name, i, props=None, action=None, exec_key=0):
    return agt.Agent(MODEL_NAME + str(i),
                     action=action,
                     exec_key=exec_key,
                     attrs={NUM_GRAINS: 0, })


sand_grps = {
    GRP0: {
        mdl.MBR_CREATOR: create_cell,
        mdl.MBR_ACTION: None,
        mdl.NUM_MBRS: 25,  # this is cheating!
        mdl.COLOR: disp.BLUE,
    },
    GRP1: {
        mdl.MBR_ACTION: None,
        mdl.NUM_MBRS: 0,
        mdl.COLOR: disp.RED,
    },
    GRP2: {
        mdl.MBR_ACTION: None,
        mdl.NUM_MBRS: 0,
        mdl.COLOR: disp.GREEN,
    },
    GRP3: {
        mdl.MBR_ACTION: None,
        mdl.NUM_MBRS: 0,
        mdl.COLOR: disp.PURPLE,
    },
    GRP4: {
        mdl.MBR_ACTION: None,
        mdl.NUM_MBRS: 0,
        mdl.COLOR: disp.YELLOW,
    },
}


class Sandpile(mdl.Model):
    """
    The Sandpile class.
    It turns out that so far, we don't really need to subclass anything!
    """


def create_model(serial_obj=None, props=None, create_for_test=False,
                 use_exec_key=None):
    """
    This is for the sake of the API server.
    """
    if serial_obj is not None:
        return Sandpile(serial_obj=serial_obj)
    else:
        return Sandpile(MODEL_NAME, grp_struct=sand_grps, props=props,
                        env_action=drop_sand,
                        random_placing=False,
                        create_for_test=create_for_test)


def setup_test_model():
    """
    Sets up the sandpile model at exec_key = 0 for testing purposes.
    :return: None
    """
    sp = create_model(serial_obj=None, props=None, create_for_test=True,
                      use_exec_key=TEST_EXEC_KEY)
    save_reg(sp.exec_key)


def main():
    model = create_model()
    model.run()
    return 0


if __name__ == "__main__":
    main()