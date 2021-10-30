"""
This is a model that inherits from model.py
Model description:
This model describes how paths emerge along
commonly traveled routes. People tend to take
routes that other travelers before them have
taken, making them more popular and causing
other travelers to follow those same routes.
"""

import random
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
    # according to weighted probability based on road's popularity
    print("person begin at " + str(agent.get_pos()))
    neighbors = acts.get_neighbors(agent)
    neighbors_popularity = {}
    for land_name in neighbors:
        if "Grassland" in land_name or "Ground" in land_name:
            neighbors_popularity[land_name] = neighbors[land_name][POPULARITY]
    print(neighbors_popularity)
    next_land_name = weighted_random(neighbors_popularity)
    # change the position to choose land
    next_land = neighbors[next_land_name]
    agent.set_pos(next_land.get_x(), next_land.get_y())
    # change the popularity of this land
    return -1


def weighted_random(pop_dict):
    # TODO
    # choose one key based on weighted probability
    result = random.choices(list(pop_dict.keys()),
                            weights=pop_dict.values(),
                            k=1)
    return result[0]


def land_action(agent, **kwargs):
    # TODO
    # print("grass in " + str(agent.get_pos()))
    # print(agent.to_json)
    return -1


def create_land(name, i, action=land_action, exec_key=None):
    """
    Create a land agent
    """
    return Agent(name + str(i),
                 attrs={POPULARITY: 0},
                 action=action,
                 exec_key=exec_key)


def create_person(name, i, action=person_action, exec_key=None):
    """
    Create a person agent
    """
    return Agent(name + str(i),
                 action=action,
                 exec_key=exec_key)


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
