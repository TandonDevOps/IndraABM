"""
This module registers agent objects by name in a dictionary,
where the value should be the actual agent object. Since groups
and environments are agents, they should be registered here as
well.
While this is (right now) a simple dictionary, providing this
interface means that in the future, we can have something fancier,
if need be.
For instance, we might turn the registry into an object, but so long
as these functions still work, and no code goes straight at the dict,
that should break nothing.
We will add to the dict a check that what is being registered is an
agent!
IMPORTANT: Given our registry structure, *every agent name must be unique in a
run of a model*!
"""
import numpy as np
from numpy import random
import os
from os import listdir
from os.path import isfile, join
import json
import types
from lib.agent import Agent
from lib.env import Env
from lib.user import APIUser, TermUser, TestUser
from lib.utils import Debug, PA_INDRA_HOME, INDRA_HOME_VAR

DEBUG = Debug()

EXEC_KEY = "exec_key"

ENV_NM = 'env'
MODEL_NM = 'model'

# SPECIAL EXEC KEY VALUES:
# We want to create a test model (why not Basic?) that always is added to
# the registry at a know exec key. This will make testing new endpoints
# much easier!
TEST_EXEC_KEY = 0
MIN_EXEC_KEY = 1
MAX_EXEC_KEY = 10 ** 9  # max is somewhat arbitrary, but make it big!

registry = None


def wrap_func_with_lock(func):
    """
    This is a decorator to prevent race conditions when updating
    registry.
    """

    def wrapper(*args, **kwargs):
        try:
            import uwsgidecorators
            locked_fn = uwsgidecorators.lock(func)
            return locked_fn(*args, **kwargs)
        except ImportError or ModuleNotFoundError or RuntimeError:
            return func(*args, **kwargs)

    return wrapper


@wrap_func_with_lock
def create_exec_env(save_on_register=True, create_for_test=False):
    """
    :param save_on_register: boolean
    :return: New registry for storing data for execution

    Need to lock this function so registry generation can be serialized.
    Since two threads could potentially come up with the same exec_key and try
    to write them to the disk there is a race condition for the disk resource.
    If not resolved one thread will overwrite the registry of the other thread
    and corrupt the run time calls of the model.
    """
    return registry.create_exec_env(save_on_register=save_on_register,
                                    create_for_test=create_for_test)


def get_exec_key(**kwargs):
    """
    Pluck an exec key out of keyword arguments.
    """
    exec_key = kwargs.get(EXEC_KEY, None)
    if exec_key is None:
        raise ValueError("Cannot find exec key:", exec_key)
    return exec_key


def get_user(exec_key):
    """
    Fetch the user assoociated with the model
    :param exec_key:
    :return: User registered for the current model
    """
    return get_model(exec_key).user


def get_model(exec_key):
    """
    The model is a special singleton member of the registry.
    """
    return get_agent(MODEL_NM, exec_key)


def get_env(exec_key=None, **kwargs):
    """
    :param execution_key: execution to fetch with
    :return: Env object
    """
    if exec_key is None:
        exec_key = get_exec_key(**kwargs)
    return get_model(exec_key).env


def reg_model(model, exec_key):
    """
    The model is a special singleton member of the registry.
    """
    registry[exec_key][MODEL_NM] = model


def reg_agent(name, agent, exec_key):
    """
    Register an agent in the registry.
    Raises an exception if `agent` is not an `Agent`.
    Return: None
    """
    if not isinstance(name, str):
        raise ValueError("Key being registered is not a string.")
    if not isinstance(agent, Agent):
        raise ValueError("Object being registered is not an agent.")
    if len(name) == 0:
        raise ValueError("Cannot register agent with empty name")
    if isinstance(agent, Env):
        name = ENV_NM
    if exec_key is None:
        raise ValueError("Cannot register agent against a None Key")
    registry[exec_key][name] = agent


def get_agent(name, exec_key=None, **kwargs):
    """
    Fetch an agent from the registry.
    Return: The agent object.
    """
    if exec_key is None:
        exec_key = get_exec_key(**kwargs)
    if len(name) == 0:
        raise ValueError("Cannot fetch agent with empty name")
    if name in registry[exec_key]:
        return registry[exec_key][name]
    else:
        registry.load_reg(exec_key)
        if name not in registry[exec_key]:
            print(f'ERROR: Did not find {name} in registry for key {exec_key}')
            return None
        return registry[exec_key][name]


