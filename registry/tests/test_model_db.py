"""
This is the test suite for model_db.py.
It assumes we have a model with ID 0 and module 'basic'.
"""

import os
from unittest import TestCase, skip
from registry import model_db as mdb

BASIC_ID = 0
BASIC_MOD = "basic"
indra_dir = os.getenv("INDRA_HOME", "/home/IndraABM/IndraABM")


class ModelDBTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_models(self):
        self.assertTrue(isinstance(mdb.get_models(indra_dir), list))

    def test_get_model_by_id(self):
        model = mdb.get_model_by_id(BASIC_ID, indra_dir)
        self.assertTrue(model[mdb.MODEL_ID] == BASIC_ID)

    def test_get_model_by_mod(self):
        model = mdb.get_model_by_mod(BASIC_MOD, indra_dir)
        self.assertTrue(model[mdb.MODEL_MOD] == BASIC_MOD)
