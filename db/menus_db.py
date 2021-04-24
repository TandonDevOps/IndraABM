"""
This module interfaces to the menus database.
"""

import json
import lib.utils as utl

DB_DIR = "db"
MODEL_MENU = "model_menu.json"
MODEL_MENU_PATH = "/" + DB_DIR + "/" + MODEL_MENU
DEBUG_MENU = "debug_menu.json"
DEBUG_MENU_PATH = "/" + DB_DIR + "/" + DEBUG_MENU

DEF_INDRA_HOME = utl.get_indra_home()


def get_menu(menu_file):
    try:
        with open(menu_file) as file:
            return json.loads(file.read())
    except FileNotFoundError:
        return None


def get_debug_menu(indra_dir=DEF_INDRA_HOME):
    """
    Return the debug menu.
    """
    return get_menu(indra_dir + DEBUG_MENU_PATH)


def get_model_menu(indra_dir=DEF_INDRA_HOME):
    """
    Return the model menu.
    """
    return get_menu(indra_dir + MODEL_MENU_PATH)
