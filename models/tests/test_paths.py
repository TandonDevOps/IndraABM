"""
This is the test for the paths model.
"""


from unittest import TestCase
from models.paths import Paths, main, MODEL_NAME
from models.paths import paths_grps


class PathsTestCase(TestCase):
    def setUp(self):
        self.paths = Paths(MODEL_NAME, grp_struct=paths_grps)

