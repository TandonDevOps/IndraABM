"""
Thomas Schelling's famous model of neighborhood 
segregation. This model illustrates how individual 
tendencies regarding neighbours can lead to segregation.
Here, each agent belongs to two groups and aims to recide
in a neighbourhood, where the fraction of friend`s is high.
Whether the agent will move, is based on two 
parameters: 'hood_ratio' and 'tolerance'.
"""
import random

import lib.actions as acts
from lib.agent import DONT_MOVE, MOVE
from lib.display_methods import RED, BLUE
import lib.model as mdl
from lib.utils import Debug

DEBUG = Debug()

MODEL_NAME = "segregation"

NUM_RED = 250
NUM_BLUE = 250

DEF_CITY_DIM = 40

TOLERANCE = "tolerance"
DEVIATION = "deviation"
GRP_INDEX = "grp_index"

DEF_HOOD_SIZE = 1
DEF_TOLERANCE = .5
DEF_SIGMA = .2

MIN_TOL = 0.1
MAX_TOL = 0.9

BLUE_GRP_IDX = 0
RED_GRP_IDX = 1

HOOD_SIZE = 4

NOT_ZERO = .001

BLUE_AGENTS = "Blue agents"
RED_AGENTS = "Red agents"

group_names = [BLUE_AGENTS, RED_AGENTS]

hood_size = None

opp_group = None


def get_tolerance(default_tolerance, sigma):
    """
    `tolerance` measures how *little* of one's own group one will
    tolerate being among.
    """
    tol = random.gauss(default_tolerance, sigma)
    # a low tolerance number here means high tolerance!
    tol = min(tol, MAX_TOL)
    tol = max(tol, MIN_TOL)
    return tol


def env_favorable(hood_ratio, my_tolerance):
    """
    Is the environment to our agent's liking or not??
    """
    return hood_ratio >= my_tolerance


def agent_action(agent, **kwargs):
    """
    This is what agents do each turn of the model.
    """
    # find out the neighborhood size:
    hood_size = acts.get_prop(agent.exec_key, "hood_size", default=4)
    # see what % of agents are in our group in our hood:
    ratio_num = acts.neighbor_ratio(agent,
                                    lambda a: a.group_name() ==
                                    agent.group_name(),
                                    size=hood_size)
    # if we like our neighborhood, stay put:
    if env_favorable(ratio_num, get_tolerance(DEF_TOLERANCE, DEF_SIGMA)):
        return DONT_MOVE
    else:
        # if we don't like our neighborhood, move!
        return MOVE


segregation_grps = {
    "blue_group": {
        mdl.GRP_ACTION: None,
        mdl.MBR_ACTION: agent_action,
        mdl.NUM_MBRS: NUM_BLUE,
        mdl.NUM_MBRS_PROP: "num_blue",
        mdl.COLOR: BLUE
    },
    "red_group": {
        mdl.GRP_ACTION: None,
        mdl.MBR_ACTION: agent_action,
        mdl.NUM_MBRS: NUM_RED,
        mdl.NUM_MBRS_PROP: "num_red",
        mdl.COLOR: RED
    },
}


class Segregation(mdl.Model):
    """
    Thomas Schelling's famous model of neighborhood segregation.
    """
    def handle_props(self, props):
        super().handle_props(props)
        # get area
        area = self.width * self.height
        # get percentage of red and blue
        dens_red = self.get_prop("dens_red")
        dens_blue = self.get_prop("dens_blue")
        # set group members
        segregation_grps["red_group"][mdl.NUM_MBRS] = int(dens_red * area)
        segregation_grps["blue_group"]mdl.[NUM_MBRS] = int(dens_blue * area)


def create_model(serial_obj=None, props=None, create_for_test=False,
                 use_exec_key=None):
    """
    This is for the sake of the API server:
    """
    if serial_obj is not None:
        return Segregation(serial_obj=serial_obj)
    else:
        return Segregation(MODEL_NAME, grp_struct=segregation_grps)


def main():
    model = create_model()
    model.run()
    return 0


if __name__ == "__main__":
    main()
