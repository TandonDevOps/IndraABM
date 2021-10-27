"""
This is a model that inherits from model.py
Model description:
This model describes the flow pof population depends on the
number of male, female and beer
"""

import lib.actions as acts
import lib.model as mdl

Agent = acts.Agent

# Names
MODEL_NAME = "paths"
GRASSLAND = "Grassland"
GROUND = "Ground"
PERSON = "Person"
POPULARITY = "popularity"
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
    # print("grass in " + str(agent.get_pos()))
    print(agent.to_json)
    return -1


def create_land(name, i, action=land_action, exec_key=None):
    """
    Create land agent
    """
    return Agent(name + str(i), attrs={POPULARITY: 0},
                 action=action, exec_key=exec_key)


paths_grps = {
    GRASSLAND: {
        mdl.MBR_CREATOR: create_land,
        mdl.MBR_ACTION: land_action,
        mdl.NUM_MBRS: DEF_NUM_LAND,
        mdl.NUM_MBRS_PROP: "initial_num_grassland",
        mdl.COLOR: acts.GREEN,
    },
    GROUND: {
        mdl.MBR_ACTION: land_action,
        mdl.NUM_MBRS: 0,
        mdl.NUM_MBRS_PROP: "initial_num_ground",
        mdl.COLOR: acts.BLACK,
    },
    PERSON: {
        mdl.MBR_ACTION: person_action,
        mdl.NUM_MBRS: DEF_NUM_PERSONS,
        mdl.NUM_MBRS_PROP: "initial_num_person",
        mdl.COLOR: acts.YELLOW,
    },
}


class Paths(mdl.Model):
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
