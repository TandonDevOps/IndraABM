
"""
A model for how fires spread through a forest.
"""

from lib.agent import DONT_MOVE
from lib.display_methods import TOMATO, GREEN, RED, SPRINGGREEN, BLACK
from lib.model import Model, MBR_ACTION, NUM_MBRS, COLOR
from lib.agent import prob_state_trans
from lib.space import exists_neighbor
from registry.registry import get_model
from lib.utils import Debug

DEBUG = Debug()

MODEL_NAME = "forest_fire"

DEF_NUM_TREES = 10
DEF_DIM = 30
DEF_DENSITY = .44
DEF_NEW_FIRE = .01
# tree group names
HEALTHY = "Healthy"
NEW_FIRE = "New Fire"
ON_FIRE = "On Fire"
BURNED_OUT = "Burned Out"
NEW_GROWTH = "New Growth"

# state numbers: create as strings for JSON,
# convert to int when we need 'em that way
HE = "0"
NF = "1"
OF = "2"
BO = "3"
NG = "4"

TRANS_TABLE = "trans_table"
state_trans = [
    [1 - DEF_NEW_FIRE, DEF_NEW_FIRE, 0.0, 0.0, 0.0],
    [0.0, 0.0, 1.0, 0.0, 0.0],
    [0.0, 0.0, 0.0, 1.0, 0.0],
    [0.0, 0.0, 0.0, .99, .01],
    [1.0, 0.0, 0.0, 0.0, 0.0],
]

GROUP_MAP = "group_map"

STATE_MAP = {HEALTHY: HE,
             NEW_FIRE: NF,
             ON_FIRE: OF,
             BURNED_OUT: BO,
             NEW_GROWTH: NG}

GROUP_MAP = {HE: HEALTHY,
             NF: NEW_FIRE,
             OF: ON_FIRE,
             BO: BURNED_OUT,
             NG: NEW_GROWTH}


def tree_action(agent, **kwargs):
    """
    A simple default agent action.
    """
    model = get_model(agent.exec_key)
    if model is None:
        print("ERROR: get_model() returned None.")
        return DONT_MOVE
    old_group = agent.group_name()
    if old_group == HEALTHY:
        if exists_neighbor(agent, lambda agent: agent.group_name() == ON_FIRE):
            agent.set_prim_group(NEW_FIRE)

    # if we didn't catch on fire above, do probabilistic transition:
    if old_group == agent.group_name():
        curr_state = STATE_MAP[old_group]
        # we gotta do these str/int shenanigans with state cause
        # JSON only allows strings as dict keys
        agent.set_prim_group(GROUP_MAP[str(prob_state_trans(int(curr_state),
                                                            state_trans))])
        if DEBUG.debug:
            if agent.group_name == NEW_FIRE:
                print("Tree spontaneously catching fire.")

    if old_group != agent.group_name():
        if DEBUG.debug:
            print(f"Add switch from {old_group} to {agent.group_name()}")
        model.add_switch(str(agent),
                         old_group,
                         agent.group_name())
    return DONT_MOVE


ff_grps = {
    HEALTHY: {
        MBR_ACTION: tree_action,
        NUM_MBRS: DEF_NUM_TREES,
        COLOR: GREEN,
    },
    NEW_FIRE: {
        NUM_MBRS: 0,
        COLOR: TOMATO,
    },
    ON_FIRE: {
        NUM_MBRS: 0,
        COLOR: RED,
    },
    BURNED_OUT: {
        NUM_MBRS: 0,
        COLOR: BLACK,
    },
    NEW_GROWTH: {
        NUM_MBRS: 0,
        COLOR: SPRINGGREEN,
    },
}


class ForestFire(Model):
    """
    The forest fire model.
    """
    def handle_props(self, props):
        super().handle_props(props)
        height = self.props.get("grid_height")
        width = self.props.get("grid_width")
        density = self.props.get("density")
        num_agents = int(height * width * density)
        self.grp_struct[HEALTHY]["num_mbrs"] = num_agents


def create_model(serial_obj=None, props=None):
    """
    This is for the sake of the API server:
    """
    if serial_obj is not None:
        return ForestFire(serial_obj=serial_obj)
    else:
        return ForestFire(MODEL_NAME, grp_struct=ff_grps,
                          props=props)


def main():
    model = create_model()
    model.run()
    return 0


if __name__ == "__main__":
    main()
