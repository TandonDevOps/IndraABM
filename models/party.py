"""
This is a model that inherits from model.py
Model description:
This model describes the flow pof population depends on the
number of male, female and beer
"""

import lib.actions as acts
import lib.model as mdl
import lib.agent as agt

# Global Variables
DEF_NUM_MBRS = 5
DEF_NUM_BEER = 15
DEF_DRINK_BEER_RATE = 2

# Names
MODEL_NAME = "party"
MALE_AT_PARTY = "male at party"
FEMALE_AT_PARTY = "female at party"
MALE_AT_HOME = "male at home"
FEMALE_AT_HOME = "female at home"
NUM_OF_BEER = "num of beer"
DRINK_BEER_RATE = "drink beer rate"
MALE = "male"
FEMALE = "female"
PLACE = "place"
HOME = "home"
PARTY = "party"
opp_group = {
    MALE_AT_PARTY: MALE_AT_HOME,
    MALE_AT_HOME: MALE_AT_PARTY,
    FEMALE_AT_PARTY: FEMALE_AT_HOME,
    FEMALE_AT_HOME: FEMALE_AT_PARTY,
}
party_opp_group = {
    MALE_AT_PARTY: FEMALE_AT_PARTY,
    FEMALE_AT_PARTY: MALE_AT_PARTY,
}


def call_friend(agent):
    """
    move one or more agents in xxx_at_home to xxx_at_party
    male at party will call male at home
    female at party will call female at home
    """
    return 0


def leave_party(agent):
    """
    change agent's group to xxx_at_party to xxx_at_home
    """
    # If there is not beer to drink, leave the party
    """agent.set_attr(PLACE, HOME)
    acts.add_switch(agent, agent.prim_group_nm(),
                    opp_group[agent.prim_group_nm()])
    """
    if agent.group_name() == MALE_AT_PARTY:
        acts.add_switch(agent, MALE_AT_PARTY, MALE_AT_HOME)
    if agent.group_name() == FEMALE_AT_PARTY:
        acts.add_switch(agent, FEMALE_AT_PARTY, FEMALE_AT_HOME)
    return acts.DONT_MOVE


def drink_beer(agent, **kwargs):
    """
    Update the number of beer, and make sure every group at the party
    share the same number of beer.
    """
    if agent.get_attr(PLACE) is None:
        agent.set_attr(PLACE, PARTY)
    currentGrp = agent.group_name()
    beerComsuption = party_grps[currentGrp][DRINK_BEER_RATE]
    numOfBeer = party_grps[currentGrp][NUM_OF_BEER]
    if numOfBeer < beerComsuption:
        leave_party(agent)
        return acts.MOVE
    else:
        party_grps[currentGrp][NUM_OF_BEER] = (numOfBeer - beerComsuption)
        party_grps[party_opp_group[currentGrp]][NUM_OF_BEER] = (
            numOfBeer - beerComsuption)
        call_friend(agent)
        return acts.DONT_MOVE


def home_action(agent, **kwargs):
    if agent.get_attr(PLACE) is None:
        agent.set_attr(PLACE, HOME)
    return acts.DONT_MOVE


def create_male(name, i, props=None, action=None, exec_key=None):
    """
    Create an male agent at the party
    """
    return agt.Agent(name+str(i),
                     action=action,
                     exec_key=exec_key)


def create_female(name, i, props=None, action=None, exec_key=None):
    """
    Create an male agent at the party
    """
    return agt.Agent(name+str(i),
                     action=action,
                     exec_key=exec_key)


party_grps = {
    MALE_AT_PARTY: {
        mdl.MBR_CREATOR: create_male,
        mdl.MBR_ACTION: drink_beer,
        mdl.NUM_MBRS: DEF_NUM_MBRS,
        mdl.NUM_MBRS_PROP: "initial_num_male_party",
        mdl.COLOR: acts.BLUE,
    },
    MALE_AT_HOME: {
        mdl.MBR_CREATOR: create_male,
        mdl.MBR_ACTION: home_action,
        mdl.NUM_MBRS: DEF_NUM_MBRS,
        mdl.COLOR: acts.GRAY,
    },
    FEMALE_AT_PARTY: {
        mdl.MBR_CREATOR: create_female,
        mdl.MBR_ACTION: drink_beer,
        mdl.NUM_MBRS: DEF_NUM_MBRS,
        mdl.NUM_MBRS_PROP: "initial_num_female_party",
        mdl.COLOR: acts.RED,
    },
    FEMALE_AT_HOME: {
        mdl.MBR_CREATOR: create_female,
        mdl.MBR_ACTION: home_action,
        mdl.NUM_MBRS: DEF_NUM_MBRS,
        mdl.COLOR: acts.GREEN,
    },
}


class Party(mdl.Model):
    """
        The party model
    """
    def handle_props(self, props):
        super().handle_props(props)
        num_of_beer = self.get_prop("initial_num_beer", DEF_NUM_BEER)
        drink_beer_rate = self.get_prop("drink_beer_rate", DEF_DRINK_BEER_RATE)
        self.grp_struct[MALE_AT_PARTY][NUM_OF_BEER] = num_of_beer
        self.grp_struct[FEMALE_AT_PARTY][NUM_OF_BEER] = num_of_beer
        self.grp_struct[MALE_AT_PARTY][DRINK_BEER_RATE] = drink_beer_rate
        self.grp_struct[FEMALE_AT_PARTY][DRINK_BEER_RATE] = drink_beer_rate


def create_model(serial_obj=None, props=None):
    if serial_obj is not None:
        return Party(serial_obj=serial_obj)
    else:
        return Party(MODEL_NAME, grp_struct=party_grps, props=props,
                     exec_key=None)


def main():
    model = create_model()
    model.run()
    return 0


if __name__ == "__main__":
    main()
