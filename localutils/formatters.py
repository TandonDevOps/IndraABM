ERROR = "Error:"

def err_return(s):
  return {ERROR: s}

TRUE_STRS = ["True", "true", "1"]

def str_to_bool(s):
    """
    Convert plausible "true" strings to bool True.
    Other values to False.
    Useful for taking URL inputs to real boolean values.
    """
    return s in TRUE_STRS