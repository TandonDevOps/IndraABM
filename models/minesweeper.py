"""
This is a minimal model that inherits from model.py
and just sets up a couple of agents in two groups that
do nothing except move around randomly.
"""

import lib.actions as acts
import lib.model as mdl


MODEL_NAME = "minesweeper"
DEF_BOMBS = 2
SAFE_GRP = "safe_cell_grp"
BOMB_GRP = "hidden_bomb_grp"


def game_action(env, **kwargs):
    """
    Ask the user to choose a cell!
    """
    x = 0
    y = 0
    print("Please choose a cell (as x, y): ")
    print(f"Chose {x}, {y}")
    # chosen_cell = env.get_agent_at(x, y)
    # grp_nm = chosen_cell.primary_group()
    # is it BOMB_GRP or SAFE_GRP?


def bomb_action(agent, **kwargs):
    """
    """
    print("Boom!")
    return acts.DONT_MOVE


def safe_cell_action(agent, **kwargs):
    """
    """
    print("Number neighboring bombs is: ")
    return acts.DONT_MOVE


minesweep_grps = {
    BOMB_GRP: {
        mdl.MBR_ACTION: None,
        mdl.NUM_MBRS: DEF_BOMBS,
        mdl.NUM_MBRS_PROP: "num_bombs",
        mdl.COLOR: acts.GREEN
    },
    "exposed_bombs_grp": {
        mdl.MBR_ACTION: None,
        mdl.NUM_MBRS: 0,
        mdl.NUM_MBRS_PROP: None,
        mdl.COLOR: acts.RED
    },
    SAFE_GRP: {
        mdl.MBR_ACTION: None,
        mdl.NUM_MBRS: 0,
        mdl.COLOR: acts.GREEN
    },
}


class Minesweeper(mdl.Model):
    """
    Plays the game of minesweep.
    """
    def handle_props(self, props):
        super().handle_props(props)
        self.grp_struct[SAFE_GRP][mdl.NUM_MBRS] = (self.height * self.width)


def create_model(serial_obj=None, props=None, create_for_test=False,
                 exec_key=None):
    """
    This is for the sake of the API server.
    """
    if serial_obj is not None:
        return Minesweeper(serial_obj=serial_obj)
    else:
        return Minesweeper(MODEL_NAME,
                           grp_struct=minesweep_grps,
                           props=props,
                           env_action=game_action,
                           create_for_test=create_for_test,
                           exec_key=exec_key,
                           random_placing=False)


def main():
    model = create_model()
    model.run()
    return 0


if __name__ == "__main__":
    main()
