"""
This file contains miscellaneous.
"""
import os
import random

from propargs.propargs import PropArgs

DEF_MODEL_DIR = "models"

INDRA_HOME_VAR = "INDRA_HOME"
PA_INDRA_HOME = "/home/IndraABM/IndraABM"

INDRA_DEBUG_VAR = "INDRA_DEBUG"
INDRA_DEBUG2_VAR = "INDRA_DEBUG2"
INDRA_DEBUG3_VAR = "INDRA_DEBUG3"
INDRA_DEBUG_LIB_VAR = "INDRA_DEBUG_LIB"
INDRA_DEBUG2_LIB_VAR = "INDRA_DEBUG2_LIB"


def agent_by_name(agent):
    return agent if isinstance(agent, str) else agent.name


def gaussian(mean, sigma, trim_at_zero=True):
    sample = random.gauss(mean, sigma)
    if trim_at_zero:
        if sample < 0:
            sample *= -1
    return sample


def get_func_name(f):
    # Until Agent.restore and Env.to_json can restore functions from function
    # names, strings will be returned as-is.
    if isinstance(f, str):
        return f
    elif f is not None:
        return f.__name__
    else:
        return ""


def get_model_dir(model_dir):
    if model_dir is None:
        return DEF_MODEL_DIR
    return model_dir


def get_prop_path(model_name, model_dir=None):
    model_dir = get_model_dir(model_dir)
    ihome = os.getenv(INDRA_HOME_VAR, PA_INDRA_HOME)
    return ihome + "/" + model_dir + "/props/" + model_name + ".props.json"


def init_props(model_nm, props=None, model_dir=None,
               skip_user_questions=False):
    model_dir = get_model_dir(model_dir)
    props_file = get_prop_path(model_nm, model_dir=model_dir)
    if props is None:
        pa = PropArgs.create_props(model_nm,
                                   ds_file=props_file,
                                   skip_user_questions=skip_user_questions)
    else:
        pa = PropArgs.create_props(model_nm,
                                   prop_dict=props,
                                   skip_user_questions=skip_user_questions)

    return pa


class Debug:
    """
    Reads the environment variables to decide on enabling debug outputs
    """

    def __init__(self):
        # Simple debugging level
        self.debug = self.get_env_var(INDRA_DEBUG_VAR)

        # Deeper debugging level
        self.debug2 = self.get_env_var(INDRA_DEBUG2_VAR)

        # Deepest debugging level
        self.debug3 = self.get_env_var(INDRA_DEBUG3_VAR)

        # Switches debugging for the library modules
        self.debug_lib = self.get_env_var(INDRA_DEBUG_LIB_VAR)

        # Switches deeper debugging for the library modules
        self.debug2_lib = self.get_env_var(INDRA_DEBUG2_LIB_VAR)

    def get_env_var(self, var_name):
        env_var = os.getenv(var_name)

        # Return false if the environment variable is not set at all
        if env_var is None:
            return False

        # Accept different styles of writing true
        if (env_var.lower() == "true") or (env_var == "1"):
            return True
        else:
            return False
