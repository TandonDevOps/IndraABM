"""
A model to simulate Conway's game of life.
"""

import lib.actions as acts
import lib.model as mdl


MODEL_NAME = "game_of_life"

DEF_NUM_ALIVE = 4
DEF_NUM_DEAD = 4

DEAD = "dead"
ALIVE = "alive"


def is_dead(agent):
    return agent.prim_group == DEAD


def game_of_life_action(biosphere):
    dead_grp = acts.get_agent(DEAD, biosphere.exec_key)
    print("Dead grp is:", repr(dead_grp))


def game_agent_action(agent):
    """
    A simple default agent action.
    """
    if acts.DEBUG.debug:
        print("GofL agent {} is acting".format(agent.name))
    return acts.DONT_MOVE


game_grps = {
    "dead": {
        mdl.NUM_MBRS: DEF_NUM_DEAD,
        mdl.NUM_MBRS_PROP: "num_blue",
        mdl.COLOR: acts.BLUE
    },
    "alive": {
        mdl.MBR_ACTION: game_agent_action,
        mdl.NUM_MBRS: DEF_NUM_ALIVE,
        mdl.NUM_MBRS_PROP: "num_red",
        mdl.COLOR: acts.RED
    },
}


def live_or_die():
    """
    Apply the rules for live agents.
    The agent passed in should be alive, meaning its color should be black.
    """
    num_live_neighbors = acts.get_num_of_neighbors(exclude_self=True,
                                                   pred=None, size=1,
                                                   region_type=None)
    # 2 and 3 should not be hard-coded!
    if (num_live_neighbors != 2 and num_live_neighbors != 3):
        return acts.BLUE
    else:
        return acts.RED


class GameOfLife(mdl.Model):
    def run(self):
        if acts.DEBUG.debug:
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
