"""
This module contains the code for the base class of all Indra models.
"""
import os
import json

from lib.utils import init_props, Debug
from lib.agent import Agent, DONT_MOVE, switch, AgentEncoder
from lib.group import Group
from lib.env import Env
from lib.space import DEF_WIDTH, DEF_HEIGHT
from lib.user import TestUser, TermUser, API, APIUser, TERMINAL, TEST
from lib.user import USER_EXIT
from lib.display_methods import RED, BLUE
from registry import registry

DEBUG = Debug()

PROPS_PATH = "./props"
DEF_TIME = 10
DEF_NUM_MEMBERS = 1

# the following are the standard names to use in props for grid dims:
GRID_HEIGHT = "grid_height"
GRID_WIDTH = "grid_width"

NUM_MBRS = "num_mbrs"
MBR_CREATOR = "mbr_creator"
MBR_ACTION = "mbr_action"
GRP_ACTION = "grp_action"
NUM_MBRS_PROP = "num_mbrs_prop"
COLOR = "color"


def def_action(agent, **kwargs):
    """
    A simple default agent action.
    """
    if DEBUG.debug_lib:
        print("Agent {} is acting".format(agent.name))
    return DONT_MOVE


def create_agent(name, i, action=None, **kwargs):
    """
    Create an agent that does almost nothing.
    """
    return Agent(name + str(i), action=action, **kwargs)


DEF_GRP_NM = "def_grp"
BLUE_GRP_NM = DEF_GRP_NM
RED_GRP_NM = "red_grp"

# The following is the template for how to specify a model's groups...
# We may want to make this a class one day.
DEF_GRP = {
    MBR_CREATOR: create_agent,
    GRP_ACTION: None,
    MBR_ACTION: def_action,
    NUM_MBRS: DEF_NUM_MEMBERS,
    NUM_MBRS_PROP: None,
    COLOR: BLUE,
}

BLUE_GRP = DEF_GRP

RED_GRP = {
    MBR_CREATOR: create_agent,
    GRP_ACTION: None,
    MBR_ACTION: def_action,
    NUM_MBRS: DEF_NUM_MEMBERS,
    NUM_MBRS_PROP: None,
    COLOR: RED,
}

DEF_GRP_STRUCT = {
    DEF_GRP_NM: DEF_GRP,
    RED_GRP_NM: RED_GRP,
}


def grp_val(grp, key):
    """
    Let's have a function that fill in defaults if a model
    fails to specify any of the above group properties.
    """
    return grp.get(key, DEF_GRP[key])


