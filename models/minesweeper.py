"""
This is a minimal model that inherits from model.py
and just sets up a couple of agents in two groups that
do nothing except move around randomly.
"""
import math
import lib.actions as acts
import lib.model as mdl

DEF_DIM = 10
MODEL_NAME = "minesweeper"
DEF_BOMBS = 2
WIDTH = "width"
HEIGHT = "height"
SAFE_GRP = "safe_cell_grp"
BOMB_GRP = "hidden_bomb_grp"
EXPOSED_BOMB_GRP = "exposed_bombs_grp"
EXPOSED_SAFE_GRP = "exposed_safe_grp"
DEF_NUM_PEOPLE = DEF_DIM*DEF_DIM
DEF_NUM_BOMB = 0
DEF_NUM_SAFE = int(.7 * DEF_NUM_PEOPLE)
DEF_NUM_BOMB = int(.3 * DEF_NUM_PEOPLE)
BOMBED = "bombed"


def game_action(env, **kwargs):
    """
    Ask the user to choose a cell!
    """
    x = 0
    y = 0
    x, y = input("Please choose a cell (as x, y): ").split()
    print(f"Chose {x}, {y}")
    if int(x) < 0 or int(y) > minesweep_grps[SAFE_GRP][HEIGHT]:
        print("Please select a cell between 0 and ",
              minesweep_grps[SAFE_GRP][HEIGHT])
    else:
        chosen_cell = env.get_agent_at(x, y)
        grp_nm = env.get_agent_at(x, y).group_name()
        if grp_nm == BOMB_GRP:
            print("You just clicked a bomb!")
            chosen_cell.has_acted = True
            acts.add_switch(chosen_cell,
                            old_group=BOMB_GRP,
                            new_group=EXPOSED_BOMB_GRP)
        elif grp_nm == SAFE_GRP:
            chosen_cell.has_acted = True
            acts.add_switch(chosen_cell,
                            old_group=SAFE_GRP,
                            new_group=EXPOSED_SAFE_GRP)


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
        mdl.GRP_ACTION: None,
        mdl.MBR_ACTION: game_action,
        mdl.NUM_MBRS: 0,
        mdl.NUM_MBRS_PROP: "num_bombs",
        BOMBED: DEF_NUM_BOMB,
        mdl.COLOR: acts.GREEN
    },
    EXPOSED_BOMB_GRP: {
        mdl.MBR_ACTION: game_action,
        mdl.NUM_MBRS: 0,
        mdl.NUM_MBRS_PROP: None,
        mdl.COLOR: acts.RED
    },
    SAFE_GRP: {
        mdl.GRP_ACTION: None,
        mdl.MBR_ACTION: game_action,
        mdl.NUM_MBRS: DEF_NUM_SAFE,
        mdl.COLOR: acts.GREEN,
        WIDTH: DEF_DIM,
        HEIGHT: DEF_DIM,
    },
    EXPOSED_SAFE_GRP: {
        mdl.MBR_ACTION: game_action,
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
        safe_box = (self.height * self.width)
        bomb_rt = self.props.get("pct_bomb") / 100
        self.num_bombs = math.floor(bomb_rt * safe_box)
        self.grp_struct[SAFE_GRP][mdl.NUM_MBRS] = int(safe_box)
        self.grp_struct[BOMB_GRP][EXPOSED_BOMB_GRP] = int(bomb_rt * safe_box)
        self.grp_struct[SAFE_GRP][WIDTH] = self.width
        self.grp_struct[SAFE_GRP][HEIGHT] = self.height


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
