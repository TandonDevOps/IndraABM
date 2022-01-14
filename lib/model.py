"""
This module contains the code for the base class of all Indra models.
"""
import json
import sys
from optparse import OptionParser
from propargs.propargs import PropArgs
from APIServer import model_singleton

import lib.actions as acts
import lib.env as env
import lib.user as user
import uuid

DEBUG = acts.DEBUG

PROPS_PATH = "./props"
DEF_TIME = 10
DEF_NUM_MEMBERS = 1
TEST_EXEC_KEY = '0'

# the following are the standard names to use in props for grid dims:
GRID_HEIGHT = "grid_height"
GRID_WIDTH = "grid_width"

NUM_MBRS = "num_mbrs"
MBR_CREATOR = "mbr_creator"
MBR_ACTION = "mbr_action"
GRP_ACTION = "grp_action"
NUM_MBRS_PROP = "num_mbrs_prop"
COLOR = "color"


DEF_GRP_NM = "def_grp"
BLUE_GRP_NM = DEF_GRP_NM
RED_GRP_NM = "red_grp"

# The following is the template for how to specify a model's groups...
# We may want to make this a class one day.
DEF_GRP = {
    MBR_CREATOR: acts.create_agent,
    GRP_ACTION: None,
    MBR_ACTION: acts.def_action,
    NUM_MBRS: DEF_NUM_MEMBERS,
    NUM_MBRS_PROP: None,
    COLOR: acts.BLUE,
}

BLUE_GRP = DEF_GRP

