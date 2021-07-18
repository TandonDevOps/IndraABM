"""
This is the test suite for model.py.
"""

from unittest import TestCase, main, skip

from lib.model import DEF_GRP, BLUE_GRP_NM, RED_GRP_NM, DEF_GRP_STRUCT
import model as mdl

from lib.agent import Agent, DONT_MOVE
from lib.env import Env
from lib.group import Group
from lib.user import User
from registry.registry import get_agent

MSG = "Hello world"

GRID_HT_NM = "grid_height"
GRID_HT_VAL = 40

PROPS_DICT = {
    GRID_HT_NM: {
        "val": GRID_HT_VAL,
        "question": "What is the grid height?",
        "atype": "INT",
        "hival": 100,
        "lowval": 2
    },
    "grid_width": {
        "val": GRID_HT_VAL,
        "question": "What is the grid width?",
        "atype": "INT",
        "hival": 100,
        "lowval": 2
    },
}

class ModelTestCase(TestCase):
    def setUp(self):
        self.model = mdl.Model(model_nm="Test model",
                              grp_struct=DEF_GRP_STRUCT,
                              props=PROPS_DICT)
        self.exec_key = self.model.exec_key
        self.agent = Agent("Test agent", exec_key=self.model.exec_key)
        self.agent2 = Agent("Test agent 2", exec_key=self.model.exec_key)
        self.blue_grp = get_agent(BLUE_GRP_NM, self.exec_key)
        self.red_grp = get_agent(RED_GRP_NM, self.exec_key)

    def tearDown(self):
        self.agent = None
        self.model = None
        self.agent2 = None
        self.blue_grp = None
        self.red_grp = None

    def test_get_prop(self):
        """
        See if we can get a property val OK.
        """
        self.assertEqual(self.model.get_prop(GRID_HT_NM),
                         GRID_HT_VAL)
        # now see if we get default when prop does not exist:
        self.assertEqual(self.model.get_prop("Not a prop!", 17),
                         17)

    def test_pending_switches(self):
        """
        Test getting count of pending switches.
        """
        self.model.add_switch(self.agent.name, BLUE_GRP_NM, RED_GRP_NM)
        self.model.add_switch(self.agent2.name, BLUE_GRP_NM, RED_GRP_NM)
        self.assertEqual(self.model.pending_switches(), 2)

    def test_add_switch(self):
        """
        Test adding a group switch.
        """
        self.model.add_switch(self.agent.name, BLUE_GRP_NM, RED_GRP_NM)
        self.assertIn((self.agent.name, BLUE_GRP_NM, RED_GRP_NM),
                      self.model.switches)

    def test_handle_switches(self):
        """
        Does executing the pending switches work?
        """
        self.red_grp += self.agent
        self.assertIn(self.agent.name, self.red_grp)
        self.model.add_switch(self.agent.name, RED_GRP_NM, BLUE_GRP_NM)
        self.model.handle_switches()
        self.assertNotIn(self.agent.name, self.red_grp)
        self.assertIn(self.agent.name, self.blue_grp)

    def test_create_env(self):
        """
        Test creating an env.
        """
        env = self.model.create_env()
        self.assertTrue(isinstance(env, Env))

    def test_create_groups(self):
        """
        Test creating groups.
        """
        groups = self.model.create_groups()
        self.assertTrue(isinstance(groups, list))

    def test_create_user(self):
        """
        Test creating a user.
        """
        user = self.model.create_user()
        self.assertTrue(isinstance(user, User))

    def test_to_json(self):
        rep = self.model.to_json()
        self.assertTrue(isinstance(rep, dict))


if __name__ == '__main__':
    main()
