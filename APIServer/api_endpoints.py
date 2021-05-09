# Indra API server
import logging
from werkzeug.exceptions import NotFound
from flask import request
from flask import Flask
from flask_cors import CORS
from flask_restx import Resource, Api, fields
from propargs.constants import VALUE, ATYPE, INT, HIVAL, LOWVAL
from registry.registry import registry, create_exec_env
from registry.registry import get_model, get_agent
from registry.model_db import get_models
from APIServer.api_utils import err_return
from APIServer.api_utils import json_converter
from APIServer.props_api import get_props
from APIServer.model_api import run_model, create_model
from models.basic import setup_test_model
from lib.utils import get_indra_home
# Let's move to doing imports like this:
import db.menus_db as mdb


PERIODS = "periods"
POPS = "pops"

HTTP_SUCCESS = 200
HTTP_NOT_FOUND = 404

HEROKU_PORT = 1643

MODELS_URL = '/models'
MODEL_RUN_URL = MODELS_URL + '/run'
MODEL_PROPS_URL = '/models/props'

app = Flask(__name__)
CORS(app)
api = Api(app)

"""
Any model can be setup for testing by adding a function called
`create_model_for_test` and calling that function here with props=None.
If custom props are needed the conventional api should be used.
This is only needed for API development since executing through terminal
or through tests anyway sets up the default props.
"""
setup_test_model()

indra_dir = get_indra_home()


TRUE_STRS = ["True", "true", "1"]


def str_to_bool(s):
    """
    Convert plausible "true" strings to bool True.
    Other values to False.
    Useful for taking URL inputs to real boolean values.
    """
    return s in TRUE_STRS


def get_model_if_exists(exec_key):
    model = get_model(exec_key)
    if model is None:
        raise NotFound(f"Model Key: {exec_key}, not found.")
    return model


@api.route('/hello')
class HelloWorld(Resource):
    @api.response(HTTP_SUCCESS, 'Success')
    @api.response(HTTP_NOT_FOUND, 'Not Found')
    def get(self):
        """
        A trivial endpoint just to see if we are running at all.
        """
        return {'hello': 'world'}


@api.route('/endpoints')
class Endpoints(Resource):
    @api.response(HTTP_SUCCESS, 'Success')
    @api.response(HTTP_NOT_FOUND, 'Not Found')
    def get(self):
        """
        List our endpoints.
        """
        
        endpoints = sorted(rule.rule for rule in api.app.url_map.iter_rules())
        return {"Available endpoints": endpoints}


group_fields = api.model("group", {
    "group_name": fields.String,
    "num_of_agents": fields.Integer,
    "color": fields.String,
    "group_actions": fields.List(fields.String),
})

# env_width/height must be >0 when adding agents
create_model_spec = api.model("model_specification", {
    "model_name": fields.String("Enter model name."),
    "env_width": fields.Integer("Enter environment width."),
    "env_height": fields.Integer("Enter environment height."),
    "groups": fields.List(fields.Nested(group_fields)),
})


@api.route('/registry')
class Registry(Resource):
    """
    A class to interact with the registry through the API.
    """
    @api.response(HTTP_SUCCESS, 'Success')
    @api.response(HTTP_NOT_FOUND, 'Not Found')
    def get(self):
        """
        Fetches the registry as {"exec_key": "model name", etc. }
        """
        return registry.to_json()


@api.route('/models/<int:exec_key>')
class Model(Resource):
    """
    Read a single model from the registry.
    """
    @api.response(HTTP_SUCCESS, 'Success')
    @api.response(HTTP_NOT_FOUND, 'Not Found')
    def get(self, exec_key):
        model = get_model_if_exists(exec_key)
        return json_converter(model)


@api.route('/pophist/<int:exec_key>')
class PopHist(Resource):
    """
    A class to interact with Population History through the API.
    """
    @api.response(HTTP_SUCCESS, 'Success')
    @api.response(HTTP_NOT_FOUND, 'Not Found')
    @api.doc(params={'exec_key': 'Indra execution key.'})
    def get(self, exec_key):
        model = get_model_if_exists(exec_key)
        pop_hist = model.get_pop_hist()
        return pop_hist.to_json()


@api.route('/models')
class Models(Resource):
    """
    This class deals with the database of models.
    """
    @api.doc(params={'active': 'Show only active models'})
    @api.response(HTTP_SUCCESS, 'Success')
    @api.response(HTTP_NOT_FOUND, 'Not Found')
    def get(self, active=False):
        """
        Get a list of available models. `active` flag true means only get
        active models.
        """
        models = get_models(indra_dir, str_to_bool(request.args.get('active')))
        if models is None:
            raise (NotFound("Models db not found."))
        return models


props = api.model("props", {
    "props": fields.String("Enter propargs.")
})


@api.route('/source/<int:model_id>')
class SourceCode(Resource):
    """
    A class to fetch source code endpoint.
    """
    @api.doc(params={'model_id': 'Which model to fetch code for.'})
    @api.response(HTTP_SUCCESS, 'Success')
    @api.response(HTTP_NOT_FOUND, 'Not Found')
    def get(self, model_id):
        return print(f"Getting source for {model_id}")


