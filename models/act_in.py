"""
This model tries to demonstrate how patterns forms in a closed system
"""

import lib.actions as acts
import lib.model as mdl
from lib.display_methods import RED, BLUE

MODEL_NAME = "act_in"
DEF_INACTIVE_MBRS = 2
DEF_ACTIVE_MBRS = 2


def act_in_action(agent, **kwargs):
    """
    We're going to use this agent action to test the new get_neighbors()
    func in space.py.
    """
    if acts.DEBUG.debug:
        print("Agent {} is located at {}".format(agent.name,
                                                 agent.get_pos()))
    for neighbor in acts.get_neighbors(agent):
        print(f"{str(agent)} has neighbor {str(neighbor)}")
    return acts.DONT_MOVE


act_in_grps = {
    "active": {
        mdl.MBR_ACTION: act_in_action,
        mdl.NUM_MBRS: DEF_ACTIVE_MBRS,
        mdl.NUM_MBRS_PROP: "num_active",
        mdl.COLOR: BLUE
    },
    "inactive": {
        mdl.MBR_ACTION: act_in_action,
        mdl.NUM_MBRS: DEF_INACTIVE_MBRS,
        mdl.NUM_MBRS_PROP: "num_inactive",
        mdl.COLOR: RED
    },
}


class ActIn(mdl.Model):
    """
    Activation-inhibition model.
    """


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
