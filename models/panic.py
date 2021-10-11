"""
A model to simulate the spread of panic in a crowd.
"""
import math

import lib.actions as acts
from lib.agent import DONT_MOVE
from lib.model import Model, MBR_ACTION, NUM_MBRS, COLOR, GRP_ACTION
from lib.utils import Debug

DEBUG = Debug()

MODEL_NAME = "panic"
PANICKED = "panicked"

DEF_DIM = 10
WIDTH = "width"
HEIGHT = "height"
DEF_NUM_PEOPLE = DEF_DIM*DEF_DIM
DEF_NUM_PANIC = 0
DEF_NUM_CALM = int(.7 * DEF_NUM_PEOPLE)
DEF_NUM_PANIC = int(.3 * DEF_NUM_PEOPLE)

AGENT_PREFIX = "Agent"
PANIC_THRESHHOLD = .2
CALM_THRESHHOLD = .7

CALM = "Calm"
PANIC = "Panic"


def agent_action(agent, **kwargs):
    """
    The action determines what state the agent is in.
    If CALM, and lots of panic about, flip to PANIC.
    If PANICKED, but lots of CALM about, flip to CALM.
    """
    mdl = acts.get_model(agent)
    if agent.group_name() == CALM:
        ratio = acts.neighbor_ratio(agent,
                                    lambda agent:
                                    agent.group_name() == PANIC)
        panic_thresh = mdl.get_prop("panic_thresh", PANIC_THRESHHOLD)
        if ratio > panic_thresh:
            if DEBUG.debug:
                print("Changing the agent's group to panic!")
            agent.has_acted = True
            acts.add_switch(agent, CALM, PANIC)
    elif agent.group_name() == PANIC:
        ratio = acts.neighbor_ratio(agent,
                                    lambda agent:
                                    agent.group_name() == CALM)
        calm_thresh = mdl.get_prop("calm_thresh", CALM_THRESHHOLD)
        if ratio > calm_thresh:
            if DEBUG.debug:
                print("Changing the agent's group to calm!")
            agent.has_acted = True
            acts.add_switch(agent, PANIC, CALM)

    return DONT_MOVE


def start_panic(env, **kwargs):
    """
    We will pick a random subset of calm agents.
    Then we will flip those agents to panicked.
    """
    if acts.get_periods(env) == 0:
        calm_grp = acts.get_group(env, CALM)
        switch_to_panic = calm_grp.rand_subset(panic_grps[PANIC][PANICKED])
        for agt_nm in switch_to_panic:
            acts.add_switch1(env, agt_nm, CALM, PANIC)


panic_grps = {
    CALM: {
        GRP_ACTION: None,
        MBR_ACTION: agent_action,
        NUM_MBRS: DEF_NUM_CALM,
        COLOR: acts.GREEN,
        WIDTH: DEF_DIM,
        HEIGHT: DEF_DIM,
    },
    PANIC: {
        GRP_ACTION: None,
        MBR_ACTION: agent_action,
        NUM_MBRS: 0,
        PANICKED: DEF_NUM_PANIC,
        COLOR: acts.RED
    },
}


class Panic(Model):
    """
    Subclass Model to override handle_props().
    """
    def handle_props(self, props):
        super().handle_props(props)
        num_agents = (self.height * self.width)
        ratio_panic = self.props.get("pct_panic") / 100
        self.num_panic = math.floor(ratio_panic * num_agents)
        self.grp_struct[CALM][NUM_MBRS] = int(num_agents)
        self.grp_struct[PANIC][PANICKED] = int(ratio_panic * num_agents)
        self.grp_struct[CALM][WIDTH] = self.width
        self.grp_struct[CALM][HEIGHT] = self.height


def create_model(serial_obj=None, props=None):
    """
    This is for the sake of the API server; main *could* just
    call Panic() directly.
    """
    if serial_obj is not None:
        return Panic(serial_obj=serial_obj)
    else:
        return Panic(MODEL_NAME, grp_struct=panic_grps,
                     env_action=start_panic,
                     props=props, random_placing=False)


def main():
    model = create_model()
    model.run()
    return 0


if __name__ == "__main__":
    main()
