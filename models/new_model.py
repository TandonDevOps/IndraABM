"""
This is a minimal model that inherits from model.py
and just sets up a couple of agents in two groups that
do nothing except move around randomly.
"""

import lib.actions as acts
import lib.model as mdl


MODEL_NAME = "new_model"
DEF_PURPLE_MBRS = 4
DEF_GREEN_MBRS = 44


def green_action(agent, **kwargs):
    """
    We're going to use this agent action to test the new get_neighbors()
    func in space.py.
    """
    if acts.DEBUG.debug:
        print("Green agent {} is located at {}".format(agent.name,
                                                       agent.get_pos()))
    return acts.MOVE


def purple_action(agent, **kwargs):
    """
    We're going to use this agent action to test the new get_neighbors()
    func in space.py.
    """
    for neighbor in acts.get_neighbors(agent):
        print(f"Purple {str(agent)} has neighbor {str(neighbor)}")
    return acts.MOVE


new_model_grps = {
    "green_grp": {
        mdl.MBR_ACTION: green_action,
        mdl.NUM_MBRS: DEF_GREEN_MBRS,
        mdl.NUM_MBRS_PROP: "num_green",
        mdl.COLOR: acts.GREEN
    },
    "purple_grp": {
        mdl.MBR_ACTION: purple_action,
        mdl.NUM_MBRS: DEF_PURPLE_MBRS,
        mdl.NUM_MBRS_PROP: "num_purple",
        mdl.COLOR: acts.PURPLE
    },
}


class NewModel(mdl.Model):
    """
    This class should just create a basic model that runs, has
    some agents that move around, and allows us to test if
    the system as a whole is working.
    It turns out that so far, we don't really need to subclass anything!
    """


def create_model(serial_obj=None, props=None, create_for_test=False,
                 exec_key=None):
    """
    This is for the sake of the API server.
    """
    if serial_obj is not None:
        return NewModel(serial_obj=serial_obj)
    else:
        return NewModel(MODEL_NAME,
                        grp_struct=new_model_grps,
                        props=props,
                        create_for_test=create_for_test,
                        exec_key=exec_key)


def main():
    model = create_model()
    model.run()
    return 0


if __name__ == "__main__":
    main()
