"""
This is the test suite for basic.py.
"""

from unittest import TestCase, skip  # , main

from models.act_in import ActIn, main, MODEL_NAME, act_in_grps


class ActInTestCase(TestCase):
    def setUp(self):
        self.act_in = ActIn(MODEL_NAME, grp_struct=act_in_grps)

    def tearDown(self):
        self.act_in = None

    def test_get_near_and_far_grps(self):
        pass

    def test_run(self):
        """
        Does running the model work? (return of 0)
        """
        self.assertEqual(0, self.act_in.run())

    def test_main(self):
        """
        Does the main func of the model work? (return of 0)
        """
        self.assertEqual(0, main())
