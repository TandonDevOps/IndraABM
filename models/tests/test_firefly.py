"""
This is the test suite for firefly.py.
"""

from unittest import TestCase, skip

import lib.agent as agt

from lib.agent import Agent, MOVE
import models.firefly as ff
import lib.actions as acts


class FireflyTestCase(TestCase):
    def setUp(self):
        import lib.space as spc
        spc.region_dict = {}
        self.mdl = ff.create_model()
        self.firefly = ff.create_firefly("firefly", 0, action=ff.firefly_action,
                                         exec_key=self.mdl.exec_key)
        # all agents should be in groups!
        self.off_grp = acts.get_group(ff.OFF_GRP)
        agt.join(self.off_grp, self.firefly)

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

    def test_to_blink_or_not(self):
        """
        See if code to determine blink state works.
        We expect two group names returned, and use their being
        different (or not) to see if we should change state.
        """
        # determine return is in right set:
        (old_state, new_state) = ff.to_blink_or_not(self.firefly)
        self.assertIn(old_state, (ff.ON, ff.OFF))

        # see if ON firefly turns off:
        self.firefly[ff.STATE] = ff.ON
        (old_state, new_state) = ff.to_blink_or_not(self.firefly)
        self.assertEqual(new_state, ff.OFF)

        # see if OFF firefly eventually turns on:
        self.firefly[ff.STATE] = ff.OFF
        for i in range(ff.DEF_MAX_BLINK_FREQ + 1):
            (old_state, new_state) = ff.to_blink_or_not(self.firefly)
            if ff.blink_now(self.firefly):
                self.assertEqual(new_state, ff.ON)
                break

