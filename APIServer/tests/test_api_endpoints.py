"""
"""
import os

import json
import random
import string
from unittest import TestCase, main, skip

from flask_restplus import Resource

from registry.model_db import get_models, MODEL_ID
from APIServer.api_endpoints import Props, RunModel
from APIServer.api_endpoints import app, HelloWorld, Endpoints, Models
from APIServer.api_endpoints import indra_dir
from APIServer.api_utils import err_return

BASIC_ID = 0
MIN_NUM_ENDPOINTS = 2


def random_name():
    return "".join(random.choices(string.ascii_letters,
                                  k=random.randrange(1, 10)))


class Test(TestCase):
    def setUp(self):
        self.hello_world = HelloWorld(Resource)
        self.endpoints = Endpoints(Resource)
        self.model = Models(Resource)
        self.props = Props(Resource)
        self.run = RunModel(Resource)
        self.models = get_models(indra_dir)

    def test_hello_world(self):
        """
        See if HelloWorld works.
        """
        rv = self.hello_world.get()
        self.assertEqual(rv, {'hello': 'world'})

    def test_endpoints(self):
        '''
        Check that /endpoints lists these endpoints.
        '''
        endpoints = self.endpoints.get()["Available endpoints"]
        self.assertGreaterEqual(len(endpoints), MIN_NUM_ENDPOINTS)

    def test_get_models(self):
        """
        See if we can get models.
        """
        with app.test_request_context():
            api_ret = self.model.get()
        for model in api_ret:
            self.assertIn(MODEL_ID, model)

    def test_get_props(self):
        """
        See if we can get props. Doing this for basic right now.
        Cannot seem to resolve props from model_id or name
        """
        model_id = 0
        rv = self.props.get(model_id)

        with open(os.path.join(indra_dir, "models", "props",
                               "basic.props.json")) as file:
            test_props = json.loads(file.read())

        self.assertTrue("exec_key" in rv)
        self.assertTrue(rv["exec_key"] is not None)
        # since exec_key is dynamically added to props the returned value
        # contains one extra key compared to the test_props loaded from file
        del rv["exec_key"]
        self.assertEqual(rv, test_props)

    def test_put_props(self):
        """
        Test whether we are able to put props and get back a model.
        This test should be re-written from scratch.
        """
        pass

    def test_model_run(self):
        model_id = 0
        props = self.props.get(model_id)
        with app.test_client() as client:
            client.environ_base['CONTENT_TYPE'] = 'application/json'
            rv = client.put('/models/props/' + str(model_id),
                            data=json.dumps(props))
        self.assertEqual(rv._status_code, 200)
        with app.test_client() as client:
            client.environ_base['CONTENT_TYPE'] = 'application/json'
            response = client.put('/models/run/' + str(10),
                                  data=json.dumps(rv.json))

        self.assertEqual(response._status_code, 200)
        self.assertNotEqual(rv.json.get('env').get('locations'),
                            response.json.get('env').get('locations'))

    '''
    def test_get_ModelMenu(self):
        """
        Testing whether we are getting the menu.
        """
        rv = self.model_menu.get()
        test_menu_file = indra_dir + "/lib/menu.json"
        with open(test_menu_file) as file:
            test_menu = json.loads(file.read())["menu_database"]
        self.assertEqual(rv, test_menu)
    '''

    def test_err_return(self):
        """
        Testing whether we are able to get the right error message
        """
        rv = err_return("error message")
        self.assertEqual(rv, {"Error:": "error message"})


if __name__ == "__main__":
    main()
