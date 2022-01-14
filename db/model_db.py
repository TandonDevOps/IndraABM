# This module handles the models portion of the API server.

import json

from localutils.env import env

MODEL_DB_DIR = "db"
MODELS_DB = "models.json"
MODEL_PATH = f"/{MODEL_DB_DIR}/{MODELS_DB}"
MODEL_ID = "modelID"
MODEL_MOD = "module"
MODEL_NAME = "name"


def get_models(active_only=False):
    """
    Return a list of available models.
    If `active_only` is True, only return active models.
    """
    model_file = env.indra_dir + MODEL_PATH
    try:
        with open(model_file) as file:
            ml = json.loads(file.read())
            if active_only:
                ml = [model for model in ml if model['active']]
            return ml
    except FileNotFoundError:
        return None


def get_model_by_name(model_name):
    """
    Fetch a model from model db by name.
    :param model_name:
    :param indra_dir:
    :return: model config
    """
    models_db = get_models(env.indra_dir)
    if models_db is None:
        return None
    for model in models_db:
        if model[MODEL_NAME] == model_name:
            return model
    return None


def get_model_by_id(model_id):
    """
    Fetch a model from the model db by id.
    """
    models_db = get_models(env.indra_dir)
    if models_db is None:
        return None
    for model in models_db:
        if int(model[MODEL_ID]) == model_id:
            return model
    return None


def get_model_by_mod(mod):
    """
    Fetch a model from the model db by module name.
    """
    models_db = get_models(env.indra_dir)
    if models_db is None:
        return None
    for model in models_db:
        if model[MODEL_MOD] == mod:
            return model
    return None
