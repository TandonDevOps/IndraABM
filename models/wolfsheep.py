from lib.agent import MOVE, DONT_MOVE, Agent
from lib.display_methods import TAN, GRAY
from lib.model import Model, NUM_MBRS, MBR_ACTION, NUM_MBRS_PROP, COLOR
from lib.model import MBR_CREATOR
from lib.utils import Debug
from lib.space import get_num_of_neighbors, get_neighbor
from registry.registry import get_model

DEBUG = Debug()

MODEL_NAME = "wolfsheep"

NUM_WOLVES = 8
NUM_SHEEP = 28
PREY_DIST = 3
TOO_CROWDED = 6
CROWDING_EFFECT = 1
MAX_ENERGY = 3
MEADOW_HEIGHT = 10
MEADOW_WIDTH = 10

WOLF_LIFESPAN = 5
WOLF_REPRO_PERIOD = 2

SHEEP_LIFESPAN = 8
SHEEP_REPRO_PERIOD = 2

TIME_TO_REPRODUCE = "time_to_repr"
DEF_TIME_TO_REPRO = 10

WOLF_GRP_NM = "wolf"
SHEEP_GRP_NM = "sheep"


def is_agent_dead(agent, **kwargs):
    # Die if the agent runs out of duration
    if agent.duration <= 0:
        agent.die()
        return True


def reproduce(agent, **kwargs):
    # Check if it is time to produce
    if agent.get_attr(TIME_TO_REPRODUCE) == 0:
        if DEBUG.debug:
            print(str(agent.name) + " is having a baby!")

        # Create babies: need group name here!
        get_model(agent.exec_key).add_child(agent.prim_group_nm())

        # Reset ttr
        agent.set_attr(TIME_TO_REPRODUCE, DEF_TIME_TO_REPRO)


def eat_sheep(agent, **kwargs):
    prey = get_neighbor(agent=agent, size=3)

    if prey is not None:
        if DEBUG.debug:
            print(str(agent) + " is eating " + str(prey))

        agent.duration += min(prey.duration, MAX_ENERGY)
        prey.die()

    else:
        agent.duration /= 2


def handle_ttr(agent, **kwargs):
    # Initialize the attribute
    if agent.get_attr(TIME_TO_REPRODUCE) is None:
        agent.set_attr(TIME_TO_REPRODUCE, DEF_TIME_TO_REPRO)

    # Decrease ttr
    agent.set_attr(TIME_TO_REPRODUCE, agent.get_attr(TIME_TO_REPRODUCE) - 1)


def sheep_action(agent, **kwargs):

    if is_agent_dead(agent):
        return DONT_MOVE

    # Handle time to reproduce attribute
    handle_ttr(agent)

    # Check neighbor count
    if get_num_of_neighbors(agent, size=10) > TOO_CROWDED:
        agent.duration -= CROWDING_EFFECT

    # Reproduce if it is the right time
    reproduce(agent)

    return MOVE


def wolf_action(agent, **kwargs):

    # Make wolf eat nearby sheep
    eat_sheep(agent)

    # Die if the agent runs out of duration
    if is_agent_dead(agent):
        return DONT_MOVE

    # Handle time to reproduce attribute
    handle_ttr(agent)

    # Reproduce if it is the right time
    reproduce(agent)

    return MOVE


def create_sheep(name, i, action=sheep_action, **kwargs):
    """
    Create a new sheep.
    """
    return Agent(name + str(i), action=action, **kwargs)


def create_wolf(name, i, action=wolf_action, **kwargs):
    """
    Create a new sheep.
    """
    return Agent(name + str(i), action=action, **kwargs)


wolfsheep_grps = {
    SHEEP_GRP_NM: {
        MBR_CREATOR: create_sheep,
        MBR_ACTION: sheep_action,
        NUM_MBRS: NUM_SHEEP,
        NUM_MBRS_PROP: "num_sheep",
        COLOR: GRAY,
    },
    WOLF_GRP_NM: {
        MBR_CREATOR: create_wolf,
        MBR_ACTION: wolf_action,
        NUM_MBRS: NUM_WOLVES,
        NUM_MBRS_PROP: "num_wolves",
        COLOR: TAN,
    },
}


class WolfSheep(Model):
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
        return WolfSheep(serial_obj=serial_obj)
    else:
        return WolfSheep(MODEL_NAME, grp_struct=wolfsheep_grps, props=props)


def main():
    model = create_model()
    model.run()

    return 0


if __name__ == "__main__":
    main()
