import random
import lib.actions as acts
import lib.model as mdl
import lib.agent as agt

# Default Settings
MODEL_NAME = "model_generator"
DEF_RED_MBRS = 2
DEF_BLUE_MBRS = 2

NUM_MBRS = "num_mbrs"
MBR_CREATOR = "mbr_creator"
MBR_ACTION = "mbr_action"
GRP_ACTION = "grp_action"
NUM_MBRS_PROP = "num_mbrs_prop"
COLOR = "color"
RATIO = "radio"
OGTA= "own-group-to-all"
RAND_MOVE = "random-move"

DEF_GRP_NM = 'name'
DEF_GRP = {
    MBR_CREATOR: acts.create_agent,
    GRP_ACTION: None,
    MBR_ACTION: None,
    NUM_MBRS: None,
    NUM_MBRS_PROP: None,
    COLOR: None,
}
DEF_GRP_STRUCT = {
    DEF_GRP_NM: DEF_GRP
}

# List for Create_Action methods:
# Add more methods here when aviliable 
MODEL_GEN_ACTION_METHOD = [RATIO]
MODEL_GEN_ACTION_SUBMETHOD = [OGTA]
MODEL_GEN_ACTION_BELOW_ACT = [RAND_MOVE]
# --------------------------------------------- Below are methods for creating Actions ------------------------------------------------------


def create_agent(name, i, action=None, **kwargs):
    """
    Create an agent that does almost nothing. Default for all user generated models
    """
    agent = agt.Agent(name + str(i), action=action, **kwargs)
    return agent.to_json()


def env_action(agent, **kwargs):
    """
    Just to see if this works!
    """
    print("The environment does NOT look perilous: you can relax.")

# --------------------------------------------- Below are methods for creating Groups ------------------------------------------------------


def create_group_struct(color, num_mbrs, name):
    DEF_GRP_NM = name
    DEF_GRP = {
        MBR_CREATOR: acts.create_agent,
        GRP_ACTION: None,
        MBR_ACTION: acts.def_action,
        NUM_MBRS: num_mbrs,
        NUM_MBRS_PROP: None,
        COLOR: color,
    }
    DEF_GRP_STRUCT = {
        DEF_GRP_NM: DEF_GRP
    }
    return DEF_GRP_STRUCT


def join(agent1, agent2):
    """
    Create connection between agent1 and agent2.
    agent1 should be a group.
    """
    if not acts.is_group(agent1):
        print("Attempt to place " + str(agent2)
              + " in non-group " + str(agent1))
        return False
    else:
        if not agent1.add_member(agent2):
            print("Could not add mbr " + str(agent2)
                  + " to " + str(agent1))
        if not agent2.add_group(agent1):
            print("Could not add grp "
                  + str(agent2)
                  + " to "
                  + str(agent1))
        return True


def grp_val(grp, key):
    """
    Let's have a function that fill in defaults if a model
    fails to specify any of the above group properties.
    """
    return grp.get(key, DEF_GRP[key])


def create_group(exec_key, jrep, color, num_mbrs, group_name):
    """
    Overrided this method in model generator's creat_group endpoint to create all groups.
    """
    groups = []
    grp_struct = create_group_struct(color, num_mbrs, group_name)
    print('created group struct is:', grp_struct)
    grps = grp_struct
    for grp_nm in grps:
        grp = grps[grp_nm]
        num_mbrs = int(grp_val(grp, NUM_MBRS))
        print('grp_nm is: ', grp)
        groups.append(acts.Group(grp_nm,
                                 action=grp_val(grp, GRP_ACTION),
                                 color=grp_val(grp, COLOR),
                                 num_mbrs=num_mbrs,
                                 mbr_creator=grp_val(grp,
                                                     MBR_CREATOR),
                                 mbr_action=grp_val(grp, MBR_ACTION),
                                 exec_key=exec_key))
    return groups


def create_action(exec_key, jrep, color, num_mbrs, group_name):
    """
    Overrided this method in model generator's creat_model endpoint to create a model.
    """
    groups = []
    grp_struct = create_group_struct(color, num_mbrs, group_name)
    print('created action struct is:', grp_struct)
    grps = grp_struct
    for grp_nm in grps:
        grp = grps[grp_nm]
        print('grp_nm is: ', grp)
        groups.append(acts.Group(grp_nm,
                                 action=grp_val(grp, GRP_ACTION),
                                 color=grp_val(grp, COLOR),
                                 num_mbrs=num_mbrs,
                                 exec_key=exec_key))
    return groups

# --------------------------------------------- Below are methods for creating Action for Ratio Method (Segregation) ------------------------------------------------------
DEF_HOOD_SIZE = 1
DEF_TOLERANCE = .5
DEF_SIGMA = .2

MIN_TOL = 0.1
MAX_TOL = 0.9

MOVE = False
DONT_MOVE = True

def ratio_get_tolerance(default_tolerance, sigma):
    """
    `tolerance` measures how *little* of one's own group one will
    tolerate being among.
    """
    tol = random.gauss(default_tolerance, sigma)
    # a low tolerance number here means high tolerance!
    tol = min(tol, MAX_TOL)
    tol = max(tol, MIN_TOL)
    return tol

def ratio_env_favorable(hood_ratio, my_tolerance):
    """
    Is the environment to our agent's liking or not??
    """
    return hood_ratio >= my_tolerance

def agent_action_ratio(agent, **kwargs):
    """
    This is what agents do each turn of the segregation model
    """
    # get neighborhood size:
    hood_size = acts.get_prop("hood_size", default=4)
    # see what % of agents are in our group in our hood:
    ratio_num = acts.neighbor_ratio(agent,
                                    lambda a: a.group_name() ==
                                    agent.group_name(),
                                    size=hood_size)
    # if we like our neighborhood, stay put:
    if ratio_env_favorable(ratio_num, ratio_get_tolerance(DEF_TOLERANCE, DEF_SIGMA)):
        return DONT_MOVE
    else:
        # if we don't like our neighborhood, move!
        return MOVE