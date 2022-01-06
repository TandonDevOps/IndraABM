"""
This module restores an env from json and runs it.
"""
import importlib

from APIServer.api_utils import err_return
import db.model_db as model_db


def module_from_model(model):
    mod_path = f'{model["package"]}.{model["module"]}'
    return importlib.import_module(mod_path)


def create_model_for_test(model, exec_key):
    """

    :param model: model to be created for testing. Loaded through name or id
    :param exec_key: exec_key to be used to register the model at.
    Can be None in which case it's created dynamically.
    :return:
    """
    module = module_from_model(model)
    return module.create_model(serial_obj=None, props=None,
                               create_for_test=True, exec_key=exec_key)


def create_model(model_id, props):
    """
    We get some props and create a model in response.
    """
    model_rec = model_db.get_model_by_id(model_id)
    if model_rec is not None:
        return module_from_model(model_rec).create_model(props=props)
    else:
        return err_return("Model not found: " + str(model_id))