def del_agent(name, exec_key=None, **kwargs):
    """
    Delete an agent from the registry.
    Return: None
    """
    if exec_key is None:
        exec_key = get_exec_key(**kwargs)
    del registry[exec_key][name]


def init_exec_key(props=None):
    if props is None:
        raise KeyError(
            "Cannot find key - {} in the passed props".format(EXEC_KEY))


def get_func_name(f):
    # Until Agent.restore and Env.to_json can restore functions from function
    # names, strings will be returned as-is.
    if isinstance(f, str):
        return f
    elif f is not None:
        return f.__name__
    else:
        return ""


def sync_api_restored_model_with_registry(api_restored_model, exec_key):
    """
    This method synchronizes the registry with the model created from the
    api response. We need to do this because we rely on the api response to
    restore the model rather on using the registry. We cannot have two distinct
    model entities(with same data) exist while the model is running because
    calls like get_model, get_agent, model.env should resolve to the same
    entity.
    NOTE: Might not need this if we only use the registry to deserialize
    the model at run time.
    """
    registry[exec_key][MODEL_NM] = api_restored_model
    for group_nm in api_restored_model.env.members:
        registry[exec_key][group_nm] = api_restored_model.env.members[group_nm]
        for member_nm in api_restored_model.env.members[group_nm].members:
            registry[exec_key][member_nm] = \
                api_restored_model.env.members[group_nm].members[member_nm]
    registry[exec_key][ENV_NM] = api_restored_model.env


class AgentEncoder(json.JSONEncoder):
    """
    The JSON encoder base class for all descendants
    of Agent.
    """

    def default(self, o):
        if hasattr(o, 'to_json'):
            return o.to_json()
        elif isinstance(o, np.int64):
            return int(o)
        elif isinstance(o, types.FunctionType):
            return get_func_name(o)  # can't JSON a function!
        else:
            return json.JSONEncoder.default(self, o)


