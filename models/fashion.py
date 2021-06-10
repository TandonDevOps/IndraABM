"""
This is the Adam Smith fashion model.
"""

import math
import numpy as np

from lib.display_methods import BLUE, DARKRED, NAVY, RED
from lib.agent import MOVE, NEUTRAL, Agent
import lib.model as mdl
from lib.utils import Debug
from registry.registry import get_group
from registry.registry import get_model
from operator import gt, lt
from lib.space import in_hood
from lib.agent import ratio_to_sin

DEBUG = Debug()

MODEL_NAME = "fashion"
DEF_NUM_TSETTERS = 5
DEF_NUM_FOLLOWERS = 55

FOLLOWER_PRENM = "follower"
TSETTER_PRENM = "tsetter"

HOOD_SIZE = 4

ENV_WEIGHT = 0.6
weightings = [1.0, ENV_WEIGHT]


BLUE_SIN = 0.0
RED_SIN = 1.0

COLOR_PREF = "color_pref"
DISPLAY_COLOR = "display_color"

TOO_SMALL = 0.01
BIG_ENOUGH = 0.03

RED_FOLLOWERS = "Red Followers"
BLUE_FOLLOWERS = "Blue Followers"
RED_TSETTERS = "Red Trendsetters"
BLUE_TSETTERS = "Blue Trendsetters"

OPP_GROUP = "opp_group"

opp_group = {
    RED_TSETTERS: BLUE_TSETTERS,
    BLUE_TSETTERS: RED_TSETTERS,
    RED_FOLLOWERS: BLUE_FOLLOWERS,
    BLUE_FOLLOWERS: RED_FOLLOWERS,
}


def new_color_pref(old_pref, env_color):
    """
    Calculate new color pref with the formula below:
    new_color = sin(avg(asin(old_pref) + asin(env_color)))
    """
    me = math.asin(old_pref)
    env = math.asin(env_color)
    avg = np.average([me, env], weights=weightings)
    new_color = math.sin(avg)
    return new_color


def dont_like_things(my_color, my_pref, op1, op2):
    # we're going to add a small value to NEUTRAL so we sit on fence
    # op1 and op2 should be greater than or less than comparisons
    if my_color == RED_SIN:
        return op1(my_pref, (NEUTRAL - TOO_SMALL))
    else:
        return op2(my_pref, (NEUTRAL + TOO_SMALL))


def change_color(agent, opp_group):
    """
    change agent's DISPLAY_COLOR to its opposite color
    """
    if DEBUG.debug:
        print(
            "Agent ",
            agent.name,
            " is changing colors; its prim group is ",
            agent.prim_group_nm(),
        )

    agent.set_attr(DISPLAY_COLOR, not agent.get_attr(DISPLAY_COLOR))
    get_model(agent.exec_key).add_switch(str(agent), agent.prim_group_nm(),
                                         opp_group[agent.prim_group_nm()])


def common_action(agent, others_red, others_blue, op1, op2, **kwargs):
    """
    Common action for both followers and trend setters, different only based on
    what op1 and op2 are.
    """
    num_others_red = len(others_red.subset(in_hood, agent, HOOD_SIZE))
    num_others_blue = len(others_blue.subset(in_hood, agent, HOOD_SIZE))
    total_others = num_others_red + num_others_blue
    if total_others > 0:
        env_color = ratio_to_sin(num_others_red / total_others)

        agent[COLOR_PREF] = new_color_pref(agent[COLOR_PREF], env_color)
        if dont_like_things(agent[DISPLAY_COLOR], agent[COLOR_PREF], op1, op2):
            change_color(agent, opp_group)
    return MOVE  # the fashion agents always keep moving!


def follower_action(agent, **kwargs):
    """
    Action for followers
    """
    return common_action(
        agent,
        get_group(RED_TSETTERS, agent.exec_key),
        get_group(BLUE_TSETTERS, agent.exec_key),
        lt,
        gt,
        **kwargs
    )


def tsetter_action(agent, **kwargs):
    """
    Action for trend setters
    """
    return common_action(
        agent,
        get_group(RED_FOLLOWERS, agent.exec_key),
        get_group(BLUE_FOLLOWERS, agent.exec_key),
        gt,
        lt,
        **kwargs)


def create_tsetter(name, i, props=None, color=RED_SIN, action=None,
                   exec_key=0):
    """
    Create a trendsetter: all RED to start.
    """
    return Agent(TSETTER_PRENM + str(i),
                 action=action,
                 exec_key=exec_key,
                 attrs={COLOR_PREF: color,
                        DISPLAY_COLOR: color})


def create_follower(name, i, props=None, color=BLUE_SIN, action=None,
                    exec_key=0):
    """
    Create a follower: all BLUE to start.
    """
    return Agent(FOLLOWER_PRENM + str(i),
                 action=action,
                 exec_key=exec_key,
                 attrs={COLOR_PREF: color,
                        DISPLAY_COLOR: color})


fashion_grps = {
    BLUE_TSETTERS: {
        mdl.MBR_CREATOR: create_tsetter,
        mdl.MBR_ACTION: tsetter_action,
        mdl.NUM_MBRS: 0,
        mdl.COLOR: NAVY,
    },
    RED_TSETTERS: {
        mdl.MBR_CREATOR: create_tsetter,
        mdl.MBR_ACTION: tsetter_action,
        mdl.NUM_MBRS: DEF_NUM_TSETTERS,
        mdl.NUM_MBRS_PROP: "num_tsetters",
        mdl.COLOR: DARKRED,
    },
    BLUE_FOLLOWERS: {
        mdl.MBR_CREATOR: create_follower,
        mdl.MBR_ACTION: follower_action,
        mdl.NUM_MBRS: DEF_NUM_FOLLOWERS,
        mdl.NUM_MBRS_PROP: "num_followers",
        mdl.COLOR: BLUE,
    },
    RED_FOLLOWERS: {
        mdl.MBR_CREATOR: create_follower,
        mdl.MBR_ACTION: follower_action,
        mdl.NUM_MBRS: 0,
        mdl.COLOR: RED,
    },
}


class Fashion(mdl.Model):
    """
    Perhaps the fashion model does not need to override anything from Model?
    """


def create_model(serial_obj=None, props=None):
    """
    This `if` is for the sake of the API server:
    """
    if serial_obj is not None:
        return Fashion(serial_obj=serial_obj)
    else:
        return Fashion(MODEL_NAME, grp_struct=fashion_grps, props=props)


def main():
    model = create_model()
    model.run()
    return 0


if __name__ == "__main__":
    main()
