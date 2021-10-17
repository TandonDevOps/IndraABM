"""
This is a model that inherits from model.py
Model description:
This model describes the flow pof population depends on the
number of male, female and beer
"""

from lib.display_methods import YELLOW, BLACK, GREEN
from lib.model import Model, MBR_ACTION, NUM_MBRS_PROP, COLOR, NUM_MBRS
# import lib.actions as acts
# from lib.model import GRP_ACTION

# Names
MODEL_NAME = "paths"
GRASSLAND = "Grassland"
GROUND = "Ground"
PERSON = "Person"
DEF_NUM_LAND = 20*20*0.8
DEF_NUM_PERSONS = 30


def person_action(agent, **kwargs):
    # TODO
    # person will choose a road
    # according to probability distribution based on road's popularity
    print("person begin at " + str(agent.get_pos()))
    # roads = acts.get_neighbors(agent)
    # Compute probability distribution and determine the new position
    return -1


def land_action(agent, **kwargs):
    # TODO
    print("grass in " + str(agent.get_pos()))
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
        height = self.props.get("grid_height")
        width = self.props.get("grid_width")
        grass_density = self.props.get("initial_grass_density")
        grass_num = int(height * width * grass_density)
        self.grp_struct[GRASSLAND]["num_mbrs"] = grass_num


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
