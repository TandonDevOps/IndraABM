# Indra API server
import logging
from http import HTTPStatus
import werkzeug.exceptions as wz

# Let's move to doing imports like this:
import db.menus_db as mdb
import db.model_db as model_db
import lib.agent as agt
import lib.actions as act
import model_generator.model_generator as mdl_gen

# not like this:
from flask import request
from flask import Flask
from flask_cors import CORS
from flask_restx import Resource, Api, fields
from propargs.propargs import PropArgs
from APIServer.api_utils import json_converter
from APIServer.props_api import get_props
from APIServer.source_api import get_source_code
from model_generator.model_generator import create_group
from APIServer.model_manager import modelManager
from utils.formatters import str_to_bool

PERIODS = "periods"
POPS = "pops"

MODELS_URL = '/models'
MODELS_GEN_URL = '/models/generate/create_model'
MODEL_GEN_CREATE_GROUP_URL = '/models/generate/create_group/<int:exec_key>'
MODEL_GEN_CREATE_ACTION_URL = '/models/generate/create_actions/<int:exec_key>'
MODEL_RUN_URL = MODELS_URL + '/run'
MODEL_PROPS_URL = MODELS_URL + '/props'

app = Flask(__name__)
CORS(app)
api = Api(app)

@api.route(MODELS_GEN_URL)
class ModelsGenerator(Resource):
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Invalid Input')
    @api.doc(params={'model_name': 'name of the model'})
    def post(self):
        """
        Generate model and return a exec_key.(Input : model name)
        """
        model_name = request.args.get('model_name')
        if model_name is None:
            raise wz.NotAcceptable('Model Name Must Not Be None.')
        model = modelManager.spawn_model(model_name=model_name)
        return json_converter(model)


color_list = act.VALID_COLORS
parser = api.parser()
parser.add_argument('group_color', type=str,
                    help='color of your group', choices=color_list)
parser.add_argument('group_name', type=str, help='name of your group')
parser.add_argument('group_number_of_members',
                    type=int, help='number of members')


@api.route(MODEL_GEN_CREATE_GROUP_URL)
class CreateGroup(Resource):
    @api.expect(parser)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Invalid Input')
    def post(self, exec_key=0):
        """
        Add groups to Generated model. (Input : exec key and other params)
        """
        group_name = request.args.get('group_name')
        if not group_name:
            raise wz.NotAcceptable('Group Name Must Not Be None.')
        group_color = request.args.get('group_color')
        if group_color not in act.VALID_COLORS:
            raise wz.NotAcceptable('Invalid Group Color.')
        group_num_of_members = request.args.get('group_number_of_members')
        model = modelManager.get_model(exec_key)
        jrep = json_converter(model)
        if group_name in jrep['env']['members']:
            return {'error': 'Group name already exists in that group'}
        model = modelManager.create_group(
            exec_key, jrep, group_color, group_num_of_members, group_name)
        return json_converter(model)


action_parser = api.parser()
action_method_list = mdl_gen.MODEL_GEN_ACTION_METHOD
action_submethod_list = mdl_gen.MODEL_GEN_ACTION_SUBMETHOD
action_below_act_list = mdl_gen.MODEL_GEN_ACTION_BELOW_ACT
action_parser.add_argument(
    'group_name', type=str, help='name of your group')
action_parser.add_argument(
    'group_action',
    type=int,
    help='number of group action')
action_parser.add_argument(
    'method', type=str,
    help='name of the method', choices=action_method_list)
action_parser.add_argument(
    'sub_method', type=str,
    help='name of the sub_method',
    choices=action_submethod_list)
action_parser.add_argument(
    'neighboorhood_size',
    type=int, help='size of the neighboorhood')
action_parser.add_argument(
    'threshold',
    type=int, help='threshold number')
action_parser.add_argument(
    'below_act', type=str,
    help='name of the below_act', choices=action_below_act_list)


@api.route(MODEL_GEN_CREATE_ACTION_URL)
class CreateActions(Resource):
    @api.expect(action_parser)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def post(self, exec_key=0):
        """
        Generate actions and add to the corresponding group.
        (Input : model name and exec_key)
        """
        # return 200 status for the front end for now
        group_name = request.args.get('group_name')
        group_action = request.args.get('group_action')
        method = request.args.get('method')
        sub_method = request.args.get('sub_method')
        neighboorhood = request.args.get('neighboorhood_size')
        threshold = request.args.get('threshold')
        below_act = request.args.get('below_act')
        return {'group_name': group_name,
                'group_action': group_action,
                'method': method,
                'sub_method': sub_method,
                'neighboorhood': neighboorhood,
                'threshold': threshold,
                'below_act': below_act,
                'model exec-key': exec_key
                }


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

model_name_defn = api.model("model_name", {
    "model_name": fields.String("Name of the model")
})

@api.route('/models/<exec_key>')
class Model(Resource):
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def get(self, exec_key=0):
        """
        Return a single model from the registry.
        exec_key is set to 0 by default.
        """
        model = modelManager.get_model(exec_key)
        return json_converter(model)


@api.route('/pophist/<exec_key>')
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
        model = modelManager.get_model(exec_key)
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
        models = model_db.get_models(str_to_bool(request.args.get('active')))
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

    @api.doc(params={'model_id': 'Which model to fetch code for.'})
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def get(self, model_id):
        """
        Get the list of properties (parameters) for a model.
        """
        props = PropArgs.create_props(str(model_id),
                                      prop_dict=get_props(model_id))
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
        model = modelManager.spawn_model(model_id, api.payload)
        return json_converter(model)


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
    "exec_key": fields.String("Exec key of the model to be run.")
})


@api.route(f'{MODEL_RUN_URL}/<int:run_time>')
class RunModel(Resource):
    """
    This endpoint deals with running models.
    """
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
            model = modelManager.run_model(exec_key, run_time)
            return json_converter(model)
        except Exception as err:
            raise wz.InternalServerError(f"Server error: {str(err)}")


@api.route('/user/msgs/<exec_key>')
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
        model = modelManager.get_model(exec_key)
        return model.get_user_msgs()


@api.route('/locations/<exec_key>')
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
        model = modelManager.get_model(exec_key)
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
        agent = modelManager.get_agent(exec_key, name)
        if agent is None:
            raise (wz.NotFound(f"Agent {name} not found."))
        return agent.to_json()


@api.route('/modelmanager/clear/<exec_key>')
class KillModel(Resource):
    """
    This kills the process for `exec_key` in the modelmanager.
    The exec_key becomes stale once the user navigates away from the
    `run model` page on the front end. When a user has finished running
    a model from the frontend we should clear it's data in the backend.
    """
    @api.doc(params={'exec_key': 'Indra execution key.'})
    @api.response(HTTPStatus.OK, 'Resource Deleted')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def delete(self, exec_key):
        print("Killing model for key - {}".format(exec_key))
        modelManager.terminate_model(exec_key)
        return {'success': True}


if __name__ == "__main__":
    logging.error("You should use api.sh to run the server.")
