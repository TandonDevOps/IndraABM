"""
This is the test suite for wolfsheep.py.
"""

from unittest import TestCase, skip  # , main
from lib.agent import Agent
from models.wolfsheep import WolfSheep, main, MODEL_NAME, wolfsheep_grps
from models.wolfsheep import WOLF_GRP_NM, SHEEP_GRP_NM
from models.wolfsheep import (
    TIME_TO_REPRO,
    WOLF_TIME_TO_REPRO,
    SHEEP_TIME_TO_REPRO,
)
from models.wolfsheep import sheep_action, wolf_action, reproduce


class WolfSheepTestCase(TestCase):
    def setUp(self):
        import lib.space as spc
        spc.region_dict = {}
        pass

    def tearDown(self):
        pass

    def test_run(self):
        """
        Does running the model work? (return of 0)
        """
        pass

    def test_main(self):
        """
        Does the main func of the model work? (return of 0)
        """
        self.assertEqual(0, main())
