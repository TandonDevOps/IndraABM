"""
Tests for the actions module.
"""

from unittest import TestCase

import lib.actions as acts
import lib.agent as agt
import lib.group as grp
import lib.space as spc

TEST_AGENT = "test agent"


class ActionsTestCase(TestCase):
    def setUp(self):
        # We will just fake an exec key for this agent:
        self.agent = agt.Agent("Test agent", exec_key=None)
        self.group = grp.Group("Test group")

    def tearDown(self):
        self.agent = None

    def test_def_action(self):
        """
        Test our default agent action.
        """
        self.assertEqual(agt.DONT_MOVE, acts.def_action(self.agent))

    def test_create_agent(self):
        self.assertIsInstance(acts.create_agent(TEST_AGENT, 0,
                              exec_key=None),
                              agt.Agent)

    def test_def_action(self):
        """
        Test for default agent.
        """
        self.assertTrue(acts.def_action(self.agent))

    def test_join(self):
        """
        Test join.
        """
        self.assertTrue(acts.join(self.group, self.agent))
        agent_not_group = agt.Agent("Test agent for group",
                                     exec_key=None)
        self.assertFalse(acts.join(agent_not_group,self.agent))

    def test_is_group(self):
        """
        Test is_group
        """
        self.assertTrue(acts.is_group(self.group))
        self.assertFalse(acts.is_group(self.agent))

    def test_get_distance(self):
        """
        Test get_distance
        """
        agent_distance_test_1 = agt.Agent("Test agent 1", exec_key=None)
        agent_distance_test_2 = agt.Agent("Test agent 2", exec_key=None)
        self.assertEqual(acts.get_distance(agent_distance_test_1, agent_distance_test_2),
                        spc.FAR_AWAY)
        agent_distance_test_1.set_pos(0, 0)
        agent_distance_test_2.set_pos(0, 5)
        self.assertEqual(acts.get_distance(agent_distance_test_1, agent_distance_test_2),
                        5)

    def test_in_hood(self):
        """
        Test in_hood
        """
        agent_in_hood_test_1 = agt.Agent("Test agent 1", exec_key=None)
        agent_in_hood_test_2 = agt.Agent("Test agent 2", exec_key=None)
        agent_in_hood_test_1.set_pos(0, 0)
        agent_in_hood_test_2.set_pos(0, 5)
        self.assertTrue(acts.in_hood(agent_in_hood_test_1,
                                      agent_in_hood_test_2, 5))
        self.assertFalse(acts.in_hood(agent_in_hood_test_1,
                                      agent_in_hood_test_2, 4))
        
