"""
This is the test suite for basic.py.
"""

import lib.actions as acts
from lib.display_methods import RED
from lib.agent import Agent
from unittest import TestCase, skip  # , main

from models.segregation import (
    Segregation,
    agent_action,
    env_favorable,
    get_tolerance,
    main,
    MODEL_NAME,
    MAX_TOL,
    MIN_TOL,
    DEF_TOLERANCE,
    DEF_SIGMA,
    BLUE_AGENTS,
    RED_AGENTS,
    segregation_grps
)


class SegregationTestCase(TestCase):
    def setUp(self):
        self.segregation = Segregation(MODEL_NAME, grp_struct=segregation_grps)
        self.blue = Agent(name="blue", exec_key=self.segregation.exec_key)
        self.red = Agent(name="red", exec_key=self.segregation.exec_key)

    def tearDown(self):
        self.segregation = None

    def test_run(self):
        """
        Does running the model work? (return of 0)
        """
        self.assertEqual(0, self.segregation.run())

    def test_main(self):
        """
        Does the main func of the model work? (return of 0)
        """
        self.assertEqual(0, main())

    def test_get_tolerance(self):
        """
        Does the get_tolerance func return a value between MAX_TOL and MIN_TOL
        """
        self.assertTrue(MIN_TOL <= get_tolerance(DEF_TOLERANCE, DEF_SIGMA) <= MAX_TOL)

    def test_env_favorable(self):
        """
        Does the env_favorable return the correct value?
        (The numbers used for tests are arbitrary.)
        """
        self.assertIsInstance(env_favorable(hood_ratio=0.8, my_tolerance=0.2), bool)
        self.assertTrue(env_favorable(hood_ratio=0.8, my_tolerance=0.2))
        self.assertIsInstance(env_favorable(hood_ratio=0.3, my_tolerance=0.5), bool)
        self.assertFalse(env_favorable(hood_ratio=0.3, my_tolerance=0.5))

    def test_agent_action(self):
        """
        Does the agent action work?
        """
        self.assertIn(agent_action(self.blue), (acts.MOVE, acts.DONT_MOVE))
        self.assertIn(agent_action(self.red), (acts.MOVE, acts.DONT_MOVE))
