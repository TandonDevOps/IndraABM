import os

from http import HTTPStatus

import json
import random
import string
from unittest import TestCase, main, skip

from flask_restx import Resource
from numpy.lib.utils import source
import werkzeug.exceptions as wz

# Let's cut over to the following kind of imports:
import APIServer.api_endpoints as epts
from APIServer.api_endpoints import Props, RunModel, SourceCode
from APIServer.api_endpoints import app, HelloWorld, Endpoints, Models
from APIServer.api_endpoints import indra_dir
from APIServer.api_utils import err_return

import db.model_db as model_db


BASIC_ID = 0
MIN_NUM_ENDPOINTS = 2

TEST_TURNS = "10"
TEST_MODEL_ID = 25


def random_name():
    return "".join(random.choices(string.ascii_letters,
                                  k=random.randrange(1, 10)))


class TestAPI(TestCase):
    def setUp(self):
        self.hello_world = HelloWorld(Resource)
        self.endpoints = Endpoints(Resource)
        self.pophist = epts.PopHist(Resource)
        self.props = Props(Resource)
        self.run = RunModel(Resource)

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

    def test_get_model_menu(self):
        mfm = epts.MenuForModel(Resource)
        self.assertTrue(isinstance(mfm.get(), dict))

    def test_get_models(self):
        """
        See if we can get models.
        """
        models = Models(Resource)
        with app.test_request_context():
            api_ret = models.get()
        for model in api_ret:
            self.assertIn(model_db.MODEL_ID, model)

    def test_user_msgs(self):
        """
        Test getting user messages.
        """
        um = epts.UserMsgs(Resource)
        self.assertTrue(isinstance(um.get(BASIC_ID), str))

    def test_get_pophist(self):
        """
        Test getting pophist.
        A rule: the number of periods must be one less than
        the length of each pop list. (Because we record pops for
        period zero.
        """
        with app.test_request_context():
            pophist = self.pophist.get(0)
        self.assertTrue(isinstance(pophist, dict))
        self.assertIn(epts.POPS, pophist)
        self.assertIn(epts.PERIODS, pophist)
        for grp in pophist[epts.POPS]:
            self.assertEqual(len(pophist[epts.POPS][grp]),
                             pophist[epts.PERIODS] + 1)

    def test_get_props(self):
        """
        See if we can get props. Doing this for basic right now.
        Cannot seem to resolve props from model_id or name
        """
        model_id = BASIC_ID
        props = self.props.get(model_id)

        with open(os.path.join(indra_dir, "models", "props",
                               "basic.props.json")) as file:
            test_props = json.loads(file.read())

        self.assertTrue("exec_key" in props)
        self.assertTrue(props["exec_key"] is not None)
        # since exec_key is dynamically added to props the returned value
        # contains one extra key compared to the test_props loaded from file
        del props["exec_key"]
        for test_key in test_props.keys():
            self.assertIn(test_key, props)

    def test_put_props(self):
        """
        Test whether we are able to put props and get back a model.
        This test should be re-written from scratch.
        """
        pass

    @skip("problem with restoring props.")
    # Internal server error instead of HTTPStatus.OK
    def test_model_run(self):
        """
        This is going to see if we can run a model.
        """
        model_id = BASIC_ID
        with app.test_client() as client:
            client.environ_base['CONTENT_TYPE'] = 'application/json'
            model_before_run = client.get(f'{epts.MODELS_URL}/{BASIC_ID}')
        self.assertEqual(model_before_run._status_code, HTTPStatus.OK)
        with app.test_client() as client:
            client.environ_base['CONTENT_TYPE'] = 'application/json'
            model_after_run = client.put(f'{epts.MODEL_RUN_URL}/{TEST_TURNS}',
                                         data=json.dumps(
                                             model_before_run.json))

        self.assertEqual(model_after_run._status_code, HTTPStatus.OK)
        # if the model really ran, the old period must be less than the new
        # period.
        self.assertLess(model_before_run.json.get('period'),
                        model_after_run.json.get('period'))

    def test_err_return(self):
        """
        Testing whether we are able to get the right error message
        """
        rv = err_return("error message")
        self.assertEqual(rv, {"Error:": "error message"})

    def test_no_model_found_for_name(self):
        with app.test_client() as client:
            client.environ_base['CONTENT_TYPE'] = 'application/json'
            response = client.post(f'{epts.MODELS_URL}/1',
                                   data=json.dumps(({'model_name': "random"})))
        self.assertEqual(response._status_code, HTTPStatus.NOT_FOUND)

    def test_model_created_for_testing_with_incorrect_id(self):
        with app.test_client() as client:
            client.environ_base['CONTENT_TYPE'] = 'application/json'
            response = client.post(f'{epts.MODELS_URL}/250',
                                   data=json.dumps({}))

        self.assertEqual(response._status_code, HTTPStatus.NOT_FOUND)

    def test_model_run_after_test_model_created(self):
        with app.test_client() as client:
            client.environ_base['CONTENT_TYPE'] = 'application/json'
            response = client.post(f'{epts.MODELS_URL}/{TEST_MODEL_ID}',
                                   data=json.dumps(({'model_name': "Basic"})))
            self.assertEqual(response._status_code, HTTPStatus.OK)
            model = response.json

        with app.test_client() as client:
            client.environ_base['CONTENT_TYPE'] = 'application/json'
            model_after_run = client.put(f'{epts.MODEL_RUN_URL}/{TEST_TURNS}',
                                         data=json.dumps(model))

        self.assertEqual(model_after_run._status_code, HTTPStatus.OK)
        self.assertLess(model.get('period'),
                        model_after_run.json.get('period'))

    def test_get_source_code(self):
        """
        test if we can get source code
        """
        sources = SourceCode(Resource)
        models = Models(Resource)
        with app.test_request_context():
            api_ret = models.get()
        for model in api_ret:
            if model.get('active'):
                sources_ret = sources.get(model.get('modelID'))
                import APIServer.source_api as src_api
                src_code = src_api.get_source_code(model.get('modelID'))
                self.assertEqual(sources_ret, src_code)
            else:
                print('skip inactive model')

if __name__ == "__main__":
    main()
