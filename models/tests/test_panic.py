"""
This is the test suite for panic.py.
"""

from unittest import TestCase  # , main
from models.panic import Panic, main, MODEL_NAME, panic_grps


class PanicTestCase(TestCase):
    def setUp(self):
        self.panic = Panic(
            MODEL_NAME, grp_struct=panic_grps, random_placing=False
        )

    def tearDown(self):
        self.panic = None

    def test_run(self):
        """
        Does running the model work? (return of 0)
        """
        self.assertEqual(0, self.panic.run())

    def test_main(self):
        """
        Does the main func of the model work? (return of 0)
        """
        self.assertEqual(0, main())
