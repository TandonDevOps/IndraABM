"""
This is the test suite for firefly.py.
"""

from unittest import TestCase, skip

from lib.agent import Agent, MOVE
import models.firefly as ff


class FireflyTestCase(TestCase):
    def setUp(self):
        self.mdl = ff.create_model()
        self.firefly = ff.create_firefly("firefly", 0, action=ff.firefly_action,
                                         exec_key=self.mdl.exec_key)

    def tearDown(self):
        self.mdl = None
        self.firefly = None

    def test_run(self):
        """
        Does running the model work? (return of 0)
        """
        self.assertEqual(0, self.mdl.run())

    def test_main(self):
        """
        Does the main func of the model work? (return of 0)
        """
        self.assertEqual(0, ff.main())

    def test_firefly_action(self):
        """
        Fireflies have to move all the time!
        """
        self.assertEqual(ff.firefly_action(self.firefly), MOVE)

    def test_adjust_blink_freq(self):
        """
        Test adjust_blink_frequency function to see if it initializes the
        BLINK_FREQ
        """
        ff.adjust_blink_freq(self.firefly)

        # A random blink frequency > 0 should have been generated
        self.assertGreater(self.firefly[ff.BLINK_FREQ], 0)
