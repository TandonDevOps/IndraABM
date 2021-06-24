"""
This model illustrates the spontaneous synronization of large crowds without a
central central clock or synronization tool. In this model, the agents
(fireflies) start chaning color (blinkin) at random frequencies. However, at
each simulation run, the agents increase or decrease the frequencies based on
the average ofneighborung agents' blinkin frequencies. After a certain number
of simulation runs, we see that all of the agents are blinking at the pretty
much same frequency.

This behaviour is shown by calculating the standard deviation in the blinking
frequencies with the environment action.

A related video that explains this phenomena:
https://www.youtube.com/watch?v=t-_VPRCtiUg

Another good website to understand this model:
https://1000fireflies.net/about
"""

import random
# import statistics
import lib.agent as agt
import lib.display_methods as disp
import lib.model as mdl
from lib.space import get_neighbors
from lib.utils import Debug
from registry.registry import save_reg, TEST_EXEC_KEY, get_model

DEBUG = Debug()

MODEL_NAME = "firefly"
DEF_DENSITY = .5
DEF_NUM_FIREFLY = 50
DEF_MIN_BLINK_FREQ = 1
DEF_MAX_BLINK_FREQ = 10
DEF_HOOD_SIZE = 2
BLINK_FREQ = "blink_freq"
LAST_BLINK_TIME = "last_blinked_at"

SELF_WEIGHT = .6
OTHER_WEIGHT = .4

ON_GRP = "Firefly On"
OFF_GRP = "Firefly Off"
STATE = "state"
OFF = 0
ON = 1
STATE_MAP = {OFF: OFF_GRP, ON: ON_GRP}


def get_blink_freq():
    return random.randint(DEF_MIN_BLINK_FREQ, DEF_MAX_BLINK_FREQ)


def set_last_blink(firefly):
    """
    Update this fly's last blink time.
    """
    firefly[LAST_BLINK_TIME] = firefly.duration


def time_to_next_blink(firefly):
    """
    How long before this bug blinks?
    """
    return firefly[BLINK_FREQ] - (firefly.duration - firefly[LAST_BLINK_TIME])


def to_blink_or_not(firefly):
    """
    The passed firefly may blink by changing its group.
    If the firefly is
    already ON, this function turns if OFF. Otherwise, checks if the
    the time passed since last blink time of the firefly is
    greater than the firefly's blinking frequency.
    Return the new firefly state.
    """
    # Get the current firefly state: happens to be the group name
    # for now!
    curr_state = firefly[STATE]
    new_state = curr_state

    # fireflies that are blinking always stop the next turn:
    if curr_state == ON:
        new_state = OFF
    # Turn ON if the blinking time has arrived
    else:
        if time_to_next_blink(firefly) == 0:
            set_last_blink(firefly)
            new_state = ON
    return (curr_state, new_state)


def adjust_blink_freq(firefly):
    """
    Inreases or decreases the firefly's blinking frequency based on the average
    of its neighbors.
    """
    nbors = get_neighbors(firefly, size=DEF_HOOD_SIZE)
    if len(nbors) > 0:
        sum_blink_freq = 0
        for ff_name in nbors:
            sum_blink_freq += nbors[ff_name][BLINK_FREQ]
        blink_freq_avg = sum_blink_freq / len(nbors)
        # Update firefly's blinking frequency based on the average
        firefly.set_attr(BLINK_FREQ,
                         firefly[BLINK_FREQ] * SELF_WEIGHT + blink_freq_avg *
                         OTHER_WEIGHT)
    return firefly[BLINK_FREQ]


def firefly_action(firefly, **kwargs):
    """
    A firefly decides whether to blink or not.
    """
    adjust_blink_freq(firefly)
    (curr_state, new_state) = to_blink_or_not(firefly)
    # Set up firefly to swith groups if needed:
    if curr_state != new_state:
        get_model(firefly.exec_key).add_switch(
            str(firefly),
            STATE_MAP[curr_state],
            STATE_MAP[new_state])
    return agt.MOVE


def create_firefly(name, i, props=None, action=None,
                   exec_key=0):
    """
    Create a trendsetter: all RED to start.
    """
    return agt.Agent(MODEL_NAME + str(i),
                     action=action,
                     exec_key=exec_key,
                     attrs={LAST_BLINK_TIME: 0,
                            BLINK_FREQ: get_blink_freq(),
                            STATE: OFF, })


def calc_blink_dev(meadow, **kwargs):
    std_dev = 0.0
    meadow.user.tell(f"Std dev of blink frequency is: {std_dev}")
    return std_dev


firefly_grps = {
    OFF_GRP: {
        mdl.MBR_ACTION: firefly_action,
        mdl.NUM_MBRS: DEF_NUM_FIREFLY,
        mdl.COLOR: disp.BLACK,
        mdl.MBR_CREATOR: create_firefly,
    },
    ON_GRP: {
        mdl.NUM_MBRS: 1,  # best for testing we have 1!
        mdl.COLOR: disp.YELLOW,
        mdl.MBR_CREATOR: create_firefly,
    },
}


class Firefly(mdl.Model):
    """
    """
    def handle_props(self, props):
        super().handle_props(props)
        density = self.get_prop("density", DEF_DENSITY)
        num_agents = int(self.height * self.width * density)
        self.grp_struct[OFF_GRP]["num_mbrs"] = num_agents


def create_model(serial_obj=None, props=None, create_for_test=False):
    """
    This is for the sake of the API server:
    """
    if serial_obj is not None:
        return Firefly(serial_obj=serial_obj)
    else:
        return Firefly(
            MODEL_NAME,
            grp_struct=firefly_grps,
            props=props,
            create_for_test=create_for_test,
            env_action=calc_blink_dev,
        )


def setup_test_model():
    """
    Set's up the Firefly model at exec_key = 0 for testing purposes.
    :return: None
    """
    create_model(props=None, create_for_test=True)
    save_reg(TEST_EXEC_KEY)


def main():
    model = create_model()
    model.run()
    return 0


if __name__ == "__main__":
    main()