@api.route('/models/props/<int:model_id>')
class Props(Resource):
    global indra_dir
    @api.doc(params={'model_id': 'Which model to fetch code for.'})
    @api.response(HTTP_SUCCESS, 'Success')
    @api.response(HTTP_NOT_FOUND, 'Not Found')
    def get(self, model_id):
        """
        Get the list of properties (parameters) for a model.
        """
        props = get_props(model_id, indra_dir)
        exec_key = create_exec_env(save_on_register=True)
        props["exec_key"] = {
            VALUE: exec_key,
            ATYPE: INT,
            HIVAL: None,
            LOWVAL: None
        }
        registry.save_reg(exec_key)
        return props
    @api.doc(params={'model_id': 'Which model to fetch code for.'})
    @api.response(400, 'Invalid Input')
    @api.response(201, 'Created')
    @api.expect(props)
    def put(self, model_id):
        """
        Put a revised list of parameters for a model back to the server.
        This should return a new model with the revised props.
        """
        exec_key = api.payload['exec_key'].get('val')
        model = json_converter(create_model(model_id, api.payload, indra_dir))
        registry.save_reg(exec_key)
        return model


@api.route('/menus/debug')
class MenuForDebug(Resource):
    """
    Return the menu for debugging a model.
    """
    @api.response(HTTP_SUCCESS, 'Success')
    @api.response(HTTP_NOT_FOUND, 'Not Found')
    def get(self):
        return mdb.get_debug_menu()


@api.route('/menus/model')
class MenuForModel(Resource):
    """
    Return the menu for interacting with a model.
    """
    @api.response(HTTP_SUCCESS, 'Success')
    @api.response(HTTP_NOT_FOUND, 'Not Found')
    def get(self):
        return mdb.get_model_menu()


env = api.model("env", {
    "model": fields.String("Should be json rep of model.")
})


@api.route(f'{MODEL_RUN_URL}/<int:run_time>')
class RunModel(Resource):
    """
    This endpoint runs the model `run_time` periods.
    """
    @api.doc(params={'exec_key': 'Indra execution key.'})
    @api.response(HTTP_SUCCESS, 'Success')
    @api.response(HTTP_NOT_FOUND, 'Not Found')
    @api.expect(env)
    def put(self, run_time):
        """
        Put a model env to the server and run it `run_time` periods.
        """
        exec_key = api.payload['exec_key']
        print(f'Executing for key {exec_key}')
        model = run_model(api.payload, run_time, indra_dir)
        if model is None:
            return err_return("Model not found: " + api.payload["module"])
        registry.save_reg(exec_key)
        return json_converter(model)


@api.route('/user/msgs/<int:exec_key>')
class UserMsgs(Resource):
    """
    This endpoint deals with messages to the user.
    """
    @api.doc(params={'exec_key': 'Indra execution key.'})
    @api.response(HTTP_SUCCESS, 'Success')
    @api.response(HTTP_NOT_FOUND, 'Not Found')
    def get(self, exec_key):
        """
        Get all user messages for an exec key.
        """
        model = get_model_if_exists(exec_key)
        return model.get_user_msgs()


@api.route('/locations/<int:exec_key>')
class Locations(Resource):
    """
    This endpoint gets an agent agent coordinate location.
    """
    @api.doc(params={'exec_key': 'Indra execution key.'})
    @api.response(HTTP_SUCCESS, 'Success')
    @api.response(HTTP_NOT_FOUND, 'Not Found')
    def get(self, exec_key):
        """
        Get all locations in a model.
        This will return a dictionary of locations as keys
        and agent names as the value.
        """
        model = get_model_if_exists(exec_key)
        return model.get_locations()


@api.route('/agent')
class Agent(Resource):
    """
    This endpoint can get an agent given exec key and agent name.
    We should eventually implement DELETE and POST methods here,
    at least.
    """

    @api.doc(params={'exec_key': 'Indra execution key.',
                     'name': 'Name of agent to fetch.'})
    @api.response(HTTP_SUCCESS, 'Success')
    @api.response(HTTP_NOT_FOUND, 'Not Found')
    def get(self):
        """
        Get agent by name from the registry.
        """
        name = request.args.get('name')
        exec_key = request.args.get('exec_key')
        if name is None:
            return err_return("You must pass an agent name.")
        agent = get_agent(name, exec_key)
        if agent is None:
            raise (NotFound(f"Agent {name} not found."))
            # trying out raising an exception so comment dis out:
            # return err_return(f"Agent {name} not found.")
        return agent.to_json()


@api.route('/registry/clear/<int:exec_key>')
class ClearRegistry(Resource):
    """
    This clears the entries for one `exec_key` out of the registry.
    The exec_key becomes stale once the user navigates away from the
    `run model` page on the front end. When a user has finished running
    a model from the frontend we should clear it's data in the backend.
    """
    @api.doc(params={'exec_key': 'Indra execution key.'})
    @api.response(HTTP_SUCCESS, 'Resource Deleted')
    @api.response(HTTP_NOT_FOUND, 'Not Found')
    def delete(self, exec_key):
        print("Clearing registry for key - {}".format(exec_key))
        try:
            registry.del_exec_env(exec_key)
        except KeyError:
            return err_return(
                "Key - {} does not exist in registry".format(exec_key))
        return {'success': True}


if __name__ == "__main__":
    logging.warning("Warning: you should use api.sh to run the server.")
    app.run(port=HEROKU_PORT, debug=True)
