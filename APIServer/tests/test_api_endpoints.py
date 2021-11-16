import os

from http import HTTPStatus

import json
import random
import string
from unittest import TestCase, main, skip

from flask_restx import Resource

# Let's cut over to the following kind of imports:
import APIServer.api_endpoints as epts
from APIServer.api_endpoints import Props, RunModel, SourceCode
from APIServer.api_endpoints import app, HelloWorld, Endpoints, Models, CreateGroup, ModelsGenerator
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
        self.creat_model = ModelsGenerator(Resource)
        self.creat_group = CreateGroup(Resource)

    def test_hello_world(self):
        """
        See if HelloWorld works.
        """
        rv = self.hello_world.get()
        self.assertEqual(rv, {'hello': 'world'})

    # @skip("Test for 200 status code for now, need to be updated")
    def test_model_generator_create_model(self):
        """
        See if ModelsGenerator create model works.(For now only test for 200 status code)
        """
        with app.test_client() as client:
            client.environ_base['CONTENT_TYPE'] = 'application/json'
            model_generate = client.post(
                epts.MODELS_GEN_URL, data=dict(model_name='model_name'))
            print(model_generate._status_code)
        self.assertEqual(model_generate._status_code, HTTPStatus.OK)

    @skip("SKIP for now as it need exec key")
    def test_model_generator_create_group(self):
        """
        See if ModelsGenerator create group works.(For now only test for 200 status code)
        """
        with app.test_client() as client:
            client.environ_base['CONTENT_TYPE'] = 'application/json'
            model_generate_create_group = client.post(epts.MODEL_GEN_CREATE_GROUP_URL,
                                                      data=dict(group_name='test',
                                                                group_color='red',
                                                                group_number_of_members='20',
                                                                group_actions='3'))
        print("model_generate_create_group._status_code",model_generate_create_group._status_code)
        self.assertEqual(
            model_generate_create_group._status_code, HTTPStatus.OK)

    
    @skip("SKIP for now as it need exec key")
    def test_model_generator_create_actions(self):
        """
        See if ModelsGenerator create actions works.(For now only test for 200 status code)
        """
        with app.test_client() as client:
            client.environ_base['CONTENT_TYPE'] = 'application/json'
            model_generate_create_actions = client.post(epts.MODEL_GEN_CREATE_GROUP_URL,
                                                      data=dict(group_name='test',
                                                                ))
        print("model_generate_create_actions._status_code",model_generate_create_actions._status_code)
        self.assertEqual(
            model_generate_create_actions._status_code, HTTPStatus.OK)


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

    def test_model_run(self):
        """
        This is going to see if we can run a model.
        """
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
        test if we can get corresponding source code based on the MODEL_NAME
        variable
        """
        sources = SourceCode(Resource)
        models = Models(Resource)
        api_ret = None
        with app.test_request_context():
            api_ret = models.get()
        for model in api_ret:
            if model.get('active'):
                src_ret = sources.get(model.get('modelID'))
                src_ret = src_ret[src_ret.index('MODEL_NAME'):]
                src_ret = src_ret[:src_ret.index('\n')]
                model_name = src_ret[src_ret.find('\"')+1:src_ret.rfind('\"')]
                self.assertEqual(model_name, model.get('module'))
            else:
                print('skip inactive model')


if __name__ == "__main__":
    main()
