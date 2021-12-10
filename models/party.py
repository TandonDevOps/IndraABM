"""
This is a model that inherits from model.py
Model description:
This model describes the flow pof population depends on the
number of male, female and beer
"""
import lib.actions as acts
import lib.model as mdl
import random

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
    move one agent in xxx_at_home to xxx_at_party
    male at party will call male at home
    female at party will call female at home
    If the input agent is at home, then there is nothing happen
    """
    groupName = agent.group_name()
    if groupName == MALE_AT_HOME or groupName == FEMALE_AT_HOME:
        return acts.DONT_MOVE
    motive = random.random()
    if agent.group_name() == MALE_AT_PARTY:
        if acts.exists_neighbor(agent,
                                lambda neighbor:
                                neighbor.group_name() == MALE_AT_HOME):
            currentGrp = agent.group_name()
            beerNum = party_grps[currentGrp][NUM_OF_BEER]
            if motive >= beerNum:
                n = acts.get_neighbor(agent,
                                      lambda neighbor:
                                      neighbor.group_name() == MALE_AT_HOME)
                acts.add_switch(n,
                                old_group=MALE_AT_HOME,
                                new_group=MALE_AT_PARTY)
            else:
                print("Motive : {}".format(motive))
                return acts.DONT_MOVE
    if agent.group_name() == FEMALE_AT_PARTY:
        if acts.exists_neighbor(agent,
                                lambda neighbor:
                                neighbor.group_name() == FEMALE_AT_HOME):
            currentGrp = agent.group_name()
            beerNum = party_grps[currentGrp][NUM_OF_BEER]
            if beerNum >= motive:
                n = acts.get_neighbor(agent,
                                      lambda neighbor:
                                      neighbor.group_name() == FEMALE_AT_HOME)
                acts.add_switch(n,
                                old_group=FEMALE_AT_HOME,
                                new_group=FEMALE_AT_PARTY)
            else:
                print("Motive : {}".format(motive))
                return acts.DONT_MOVE
    return acts.MOVE


def leave_party(agent):
    """
    change agent's group to xxx_at_party to xxx_at_home
    If there is not beer to drink, leave the party
    """
    if acts.DEBUG.debug:
        if agent.group_name() == MALE_AT_PARTY:
            acts.add_switch(agent, MALE_AT_PARTY, MALE_AT_HOME)
        elif agent.group_name() == FEMALE_AT_PARTY:
            acts.add_switch(agent, FEMALE_AT_PARTY, FEMALE_AT_HOME)
        else:
            return acts.MOVE
    return acts.DONT_MOVE


def join_party(agent):
    """
    Make agent join the party if his/her status is at home
    Change agent's group to xxx_at_home to xxx_at_party
    If the current agent is at party, then nothing happen
    """
    if acts.DEBUG.debug:
        if agent.group_name() == MALE_AT_HOME:
            acts.add_switch(agent, MALE_AT_HOME, MALE_AT_PARTY)
        elif agent.group_name() == FEMALE_AT_HOME:
            acts.add_switch(agent, FEMALE_AT_HOME, FEMALE_AT_PARTY)
        else:
            return acts.DONT_MOVE
    return acts.MOVE


def bring_beer(agent, n):
    """
    When agen switch from HOME to Party, each number bring
    rand number of beers
    """
    groupName = agent.group_name()
    drinkBeerRate = party_grps[groupName][DRINK_BEER_RATE]
    numOfNewBeer = random.randint(n, n*drinkBeerRate)
    currentBeerNum = party_grps[groupName][NUM_OF_BEER]
    newNumOfBeer = currentBeerNum + numOfNewBeer
    party_grps[groupName][NUM_OF_BEER] = newNumOfBeer
    party_grps[party_opp_group[groupName]][NUM_OF_BEER] = newNumOfBeer


def drink_beer(agent, **kwargs):
    """
    Update the number of beer, and make sure every group at the party
    share the same number of beer.
    """
    if agent.get_attr(PLACE) is None:
        agent.set_attr(PLACE, PARTY)
    currentGrp = agent.group_name()
    numOfBeer = party_grps[currentGrp][NUM_OF_BEER]
    if numOfBeer == 0:
        return acts.DONT_MOVE
    else:
        beerComsuption = party_grps[currentGrp][DRINK_BEER_RATE]
        if numOfBeer < beerComsuption:
            party_grps[currentGrp][NUM_OF_BEER] = 0
            party_grps[party_opp_group[currentGrp]][NUM_OF_BEER] = 0
            leave_party(agent)
            return acts.MOVE
        else:
            newNumOfBeer = numOfBeer - beerComsuption
            party_grps[currentGrp][NUM_OF_BEER] = newNumOfBeer
            party_grps[party_opp_group[currentGrp]][NUM_OF_BEER] = newNumOfBeer
            call_friend(agent)
            return acts.DONT_MOVE


def home_action(agent, **kwargs):
    """
    Place agent at home
    """
    if acts.DEBUG.debug:
        if agent.get_attr(PLACE) is None:
            agent.set_attr(PLACE, HOME)
    return acts.DONT_MOVE


def create_male(name, i, props=None, action=None, exec_key=None):
    """
    Create an male agent at the party
    """
    return acts.agt.Agent(name+str(i),
                          action=action,
                          exec_key=exec_key)


def create_female(name, i, props=None, action=None, exec_key=None):
    """
    Create an female agent at the party
    """
    return acts.agt.Agent(name+str(i),
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
        mdl.COLOR: acts.NAVY,
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
        mdl.COLOR: acts.MAGENTA,
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
