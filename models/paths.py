"""
This is a model that inherits from model.py
Model description:
This model describes the flow pof population depends on the
number of male, female and beer
"""

from lib.display_methods import YELLOW, BLACK, GREEN
from lib.model import Model, MBR_ACTION, NUM_MBRS_PROP, COLOR, NUM_MBRS
# from lib.model import GRP_ACTION

# Names
MODEL_NAME = "paths"

GRASSLAND = "Grassland"
GROUND = "Ground"
PERSON = "Person"

DEF_NUM_LAND = 100*100
DEF_NUM_PERSONS = 250


def land_action(agent, **kwargs):
    # TODO
    return -1


def person_action(agent, **kwargs):
    # check male num, check female num, check beer num if equals to 0
    return -1


paths_grps = {
    GRASSLAND: {
        MBR_ACTION: land_action,
        NUM_MBRS: DEF_NUM_LAND,
        NUM_MBRS_PROP: "initial_num_grassland",
        COLOR: GREEN,
    },
    GROUND: {
        MBR_ACTION: land_action,
        NUM_MBRS: 0,
        NUM_MBRS_PROP: "initial_num_ground",
        COLOR: BLACK,
    },
    PERSON: {
        MBR_ACTION: person_action,
        NUM_MBRS: DEF_NUM_PERSONS,
        NUM_MBRS_PROP: "initial_num_person",
        COLOR: YELLOW,
    },
}


class Paths(Model):
    """
        The paths model
    """
    def handle_props(self, props):
        super().handle_props(props)
        threshold = self.props.get("threshold")
        self.grp_struct[GRASSLAND]["threshold"] = threshold


def create_model(serial_obj=None, props=None):
    if serial_obj is not None:
        return Paths(serial_obj=serial_obj)
    else:
        return Paths(MODEL_NAME, grp_struct=paths_grps, props=props,
                     exec_key=None)


def main():
    model = create_model()
    model.run()

    return 0


if __name__ == "__main__":
    main()