class Model():
    """
    This class is the base class for all Indra models.
    It will have all of the basic methods a model needs, as
    well as a `run()` method that will kick of the model,
    display the menu (if on a terminal), and register all
    methods necessary to be registered for the API server
    to work properly.
    It should also make the notebook generator much simpler,
    since the class methods will necessarily be present.
    """

    # NOTE: random_placing needs to be handled on the API side
    def __init__(self, model_nm="BaseModel", props=None,
                 grp_struct=DEF_GRP_STRUCT,
                 env_action=None, random_placing=True,
                 serial_obj=None, exec_key=None, create_for_test=False):
        self.num_switches = 0
        if serial_obj is None:
            self.create_anew(model_nm, props, grp_struct, exec_key,
                             env_action, random_placing, create_for_test)
        else:
            self.create_from_serial_obj(serial_obj)

    def create_anew(self, model_nm, props, grp_struct, exec_key,
                    env_action, random_placing, create_for_test=False):
        """
        Create the model for the first time.
        """
        self.module = model_nm
        self.grp_struct = grp_struct
        self.handle_props(props)
        if exec_key is not None:
            self.exec_key = exec_key
        elif self.props.get("exec_key", None) is not None:
            self.exec_key = self.props.get("exec_key")
        else:
            self.exec_key = registry.create_exec_env(
                create_for_test=create_for_test)
        self.create_user()
        registry.reg_model(self, self.exec_key)
        self.groups = self.create_groups()
        self.env = self.create_env(env_action=env_action,
                                   random_placing=random_placing)
        self.switches = []  # for agents waiting to switch groups
        self.period = 0

    def handle_props(self, props, model_dir=None):
        self.user_type = os.getenv("user_type", API)
        if self.user_type == API:
            self.props = init_props(self.module, props, model_dir=model_dir,
                                    skip_user_questions=True)
        else:
            self.props = init_props(self.module, props, model_dir=model_dir)
        self.height = self.props.get(GRID_HEIGHT, DEF_HEIGHT)
        self.width = self.props.get(GRID_WIDTH, DEF_WIDTH)

    def create_from_serial_obj(self, serial_obj):
        """
        Restore the model from its serialized version.
        """
        self.from_json(serial_obj)

    def from_json(self, jrep):
        """
        This method restores a model from its JSON rep.
        """
        self.module = jrep["module"]
        self.exec_key = jrep["exec_key"]
        self.period = jrep["period"]
        self.switches = jrep["switches"]
        # We should restore user from json:
        # self.user = jrep["user"]
        # But for the moment we will hard code this:
        self.user = APIUser(model=self, name="API",
                            exec_key=self.exec_key, serial_obj=jrep["user"])
        self.user_type = jrep["user_type"]
        self.props = jrep["props"]
        self.env = Env(self.module, serial_obj=jrep["env"],
                       exec_key=self.exec_key)
        # since self.groups is a list and self.env.members is an OrderedDict
        self.groups = [self.env.members[group_nm] for group_nm in
                       self.env.members]

    def to_json(self):
        """
        This method generates the JSON representation for this model.
        """
        jrep = {}
        jrep["module"] = self.module
        jrep["exec_key"] = self.exec_key
        jrep["period"] = self.period
        jrep["switches"] = self.switches
        jrep["user"] = self.user.to_json()
        jrep["user_type"] = self.user_type
        jrep["props"] = self.props
        jrep["env"] = self.env.to_json()
        jrep["type"] = "Model"
        return jrep

    def __str__(self):
        return self.module

    def __repr__(self):
        return json.dumps(self.to_json(), cls=AgentEncoder, indent=4)

    def create_user(self):
        """
        This will create a user of the correct type.
        """
        self.user = None
        self.user_type = os.getenv("user_type", API)
        try:
            if self.user_type == TERMINAL:
                self.user = TermUser(model=self, exec_key=self.exec_key)
                self.user.tell("Welcome to Indra, " + str(self.user) + "!")
            elif self.user_type == TEST:
                self.user = TestUser(model=self, exec_key=self.exec_key)
            else:  # right now API is the only other possibility
                self.user = APIUser(model=self, name="API",
                                    exec_key=self.exec_key)
            return self.user
        except ValueError:
            raise ValueError("User type was not specified.")

    def create_env(self, env_action=None, random_placing=True):
        """
        Override this method to create a unique env...
        but this one will already set the model name and add
        the groups.
        """
        # NOTE: WE DEFAULT TO RANDOM PLACING ALL THE TIME
        # EVEN FOR MODELS LIKE FOREST FIRE
        self.env = Env(self.module, members=self.groups,
                       exec_key=self.exec_key, width=self.width,
                       height=self.height, action=env_action,
                       random_placing=random_placing)
        self.env.user = self.user
        self.env.user_type = self.user_type
        self.create_pop_hist()
        return self.env

    def create_pop_hist(self):
        self.env.create_pop_hist()

    def create_groups(self):
        """
        Override this method in your model to create all of your groups.
        In general, you shouldn't need to: fill in the grp_struct instead.
        """
        self.groups = []
        grps = self.grp_struct
        for grp_nm in grps:
            grp = grps[grp_nm]
            num_mbrs = grp_val(grp, NUM_MBRS)
            if NUM_MBRS_PROP in grp:
                num_mbrs = self.props.get(grp[NUM_MBRS_PROP], num_mbrs)
            self.groups.append(Group(grp_nm,
                                     action=grp_val(grp, GRP_ACTION),
                                     color=grp_val(grp, COLOR),
                                     num_mbrs=num_mbrs,
                                     mbr_creator=grp_val(grp, MBR_CREATOR),
                                     mbr_action=grp_val(grp, MBR_ACTION),
                                     exec_key=self.exec_key))
        return self.groups

    def run(self, periods=None):
        """
        This method runs the model. If `periods` is not None,
        it will run it for that many periods. Otherwise, on
        a terminal, it will display the menu.
        Return: 0 if run was fine.
        """
        if (self.user is None) or (self.user_type == TEST) or (self.user_type
                                                               == API):
            self.runN()
        else:
            self.user.tell("Running model " + self.module)
            while True:
                # run until user exit!
                if self.user() == USER_EXIT:
                    break

        return 0

    def runN(self, periods=DEF_TIME):
        """
            Run our model for N periods.
            Return the total number of actions taken.
        """
        num_acts = 0
        num_moves = 0
        for i in range(periods):
            self.period += 1

            # now we call upon the env to act:
            if DEBUG.debug_lib:
                print("From model, calling env to act.")
            (num_acts, num_moves) = self.env()
            census_rpt = self.rpt_census(num_acts, num_moves)
            if DEBUG.debug_lib:
                print(census_rpt)
            self.user.tell(census_rpt)
            # these things need to be done before action loop:
            self.handle_switches()
            self.update_pop_hist()
            self.handle_womb()
        return num_acts

    def handle_womb(self):
        """
        This method adds new agents from the womb.
        """
        self.env.handle_womb()

    def add_child(self, group):
        """
        Put a child agent in the womb.
        group: which group will add new agent
        """
        self.env.add_child(group)

    def update_pop_hist(self):
        """
        This method records our populations each period.
        """
        self.env.handle_pop_hist()

    def rpt_census(self, acts, moves):
        """
        This is the default census report.
        Right now, `acts` is not used: do we need it?
        Return: a string saying what happened in a period.
        """
        ret = self.env.get_census(moves, self.num_switches)
        self.num_switches = 0
        return ret

    def pending_switches(self):
        """
        How many switches are there to execute?
        """
        return len(self.switches)

    def rpt_switches(self):
        """
        Generate a string to report our switches.
        """
        return "# switches = " + str(self.pending_switches()) + "; id: " \
               + str(id(self.switches))

    def add_switch(self, agent_nm, from_grp_nm, to_grp_nm):
        """
        Switch agent from 1 group to another.
        The agent and groups should be passed by name.
        """
        self.switches.append((agent_nm, from_grp_nm, to_grp_nm))

    def handle_switches(self):
        """
        This will actually process the pending switches.
        """
        if self.switches is not None:
            for (agent_nm, from_grp_nm, to_grp_nm) in self.switches:
                switch(agent_nm, from_grp_nm, to_grp_nm, self.exec_key)

                self.num_switches += 1
            self.switches.clear()
        pass

    def line_graph(self):
        self.env.line_graph()

    def bar_graph(self):
        self.env.bar_graph()

    def scatter_plot(self):
        self.env.scatter_plot()


def main():
    model = Model()
    model.run()
    return 0


if __name__ == "__main__":
    main()
