"""
A model to simulate voting distribution
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

MODEL_NAME = "voting"

DEF_NUM_BLUE = 4
DEF_NUM_RED = 4

NUM_NEIGHBORS = 8   #number of surrounding voters

BLUE_VOTE = "blue_voter"
RED_VOTE = "red_voter"


def voting_blue(agent):
    return agent.prim_group == BLUE_VOTER


def voting_action(biosphere, **kwargs):
    blue_grp = get_agent(BLUE_VOTE, biosphere.exec_key)
    print("Blue group is:", repr(blue_grp))


def game_agent_action(agent, **kwargs):
    """
    A simple default agent action.
    """
    if DEBUG.debug:
        print("GofL agent {} is acting".format(agent.name))
    return DONT_MOVE


game_grps = {
    "blue_voter": {
        NUM_MBRS: DEF_NUM_BLUE,
        NUM_MBRS_PROP: "num_blue",
        COLOR: BLUE
    },
    "red_voter": {
        MBR_ACTION: game_agent_action,
        NUM_MBRS: DEF_NUM_RED,
        NUM_MBRS_PROP: "num_red",
        COLOR: RED
    },
}


def populate_board(patterns, pattern_num):
    agent_locs = patterns[pattern_num]
    grp = game_grps["blue_voter"]
    for loc in agent_locs:
        agent = create_agent(loc[X], loc[Y], game_agent_action)
        grp += create_agent
        get_agent().place_member(agent, xy=loc)


def vote_or_change(agent):
    """
    Apply the rules for agents.
    The agent passed in will either keep their vote the same, or change it,
    based on how its neighbors are voting.
    """
    num_red_neighbors = get_num_of_neighbors(exclude_self=True, pred=None,
                                              size=1, region_type=None)
    if (num_red_neighbors >= NUM_NEIGHBORS / 2):
        return BLUE
    else:
        return RED


class Voting(Model):
    def run(self):
        if DEBUG.debug:
            print("My groups are:", self.groups)
        return super().run()


def create_model(serial_obj=None, props=None):
    """
    This is for the sake of the API server:
    """
    if serial_obj is not None:
        return Voting(serial_obj=serial_obj)
    else:
        return Voting(MODEL_NAME, grp_struct=game_grps, props=props)


def main():
    model = create_model()
    model.run()
    return 0


if __name__ == "__main__":
    main()
