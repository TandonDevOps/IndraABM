"""
This module restores an env from json and runs it.
"""
import importlib

from registry.registry import sync_api_restored_model_with_registry, registry
from registry.model_db import get_model_by_id, get_model_by_mod
from APIServer.api_utils import err_return


def module_from_model(model):
    mod_path = f'{model["package"]}.{model["module"]}'
    return importlib.import_module(mod_path)


def create_model(model_id, props, indra_dir):
    """
    We get some props and create a model in response.
    """
    model_rec = get_model_by_id(model_id, indra_dir=indra_dir)
    if model_rec is not None:
        return module_from_model(model_rec).create_model(props=props)
    else:
        return err_return("Model not found: " + str(model_id))


def run_model(serial_model, periods, indra_dir):
    """
    We get passed `serial_model` and run it `periods` times.
    `model_rec` refers to the record from the model db.
    `model` refers to an instance of the Python Model class.

    The passed serial model is not in the registry so calls for
    registry.get_model will fail. Also calls for model.group will fail
    because the api serial_obj does not contain serialized groups. They are
    present in model.env.members.
    Since we always rely on the api response to construct the model at run time
    we need to sync the registry with the model restored from the api response.

    NOTE: Maybe we should only use the registry to restore - could decrease the
    api payload size and give performance boost.
    """
    model_rec = get_model_by_mod(serial_model["module"], indra_dir=indra_dir)
    if model_rec is not None:
        module = module_from_model(model_rec)
        model = module.create_model(serial_obj=serial_model)
        registry.load_reg(model.exec_key)
        sync_api_restored_model_with_registry(model, model.exec_key)
        model.runN(periods)
        return model
    else:
        return None
