import json

from lib.utils import get_prop_path
from APIServer.api_utils import err_return

import db.model_db as model_db


def get_props(model_id):
    try:
        model = model_db.get_model_by_id(model_id)
        if model is None:
            return err_return(f"Model id {model_id} not found.")
        prop_file = get_prop_path(model["module"], model["package"])
        print("prop_file = ", prop_file)
        with open(prop_file) as file:
            props = json.loads(file.read())
        return props
    except (IndexError, KeyError, ValueError):
        return err_return("Invalid model id " + str(model_id))
    except FileNotFoundError:  # noqa: F821
        return err_return("Models or props file not found")
