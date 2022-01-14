"""
This is the test suite for minesweeper.py.
"""

from unittest import TestCase, skip  # , main

from models.minesweeper import Minesweeper, main, MODEL_NAME, minesweep_grps


class MinesweeperTestCase(TestCase):
    def setUp(self):
        import lib.space as spc
        spc.region_dict = {}
        self.mine = Minesweeper(MODEL_NAME, grp_struct=minesweep_grps,random_placing=False)

    def tearDown(self):
        self.mine = None

    # @skip("Problem at present with grid being all full.")
    def test_run(self):
        """
        Does running the model work? (return of 0)
        """
        self.assertEqual(0, self.mine.run())

    @skip("Problem at present with grid being all full.")
    def test_main(self):
        """
        Does the main func of the model work? (return of 0)
        """
        self.assertEqual(0, main())
