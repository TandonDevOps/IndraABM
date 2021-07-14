# Indra API server
import logging
from http import HTTPStatus
import werkzeug.exceptions as wz

from flask import request
from flask import Flask
from flask_cors import CORS
from flask_restx import Resource, Api, fields
from propargs.propargs import PropArgs
from registry.registry import registry, create_exec_env
from registry.registry import get_model, get_agent
from APIServer.api_utils import json_converter
from APIServer.model_api import run_model, create_model, create_model_for_test
from APIServer.props_api import get_props
from APIServer.source_api import get_source_code
from models.basic import setup_test_model
from lib.utils import get_indra_home
# Let's move to doing imports like this:
import db.menus_db as mdb
import db.model_db as model_db

PERIODS = "periods"
POPS = "pops"

HEROKU_PORT = 1643

MODELS_URL = '/models'
MODEL_RUN_URL = MODELS_URL + '/run'
MODEL_PROPS_URL = MODELS_URL + '/props'

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
    """
    A function that returns the model running at `exec_key`
    or raises a 404 error if it doesn't exist.
    """
    model = get_model(exec_key)
    if model is None:
        raise wz.NotFound(f"Model Key: {exec_key}, not found.")
    return model


@api.route('/hello')
class HelloWorld(Resource):
    @api.response(HTTPStatus.OK, 'Success')
    def get(self):
        """
        A trivial endpoint just to see if we are running at all.
        """
        return {'hello': 'world'}


@api.route('/endpoints')
class Endpoints(Resource):
    """
    A class to deal with our endpoints themselves.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
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
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def get(self):
        """
        Fetches the registry as {"exec_key": "model name", etc. }
        """
        return registry.to_json()


model_name_defn = api.model("model_name", {
    "model_name": fields.String("Name of the model")
})


@api.route('/models/<int:exec_key>')
class Model(Resource):
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def get(self, exec_key):
        """
        Return a single model from the registry.
        """
        model = get_model_if_exists(exec_key)
        return json_converter(model)

    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    @api.expect(model_name_defn)
    def post(self, exec_key):
        """
        Setup a test model in the registry.
        """
        model_name = None
        if 'model_name' in api.payload:
            model_name = api.payload['model_name']

        if model_name is None:
            # exec_key is supposed to match the model id if model_name is
            # not given
            model = model_db.get_model_by_id(exec_key, indra_dir)
            if model is None:
                raise (wz.NotFound(f"Model {exec_key} doesn't exist."))
            # check if a test model already exists against the given exec_
            # key which matches the model id
            model = get_model(exec_key)
            if model is not None:
                return {"msg": f'A test model {model.name} already exists'}
            else:
                return model.to_json()
        else:
            model_rec = model_db.get_model_by_name(model_name, indra_dir)
            if model_rec is None:
                raise wz.NotFound(f'Model with name {model_name} is not found')
            model = create_model_for_test(model_rec, exec_key)
            return json_converter(model)


@api.route('/pophist/<int:exec_key>')
class PopHist(Resource):
    """
    A class for endpoints that interact with population history.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    @api.doc(params={'exec_key': 'Indra execution key.'})
    def get(self, exec_key):
        """
        This returns the population history for a running model.
        """
        model = get_model_if_exists(exec_key)
        pop_hist = model.get_pop_hist()
        return pop_hist.to_json()


@api.route('/models')
class Models(Resource):
    """
    This class deals with the database of models.
    """

    @api.doc(params={'active': 'If true, show only active models'})
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def get(self, active=False):
        """
        Get a list of available models.
        """
        models = model_db.get_models(indra_dir, str_to_bool(request.args.get('active')))
        if models is None:
            raise (wz.NotFound("Models db not found."))
        return models


props = api.model("props", {
    "props": fields.String("Enter propargs.")
})


@api.route('/source/<int:model_id>')
class SourceCode(Resource):
    """
    This endpoint deals with model source code.
    """
    @api.doc(params={'model_id': 'Which model to fetch code for.'})
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def get(self, model_id):
        code = get_source_code(model_id)
        if code is None:
            raise (wz.NotFound(f"Model {model_id} does not exist."))
        else:
            return code


@api.route('/models/props/<int:model_id>')
class Props(Resource):
    """
    An endpoint to deal with props (parameters).
    """
    global indra_dir

    @api.doc(params={'model_id': 'Which model to fetch code for.'})
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def get(self, model_id):
        """
        Get the list of properties (parameters) for a model.
        """
        props = PropArgs.create_props(str(model_id),
                                      prop_dict=get_props(model_id, indra_dir))
        exec_key = create_exec_env(save_on_register=True)
        props["exec_key"] = exec_key
        registry.save_reg(exec_key)
        return props.to_json()

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
    This endpoint deals with the debug menu.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def get(self):
        """
        Return the menu for debugging a model.
        """
        return mdb.get_debug_menu()


@api.route('/menus/model')
class MenuForModel(Resource):
    """
    This endpoint deals with the model menu.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def get(self):
        """
        Return the menu for interacting with a model.
        """
        return mdb.get_model_menu()


env = api.model("env", {
    "model": fields.String("Should be json rep of model.")
})


@api.route(f'{MODEL_RUN_URL}/<int:run_time>')
class RunModel(Resource):
    """
    This endpoint deals with running models.
    """
    @api.doc(params={'exec_key': 'Indra execution key.'})
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    @api.response(HTTPStatus.INTERNAL_SERVER_ERROR, 'Server Error')
    @api.expect(env)
    def put(self, run_time):
        """
        Put a model env to the server and run it `run_time` periods.
        Catch all possible exceptions to keep the server responsive.
        """
        try:
            exec_key = api.payload['exec_key']
            print(f'Executing for key {exec_key}')
            model = run_model(api.payload, run_time, indra_dir)
            if model is None:
                raise wz.NotFound(f"Model not found: {api.payload['module']}")
            registry.save_reg(exec_key)
            return json_converter(model)
        except Exception as err:
            raise wz.InternalServerError(f"Server error: {str(err)}")


@api.route('/user/msgs/<int:exec_key>')
class UserMsgs(Resource):
    """
    This endpoint deals with messages to the user.
    """

    @api.doc(params={'exec_key': 'Indra execution key.'})
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
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
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
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
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    @api.response(HTTPStatus.BAD_REQUEST, 'Bad Request')
    def get(self):
        """
        Get agent by name from the registry.
        """
        name = request.args.get('name')
        exec_key = request.args.get('exec_key')
        if name is None:
            raise wz.BadRequest("You must pass an agent name.")
        agent = get_agent(name, exec_key)
        if agent is None:
            raise (wz.NotFound(f"Agent {name} not found."))
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
    @api.response(HTTPStatus.OK, 'Resource Deleted')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def delete(self, exec_key):
        print("Clearing registry for key - {}".format(exec_key))
        try:
            registry.del_exec_env(exec_key)
        except KeyError:
            raise wz.NotFound(f"Key - {exec_key} does not exist in registry")
        return {'success': True}


if __name__ == "__main__":
    logging.warning("Warning: you should use api.sh to run the server.")
    app.run(port=HEROKU_PORT, debug=True)