class Registry(object):
    def __init__(self):
        print("Creating new registry")
        self.registries = dict()
        indra_dir = os.getenv(INDRA_HOME_VAR, PA_INDRA_HOME)
        self.db_dir = os.path.join(indra_dir, 'registry', 'db')
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

    '''
    set the item in the registry dictionary.
    if the flag save_on_register is set to true for
    agents stored against this key then save the
    registry to disk.
    NOTE: If save_on_register is set to false, the
    contents of registry wont be written to disk until someone
    calls save_reg with this key.
    '''

    def __setitem__(self, key, value):
        self.registries[key] = value

    '''
    Always fetch the items from the file for now.
    There might be optimizations here later.
    '''

    def __getitem__(self, key):
        if key not in self:
            '''
            notice that this is only accessed by a thread that did not
            create this key.
            '''
            print(f'key not found {key}')
            self.load_reg(key)
            return self.registries[key]
        return self.registries[key]

    '''
    Always check the files already written to the disk since
    some other thread might have stored a dictionary and the key
    will not be present here.
    NOTE: This might be a potential use for generators to lazy load
    the dictionary from file.
    '''

    def __contains__(self, key):
        if key in self.registries.keys():
            return True
        else:
            registry_files = [file for file in listdir(self.db_dir) if
                              isfile(join(self.db_dir, file))]
            for file in registry_files:
                # only check files which are json
                if file[-4:] != 'json':
                    continue
                try:
                    if int(file.split("-")[0]) == key:
                        self.load_reg(key)
                        return True
                except ValueError:
                    # ignore files that don't start with an int!
                    pass
            return False

    def __delitem__(self, key):
        del self.registries[key]

    def __get_unique_key(self):
        key = random.randint(MIN_EXEC_KEY, MAX_EXEC_KEY)
        '''
        Try to get a key that is not already being used.
        This means that key should not be in the registry for the current
        thread and also not saved on the disk by some other thread.
        '''
        while key in self.registries.keys() or os.path.isfile(
                self.__get_reg_file_name(key)):
            key = random.randint(MIN_EXEC_KEY, MAX_EXEC_KEY)
        return key

    def __get_reg_file_name(self, key):
        file_path = os.path.join(self.db_dir, '{}-reg.json'.format(key))
        return file_path

    def __does_key_exists(self, key):
        if key not in self:
            raise KeyError("Key - {} does not exist in registry.".format(key))
        return True

    def save_reg(self, key):
        file_path = self.__get_reg_file_name(key)
        serial_object = json.dumps(self[key], cls=AgentEncoder,
                                   indent=4)
        with open(file_path, 'w') as file:
            file.write(serial_object)

    def load_reg(self, key):
        print(f'loading reg for key {key}')
        file_path = self.__get_reg_file_name(key)
        with open(file_path, 'r') as file:
            registry_as_str = file.read()
        self.registries[key] = {}
        obj = self.__json_to_object(json.loads(registry_as_str), key)
        self.registries[key] = obj

    def to_json(self):
        """
        Writes out the registry as a JSON object, perhaps to be served by API
        server.
        I think we should *not* send back the whole model or env, because they
        will contain all of the other agents. Also, groups should just send
        back the group members names.
        Only individual agents should be fully represented in the returned
        JSON.
        """

    def __json_to_object(self, serial_obj, exec_key):
        """
        Takes a serial JSON object back into a live Python object.
        """
        restored_obj = dict()
        restored_groups = []
        model_deserialized = False
        for obj_name in serial_obj:
            should_restore_object = isinstance(serial_obj[obj_name],
                                               dict) and "type" in serial_obj[
                                        obj_name]
            if should_restore_object:
                if serial_obj[obj_name]["type"] == "TestUser":
                    restored_obj[obj_name] = TermUser(name=obj_name,
                                                      serial_obj=serial_obj[
                                                          obj_name],
                                                      exec_key=exec_key)
                if serial_obj[obj_name]["type"] == "APIUser":
                    restored_obj[obj_name] = APIUser(name=obj_name,
                                                     serial_obj=serial_obj[
                                                         obj_name],
                                                     exec_key=exec_key)
                if serial_obj[obj_name]["type"] == "Agent":
                    restored_obj[obj_name] = Agent(name=obj_name,
                                                   serial_obj=serial_obj[
                                                       obj_name],
                                                   exec_key=exec_key)
                elif serial_obj[obj_name]["type"] == "Model":
                    from lib.model import Model
                    print(f'restoring model for key {exec_key}')
                    restored_obj[obj_name] = Model(exec_key=exec_key,
                                                   serial_obj=serial_obj[
                                                       obj_name])
                    model_deserialized = True
                elif serial_obj[obj_name]["type"] == "Group":
                    from lib.group import Group
                    restored_obj[obj_name] = Group(exec_key=exec_key,
                                                   serial_obj=serial_obj[
                                                       obj_name],
                                                   name=serial_obj[obj_name][
                                                       'name'])
                    restored_groups.append(restored_obj[obj_name])
                elif serial_obj[obj_name]["type"] == "Env":
                    restored_obj[obj_name] = Env(exec_key=exec_key,
                                                 serial_obj=serial_obj[
                                                     obj_name],
                                                 name=serial_obj[obj_name][
                                                     'name'])
            else:
                restored_obj[obj_name] = serial_obj[obj_name]

            self.registries[exec_key][obj_name] = restored_obj[obj_name]

        if model_deserialized:
            restored_obj['model'].groups = restored_groups
            restored_obj['model'].env = restored_obj['env']
            self.registries[exec_key]['model'] = restored_obj['model']
        return restored_obj

    def create_exec_env(self, save_on_register=True, create_for_test=False):
        """
        Create a new execution environment and return its key.
        """
        if create_for_test:
            key = TEST_EXEC_KEY
        else:
            key = self.__get_unique_key()
        print("Creating new registry with key: {}".format(key))
        self.registries[key] = {}
        self.registries[key] = {'save_on_register': save_on_register}
        # stores the file paths of pickled functions
        self.registries[key]['functions']: {str: str} = {}
        '''
        Need to do this so that some other thread which creates a new registry
        doesnt end up using the same exec_key value
        '''
        self.save_reg(key)
        return key

    def del_exec_env(self, key):
        """
        Remove an execution environment from the registry.
        """
        if self.__does_key_exists(key):
            if DEBUG.debug_lib:
                print("Clearing exec env {} from registry".format(key))
            del self.registries[key]
            if isfile(self.__get_reg_file_name(key)):
                os.remove(self.__get_reg_file_name(key))


registry = Registry()


def setup_test_model():
    """
    Set's up the basic model at exec_key = 0 for testing purposes.
    Any model can setup for testing by adding a function called
    `create_model_for_test` and calling that function here with props=None.
    If custom props are needed the conventional api should be used.
    This method is only executed at run time. Running it while running tests
    will cause ImportError because of circular imports between Registry and
    Model classes.
    :return: None
    """
    user_type = os.getenv("user_type", TestUser)
    if user_type == "test":
        return
    else:
        from models.basic import create_model_for_test
        create_model_for_test(props=None)
        registry.save_reg(TEST_EXEC_KEY)


setup_test_model()
