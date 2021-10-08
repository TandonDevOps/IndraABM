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
import statistics as stats

import lib.actions as acts
import lib.model as mdl

Agent = acts.Agent

DEBUG = acts.DEBUG

MODEL_NAME = "firefly"
DEF_DENSITY = .5
DEF_NUM_FIREFLY = 50
DEF_MIN_BLINK_FREQ = 1
DEF_MAX_BLINK_FREQ = 10
DEF_HOOD_SIZE = 2
BLINK_FREQ = "blink_freq"
TIME_TO_BLINK = "last_blinked_at"

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


def reset_time_to_blink(firefly):
    """
    Update this fly's last blink time.
    """
    firefly[TIME_TO_BLINK] = firefly[BLINK_FREQ]


def blink_now(firefly):
    """
    Predicate asking if the time is now.
    """
    return firefly[TIME_TO_BLINK] <= 0


def time_to_next_blink(firefly):
    """
    How long before this bug blinks?
    """
    return firefly[TIME_TO_BLINK]


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
        firefly[TIME_TO_BLINK] -= 1
        if blink_now(firefly):
            reset_time_to_blink(firefly)
            new_state = ON
    return (curr_state, new_state)


def adjust_blink_freq(firefly):
    """
    Inreases or decreases the firefly's blinking frequency based on the average
    of its neighbors.
    """
    nbors = acts.get_neighbors(firefly, size=DEF_HOOD_SIZE,
                               model_name=MODEL_NAME)
    if len(nbors) > 0:
        sum_blink_freq = 0
        for ff_name in nbors:
            sum_blink_freq += nbors[ff_name][BLINK_FREQ]
        blink_freq_avg = sum_blink_freq / len(nbors)
        # Update firefly's blinking frequency based on the average
        firefly[BLINK_FREQ] = (firefly[BLINK_FREQ] * SELF_WEIGHT
                               + blink_freq_avg * OTHER_WEIGHT)
    return firefly[BLINK_FREQ]


def switch_state(firefly, curr_state, new_state):
    """
    Actually swap states.
    """
    firefly[STATE] = new_state
    acts.get_model(firefly).add_switch(str(firefly),
                                       STATE_MAP[curr_state],
                                       STATE_MAP[new_state])


def firefly_action(firefly, **kwargs):
    """
    A firefly decides whether to blink or not.
    """
    adjust_blink_freq(firefly)
    (curr_state, new_state) = to_blink_or_not(firefly)
    # Set up firefly to swith groups if needed:
    if curr_state != new_state:
        switch_state(firefly, curr_state, new_state)
    return acts.MOVE


def create_firefly(name, i, props=None, action=None, exec_key=0):
    """
    Create a trendsetter: all RED to start.
    """
    blink_freq = get_blink_freq()
    return Agent(MODEL_NAME + str(i),
                 action=action,
                 exec_key=exec_key,
                 attrs={TIME_TO_BLINK: blink_freq,
                        BLINK_FREQ: blink_freq,
                        STATE: OFF, })


def calc_blink_dev(meadow, **kwargs):
    std_dev = 0.0
    freqs = []
    # the std dev of just the off group is a fine proxy for
    # that of all fireflies.
    for ff_name in meadow[OFF_GRP]:
        firefly = acts.get_agent(ff_name, meadow.exec_key)
        freqs.append(firefly[BLINK_FREQ])
    std_dev = stats.stdev(freqs)
    meadow.user.tell(f"Std dev of blink frequency is: {std_dev:.2f}")
    return std_dev


firefly_grps = {
    OFF_GRP: {
        mdl.MBR_ACTION: firefly_action,
        mdl.NUM_MBRS: DEF_NUM_FIREFLY,
        mdl.COLOR: acts.BLACK,
        mdl.MBR_CREATOR: create_firefly,
    },
    ON_GRP: {
        mdl.NUM_MBRS: 1,  # best for testing we have 1!
        mdl.COLOR: acts.YELLOW,
        mdl.MBR_CREATOR: create_firefly,
    },
}


class Firefly(mdl.Model):
    """
    """

    def handle_props(self, props):
        super().handle_props(props)
        density = self.get_prop("density", DEF_DENSITY)
        assert density > 0.0 and density < 1.0
        num_agents = int(self.height * self.width * density)
        self.grp_struct[OFF_GRP]["num_mbrs"] = num_agents


def create_model(serial_obj=None, props=None, create_for_test=False,
                 exec_key=None):
    """
    This is for the sake of the API server:
    """
    if serial_obj is not None:
        return Firefly(serial_obj=serial_obj)
    else:
        return Firefly(MODEL_NAME,
                       grp_struct=firefly_grps,
                       props=props,
                       env_action=calc_blink_dev,
                       create_for_test=create_for_test,
                       exec_key=exec_key)


def main():
    model = create_model()
    model.run()
    return 0


if __name__ == "__main__":
    main()
