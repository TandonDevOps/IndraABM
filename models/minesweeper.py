"""
This is a minimal model that inherits from model.py
and just sets up a couple of agents in two groups that
do nothing except move around randomly.
"""
import math
import lib.actions as acts
import lib.model as mdl

DEF_DIM = 2
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
DEF_NUM_BOMB = int(.1 * DEF_NUM_PEOPLE)
INIT_BOMBS = "bombs"


def game_action(env, **kwargs):
    """
    Ask the user to choose a cell!
    """
    if acts.get_periods(env) == 0:
        place_bombs(env)
    else:
        x = None
        y = None
        safeLen = len(env.pop_hist.pops['safe_cell_grp'])
        while True:
            x, y = map(int, input("Please choose a cell (x, y): ").split(','))
            print(f"Chose {x}, {y}")
            if (x >= 0 and x < env.width and y >= 0 and y < env.height):
                chosen_cell = env.get_agent_at(x, y)
                if chosen_cell.active is False:
                    print("Cell is already open! Make a new choice")
                    continue
                else:
                    break
        print(f"{chosen_cell=}")
        grp_nm = chosen_cell.group_name()
        if env.pop_hist.pops['safe_cell_grp'][safeLen-1] == 0:
            print("Success!! You win")
            return 0
        else:
            if grp_nm == BOMB_GRP:
                print("You just clicked a bomb!")
                bomb_action(chosen_cell)
                return 0
            elif grp_nm == SAFE_GRP:
                print("You just clicked a safe cell!")
                chosen_cell.active = False
                acts.switch(chosen_cell.name,
                            SAFE_GRP, EXPOSED_SAFE_GRP, env.exec_key)
                adjacent_bombs(chosen_cell)


def place_bombs(env):
    """
    We will pick a random subset of safe cells.
    Then we will flip those agents to bomb cells.
    """
    if acts.get_periods(env) == 0:
        safe_grp = acts.get_group(env, SAFE_GRP)
        num_bombs = minesweep_grps[BOMB_GRP][INIT_BOMBS]
        switch_to_bomb = safe_grp.rand_subset(num_bombs)
        for agt_nm in switch_to_bomb:
            print(f"{agt_nm=}")
            acts.switch(agt_nm,
                        SAFE_GRP, BOMB_GRP, env.exec_key)


def bomb_action(agent, **kwargs):
    """
    """
    print("Boom!")
    acts.add_switch(agent,
                    old_group=BOMB_GRP,
                    new_group=EXPOSED_BOMB_GRP)
    return acts.DONT_MOVE


def adjacent_bombs(agent, **kwargs):
    """
    """
    count = 0
    nbors = acts.get_neighbors(agent)
    for neigh in nbors.members.items():
        if(neigh[1].group_name().startswith('hidden')):
            count = count + 1
    print(' there is/are ', count, ' bomb cell near by')


minesweep_grps = {
    BOMB_GRP: {
        mdl.NUM_MBRS: 0,
        mdl.NUM_MBRS_PROP: "num_bombs",
        INIT_BOMBS: DEF_NUM_BOMB,
        mdl.COLOR: acts.GREEN
    },
    EXPOSED_BOMB_GRP: {
        mdl.NUM_MBRS: 0,
        mdl.NUM_MBRS_PROP: None,
        mdl.COLOR: acts.RED
    },
    SAFE_GRP: {
        mdl.NUM_MBRS: DEF_NUM_SAFE,
        mdl.COLOR: acts.GREEN
    },
    EXPOSED_SAFE_GRP: {
        mdl.NUM_MBRS:  0,
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
        self.grp_struct[BOMB_GRP][INIT_BOMBS] = math.floor(bomb_rt * safe_box)
        self.grp_struct[SAFE_GRP][mdl.NUM_MBRS] = int(safe_box)


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
