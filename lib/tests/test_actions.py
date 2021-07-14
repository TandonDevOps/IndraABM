"""
Tests for the actions module.
"""

from unittest import TestCase

import lib.actions as acts
import lib.agent as agt

class ActionsTestCase(TestCase):
    def setUp(self):
        # We will just fake an exec key for this agent:
        self.agent = agt.Agent("Test agent", exec_key=0)

    def test_def_action(self):
        """
        Test our default agent action.
        """
        self.assertEqual(agt.DONT_MOVE, acts.def_action(self.agent))
