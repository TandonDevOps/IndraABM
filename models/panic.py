"""
A model to simulate the spread of panic in a crowd.
"""
import math
from lib.agent import DONT_MOVE
from lib.space import neighbor_ratio
from lib.display_methods import RED, GREEN
from lib.model import Model, MBR_ACTION, NUM_MBRS, COLOR, GRP_ACTION
from registry.registry import get_model, get_agent
import random as rand
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
THRESHHOLD = .2

CALM = "Calm"
PANIC = "Panic"
first_period = True


def agent_action(agent, **kwargs):
    """
    This is what agents do each turn of the model.
    """
    if DEBUG.debug:
        print("The agent is called", agent)
    global first_period
    if first_period:
        start_panic(agent.exec_key)
    first_period = False
    if agent.group_name() == CALM:
        ratio = neighbor_ratio(agent,
                               lambda agent: agent.group_name() == PANIC)
        if ratio > THRESHHOLD:
            if DEBUG.debug:
                print("Changing the agent's group to panic!")
            agent.has_acted = True
            get_model(agent.exec_key).add_switch(str(agent), CALM, PANIC)
    return DONT_MOVE


def start_panic(exec_key):
    maxPosn = panic_grps[CALM][WIDTH] * panic_grps[CALM][HEIGHT]
    num_panic = panic_grps[PANIC][PANICKED]
    for i in range(0, num_panic):
        agent_posn = rand.randint(0, maxPosn)
        agent_name = "Calm" + str(agent_posn)
        agent = get_agent(agent_name, exec_key)
        if agent is not None and agent.group_name() == CALM:
            get_model(exec_key).add_switch(agent_name, CALM, PANIC)


panic_grps = {
    CALM: {
        GRP_ACTION: None,
        MBR_ACTION: agent_action,
        NUM_MBRS: DEF_NUM_CALM,
        COLOR: GREEN,
        WIDTH: DEF_DIM,
        HEIGHT: DEF_DIM,
    },
    PANIC: {
        GRP_ACTION: None,
        MBR_ACTION: agent_action,
        NUM_MBRS: 0,
        PANICKED: DEF_NUM_PANIC,
        COLOR: RED
    },
}


class Panic(Model):
    def handle_props(self, props):
        super().handle_props(props)
        grid_height = self.props.get("grid_height")
        grid_width = self.props.get("grid_width")
        num_agents = (grid_height * grid_width)
        if DEBUG.debug:
            print("The grid dimencions are", grid_height * grid_width)
            print("The number of agents is", num_agents)
        ratio_panic = self.props.get("pct_panic") / 100
        self.num_panic = math.floor(ratio_panic * num_agents)
        self.grp_struct[CALM][NUM_MBRS] = int(num_agents)
        self.grp_struct[PANIC][PANICKED] = int(ratio_panic * num_agents)
        self.grp_struct[CALM][WIDTH] = grid_width
        self.grp_struct[CALM][HEIGHT] = grid_height


def create_model(serial_obj=None, props=None):
    """
    This is for the sake of the API server:
    """
    if serial_obj is not None:
        return Panic(serial_obj=serial_obj)
    else:
        return Panic(MODEL_NAME, grp_struct=panic_grps,
                     props=props, random_placing=False)


def main():
    model = create_model()
    model.run()
    return 0


if __name__ == "__main__":
    main()
