"""
This is the test suite for fashion.py.
"""

from unittest import TestCase, skip  # , main

from models.fashion import MODEL_NAME, Fashion, fashion_grps, main


class FashionTestCase(TestCase):
    def setUp(self):
        self.fashion = Fashion(MODEL_NAME, grp_struct=fashion_grps)

    def tearDown(self):
        self.fashion = None

    def test_run(self):
        """
        Does running the model work? (return of 0)
        """
        self.assertEqual(0, self.fashion.run())

    def test_main(self):
        """
        Does the main func of the model work? (return of 0)
        """
        self.assertEqual(0, main())
