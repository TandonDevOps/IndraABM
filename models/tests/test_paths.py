"""
This is the test for the paths model.
"""


from unittest import TestCase
from models.paths import Paths, main, MODEL_NAME
from models.paths import paths_grps
from models.paths import create_land, create_person


class PathsTestCase(TestCase):
    def setUp(self):
        self.paths = Paths(MODEL_NAME, grp_struct=paths_grps)
        self.land = create_land("Grassland", 0, exec_key=self.ef.exec_key)
        self.person = create_person("Person", 0, exec_key=self.ef.exec_key)


    def tearDown(self):
        self.paths = None

    # def test_main(self):
        # self.assertEqual(0, main())

    # def test_run(self):
        # self.assertEqual(0, self.paths.run())

