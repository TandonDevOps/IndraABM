"""
This file defines User, which represents a user in our system.
"""
import json
import os
from abc import abstractmethod

# from IPython import embed

from lib.agent import Agent
from lib.utils import PA_INDRA_HOME

TERMINAL = "terminal"
TEST = "test"
API = "api"
GUI = "gui"
CANT_ASK_TEST = "Can't ask anything of a scripted test"
DEF_STEPS = 1
DEFAULT_CHOICE = '1'
USER_EXIT = -999

MENU_SUBDIR = "lib"
indra_home = os.getenv("INDRA_HOME", PA_INDRA_HOME)
menu_dir = f"{indra_home}/{MENU_SUBDIR}"
menu_file = "menu.json"
menu_src = menu_dir + "/" + menu_file

ACTIVE = "active"
RADIO_SET = "radio_set"
FUNC = "func"

SCATTER_PLOT = "scatter_plot"
LINE_GRAPH = "line_graph"
BAR_GRAPH = "bar_graph"


def get_menu_json():
    menu_json = None
    try:
        with open(menu_src, 'r') as f:
            menu_db = json.load(f)
            menu_json = menu_db["menu_database"]
    except FileNotFoundError:
        print("Could not open menu file:", menu_src)
    return menu_json


def run(user, test_run=False):
    """
    Run the model for the number of periods the user wants.
    """
    if not test_run:
        steps = user.ask("How many periods?")
        if steps is None or steps == "" or steps.isspace():
            steps = DEF_STEPS
        else:
            steps = int(steps)
            user.tell("Steps = " + str(steps))
    else:
        steps = DEF_STEPS

    acts = 0
    if user.model is not None:
        print("In user, calling model to run {} steps.".format(steps))
        acts = user.model.runN(steps)
    return acts


def leave(user, **kwargs):
    user.tell("Goodbye, " + user.name + ", I will miss you!")
    return USER_EXIT


def scatter_plot(user, update=False):
    from registry.registry import get_model
    return get_model(user.exec_key).scatter_plot()


def line_graph(user, update=False):
    from registry.registry import get_model
    return get_model(user.exec_key).line_graph()


def bar_graph(user, update=False):
    from registry.registry import get_model
    return get_model(user.exec_key).bar_graph()


def view_model(user, update=False):
    from registry.registry import get_model
    return user.debug(repr(get_model(user.exec_key)))


menu_functions = {
    "run": run,
    "leave": leave,
    SCATTER_PLOT: scatter_plot,
    LINE_GRAPH: line_graph,
    BAR_GRAPH: bar_graph,
    "view_model": view_model,
}


class User(Agent):
    """
    A representation of the user in the system.
    It is an abstract class!
    """

    def __init__(self, name="User", model=None, **kwargs):
        super().__init__(name, **kwargs)
        self.menu = get_menu_json()
        self.user_msgs = ''
        self.debug_msg = ''
        self.error_message = {}
        self.model = model
        if 'serial_obj' in kwargs:
            self.from_json(kwargs['serial_obj'])

    def __call__(self):
        """
        Can't present menu to a scripted test!
        """
        run(self, self.model)

    def to_json(self):
        json_rep = super().to_json()
        json_rep["user_msgs"] = self.user_msgs
        json_rep["debug"] = self.debug_msg
        json_rep["name"] = self.name
        return json_rep

    def from_json(self, serial_obj):
        """
        This must be written!
        """
        super().from_json(serial_obj)
        self.user_msgs = serial_obj['user_msgs']
        self.name = serial_obj['name']
        self.debug_msg = serial_obj['debug']

    def exclude_menu_item(self, to_exclude):
        """
        This will immediately remove an item from the menu.
        """
        to_del = -1  # just some invalid index!
        if self.menu is not None:
            for index, item in enumerate(self.menu):
                if item["func"] == to_exclude:
                    to_del = index
            if to_del >= 0:
                del self.menu[to_del]

    @abstractmethod
    def tell(self, msg, end='\n'):
        """
        How to tell the user something.
        """
        pass

    @abstractmethod
    def ask(self, msg, default=None):
        """
        How to ask the user something.
        """
        pass

    def log(self, msg):
        """
        By default log just does whatever tell() does.
        """
        self.tell(msg)

    def tell_err(self, msg, end='\n'):
        self.tell("ERROR: " + msg, end)

    def tell_warn(self, msg, end='\n'):
        self.tell("WARNING: " + msg, end)


