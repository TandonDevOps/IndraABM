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
from lib.user import APIUser, TermUser
from lib.utils import Debug, get_indra_home
import glob

DEBUG = Debug()

EXEC_KEY = "exec_key"

ENV_NM = 'env'
MODEL_NM = 'model'

# SPECIAL EXEC KEY VALUES:
# We want to create a test model (why not Basic?) that always is added to
# the registry at a know exec key. This will make testing new endpoints
# much easier!
TEST_EXEC_KEY = 0
MIN_EXEC_KEY = 0
RESERVED_KEY_LIMIT = 1000
MAX_EXEC_KEY = 10 ** 9  # max is somewhat arbitrary, but make it big!

registry = None


class MockModel():
    """
    This just exsits to test model code within the registry to avoid circular
    imports.
    """

    def __init__(self, name):
        self.name = name
        self.props = None

    def __str__(self):
        return self.name


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
def create_exec_env(save_on_register=True, create_for_test=False,
                    exec_key=None):
    """
    :param save_on_register: boolean
    :param create_for_test: boolean
    :return: New registry for storing data for execution

    Need to lock this function so registry generation can be serialized.
    Since two threads could potentially come up with the same exec_key and try
    to write them to the disk there is a race condition for the disk resource.
    If not resolved one thread will overwrite the registry of the other thread
    and corrupt the run time calls of the model.
    """
    return registry.create_exec_env(save_on_register=save_on_register,
                                    create_for_test=create_for_test,
                                    use_exec_key=exec_key)


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
    return get_agent(MODEL_NM, exec_key=exec_key)


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
    Note: importing Env here is to avoid a circular import
    """
    from lib.env import Env
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


def get_group(name, exec_key):
    """
    Groups *are* agents, so:
    It's a separate func for clarity and in case one day things change.
    """
    return get_agent(name, exec_key=exec_key)


def get_agent(name, exec_key=None, **kwargs):
    """
    Fetch an agent from the registry.
    Return: The agent object, or None if not found.
    """
    try:
        if exec_key is None:
            exec_key = get_exec_key(**kwargs)
        if len(name) == 0:
            raise ValueError("Cannot fetch agent with empty name")
        if name in registry[exec_key]:
            return registry[exec_key][name]
        else:
            registry.load_reg(exec_key)
            if name not in registry[exec_key]:
                print(f'ERROR: Did not find {name} in registry for {exec_key}')
                return None
            return registry[exec_key][name]
    except (FileNotFoundError, IOError):
        print(f'ERROR: Exec key {exec_key} does not exist.')
        return None


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


def save_reg(exec_key):
    if exec_key is None:
        raise ValueError("Cannot save registry with key None")
    registry.save_reg(exec_key)


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
        indra_dir = get_indra_home()
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

    def __contains__(self, key):
        '''
        Always check the files already written to the disk since
        some other thread might have stored a dictionary and the key
        will not be present here.
        NOTE: This might be a potential use for generators to lazy load
        the dictionary from file.
        '''
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

    def __get_reserved_key(self):
        key = random.randint(MIN_EXEC_KEY, RESERVED_KEY_LIMIT)

        while key in self:
            key = random.randint(MIN_EXEC_KEY, RESERVED_KEY_LIMIT)

        return key

    def __get_unique_key(self, reserved=False):
        if reserved:
            return self.__get_reserved_key()
        key = random.randint(RESERVED_KEY_LIMIT + 1, MAX_EXEC_KEY)
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
        For now, we will just do exec_keys and model names.
        """
        ret_json = {}
        for key in self.registries:
            ret_json[key] = str(get_model(key))
        return ret_json

    def __json_to_object(self, sobj, ekey):
        """
        Takes a serial JSON object back into a live Python object.
        note: imorting Env here is to avoid a circular import
                at the global scope
        """
        from lib.env import Env
        robj = dict()
        restored_groups = []
        model_deserialized = False
        for objnm in sobj:
            should_restore_object = isinstance(sobj[objnm],
                                               dict) and "type" in sobj[objnm]
            if should_restore_object:
                if sobj[objnm]["type"] == "TestUser":
                    robj[objnm] = TermUser(name=objnm, serial_obj=sobj[objnm],
                                           exec_key=ekey)
                if sobj[objnm]["type"] == "APIUser":
                    robj[objnm] = APIUser(name=objnm, serial_obj=sobj[objnm],
                                          exec_key=ekey)
                if sobj[objnm]["type"] == "Agent":
                    robj[objnm] = Agent(name=objnm, serial_obj=sobj[objnm],
                                        exec_key=ekey)
                elif sobj[objnm]["type"] == "Model":
                    from lib.model import Model
                    robj[objnm] = Model(exec_key=ekey, serial_obj=sobj[objnm])
                    model_deserialized = True
                elif sobj[objnm]["type"] == "Group":
                    from lib.group import Group
                    robj[objnm] = Group(exec_key=ekey, serial_obj=sobj[objnm],
                                        name=sobj[objnm]['name'])
                    restored_groups.append(robj[objnm])
                elif sobj[objnm]["type"] == "Env":
                    robj[objnm] = Env(exec_key=ekey, serial_obj=sobj[objnm],
                                      name=sobj[objnm]['name'])
            else:
                robj[objnm] = sobj[objnm]

            self.registries[ekey][objnm] = robj[objnm]

        if model_deserialized:
            robj['model'].groups = restored_groups
            robj['model'].env = robj['env']
            self.registries[ekey]['model'] = robj['model']
        return robj

    def create_exec_env(self, save_on_register=True, create_for_test=False,
                        use_exec_key=None):
        """
        Create a new execution environment and return its key.
        """
        if use_exec_key is None and create_for_test:
            key = self.__get_unique_key(reserved=create_for_test)
        elif use_exec_key is not None and create_for_test:
            if use_exec_key >= MIN_EXEC_KEY \
                    and use_exec_key <= RESERVED_KEY_LIMIT:
                key = use_exec_key
            else:
                raise ValueError(
                    f'Cannot use {use_exec_key} to setup model. '
                    f'The key must be between {MIN_EXEC_KEY} and '
                    f'{RESERVED_KEY_LIMIT}')
        else:
            # create for test should be false here
            key = self.__get_unique_key(reserved=create_for_test)
        print("Creating new registry entry with key: {}".format(key))
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

    def __remove_pkl_files(self, key):
        pkl_files = glob.glob(f'{self.db_dir}/{key}*.pkl')
        for file in pkl_files:
            if isfile(file):
                os.remove(file)

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
            self.__remove_pkl_files(key)


registry = Registry()


def main():
    """
    A main to run quick experiments with registry!
    """
    create_exec_env(create_for_test=True)
    reg_model(MockModel("Test model"), TEST_EXEC_KEY)
    print(json.dumps(registry.to_json(), indent=4))


if __name__ == "__main__":
    main()
