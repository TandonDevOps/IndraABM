import lib.actions as acts
import lib.model as mdl

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

DEF_GRP_NM = 'name'
DEF_GRP = {
    MBR_CREATOR: None,
    GRP_ACTION: None,
    MBR_ACTION: None,
    NUM_MBRS: None,
    NUM_MBRS_PROP: None,
    COLOR: None,
}
DEF_GRP_STRUCT = {
    DEF_GRP_NM: DEF_GRP
}


def env_action(agent, **kwargs):
    """
    Just to see if this works!
    """
    print("The environment does NOT look perilous: you can relax.")


def create_group_struct(color, num_mbrs, name):
    DEF_GRP_NM = name
    DEF_GRP = {
        MBR_CREATOR: None,
        GRP_ACTION: None,
        MBR_ACTION: None,
        NUM_MBRS: num_mbrs,
        NUM_MBRS_PROP: None,
        COLOR: color,
    }
    DEF_GRP_STRUCT = {
        DEF_GRP_NM: DEF_GRP
    }
    return DEF_GRP_STRUCT


def grp_val(grp, key):
    """
    Let's have a function that fill in defaults if a model
    fails to specify any of the above group properties.
    """
    return grp.get(key, DEF_GRP[key])


def create_group(exec_key, jrep, color, num_mbrs, group_name):
    """
    Override this method in your model to create all of your groups.
    In general, you shouldn't need to: fill in the grp_struct instead.
    """
    groups = []
    grp_struct = create_group_struct(color, num_mbrs, group_name)
    print('created group struct is:', grp_struct)
    grps = grp_struct
    for grp_nm in grps:
        grp = grps[grp_nm]
        num_mbrs = grp_val(grp, NUM_MBRS)
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
