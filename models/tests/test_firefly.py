"""
This is the test suite for firefly.py.
"""

from unittest import TestCase, skip  # , main

from models.firefly import Firefly, main, MODEL_NAME, firefly_grps


class FireflyTestCase(TestCase):
    def setUp(self):
        self.firefly = Firefly(MODEL_NAME, grp_struct=firefly_grps)

    def tearDown(self):
        self.firefly = None

    def test_run(self):
        """
        Does running the model work? (return of 0)
        """
        self.assertEqual(0, self.firefly.run())

    def test_main(self):
        """
        Does the main func of the model work? (return of 0)
        """
        self.assertEqual(0, main())
