"""
This file contains functions dealing with getting source code from a repo.
"""

import requests
from http import HTTPStatus

import registry.model_db as mdb
from lib.utils import get_indra_home

GITHUB_API = 'https://api.github.com/repos/'
SOURCE_CODE_URL = GITHUB_API + 'TandonDevOps/IndraABM/contents/'

indra_dir = get_indra_home()


def path_from_model(model):
    return model.get('package') + '/' + model.get('module') + '.py'


def get_source_code(model_id):
    """
    Return the source code for a model.
    """
    model = mdb.get_model_by_id(model_id, indra_dir)
    if model is None:
        return None
    path = path_from_model(model)
    codebase_response = requests.get(SOURCE_CODE_URL + path)
    if codebase_response.status_code == HTTPStatus.OK:
        return codebase_response.json()
    else:
        return None
