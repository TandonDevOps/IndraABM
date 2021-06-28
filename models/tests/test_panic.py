"""
This is the test suite for panic.py.
"""

from unittest import TestCase, skip  # , main
from lib.agent import DONT_MOVE
from lib.agent import Agent
from models.panic import Panic, main, MODEL_NAME, panic_grps, agent_action


class PanicTestCase(TestCase):
    def setUp(self):
        self.panic = Panic(MODEL_NAME, grp_struct=panic_grps, random_placing=False)
        self.calm_agent = Agent(name="calm",
                                     exec_key=self.panic.exec_key)
        self.panic_agent = Agent(name="panic",
                                     exec_key=self.panic.exec_key)

    def tearDown(self):
        self.panic = None

    def test_agent_action(self):
        self.assertEqual(DONT_MOVE, agent_action(self.calm_agent))

    def test_run(self):
        """
        Does running the model work? (return of 0)
        """
        self.assertEqual(0, self.panic.run())

    def test_main(self):
        """
        Does the main func of the model work? (return of 0)
        """
        self.assertEqual(0, main())
