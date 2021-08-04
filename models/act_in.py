"""
This model tries to demonstrate how patterns forms in a closed system
"""

import lib.actions as acts
import lib.model as mdl
from lib.display_methods import RED, BLUE
import registry.registry as reg

MODEL_NAME = "act_in"
DEF_INACTIVE_MBRS = 2
DEF_ACTIVE_MBRS = 2
DEF_ACT_STRENGTH = 1
DEF_IN_STRENGTH = -0.1
DEF_NEARBY_CELLS = 5
DEF_FARTHER_CELLS = 10
DEF_BIAS = 0

ACTIVE = "active"
INACTIVE = "inactive"
NEARBY_CELLS = "nearby_cells"
FARTHER_CELLS = "farther_cells"
ACT_STRENGTH = "activation_strengh"
IN_STRENGTH = "inhibition_strengh"
BIAS = "bias"


def get_near_and_far_grps(agent):
    near_grp = acts.get_neighbors(agent,
                                  size=act_in_grps[ACTIVE][NEARBY_CELLS])
    far_and_near = acts.get_neighbors(agent,
                                      size=act_in_grps[ACTIVE][FARTHER_CELLS])
    far_grp = far_and_near - near_grp
    return (near_grp, far_grp)


def group_power(grp, exec_key):
    print(exec_key)
    power = 0
    for cell in grp:
        cell = reg.get_agent(cell, exec_key)
        if cell.group_name() == ACTIVE:
            power += 1
        else:
            power -= 1
    return power


def act_val(act_power, in_power):
    return (act_power * act_in_grps[ACTIVE][ACT_STRENGTH]
            + in_power * act_in_grps[INACTIVE][IN_STRENGTH] +
            act_in_grps[INACTIVE][BIAS])


def act_in_action(agent, **kwargs):
    """
    We're going to use this agent action to test the new get_neighbors()
    func in space.py.
    """
    (near_grp, far_grp) = get_near_and_far_grps(agent)
    if acts.DEBUG.debug:
        print("Agent {} is located at {}".format(agent.name, agent.get_pos()))
        for neighbor in near_grp:
            print(f"{str(agent)} has near neighbor {str(neighbor)}")
        for neighbor in far_grp:
            print(f"{str(agent)} has far neighbor {str(neighbor)}")
    exec_key = agent.exec_key
    act_power = group_power(near_grp, exec_key)
    in_power = group_power(far_grp, exec_key)
    act_in_val = act_val(act_power, in_power)
    if act_in_val > 0:
        if agent.group_name() != ACTIVE:
            agent.has_acted = True
            acts.add_switch(agent, INACTIVE, ACTIVE)
    elif act_in_val < 0:
        if agent.group_name() != INACTIVE:
            agent.has_acted = True
            acts.add_switch(agent, ACTIVE, INACTIVE)
    return acts.DONT_MOVE


act_in_grps = {
    ACTIVE: {
        mdl.MBR_ACTION: act_in_action,
        mdl.NUM_MBRS: DEF_ACTIVE_MBRS,
        mdl.NUM_MBRS_PROP: "num_active",
        mdl.COLOR: BLUE,
        NEARBY_CELLS: DEF_NEARBY_CELLS,
        FARTHER_CELLS: DEF_FARTHER_CELLS,
        ACT_STRENGTH: DEF_ACT_STRENGTH
    },
    INACTIVE: {
        mdl.MBR_ACTION: act_in_action,
        mdl.NUM_MBRS: DEF_INACTIVE_MBRS,
        mdl.NUM_MBRS_PROP: "num_inactive",
        mdl.COLOR: RED,
        IN_STRENGTH: DEF_IN_STRENGTH,
        BIAS: DEF_BIAS,
    },
}


class ActIn(mdl.Model):
    """
    Activation-inhibition model.
    """
    def handle_props(self, props):
        super().handle_props(props)
        self.get_prop(FARTHER_CELLS, DEF_FARTHER_CELLS)
        act_in_grps[ACTIVE][NEARBY_CELLS] = self.get_prop(NEARBY_CELLS,
                                                          DEF_NEARBY_CELLS)
        act_in_grps[ACTIVE][FARTHER_CELLS] = self.get_prop(FARTHER_CELLS,
                                                           DEF_FARTHER_CELLS)
        act_in_grps[INACTIVE][IN_STRENGTH] = self.get_prop(IN_STRENGTH,
                                                           DEF_IN_STRENGTH)
        act_in_grps[INACTIVE][ACT_STRENGTH] = self.get_prop(ACT_STRENGTH,
                                                            DEF_ACT_STRENGTH)
        act_in_grps[INACTIVE][BIAS] = self.get_prop(BIAS, DEF_BIAS)


def create_model(serial_obj=None, props=None, create_for_test=False,
                 exec_key=None):
    """
    This is for the sake of the API server.
    """
    if serial_obj is not None:
        return ActIn(serial_obj=serial_obj)
    else:
        return ActIn(MODEL_NAME, grp_struct=act_in_grps, props=props,
                     create_for_test=create_for_test)


def main():
    model = create_model()
    model.run()
    return 0


if __name__ == "__main__":
    main()
