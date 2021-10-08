import lib.actions as acts

from lib.agent import Agent
from lib.display_methods import TAN, GRAY
from lib.model import Model, MBR_ACTION, NUM_MBRS_PROP, COLOR
from lib.model import MBR_CREATOR
from lib.utils import Debug
from lib.space import get_num_of_neighbors, get_neighbor
from registry.registry import get_model

DEBUG = Debug()

MODEL_NAME = "wolfsheep"
TIME_TO_REPRODUCE = "time_to_repr"
WOLF_GRP_NM = "wolf"
SHEEP_GRP_NM = "sheep"

# Constants for the model
TOO_CROWDED = 6
CROWDING_EFFECT = 1
MAX_ENERGY = 3

# Can be changed by user
DEFAULT_TIME_TO_REPRO = 5
WOLF_TIME_TO_REPRO = 4
SHEEP_TIME_TO_REPRO = 7
PREY_DIST = 8


def is_agent_dead(agent, **kwargs):
    # Die if the agent runs out of duration
    if agent.duration <= 0:
        agent.die()
        return True


def reproduce(agent, reproduction_period, **kwargs):
    # Check if it is time to produce
    if agent.get_attr(TIME_TO_REPRODUCE) == 0:
        if DEBUG.debug:
            print(str(agent.name) + " is having a baby!")

        # Create babies: need group name here!
        acts.get_model(agent).add_child(agent.prim_group_nm())

        # Reset ttr
        agent.set_attr(TIME_TO_REPRODUCE, reproduction_period)


def eat_sheep(agent, **kwargs):
    prey = get_neighbor(agent=agent, size=PREY_DIST)

    if prey is not None:
        if DEBUG.debug:
            print(str(agent) + " is eating " + str(prey))

        agent.duration += min(prey.duration, MAX_ENERGY)
        prey.die()

    else:
        agent.duration /= 2


def handle_ttr(agent, **kwargs):
    """
    This function adjusts the time to reproduce for a wolf or a sheep.
    An individual gets this parameter from its species.
    """
    if agent.get_attr(TIME_TO_REPRODUCE) is None:
        if agent.prim_group_nm() == WOLF_GRP_NM:
            agent.set_attr(TIME_TO_REPRODUCE, WOLF_TIME_TO_REPRO)
        elif agent.prim_group_nm() == SHEEP_GRP_NM:
            agent.set_attr(TIME_TO_REPRODUCE, SHEEP_TIME_TO_REPRO)
        else:
            agent.set_attr(TIME_TO_REPRODUCE, DEFAULT_TIME_TO_REPRO)
    # Decrease ttr
    agent.set_attr(TIME_TO_REPRODUCE, agent.get_attr(TIME_TO_REPRODUCE) - 1)


def sheep_action(agent, **kwargs):
    """
    This is what a sheep does every period.
    """
    if is_agent_dead(agent):
        return acts.DONT_MOVE
    handle_ttr(agent)
    if get_num_of_neighbors(agent, size=10) > TOO_CROWDED:
        agent.duration -= CROWDING_EFFECT
    # Reproduce if it is the right time
    reproduce(agent, SHEEP_TIME_TO_REPRO)
    return acts.MOVE


def wolf_action(agent, **kwargs):
    if is_agent_dead(agent):
        return acts.DONT_MOVE
    eat_sheep(agent)
    # Handle time to reproduce attribute
    handle_ttr(agent)
    # Check neighbor count
    if get_num_of_neighbors(agent, size=10) > TOO_CROWDED:
        agent.duration -= CROWDING_EFFECT
    # Reproduce if it is the right time
    reproduce(agent, WOLF_TIME_TO_REPRO)
    return acts.MOVE


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
        NUM_MBRS_PROP: "num_sheep",
        COLOR: GRAY,
    },
    WOLF_GRP_NM: {
        MBR_CREATOR: create_wolf,
        MBR_ACTION: wolf_action,
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

    def handle_props(self, props):
        super().handle_props(props)
        prey_dist = self.props.get("prey_dist")
        wolf_time_to_repro = self.props.get("repr_wolves")
        sheep_time_to_repro = self.props.get("repr_sheep")
        self.grp_struct[WOLF_GRP_NM]["prey_dist"] = prey_dist
        self.grp_struct[WOLF_GRP_NM]["wolf_time_to_repro"] = wolf_time_to_repro
        self.grp_struct[SHEEP_GRP_NM]["prey_dist"] = prey_dist
        self.grp_struct[SHEEP_GRP_NM][
            "sheep_time_to_repro"
        ] = sheep_time_to_repro


def create_model(serial_obj=None, props=None, create_for_test=False,
                 exec_key=None):
    """
    This is for the sake of the API server:
    """
    if serial_obj is not None:
        return WolfSheep(serial_obj=serial_obj)
    else:
        return WolfSheep(MODEL_NAME, grp_struct=wolfsheep_grps,
                         props=props, create_for_test=create_for_test,
                         exec_key=exec_key)


def main():
    model = create_model()
    model.run()

    return 0


if __name__ == "__main__":
    main()
