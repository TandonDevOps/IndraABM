"""
This is the test suite for basic.py.
"""

from unittest import TestCase, skip

from models.game_of_life import GameOfLife, main, MODEL_NAME, game_grps


class BasicTestCase(TestCase):
    def setUp(self):
        self.g_of_l = GameOfLife(MODEL_NAME, grp_struct=game_grps)

    def tearDown(self):
        self.g_of_l = None

    def test_run(self):
        """
        Does running the model work? (return of 0)
        """
        self.assertEqual(0, self.g_of_l.run())

    def test_main(self):
        """
        Does the main func of the model work? (return of 0)
        """
        self.assertEqual(0, main())
