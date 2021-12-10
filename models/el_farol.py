"""
El Farol Bar model: a famous model from the Santa Fe Institute.
"""

import random

import lib.actions as acts
import lib.model as mdl

DEBUG = acts.DEBUG

Agent = acts.Agent

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


def drinker_action(agent):
    """
    To go or not to go, that is the question.
    The decision is based on the agent's memory of how crowded the
    bar has been recently (a parameter).
    """
    if DEBUG.debug:
        print("Alcoholic {} is located at {}".format(agent.name,
                                                     agent.get_pos()))
    percent_full = memory_check(agent)
    # agent motivation is inverse agent's memory of percentage full
    agent[MOTIV] = 1 - percent_full
    going = get_decision(agent)
    if agent.group_name() == AT_HOME:
        if going:
            acts.add_switch(agent, old_group=AT_HOME, new_group=AT_BAR)
    else:
        if not going:
            acts.add_switch(agent, old_group=AT_BAR, new_group=AT_HOME)
        # Updating the agent's memory for last night.
        # There might be a better place to do this.
        # doing it here has a one day lag.
        population = DEF_AT_HOME + DEF_AT_BAR
        attendance = acts.get_model(agent).env.pop_hist.pops[AT_BAR]
        last_att_perc = attendance[-1] / population
        agent[MEMORY].pop(0)
        agent[MEMORY].append(last_att_perc)
    return acts.MOVE


def create_drinker(name, i, exec_key=None, action=drinker_action):
    """
    Create a drinker, who starts with a random motivation.
    """
    rand_motive = random.random()
    recent_crowds = [HALF_FULL] * acts.get_prop(exec_key,
                                                MEMORY,
                                                DEF_MEM_CAPACITY)
    return Agent(name + str(i),
                 attrs={MOTIV: rand_motive, MEMORY: recent_crowds},
                 action=action, exec_key=exec_key)


el_farol_grps = {
    AT_HOME: {
        mdl.MBR_CREATOR: create_drinker,
        mdl.MBR_ACTION: drinker_action,
        mdl.NUM_MBRS: DEF_AT_HOME,
        mdl.COLOR: acts.BLUE
    },
    AT_BAR: {
        mdl.MBR_CREATOR: create_drinker,
        mdl.MBR_ACTION: drinker_action,
        mdl.NUM_MBRS: DEF_AT_BAR,
        mdl.COLOR: acts.RED
    },
}


class ElFarol(mdl.Model):
    """
    The El Farol bar: a great place to be, unless everyone else goes there
    also!
    """
    def handle_props(self, props):
        super().handle_props(props)
        num_mbrs = self.get_prop("population")
        at_bar = num_mbrs // 2
        at_home = num_mbrs - at_bar
        el_farol_grps[AT_BAR]["num_mbrs"] = at_bar
        el_farol_grps[AT_HOME]["num_mbrs"] = at_home


def create_model(serial_obj=None, props=None):
    """
    `create_model()` exists for the sake of the API server:
    """
    if serial_obj is not None:
        return ElFarol(serial_obj=serial_obj)
    elif props is not None:
        return ElFarol(MODEL_NAME, grp_struct=el_farol_grps, props=props)
    else:
        return ElFarol(MODEL_NAME, grp_struct=el_farol_grps)


def main():
    model = create_model()
    model.run()
    return 0


if __name__ == "__main__":
    main()
