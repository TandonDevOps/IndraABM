# This module handles the models portion of the API server.

import json

REGISTRY = "registry"
MODELS_DB = "models.json"
MODEL_PATH = "/" + REGISTRY + "/" + MODELS_DB
MODEL_ID = "modelID"
MODEL_MOD = "module"


def get_models(indra_dir, active_only=False):
    """
    Return a list of available models.
    If `active_only` is True, only return active models.
    """
    model_file = indra_dir + MODEL_PATH
    try:
        with open(model_file) as file:
            ml = json.loads(file.read())
            if active_only:
                ml = [model for model in ml if model['active']]
            return ml
    except FileNotFoundError:
        return None


def get_model_by_id(model_id, indra_dir=''):
    """
    Fetch a model from the model db by id.
    """
    models_db = get_models(indra_dir)
    if models_db is None:
        return None
    for model in models_db:
        if int(model[MODEL_ID]) == model_id:
            return model
    return None


def get_model_by_mod(mod, indra_dir=''):
    """
    Fetch a model from the model db by module name.
    """
    models_db = get_models(indra_dir)
    if models_db is None:
        return None
    for model in models_db:
        if model[MODEL_MOD] == mod:
            return model
    return None
