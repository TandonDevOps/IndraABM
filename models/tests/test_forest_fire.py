"""
This is the test suite for forest_fire.py.
"""

from unittest import TestCase
from models.forest_fire import ForestFire, main, MODEL_NAME, ff_grps
from models.forest_fire import HEALTHY, ON_FIRE
from lib.agent import Agent


class ForestFireTestCase(TestCase):
    def setUp(self):
        import lib.space as spc
        spc.region_dict = {}
        self.ff = ForestFire(MODEL_NAME, grp_struct=ff_grps)
        """
        self.htree = plant_tree("htree", 1,
                                exec_key=self.ff.exec_key)
        self.oftree = plant_tree("oftree", 1, state=OF,
                                 exec_key=self.ff.exec_key)
        """
        self.htree = Agent(
            name="htree", group=HEALTHY, exec_key=self.ff.exec_key
        )
        self.oftree = Agent(
            name="oftree", group=ON_FIRE, exec_key=self.ff.exec_key
        )

    def tearDown(self):
        self.ff = None
        self.htree = None
        self.oftree = None

    def test_run(self):
        """
        Does running the model work? (return of 0)
        """
        self.assertEqual(0, self.ff.run())

    def test_main(self):
        """
        Does the main func of the model work? (return of 0)
        """
        self.assertEqual(0, main())
