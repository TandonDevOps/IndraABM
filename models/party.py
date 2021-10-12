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
MALE = "male"
FEMALE = "female"
BEER = "beer"


def call_friend(agent, **kwargs):
    # TODO
    return -1


def is_party_over(agent, **kwargs):
    # check male num, check female num, check beer num if equals to 0
    return -1


def drink_beer(agent, **kwargs):
    # TODO
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


def beer_action(agent, **kwargs):
    # TODO
    return -1


party_grps = {
    MALE: {
        mdl.GRP_ACTION: None,
        mdl.MBR_ACTION: male_action,
        mdl.NUM_MBRS_PROP: "initial_num_male",
        mdl.COLOR: acts.BLUE,
    },
    FEMALE: {
        mdl.GRP_ACTION: None,
        mdl.MBR_ACTION: female_action,
        mdl.NUM_MBRS_PROP: "initial_num_female",
        mdl.COLOR: acts.RED,
    },
    BEER: {
        mdl.GRP_ACTION: None,
        mdl.MBR_ACTION: beer_action,
        mdl.NUM_MBRS_PROP: "initial_num_beer",
        mdl.COLOR: acts.YELLOW,
    },
}


class Party(mdl.Model):
    """
        The party model
    """
    def handle_props(self, props):
        super().handle_props(props)
        drink_beer_rate = self.props.get("drink_beer_rate")
        self.grp_struct[BEER]["drink_beer_rate"] = drink_beer_rate


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
