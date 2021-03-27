"""
This is the test suite for creating basic.ipynb. WIP
"""

from unittest import TestCase
import sys

from notebooks.create_model_nb import main

class create_basic_testcase(TestCase):
    def setUp(self):
        sys.argv = ["", "../models/basic.py"]
    def test_main(self):
        """
        Does the main func without problems? (return of 0)
        """
        self.assertEqual(None, main())
