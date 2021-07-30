"""
This is the test suite for sandpile.py.
"""

from unittest import TestCase, skip

import models.sandpile as sp


class SandpileTestCase(TestCase):
    def setUp(self):
        self.pile = sp.Sandpile(sp.MODEL_NAME, grp_struct=sp.sand_grps)

    def tearDown(self):
        self.pile = None

    def test_run(self):
        """
        Does running the sandpile work? (return of 0)
        """
        self.assertEqual(0, self.pile.run())

    def test_main(self):
        """
        Does the main func of sandpile work? (return of 0)
        """
        self.assertEqual(0, sp.main())
