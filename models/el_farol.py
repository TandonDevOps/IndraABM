"""
El Farol Bar model: a famous model from the Santa Fe Institute.
"""

import random
from lib.agent import MOVE, Agent
from lib.display_methods import RED, BLUE
from lib.model import Model, NUM_MBRS, MBR_ACTION
from lib.model import COLOR, MBR_CREATOR
from registry.registry import get_model
from lib.utils import Debug

DEBUG = Debug()

AT_HOME = "At home"
AT_BAR = "At bar"

MODEL_NAME = "el_farol"
DEF_AT_HOME = 2
DEF_AT_BAR = 2
DEF_MOTIV = 0.6
MOTIV = "motivation"
BAR_ATTEND = "bar attendees"
HALF_FULL = .5
OPT_OCUPANCY = 0.6
MEMORY = 'memory'
DEF_MEM_CAPACITY = 7  # Must be an integer
mem_capacity = DEF_MEM_CAPACITY


def get_decision(agent):
    """
    Decide whether to get wasted today or not
    """
    return random.random() <= agent[MOTIV]


def add_up_to(n):
    """
    Given an integer n, returns the sum
    from 0 to n.
    """
    if n <= 0:
        return 0
    return add_up_to(n-1) + n


def weighted_sum(arr):
    """
    Given an array representing agent
    memories, return a weighted sum.
    Recent memories weight more.
    """
    total = 0
    for i in range(len(arr)):
        total += arr[i] * (i + 1)
    return total


def memory_check(agent):
    """
    Return percentage of capacity the bar was at
    based on last attendances.
    """
    mem_attendance = agent[MEMORY]
    w_sum = weighted_sum(mem_attendance)
    total = add_up_to(len(mem_attendance))
    percent_full = w_sum / total
    if DEBUG.debug:
        print("Percent empty:", 1 - percent_full)
    return percent_full


def drinker_action(agent, **kwargs):
    """
    To go or not to go, that is the question.
    The decision is based on the agent's memory of how crowded the
    bar has been recently (a parameter).
    """
    if DEBUG.debug:
        print("Alcoholic {} is located at {}".format(agent.name,
                                                     agent.get_pos()))
    bar = get_model(agent.exec_key)
    percent_full = memory_check(agent)
    # agent motivation is inverse agent's memory of percentage full
    agent[MOTIV] = 1 - percent_full
    going = get_decision(agent)
    if agent.group_name() == AT_HOME:
        if going:
            bar.add_switch(str(agent), AT_HOME, AT_BAR)
    else:
        if not going:
            bar.add_switch(str(agent), AT_BAR, AT_HOME)
        # Updating the agent's memory for last night.
        # There might be a better place to do this.
        # doing it here has a one day lag.
        population = sum([len(group.members) for group in bar.groups])
        attendance = bar.env.pop_hist.pops[AT_BAR]
        last_att_perc = attendance[-1]/population
        agent[MEMORY].pop(0)
        agent[MEMORY].append(last_att_perc)
    return MOVE


def create_drinker(name, i, exec_key=None, action=drinker_action):
    """
    Create a drinker, who starts with a random motivation.
    """
    rand_motive = random.random()
    recent_crowds = [HALF_FULL]*mem_capacity
    return Agent(name + str(i),
                 attrs={MOTIV: rand_motive, MEMORY: recent_crowds},
                 action=action, exec_key=exec_key)


el_farol_grps = {
    AT_HOME: {
        MBR_CREATOR: create_drinker,
        MBR_ACTION: drinker_action,
        NUM_MBRS: DEF_AT_HOME,
        COLOR: BLUE
    },
    AT_BAR: {
        MBR_CREATOR: create_drinker,
        MBR_ACTION: drinker_action,
        NUM_MBRS: DEF_AT_BAR,
        COLOR: RED
    },
}


class ElFarol(Model):
    """
    The El Farol bar: a great place to be, unless everyone else goes there
    also!
    """


def create_model(serial_obj=None, props=None):
    """
    `create_model()` exists for the sake of the API server:
    """
    global mem_capacity
    if serial_obj is not None:
        return ElFarol(serial_obj=serial_obj)
    elif props is not None:
        num_mbrs = props["population"]['val']
        at_bar = num_mbrs // 2
        at_home = num_mbrs - at_bar
        el_farol_grps[AT_BAR]["num_mbrs"] = at_bar
        el_farol_grps[AT_HOME]["num_mbrs"] = at_home
        mem_capacity = DEF_MEM_CAPACITY
        if props['memory'] is not None and props['memory']['val'] is not None:
            mem_capacity = props['memory']['val']
        return ElFarol(MODEL_NAME, grp_struct=el_farol_grps, props=props)
    else:
        return ElFarol(MODEL_NAME, grp_struct=el_farol_grps)


def main():
    model = create_model()
    model.run()
    return 0


if __name__ == "__main__":
    main()
