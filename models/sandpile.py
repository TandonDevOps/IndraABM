"""
This is a minimal model that inherits from model.py
and just sets up a couple of agents in two groups that
do nothing except move around randomly.
"""

import lib.actions as acts
import lib.model as mdl

Agent = acts.Agent

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

# this dict maps number of grains to a group name:
GRP_MAP = {
    0: GRP0,
    1: GRP1,
    2: GRP2,
    3: GRP3,
    4: GRP4,
}


def drop_sand(env, **kwargs):
    """
    Just to see if this works!
    """
    center_loc = env.get_center()
    center_agent = env.get_agent_at(center_loc[acts.X], center_loc[acts.Y])
    print(f"Going to drop grain on: {center_agent} at {center_loc}")
    add_grain(center_agent)


def add_grain(agent):
    agent[NUM_GRAINS] += 1
    if check_topple(agent):
        topple(agent)
    old_grp = agent.group_name()
    new_group_number = 1 + int(old_grp[0])
    if new_group_number == 4:
        new_group_number = 0
    new_grp = GRP_MAP[new_group_number]
    acts.add_switch(agent, old_group=old_grp, new_group=new_grp)


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
        print(f"I am toppling! {agent[NUM_GRAINS]}")
        return True
    else:
        print(f"I am not toppling! {agent[NUM_GRAINS]}")
        return False


def create_cell(name, i, props=None, action=None, exec_key=0):
    print("Creating agent")
    return Agent(MODEL_NAME + str(i),
                 action=action,
                 exec_key=exec_key,
                 attrs={NUM_GRAINS: 0, })


sand_grps = {
    GRP0: {
        mdl.MBR_CREATOR: create_cell,
        mdl.MBR_ACTION: None,
        mdl.NUM_MBRS: 0,
        mdl.COLOR: acts.BLUE,
    },
    GRP1: {
        mdl.MBR_ACTION: None,
        mdl.NUM_MBRS: 0,
        mdl.COLOR: acts.YELLOW,
    },
    GRP2: {
        mdl.MBR_ACTION: None,
        mdl.NUM_MBRS: 0,
        mdl.COLOR: acts.BLACK,
    },
    GRP3: {
        mdl.MBR_ACTION: None,
        mdl.NUM_MBRS: 0,
        mdl.COLOR: acts.GREEN,
    },
    GRP4: {
        mdl.MBR_ACTION: None,
        mdl.NUM_MBRS: 0,
        mdl.COLOR: acts.RED,
    },
}


class Sandpile(mdl.Model):
    """
    The Sandpile class.
    It turns out that so far, we don't really need to subclass anything!
    """
    def handle_props(self, props):
        super().handle_props(props)
        num_cells = (self.height * self.width)
        self.grp_struct[GRP0][mdl.NUM_MBRS] = num_cells


def create_model(serial_obj=None, props=None, create_for_test=False,
                 exec_key=None):
    """
    This is for the sake of the API server.
    """
    if serial_obj is not None:
        return Sandpile(serial_obj=serial_obj)
    else:
        return Sandpile(MODEL_NAME,
                        grp_struct=sand_grps,
                        props=props,
                        env_action=drop_sand,
                        random_placing=False,
                        create_for_test=create_for_test,
                        exec_key=exec_key)


def main():
    model = create_model()
    model.run()
    return 0


if __name__ == "__main__":
    main()