class TermUser(User):
    """
    A representation of the user on a terminal.
    """

    def __init__(self, name=TERMINAL, **kwargs):
        super().__init__(name, **kwargs)
        self.menu_title = "Menu of Actions"
        self.stars = "*" * len(self.menu_title)
        self.exclude_menu_item("source")
        self.show_line_graph = False
        self.show_scatter_plot = False
        self.show_bar_graph = False
        if 'serial_obj' in kwargs:
            self.from_json(kwargs['serial_obj'])
        self.graph_options = [LINE_GRAPH, BAR_GRAPH, SCATTER_PLOT]

    def tell(self, msg, end='\n'):
        """
        How to tell the user something.
        """
        print(msg, end=end)  # noqa E999
        return msg

    def debug(self, msg, end='\n'):
        self.tell(msg, end)
        return msg

    def ask(self, msg, default=None):
        """
        How to ask the user something.
        """
        self.tell(msg, end=' ')
        choice = input()
        if not choice:
            return default
        else:
            return choice

    def log(self, msg, end='\n'):
        """
        How to log something for this type of user.
        Our default is going to be the same as tell, for now!
        """
        return self.tell(msg, end)

    def is_number(self, c):
        """
        Check if `c` is a number.
        """
        try:
            int(c)
            return True
        except ValueError:
            return False

    def to_json(self):
        json_rep = super().to_json()
        json_rep["user_msgs"] = self.user_msgs
        json_rep["debug"] = self.debug_msg
        json_rep["name"] = self.name
        return json_rep

    def from_json(self, serial_obj):
        super().from_json(serial_obj)

    def get_opt_by_func_nm(self, func_nm):
        """
        For now we have this awkward business of fetching by func
        name.
        """
        for menu_opt in self.menu:
            if menu_opt[FUNC] == func_nm:
                return menu_opt
        return None

    def get_radio(self, item):
        return item.get(RADIO_SET, False)

    def __call__(self):
        self.tell('\n' + self.stars + '\n' + self.menu_title + '\n'
                  + self.stars)
        for item in self.menu:
            print(str(item["id"]) + ". ", item["question"])
        for func_nm in self.graph_options:
            opt = self.get_opt_by_func_nm(func_nm)
            if opt is not None and opt[ACTIVE]:
                menu_functions[func_nm](self, update=True)
        self.tell("Please choose a number from the menu above:")
        c = input()
        if not c or c.isspace():
            c = DEFAULT_CHOICE
        if self.is_number(c):
            choice = int(c)
            if choice >= 0:
                for item in self.menu:
                    if item["id"] == choice:
                        if self.get_radio(item):
                            self.set_radio_options(item)
                        return menu_functions[item[FUNC]](self)
            self.tell_err(str(c) + " is an invalid option. "
                          + "Please enter a valid option.")
        else:
            self.tell_err(str(c) + " is an invalid option. "
                          + "Please enter a valid option.")

    def set_radio_options(self, item):
        radio_set = item[RADIO_SET]
        item[ACTIVE] = True
        for opt in self.menu:
            if (opt is not item and self.get_radio(opt) == radio_set):
                opt[ACTIVE] = False


class TestUser(TermUser):
    """
        This is our test user, who has some characteristics different from the
        terminal user, such as overriding ask() and __call__().
    """

    def ask(self, msg, default=None):
        """
        Can't ask anything of a scripted test!
        """
        return self.tell(CANT_ASK_TEST, end=' ')


class APIUser(User):
    """
    This is our web user, who is expected to communicate with a web page
    frontend.
    This class needs from_json() and to_json() methods.
    """

    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        if 'serial_obj' in kwargs is not None:
            self.from_json(kwargs['serial_obj'])

    def tell(self, msg, end='\n'):
        """
        Tell the user something by showing it on the web page
        """
        self.user_msgs += (msg + end)
        return msg

    def log(self, msg):
        """
        When running on a server, `print()` ought to write to the
        log. But let's also add the logging messages to return to
        the front-end.
        """
        self.debug_msg += (msg + '\n')
        print(msg)

    def debug(self, msg, end='\n'):
        """
        Tell the user some debug info.
        """
        self.debug_msg += (msg + end)
        return msg

    def ask(self, msg, default=None):
        """
        Ask the user something and present it to the web page
        """
        # Some json thing
        pass

    def __call__(self, menuid=None):
        menu_id = menuid
        menu = get_menu_json()
        if menu_id is None:
            return menu

    def to_json(self):
        json_rep = super().to_json()
        json_rep["user_msgs"] = self.user_msgs
        json_rep["debug"] = self.debug_msg
        json_rep["name"] = self.name
        return json_rep

    def from_json(self, serial_obj):
        super().from_json(serial_obj)
