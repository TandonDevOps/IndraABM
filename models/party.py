"""
This is a model that inherits from model.py
Model description:
This model describes the flow pof population depends on the
number of male, female and beer
"""

import lib.actions as acts
import lib.model as mdl

# Names
MODEL_NAME = "party"
MALE_AT_PARTY = "male_at_party"
FEMALE_AT_PARTY = "female_at_party"


def call_friend(agent, **kwargs):
    # TODO
    return -1


def is_party_over(agent, **kwargs):
    # check male num, check female num, check beer num if equals to 0
    return -1


def drink_beer(agent, **kwargs):
    # update beer number
    return -1


def leave_party(agent, **kwargs):
    # TODO
    return -1


def male_action(agent, **kwargs):
    # TODO
    return -1


def female_action(agent, **kwargs):
    # TODO
    return -1


party_grps = {
    MALE_AT_PARTY: {
        mdl.GRP_ACTION: None,
        mdl.MBR_ACTION: male_action,
        mdl.NUM_MBRS_PROP: "initial_num_male_party",
        mdl.COLOR: acts.BLUE,
    },
    FEMALE_AT_PARTY: {
        mdl.GRP_ACTION: None,
        mdl.MBR_ACTION: female_action,
        mdl.NUM_MBRS_PROP: "initial_num_female_party",
        mdl.COLOR: acts.RED,
    },
}


class Party(mdl.Model):
    """
        The party model
    """
    def handle_props(self, props):
        super().handle_props(props)
        num_of_beer = self.props.get("initial_num_beer")
        self.grp_struct[MALE_AT_PARTY]["num_of_beer"] = num_of_beer
        self.grp_struct[FEMALE_AT_PARTY]["num_of_beer"] = num_of_beer
        drink_beer_rate = self.props.get("drink_beer_rate")
        self.grp_struct[MALE_AT_PARTY]["drink_beer_rate"] = drink_beer_rate
        self.grp_struct[FEMALE_AT_PARTY]["drink_beer_rate"] = drink_beer_rate


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
