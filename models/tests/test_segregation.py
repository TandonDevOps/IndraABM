"""
This is the test suite for basic.py.
"""

from unittest import TestCase, skip  # , main

from models.segregation import Segregation, main, MODEL_NAME, segregation_grps


class SegregationTestCase(TestCase):
    def setUp(self):
        self.segregation = Segregation(MODEL_NAME, grp_struct=segregation_grps)

    def tearDown(self):
        self.segregation = None

    def test_run(self):
        """
        Does running the model work? (return of 0)
        """
        self.assertEqual(0, self.segregation.run())

    def test_main(self):
        """
        Does the main func of the model work? (return of 0)
        """
        self.assertEqual(0, main())
