import json

from lib.utils import get_prop_path
from registry.model_db import get_model_by_id
from APIServer.api_utils import err_return


def get_props(model_id, indra_dir):
    try:
        model = get_model_by_id(model_id, indra_dir=indra_dir)
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
