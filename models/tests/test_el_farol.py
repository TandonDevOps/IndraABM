"""
This is the test suite for el_farol.py.
"""

from unittest import TestCase, main, skip

from lib.agent import MOVE
import models.el_farol as el_farol
from models.el_farol import MODEL_NAME
from models.el_farol import ElFarol, el_farol_grps, drinker_action
from models.el_farol import create_drinker


def header(s):
    print("\n==================")
    print(s)
    print("==================")


class ElFarolTestCase(TestCase):

    def setUp(self):
        header("Setting up")
        # Create an evirement for testing and get exect key.
        self.ef = ElFarol(MODEL_NAME, grp_struct=el_farol_grps)
        self.drinker = create_drinker("drinker", 0, exec_key=self.ef.exec_key)

    def tearDown(self):
        """
        This should undo what setup() does!
        """
        header("Tearing Down")
        self.bob = None

    def test_drinker_action(self):
        """
        Test drinker action
        """
        return self.assertEqual(MOVE,
                                drinker_action(self.drinker))

    @skip("Not implimented yet")
    def test_discourage(self):
        discouraged = el_farol.discourage(1)
        self.assertEqual(discouraged, 1)

    def test_main(self):
        self.assertEqual(el_farol.main(), 0)


if __name__ == '__main__':
    main()
