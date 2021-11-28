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
THRESHOLD = 20
DECAY_DEGREE = 4


def person_action(agent, **kwargs):
    '''
    On setup, each person chooses a random grassland.
    On each step, the person sees the popularity of the land on the way,
    and more likely to choose the most popular way.
    Then the move of the person will make the land more popular.
    '''
    # person will choose a road
    # according to weighted probability based on road's popularity
    print("person begin at " + str(agent.get_pos()))
    neighbors = acts.get_neighbors(agent)
    neighbors_popularity = {}
    for land in neighbors:
        if "Grassland" in land or "Ground" in land:
            neighbors_popularity[land] = neighbors[land][POPULARITY]
    if acts.DEBUG.debug:
        print(neighbors_popularity)
    next_land_name = weighted_random(neighbors_popularity)
    # change the position to choose land
    next_land = neighbors[next_land_name]
    if acts.DEBUG.debug:
        print("before:" + str(agent.get_pos()))
    agent.set_pos(next_land.get_x(), next_land.get_y())
    if acts.DEBUG.debug:
        print("after:" + str(agent.get_pos()))
    # change the popularity of this land after the person moved
    next_land[POPULARITY] = next_land[POPULARITY] + 4
    # dont move or it will change position again
    return acts.DONT_MOVE


def weighted_random(pop_dict):
    '''
    Choose one key based on weighted probability
    '''
    # weight initialization, otherwise it will always choose the last one
    # when all the lands weight equals to zero
    for land in pop_dict:
        pop_dict[land] = pop_dict[land] + 1
    result = random.choices(list(pop_dict.keys()),
                            weights=pop_dict.values(),
                            k=1)
    return result[0]


def land_action(agent, **kwargs):
    '''
    If people move to a grassland enough times,
    and make the grassland reach a certain popularity threshold,
    it will turn ground to indicate the presence of an established route.
    '''
    if acts.DEBUG.debug:
        print("grass in " + str(agent.get_pos()))
        print(agent.to_json)
        print(agent[POPULARITY])
    old_group = agent.group_name()
    new_group = old_group
    # the popularity will attenuat after each period
    if acts.DEBUG.debug:
        print("Popularity before: " + str(agent[POPULARITY]))
    if agent[POPULARITY] > 10:
        if old_group == GRASSLAND:
            # agent[POPULARITY] -= 0
            agent[POPULARITY] -= DECAY_DEGREE
        if old_group == GROUND:
            # agent[POPULARITY] -= 0
            agent[POPULARITY] -= DECAY_DEGREE / 2
    if acts.DEBUG.debug:
        print("Popularity after: " + str(agent[POPULARITY]))
    # change group when the popularity reach the threshold
    if old_group == GRASSLAND:
        if(agent[POPULARITY] >= THRESHOLD):
            new_group = GROUND
    # ground land will change to grassland when popularity is reducing
    if old_group == GROUND:
        if(agent[POPULARITY] < (THRESHOLD / 2)):
            new_group = GRASSLAND
    if old_group != new_group:
        acts.add_switch(agent, old_group, new_group)
    return acts.DONT_MOVE


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
        mdl.MBR_CREATOR: create_person,
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
        threshold = self.props.get("threshold", THRESHOLD)
        decay_degree = self.props.get("decay_degree", DECAY_DEGREE)
        self.grp_struct[GRASSLAND]["decay_degree"] = decay_degree
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
