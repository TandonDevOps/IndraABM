"""
This is the test suite for registry.py.
"""

from unittest import TestCase, skip
import os
from lib.agent import Agent
from lib.env import Env
from lib.model import Model, DEF_GRP, GRP_ACTION, COLOR, MBR_CREATOR
from registry.registry import registry, get_agent, reg_agent, MockModel
from registry.registry import get_env, del_agent, reg_model, get_model
from registry.registry import create_exec_env, TEST_EXEC_KEY
from unittest.mock import patch
from lib.display_methods import RED, BLUE
from lib.utils import PA_INDRA_NET, get_indra_home

TEST_VAL_STR = "test_val"
TEST_VAL = 1
TEST_AGENT_NM = "Test agent"
TEST_ENV_NM = "Test env"


class RegisteryTestCase(TestCase):
    def setUp(self):
        self.exec_key = registry.create_exec_env(save_on_register=True)
        self.already_cleared = False
        self.test_agent = Agent(TEST_AGENT_NM, exec_key=self.exec_key,
                                action=self.agent_action)

    def tearDown(self):
        if not self.already_cleared:
            registry.del_exec_env(self.exec_key)
        print(f"rm {registry.db_dir}/*json")
        os.system(f"rm {registry.db_dir}/*json")
        pkl_file = self.get_action_pkl_file()
        self.test_agent = None
        self.assertTrue(not os.path.exists(pkl_file))

    def get_action_pkl_file(self):
        pkl_file = os.path.join(registry.db_dir,
                                f'{self.exec_key}-{self.test_agent.name}-{self.agent_action.__name__}')
        return pkl_file

    def test_get_model(self):
        """
        Register a model and fetch it back.
        """
        self.model = Model(exec_key=self.exec_key)
        reg_model(self.model, self.exec_key)
        self.assertEqual(self.model, get_model(self.exec_key))

    def test_get_agent(self):
        """
        See if we get an agent we have registered back.
        """
        reg_agent(TEST_AGENT_NM, self.test_agent, self.exec_key)
        self.assertEqual(self.test_agent, get_agent(TEST_AGENT_NM,
                                                    self.exec_key))

    def test_get_env(self):
        """
        See if we get an env we have registered back as the env.
        """
        model = Model("Test model")
        self.assertEqual(model.env, get_env(exec_key=model.exec_key))

    def test_del_agent(self):
        """
        Test deleting an agent.
        """
        reg_agent(TEST_AGENT_NM, self.test_agent, self.exec_key)
        del_agent(TEST_AGENT_NM, self.exec_key)
        self.assertEqual(None,
                         get_agent(TEST_AGENT_NM, exec_key=self.exec_key))

    def test_registry_to_json(self):
        create_exec_env(create_for_test=True, exec_key=TEST_EXEC_KEY)
        reg_model(MockModel("Test model"), TEST_EXEC_KEY)
        json_rep = registry.to_json()
        self.assertIn(TEST_EXEC_KEY, json_rep)

    def test_registry_key_creation(self):
        self.assertTrue(self.exec_key in registry)

    def test_registration(self):
        registry[self.exec_key]["name"] = "Abhinav"
        self.assertTrue("name" in registry[self.exec_key])
        self.assertTrue("Abhinav" == registry[self.exec_key]["name"])

    @skip("Skipping load from disk test until rm reg problem resolved.")
    @patch('pickle.dump')
    @patch('pickle.load')
    def test_registry_saved_to_disk(self, dump, load):
        indra_dir = get_indra_home(PA_INDRA_NET)
        file_path = os.path.join(indra_dir, 'registry', 'db',
                                 '{}-reg.json'.format(self.exec_key))
        registry[self.exec_key]["name"] = "Abhinav"
        registry.save_reg(self.exec_key)
        self.assertTrue(os.path.exists(file_path))

    @skip("Skipping fetch from disk test until rm reg problem resolved.")
    @patch('pickle.dump')
    @patch('pickle.load')
    def test_registry_fetch_from_disk(self, dump, load):
        registry[self.exec_key]["name"] = "Abhinav"
        registry.save_reg(self.exec_key)
        loaded_object_name = get_agent("name", self.exec_key)
        self.assertTrue("Abhinav" == loaded_object_name)

    @patch('pickle.dump')
    @patch('pickle.load')
    def test_del_exec_env(self, dump, load):
        registry[self.exec_key]["name"] = "Abhinav"
        registry.save_reg(self.exec_key)
        registry.del_exec_env(self.exec_key)
        self.already_cleared = True
        self.assertRaises(KeyError, registry.del_exec_env, self.exec_key)
        self.assertTrue(not os.path.exists(self.get_action_pkl_file()))

    def test_agent_registration(self):
        agent = Agent("test_agent", action=None, exec_key=self.exec_key)
        registry[self.exec_key][agent.name] = agent
        self.assertTrue(agent == registry[self.exec_key][agent.name])

    def agent_action(self):
        print("Agent action")
        return True

    @patch('pickle.dump')
    def test_agent_save_to_disk(self, dump):
        agent = Agent("test_agent", action=self.agent_action,
                      exec_key=self.exec_key)
        registry[self.exec_key][agent.name] = agent
        registry.save_reg(self.exec_key)

    @skip("Skipping load from disk test until rm reg problem resolved.")
    @patch('pickle.dump')
    @patch('pickle.load')
    def test_agent_load_from_disk(self, dump, load):
        registry.save_reg(self.exec_key)
        registry.load_reg(self.exec_key)
        loaded_agent = get_agent(TEST_AGENT_NM, self.exec_key)
        (acted, moved) = loaded_agent()
        self.assertTrue(acted)
        self.assertTrue(not moved)

    @patch('pickle.dump')
    @patch('pickle.load')
    def test_should_only_pickle_once(self, dump, load):
        agent1 = Agent("test_agent1", action=self.agent_action,
                       exec_key=self.exec_key)
        agent2 = Agent("test_agent2", action=self.agent_action,
                       exec_key=self.exec_key)
        registry.save_reg(self.exec_key)
        self.assertTrue(registry[self.exec_key]['functions'] is not None)

        pickle_files = list(
            filter(lambda file: 'agent-agent_action.pkl' in file,
                   [value for value in registry[self.exec_key]
                   ['functions'].values()]))

        self.assertTrue(len(pickle_files) != 0)
        self.assertTrue(len(pickle_files) == 1)

    def complex_agent_action(self, agent, **kwargs):
        print("Complex Agent action")
        if agent.color == BLUE:
            for member in agent.members:
                agent[member].set_attr("value",
                                       agent[member].get_attr("value") * 2)

    def complex_agent_create(self, name, i, action=None, **kwargs):
        agent = Agent(name + str(i), action=action, **kwargs)
        agent.set_attr("value", 5)
        return agent

    @skip("Skipping load from disk test until rm reg problem resolved.")
    @patch('pickle.dump')
    @patch('pickle.load')
    def test_model_save_load_run_from_disk(self, dump, load):
        DEF_GRP[GRP_ACTION] = self.complex_agent_action
        DEF_GRP[MBR_CREATOR] = self.complex_agent_create
        SECOND_GRP = DEF_GRP.copy()
        SECOND_GRP[COLOR] = RED
        GRP_STRUCT = {
            "COMPLEX_RED_GRP": SECOND_GRP,
            "COMPLEX_BLUE_GRP": DEF_GRP
        }
        complexModel = Model(grp_struct=GRP_STRUCT, model_nm="Basic")
        complexModel.run(5)
        registry.save_reg(key=complexModel.exec_key)
        registry.load_reg(complexModel.exec_key)
        loaded_object = get_model(complexModel.exec_key)
        self.assertTrue(type(loaded_object) == Model)
        self.assertTrue("Basic" == loaded_object.module)
        all_red_members_have_attribute_5 = True
        all_blue_memebrs_have_attribute_10 = True
        deserialized_model = loaded_object
        deserialized_model.run(5)
        for grp in deserialized_model.groups:
            for member in grp.members:
                if grp.color == BLUE:
                    all_blue_memebrs_have_attribute_10 = \
                        all_blue_memebrs_have_attribute_10 and (
                                grp[member].get_attr("value") != 5)
                else:
                    all_red_members_have_attribute_5 = \
                        all_red_members_have_attribute_5 and (
                                grp[member].get_attr("value") == 5)

        self.assertTrue(all_red_members_have_attribute_5)
        self.assertTrue(all_blue_memebrs_have_attribute_10)