RED_GRP = {
    MBR_CREATOR: acts.create_agent,
    GRP_ACTION: None,
    MBR_ACTION: acts.def_action,
    NUM_MBRS: DEF_NUM_MEMBERS,
    NUM_MBRS_PROP: None,
    COLOR: acts.RED,
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
    well as a `run()` method that will run the model,
    display the menu (if on a terminal), and register all
    methods necessary to be registered for the API server
    to work properly.
    It should also make the notebook generator much simpler,
    since the class methods will necessarily be present.
    """

    # NOTE: random_placing needs to be handled on the API side
    def __init__(self, model_nm="model", props=None,
                 grp_struct=DEF_GRP_STRUCT, exec_key=None,
                 env_action=None, random_placing=True, create_for_test=False):
        model_singleton.instance = self
        self.num_switches = 0
        self.agents = {}
        # set stat output to stdout by default
        self.stat_file = None
        self.runs = None
        self.steps = None
        self.module = model_nm
        self.grp_struct = grp_struct
        self.handle_props(props)
        if(create_for_test):
            self.exec_key = TEST_EXEC_KEY
        else:
            self.exec_key = str(uuid.uuid4())
        self.create_user()
        if not self.is_test_user() and not self.is_api_user():
            self.handle_args()
        self.groups = self.create_groups()
        self.env = self.create_env(env_action=env_action,
                                   random_placing=random_placing)
        self.switches = []  # for agents waiting to switch groups
        self.period = 0
        self.stats = ""

    def handle_args(self):
        parser = OptionParser(usage='usage: %prog [options] arguments')
        parser.add_option('-s', dest='filename')
        parser.add_option('-r', dest='runs')
        parser.add_option('-n', dest='steps')
        (options, args) = parser.parse_args()
        if options.filename:
            self.stat_file = options.filename
        if options.runs:
            self.runs = options.runs
        if options.steps:
            self.steps = options.steps

    def handle_props(self, props, model_dir=None):
        """
        A generic parameter handling method.
        We get height and width here, since so many models use them.
        """
        self.user_type = acts.get_user_type(user.API)
        if self.user_type == user.API:
            self.props = acts.init_props(self.module,
                                         props,
                                         model_dir=model_dir,
                                         skip_user_questions=True)
        else:
            self.props = acts.init_props(self.module,
                                         props, model_dir=model_dir)
        self.height = self.props.get(GRID_HEIGHT, acts.DEF_HEIGHT)
        self.width = self.props.get(GRID_WIDTH, acts.DEF_WIDTH)

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
        self.user = user.APIUser(model=self, name="API",
                                 exec_key=self.exec_key,
                                 serial_obj=jrep["user"])
        self.user_type = jrep["user_type"]
        if isinstance(jrep["props"], dict):
            self.props = PropArgs.create_props(self.module,
                                               prop_dict=jrep["props"])
        else:
            self.props = None
        self.env = env.Env(self.module, serial_obj=jrep["env"],
                           exec_key=self.exec_key)
        # since self.groups is a list and self.env.members is an OrderedDict:
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
        """
        This returns a JSON representation of the model.
        """
        return json.dumps(self.to_json(), cls=acts.AgentEncoder, indent=4)

    def get_prop(self, prop_nm, default=None):
        """
        Have a way to get a prop through the model to hide props structure.
        """
        if self.props is None:
            return default
        else:
            return self.props.get(prop_nm, default)

    def is_test_user(self):
        return self.user_type == user.TEST

    def is_api_user(self):
        return self.user_type == user.API

    def create_user(self):
        """
        This will create a user of the correct type.
        """
        self.user = None
        self.user_type = acts.get_user_type(user.API)
        try:
            if self.user_type == user.TERMINAL:
                self.user = user.TermUser(model=self, exec_key=self.exec_key)
                self.user.tell("Welcome to Indra, " + str(self.user) + "!")
            elif self.user_type == user.TEST:
                self.user = user.TestUser(model=self, exec_key=self.exec_key)
            elif self.user_type == user.BATCH:
                self.user = user.BatchUser(model=self, exec_key=self.exec_key)
            else:
                self.user = user.APIUser(model=self, exec_key=self.exec_key)
            return self.user
        except ValueError:
            raise ValueError("User type was not specified.")

    def get_locations(self):
        return self.env.get_locations()

    def get_user_msgs(self):
        return self.user.get_msgs()

    def create_env(self, env_action=None, random_placing=True):
        """
        Override this method to create a unique env...
        but this one will already set the model name and add
        the groups.
        """
        self.env = env.Env(self.module, members=self.groups,
                           exec_key=self.exec_key, width=self.width,
                           height=self.height, action=env_action,
                           random_placing=random_placing)
        self.env.user = self.user
        self.env.user_type = self.user_type
        self.create_pop_hist()
        return self.env

    def create_pop_hist(self):
        """
        There are several methods that still (like in V2) reside in
        Env, but which we mean to move to Model. So we provide an interface to
        them here so when we move them other code won't break.
        `create_pop_hist()` is such a method.
        """
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
            self.groups.append(acts.Group(grp_nm,
                                          action=grp_val(grp, GRP_ACTION),
                                          color=grp_val(grp, COLOR),
                                          num_mbrs=num_mbrs,
                                          mbr_creator=grp_val(grp,
                                                              MBR_CREATOR),
                                          mbr_action=grp_val(grp, MBR_ACTION),
                                          exec_key=self.exec_key))
        return self.groups

    def get_periods(self):
        return self.env.get_periods()

    def run(self, periods=None):
        """
        This method runs the model. If `periods` is not None,
        it will run it for that many periods. Otherwise, on
        a terminal, it will display the menu.
        Return: 0 if run was fine.
        """
        if not self.user.is_interactive() and not self.user.is_batch:
            self.runN()
            self.collect_stats()
            self.rpt_stats()

        elif not self.user.is_interactive() and self.user.is_batch:
            if self.runs is not None and self.steps is not None:
                self.run_batch(int(self.runs), int(self.steps))
            else:
                self.runN()
        else:
            self.user.tell("Running model " + self.module)
            while True:
                # run until user exit!
                if self.user() == user.USER_EXIT:
                    break
            self.collect_stats()
            self.rpt_stats()
        return 0

    def run_batch(self, runs, steps):
        """
            Run our model for N periods X steps.
            Writes the period specific model statistics to a CSV file.
            Files are saved as input filename-[integer-counter].csv
            Returns the total number of actions taken.
        """
        acts = 0
        print("model will run {} times with {} steps.".format(runs, steps))
        self.base_file = str(self.stat_file).split(".")[0]
        for i in range(runs):
            print("\n\n\n**** Batch run {} ****".format(i))
            self.stats = ""
            self.stat_file = str(self.base_file) + "-" + str(i) + ".csv"
            acts += self.runN(steps)
            self.collect_stats()
            self.rpt_stats()
        return acts

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

    def reg_agent(self, name, agent):
        self.agents[name] = agent

    def get_agent(self, name):
        return self.agents[name]

    def handle_womb(self):
        """
        This method adds new agents from the womb.
        The womb should move up into model eventually.
        """
        self.env.handle_womb()

    def add_child(self, group):
        """
        Put a child agent in the womb.
        group: which group will add new agent
        The womb should move up into model eventually.
        """
        self.env.add_child(group)

    def get_pop_hist(self):
        return self.env.get_pop_hist()

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
                acts.switch(agent_nm, from_grp_nm, to_grp_nm)

                self.num_switches += 1
            self.switches.clear()
        pass

    def line_graph(self):
        self.env.line_graph()

    def bar_graph(self):
        self.env.bar_graph()

    def scatter_plot(self):
        self.env.scatter_plot()

    def collect_stats(self):
        self.stats = "No statistics to report for this model."

    def rpt_stats(self):
        """
        This is a "wrap up" report on the results of a model run.
        Each model can do what it wants here.
        perhaps will take an iterator object?
        a file?
        Function takes in a CSV formatted string from function
        collect_stats() and writes it to a csv file.

        Note: added logic so func will not write to stdout
        """
        if self.stat_file and self.stat_file != sys.stdout:
            with open(str(self.stat_file), 'w') as f:
                f.write(str(self.stats))
            print(str(self.stat_file) + " saved")


def main():
    model = Model()
    model.run()
    return 0


if __name__ == "__main__":
    main()
