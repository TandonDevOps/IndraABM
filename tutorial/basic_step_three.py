"""
This is a minimal model that inherits from model.py
and just sets up a couple of agents in two groups that
do nothing except move around randomly.
"""
import random

import lib.actions as acts
import lib.model as mdl

MODEL_NAME = "segregation"

# default and fallback values
NUM_RED = 250
NUM_BLUE = 250

DEF_TOLERANCE = .5
DEF_SIGMA = .2

MIN_TOL = 0.1
MAX_TOL = 0.9

DEF_WIDTH = 10
DEF_HEIGHT = 10
DEF_DENSITY_RED = 0.33
DEF_DENSITY_BLUE = 0.33


def env_action(agent, **kwargs):
    """
    Just to see if this works!
    """
    print("The environment does NOT look perilous: you can relax.")


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
        return acts.DONT_MOVE
    else:
        # if we don't like our neighborhood, move!
        return acts.MOVE


segregation_grps = {
    "blue_group": {
        mdl.MBR_ACTION: agent_action,
        mdl.NUM_MBRS: NUM_BLUE,
        mdl.NUM_MBRS_PROP: "num_blue",
        mdl.COLOR: acts.BLUE
    },
    "red_group": {
        mdl.MBR_ACTION: agent_action,
        mdl.NUM_MBRS: NUM_RED,
        mdl.NUM_MBRS_PROP: "num_red",
        mdl.COLOR: acts.RED
    },
}


class Segregation(mdl.Model):
    """
    Thomas Schelling's famous model of neighborhood segregation.
    """

    def handle_props(self, props):
        super().handle_props(props)
        # get area
        area = DEF_WIDTH * DEF_HEIGHT
        # get percentage of red and blue
        dens_red = DEF_DENSITY_RED
        dens_blue = DEF_DENSITY_BLUE
        # set group members
        segregation_grps["red_group"][mdl.NUM_MBRS] = int(dens_red * area)
        segregation_grps["blue_group"][mdl.NUM_MBRS] = int(dens_blue * area)


def create_model(serial_obj=None, props=None, create_for_test=False,
                 exec_key=None):
    """
    This is for the sake of the API server.
    """
    if serial_obj is not None:
        return Segregation(serial_obj=serial_obj)
    else:
        return Segregation(MODEL_NAME,
                           grp_struct=segregation_grps,
                           props=props,
                           env_action=env_action,
                           create_for_test=create_for_test,
                           exec_key=exec_key)


def main():
    model = create_model()
    model.run()
    return 0


if __name__ == "__main__":
    main()
