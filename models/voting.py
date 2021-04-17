"""
A model to simulate Conway's game of life.
"""

from lib.display_methods import RED, BLUE
from lib.agent import DONT_MOVE
from lib.model import Model, create_agent, NUM_MBRS, NUM_MBRS_PROP
from lib.model import COLOR, MBR_ACTION
from lib.space import get_num_of_neighbors
from registry.registry import get_agent
from lib.agent import X, Y
from lib.utils import Debug

DEBUG = Debug()

MODEL_NAME = "game_of_life"

DEF_NUM_ALIVE = 4
DEF_NUM_DEAD = 4

DEAD = "dead"
ALIVE = "alive"


def is_dead(agent):
    return agent.prim_group == DEAD


def game_of_life_action(biosphere, **kwargs):
    dead_grp = get_agent(DEAD, biosphere.exec_key)
    print("Dead grp is:", repr(dead_grp))


def game_agent_action(agent, **kwargs):
    """
    A simple default agent action.
    """
    if DEBUG.debug:
        print("GofL agent {} is acting".format(agent.name))
    return DONT_MOVE


game_grps = {
    "dead": {
        NUM_MBRS: DEF_NUM_DEAD,
        NUM_MBRS_PROP: "num_blue",
        COLOR: BLUE
    },
    "alive": {
        MBR_ACTION: game_agent_action,
        NUM_MBRS: DEF_NUM_ALIVE,
        NUM_MBRS_PROP: "num_red",
        COLOR: RED
    },
}


def populate_board(patterns, pattern_num):
    agent_locs = patterns[pattern_num]
    grp = game_grps["dead"]
    for loc in agent_locs:
        agent = create_agent(loc[X], loc[Y], game_agent_action)
        grp += create_agent
        get_agent().place_member(agent, xy=loc)


def live_or_die(agent):
    """
    Apply the rules for live agents.
    The agent passed in should be alive, meaning its color should be black.
    """
    num_live_neighbors = get_num_of_neighbors(exclude_self=True, pred=None,
                                              size=1, region_type=None)
    # 2 and 3 should not be hard-coded!
    if (num_live_neighbors != 2 and num_live_neighbors != 3):
        return BLUE
    else:
        return RED


class GameOfLife(Model):
    def run(self):
        if DEBUG.debug:
            print("My groups are:", self.groups)
        return super().run()


def create_model(serial_obj=None, props=None):
    """
    This is for the sake of the API server:
    """
    if serial_obj is not None:
        return GameOfLife(serial_obj=serial_obj)
    else:
        return GameOfLife(MODEL_NAME, grp_struct=game_grps, props=props)


def main():
    model = create_model()
    model.run()
    return 0


if __name__ == "__main__":
    main()
