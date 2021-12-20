"""
A model for how fires spread through a forest.
"""

import lib.actions as acts
import lib.model as mdl

MODEL_NAME = "forest_fire"

DEF_NUM_TREES = 10
DEF_DIM = 30
DEF_DENSITY = 0.44
DEF_NEW_FIRE = 0.01
# tree group names
HEALTHY = "Healthy"
NEW_FIRE = "New Fire"
ON_FIRE = "On Fire"
BURNED_OUT = "Burned Out"
NEW_GROWTH = "New Growth"

# state numbers: create as strings for JSON,
# convert to int when we need 'em that way
HE = "0"
NF = "1"
OF = "2"
BO = "3"
NG = "4"

TRANS_TABLE = "trans_table"
state_trans = [
    [1 - DEF_NEW_FIRE, DEF_NEW_FIRE, 0.0, 0.0, 0.0],
    [0.0, 0.0, 1.0, 0.0, 0.0],
    [0.0, 0.0, 0.0, 1.0, 0.0],
    [0.0, 0.0, 0.0, 0.99, 0.01],
    [1.0, 0.0, 0.0, 0.0, 0.0],
]

GRP_MAP = "group_map"

STATE_MAP = {
    HEALTHY: HE,
    NEW_FIRE: NF,
    ON_FIRE: OF,
    BURNED_OUT: BO,
    NEW_GROWTH: NG,
}

GRP_MAP = {
    HE: HEALTHY,
    NF: NEW_FIRE,
    OF: ON_FIRE,
    BO: BURNED_OUT,
    NG: NEW_GROWTH,
}

state_transitions = [
    {"current_group": NEW_GROWTH, "next_group": HEALTHY,},
    {"current_group": BURNED_OUT, "next_group": NEW_GROWTH},
    {"current_group": ON_FIRE, "next_group": BURNED_OUT},
    {"current_group": NEW_FIRE, "next_group": ON_FIRE},
    {"current_group": HEALTHY, "next_group": HEALTHY},
]


def forest_action(env, **kwargs):
    for group_info in state_transitions:
        current_group = group_info["current_group"]
        new_group = group_info["next_group"]
        group = acts.get_group(env, current_group)
        members = group.get_members()
        for agt_nm in members:
            if current_group == HEALTHY:
                curr_state = STATE_MAP[current_group]
                new_group = GRP_MAP[
                    str(acts.prob_state_trans(int(curr_state), state_trans))
                ]
            if new_group != current_group:
                acts.add_switch(
                    agent=acts.get_agent(agt_nm, env.exec_key),
                    old_group=current_group,
                    new_group=new_group,
                )


def on_fire_action(group, **kwargs):
    healthy_neighbors = set()
    members = group.get_members()
    for agt_nm in members:
        neighbors = acts.get_neighbors(
            acts.get_agent(agt_nm, group.exec_key),
            lambda neighbor: neighbor.group_name() == HEALTHY,
        )
        for neighbor in neighbors:
            healthy_neighbors.add(neighbor)
    for neighbor in healthy_neighbors:
        acts.add_switch(
            agent=acts.get_agent(neighbor, group.exec_key),
            old_group=HEALTHY,
            new_group=NEW_FIRE,
        )


# A function that acts only on trees that are on fire in the wind direction
def wind_tree_action(agent):
    """
    How should the tree state change if the wind direction changes
    """
    old_group = agent.group_name()
    new_group = old_group  # for now!
    if old_group == HEALTHY:
        if acts.exists_neighbor(
            agent, lambda neighbor: neighbor.group_name() == ON_FIRE
        ):
            new_group = NEW_FIRE

    # apply wind in X-axis
    new_x_coordinates = acts.get_x_hood(agent, width=1)
    # if we didn't catch on fire above, do probabilistic transition:
    if old_group == new_group:
        curr_state = STATE_MAP[old_group]
        # we gotta do these str/int shenanigans with state cause
        # JSON only allows strings as dict keys
        new_group = GRP_MAP[
            str(acts.prob_state_trans(int(curr_state), state_trans * 10))
        ]
        if acts.DEBUG.debug:
            if agent.group_name == NEW_FIRE:
                print("Latest x coordinates after wind: ", new_x_coordinates)

    if old_group != new_group:
        if acts.DEBUG.debug:
            print(f"Add switch from {old_group} to {new_group}")
        acts.add_switch(agent, old_group=old_group, new_group=new_group)
    return acts.DONT_MOVE


