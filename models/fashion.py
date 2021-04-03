"""
This is the Adam Smith fashion model.
"""

import math
import numpy as np

from lib.display_methods import BLUE, DARKRED, NAVY, RED
from lib.agent import MOVE, DONT_MOVE, NEUTRAL
from lib.model import COLOR, MBR_ACTION, NUM_MBRS, NUM_MBRS_PROP, Model
from lib.utils import Debug
from registry.registry import get_agent

# from registry.registry import get_model
from operator import gt, lt
from lib.space import in_hood
from lib.agent import ratio_to_sin

DEBUG = Debug()

MODEL_NAME = "fashion"
DEF_NUM_TSETTERS = 5
DEF_NUM_FOLLOWERS = 55

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


def env_unfavorable(my_color, my_pref, op1, op2):
    # we're going to add a small value to NEUTRAL so we sit on fence
    # op1 and op2 should be greater than or less than comparisons
    if my_color == RED_SIN:
        return op1(my_pref, (NEUTRAL - TOO_SMALL))
    else:
        return op2(my_pref, (NEUTRAL + TOO_SMALL))


def change_color(agent, society, opp_group):
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
    society.add_switch(
        agent, agent.prim_group_nm(), opp_group[agent.prim_group_nm()]
    )


def common_action(agent, others_red, others_blue, op1, op2, **kwargs):
    """
    Common action for both followers and trend setters
    """
    if DEBUG.debug:
        print("Agent", str(agent), "is acting.")

    others_red.subset(
        in_hood, agent, HOOD_SIZE, name=agent.name, exec_key=agent.exec_key
    )

    num_others_red = len(
        others_red.subset(
            in_hood, agent, HOOD_SIZE, name=agent.name, exec_key=agent.exec_key
        )
    )

    num_others_blue = len(
        others_blue.subset(
            in_hood, agent, HOOD_SIZE, name=agent.name, exec_key=agent.exec_key
        )
    )

    total_others = num_others_red + num_others_blue
    if total_others <= 0:
        return MOVE

    env_color = ratio_to_sin(num_others_red / total_others)

    # Initialize the color preference if not initialized yet
    if agent.get_attr(COLOR_PREF) is None:
        if DEBUG.debug:
            print(
                "Agent",
                str(agent),
                " doesn't have a color preference set yet, creating it now",
            )
        if (
            agent.prim_group_nm() == RED_TSETTERS
            or agent.prim_group_nm() == RED_FOLLOWERS
        ):
            agent.set_attr(COLOR_PREF, new_color_pref(RED_SIN, env_color))
            agent.set_attr(DISPLAY_COLOR, RED_SIN)
        elif (
            agent.prim_group_nm() == BLUE_TSETTERS
            or agent.prim_group_nm() == BLUE_FOLLOWERS
        ):
            agent.set_attr(COLOR_PREF, new_color_pref(BLUE_SIN, env_color))
            agent.set_attr(DISPLAY_COLOR, BLUE_SIN)
    # If already initialized, update the color preference
    else:
        agent.set_attr(
            COLOR_PREF, new_color_pref(agent.get_attr(COLOR_PREF), env_color)
        )

    if env_unfavorable(
        agent.get_attr(DISPLAY_COLOR), agent.get_attr(COLOR_PREF), op1, op2
    ):
        # change_color(agent, get_model(agent.exec_key), opp_group)
        return DONT_MOVE
    else:
        return MOVE


def follower_action(agent, **kwargs):
    """
    Action for followers
    """
    return common_action(
        agent,
        get_agent(RED_TSETTERS, agent.exec_key),
        get_agent(BLUE_TSETTERS, agent.exec_key),
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
        get_agent(RED_FOLLOWERS, agent.exec_key),
        get_agent(BLUE_FOLLOWERS, agent.exec_key),
        lt,
        gt,
        **kwargs
    )


fashion_grps = {
    BLUE_TSETTERS: {
        MBR_ACTION: tsetter_action,
        NUM_MBRS: DEF_NUM_TSETTERS,
        NUM_MBRS_PROP: "num_tsetters",
        COLOR: NAVY,
    },
    RED_TSETTERS: {
        MBR_ACTION: tsetter_action,
        NUM_MBRS: DEF_NUM_TSETTERS,
        NUM_MBRS_PROP: "num_tsetters",
        COLOR: DARKRED,
    },
    BLUE_FOLLOWERS: {
        MBR_ACTION: follower_action,
        NUM_MBRS: DEF_NUM_FOLLOWERS,
        NUM_MBRS_PROP: "num_followers",
        COLOR: BLUE,
    },
    RED_FOLLOWERS: {
        MBR_ACTION: follower_action,
        NUM_MBRS: DEF_NUM_FOLLOWERS,
        NUM_MBRS_PROP: "num_followers",
        COLOR: RED,
    },
}


class Fashion(Model):
    """
    This class should just create a basic model that runs, has
    some agents that move around, and allows us to test if
    the system as a whole is working.
    It turns out that so far, we don't really need to subclass anything!
    """


def create_model(serial_obj=None, props=None):
    """
    This is for the sake of the API server:
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
