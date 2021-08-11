"""
This file contains functions dealing with getting source code from a repo.
"""
import db.model_db as model_db
from lib.utils import get_indra_home

indra_dir = get_indra_home()


def path_from_model(model):
    return '/' + model.get('package') + '/' + model.get('module') + '.py'


def get_source_code(model_id):
    """
    Return the source code for a model.
    """
    model = model_db.get_model_by_id(model_id, indra_dir)
    if model is None:
        return None
    path = path_from_model(model)
    try:
        file = open(indra_dir + path)
        source_code = file.read()
        file.close()
        return source_code
    except OSError:
        return None