# A function that acts only on trees that are on fire in the wind direction
def new_tree_action(agent):
    old_group = agent.group_name()
    new_group = old_group  # for now!
    if old_group == NEW_FIRE:
        if acts.exists_neighbor(
            agent, lambda neighbor: neighbor.group_name() == ON_FIRE
        ):
            new_group = ON_FIRE
    if old_group == HEALTHY:
        if acts.exists_neighbor(
            agent, lambda neighbor: neighbor.group_name() == ON_FIRE
        ):
            new_group = NEW_FIRE
    if old_group == new_group:
        curr_state = STATE_MAP[old_group]
        # we gotta do these str/int shenanigans with state cause
        # JSON only allows strings as dict keys
        new_group = GRP_MAP[
            str(acts.prob_state_trans(int(curr_state), state_trans * 10))
        ]

    if old_group != new_group:
        if acts.DEBUG.debug:
            print(f"Add switch from {old_group} to {new_group}")
        acts.add_switch(agent, old_group=old_group, new_group=new_group)
    return acts.DONT_MOVE


def spark_action(agent):
    old_group = agent.group_name()
    new_group = old_group
    if old_group == new_group:
        curr_state = STATE_MAP[old_group]
        new_group = GRP_MAP[
            str(acts.prob_state_trans(int(curr_state), state_trans * 10))
        ]
        if acts.DEBUG.debug:
            if agent.group_name == NEW_FIRE:
                print("Spark has enhanced fire here")
            acts.add_switch(agent, old_group=old_group, new_group=new_group)

    if old_group == HEALTHY:
        curr_state = STATE_MAP[old_group]
        new_group = GRP_MAP[
            str(acts.prob_state_trans(int(curr_state), state_trans))
        ]

    if old_group != new_group:
        if acts.DEBUG.debug:
            print(f"Add switch from {old_group} to {new_group}")
        acts.add_switch(agent, old_group=old_group, new_group=new_group)
    return acts.DONT_MOVE


def y_wind_action(agent):
    """
    How should the tree state change if the wind direction changes
    in the y direction
    """
    old_group = agent.group_name()
    new_group = old_group
    if old_group == HEALTHY:
        if acts.exists_neighbor(
            agent, lambda neighbor: neighbor.group_name() == ON_FIRE
        ):
            new_group = NEW_FIRE

    # apply wind in Y-axis
    new_y_coordinates = acts.get_y_hood(agent, width=1)

    if old_group == new_group:
        curr_state = STATE_MAP[old_group]
        new_group = GRP_MAP[
            str(acts.prob_state_trans(int(curr_state), state_trans * 10))
        ]
        if acts.DEBUG.debug:
            if agent.group_name == NEW_FIRE:
                print("Latest y coordinates after wind: ", new_y_coordinates)

    if old_group == HEALTHY:
        curr_state = STATE_MAP[old_group]
        new_group = GRP_MAP[
            str(acts.prob_state_trans(int(curr_state), state_trans))
        ]

    if old_group != new_group:
        if acts.DEBUG.debug:
            print(f"Add switch from {old_group} to {new_group}")
        acts.add_switch(agent, old_group=old_group, new_group=new_group)
    return acts.DONT_MOVE


# Groups need to be in below order
ff_grps = {
    NEW_GROWTH: {
        mdl.NUM_MBRS: 0,
        mdl.COLOR: acts.SPRINGGREEN,
    },
    BURNED_OUT: {
        mdl.NUM_MBRS: 0,
        mdl.COLOR: acts.BLACK,
    },
    ON_FIRE: {
        mdl.NUM_MBRS: 0,
        mdl.GRP_ACTION: on_fire_action,
        mdl.COLOR: acts.RED,
    },
    NEW_FIRE: {
        mdl.NUM_MBRS: 0,
        mdl.COLOR: acts.TOMATO,
    },
    HEALTHY: {
        mdl.NUM_MBRS: DEF_NUM_TREES,
        mdl.COLOR: acts.GREEN,
    },
}


class ForestFire(mdl.Model):
    """
    The forest fire model.
    """

    def handle_props(self, props):
        super().handle_props(props)
        density = self.get_prop("density", DEF_DENSITY)
        num_agents = int(self.height * self.width * density)
        self.grp_struct[HEALTHY]["num_mbrs"] = num_agents


def create_model(
    serial_obj=None, props=None, create_for_test=False, exec_key=None
):
    """
    This is for the sake of the API server:
    """
    if serial_obj is not None:
        return ForestFire(serial_obj=serial_obj)
    else:
        return ForestFire(
            MODEL_NAME,
            grp_struct=ff_grps,
            props=props,
            create_for_test=create_for_test,
            exec_key=exec_key,
            env_action=forest_action,
        )


def main():
    model = create_model()
    model.run()
    return 0


if __name__ == "__main__":
    main()
