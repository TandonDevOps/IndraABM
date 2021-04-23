"""
"""
import os

import json
import random
import string
from unittest import TestCase, main, skip

from flask_restx import Resource

from registry.model_db import get_models, MODEL_ID
# Let's cut over to the following kind of imports:
import APIServer.api_endpoints as epts
from APIServer.api_endpoints import Props, RunModel
from APIServer.api_endpoints import app, HelloWorld, Endpoints, Models
from APIServer.api_endpoints import indra_dir
from APIServer.api_utils import err_return

BASIC_ID = 0
MIN_NUM_ENDPOINTS = 2

TEST_TURNS = "10"


def random_name():
    return "".join(random.choices(string.ascii_letters,
                                  k=random.randrange(1, 10)))


class TestAPI(TestCase):
    def setUp(self):
        self.hello_world = HelloWorld(Resource)
        self.endpoints = Endpoints(Resource)
        self.model = Models(Resource)
        self.pophist = epts.PopHist(Resource)
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

    def test_get_model_menu(self):
        mfm = epts.MenuForModel(Resource)
        self.assertTrue(isinstance(mfm.get(), dict))

    def test_get_models(self):
        """
        See if we can get models.
        """
        with app.test_request_context():
            api_ret = self.model.get()
        for model in api_ret:
            self.assertIn(MODEL_ID, model)

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
        """
        This is going to see if we can run a model.
        """
        model_id = BASIC_ID
        props = self.props.get(model_id)
        with app.test_client() as client:
            client.environ_base['CONTENT_TYPE'] = 'application/json'
            model_before_run = client.put('/models/props/' + str(model_id),
                            data=json.dumps(props))
        self.assertEqual(model_before_run._status_code, epts.HTTP_SUCCESS)
        with app.test_client() as client:
            client.environ_base['CONTENT_TYPE'] = 'application/json'
            print(model_before_run)
            model_after_run = client.put(f'{epts.MODEL_RUN_URL}/{TEST_TURNS}',
                                         data=json.dumps(model_before_run.json))

        self.assertEqual(model_after_run._status_code, epts.HTTP_SUCCESS)
        # This asserts that the agents are in new places... is that a good
        # test? Somewhat chancy! Depends upon which model and random movements.
        self.assertNotEqual(model_before_run.json.get('env').get('locations'),
                            model_after_run.json.get('env').get('locations'))


    def test_err_return(self):
        """
        Testing whether we are able to get the right error message
        """
        rv = err_return("error message")
        self.assertEqual(rv, {"Error:": "error message"})


if __name__ == "__main__":
    main()
