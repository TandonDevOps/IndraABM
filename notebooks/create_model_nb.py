
"""
This script takes an Indra ABM model as input and outputs a notebook.
It writes stdout.
"""

import sys
import nbformat as nbf


USERTYPE_TXT = "Set ENV user_type to properly run the model in the notebook"


def set_user_type(curr_line, mdl_lines):
    content = ''
    content += 'import os\n'
    content += 'os.environ["user_type"] = "terminal"'
    return (curr_line, content.strip())


DOCSTRING_TXT = "A short description about this model."


def read_docstring(curr_line, mdl_lines):
    content = ""

    while not mdl_lines[curr_line].startswith("from ") \
            and not mdl_lines[curr_line].startswith("import "):
        content += mdl_lines[curr_line]
        curr_line += 1

    return (curr_line, content.strip())


IMPORT_TXT = "We import all necessary modules and functions from other files."


def read_imports(curr_line, mdl_lines):
    content = ""

    while mdl_lines[curr_line].startswith("from ") \
            or mdl_lines[curr_line].startswith("import ") \
            or mdl_lines[curr_line].startswith("\n"):
        content += mdl_lines[curr_line]
        curr_line += 1

    return (curr_line, content.strip())


CONSTANT_TXT = "These are the constants and global variables we used in this model."


def read_constants(curr_line, mdl_lines):
    content = ""

    while not mdl_lines[curr_line].startswith("def "):
        content += mdl_lines[curr_line]
        curr_line += 1

    return (curr_line, content.strip())


ACTIONS_CREATORS_TXT = "The following functions define some actions that our agents can make."


def read_actions_creators(curr_line, mdl_lines):
    content = ""

    while not mdl_lines[curr_line].endswith("_grps = {\n"):
        content += mdl_lines[curr_line]
        curr_line += 1

    return (curr_line, content.strip())


GRP_STRUCT_TXT = "This structure defines the groups that characterize our agents."


def read_grp_struct(curr_line, mdl_lines):
    content = ""

    while not mdl_lines[curr_line].startswith("class "):
        content += mdl_lines[curr_line]
        curr_line += 1

    return (curr_line, content.strip())


MODEL_CLASS_TXT = "We subclass `Model` to create our own variant of it."


def read_model_class(curr_line, mdl_lines):
    content = ""

    while not mdl_lines[curr_line].startswith("def create_model"):
        content += mdl_lines[curr_line]
        curr_line += 1

    return (curr_line, content.strip())


CREATE_MODEL_TXT = "Here's where we create the model class."


def read_create_model(curr_line, mdl_lines):
    content = ""

    while not mdl_lines[curr_line].startswith("def main"):
        content += mdl_lines[curr_line]
        curr_line += 1

    return (curr_line, content.strip())


MAIN_TXT = "The main function runs the whole model."


def read_main(curr_line, mdl_lines):
    content = ""

    while not mdl_lines[curr_line].startswith("if __name__"):
        content += mdl_lines[curr_line]
        curr_line += 1

    return (curr_line, content.strip())


CALLMAIN_TXT = "Now just call main!"


def call_main(curr_line, mdl_lines):
    content = ""

    while curr_line < len(mdl_lines):
        content += mdl_lines[curr_line]
        curr_line += 1

    return (curr_line, content.strip())


NB_STRUCT = [
    {"text": USERTYPE_TXT, "func": set_user_type},
    {"text": DOCSTRING_TXT, "func": read_docstring},
    {"text": IMPORT_TXT, "func": read_imports},
    {"text": CONSTANT_TXT, "func": read_constants},
    {"text": ACTIONS_CREATORS_TXT, "func": read_actions_creators},
    {"text": GRP_STRUCT_TXT, "func": read_grp_struct},
    {"text": MODEL_CLASS_TXT, "func": read_model_class},
    {"text": CREATE_MODEL_TXT, "func": read_create_model},
    {"text": MAIN_TXT, "func": read_main},
    {"text": CALLMAIN_TXT, "func": call_main},
]


def output_md_cell(nb, text):
    nb["cells"].append(nbf.v4.new_markdown_cell(text))


def output_code_cell(nb, code):
    nb["cells"].append(nbf.v4.new_code_cell(code))


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} [input file]")
        exit(1)

    mdl_path = sys.argv[1]
    with open(mdl_path, "r") as infile:
        mdl_lines = infile.readlines()

    nb = nbf.v4.new_notebook()
    curr_line = 0
    for section in NB_STRUCT:
        output_md_cell(nb, section["text"])
        (curr_line, code) = section["func"](curr_line, mdl_lines)
        output_code_cell(nb, code)
    print(nbf.writes(nb))


if __name__ == "__main__":
    main()
