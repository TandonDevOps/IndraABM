"""
This is the test suite for firefly.py.
"""

from unittest import TestCase, skip  # , main

from lib.agent import Agent
from models.firefly import (
    Firefly,
    main,
    MODEL_NAME,
    firefly_grps,
    firefly_action,
    MOVE,
    BLINK_FREQUENCY,
    LAST_BLINKED_AT,
    FIREFLY_OFF,
    FIREFLY_ON,
    firefly_blink,
    adjust_blink_frequency,
)


class FireflyTestCase(TestCase):
    def setUp(self):
        self.ff = Firefly(MODEL_NAME, grp_struct=firefly_grps)
        self.firefly = Agent(name="firefly", exec_key=self.ff.exec_key)

    def tearDown(self):
        self.firefly = None

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

    def test_firefly_action(self):
        """
        Fireflies have to move all the time!
        """
        self.assertEqual(firefly_action(self.firefly), MOVE)

    def test_blink_turn_on(self):
        """
        Test the firefly_blink function and see if flips between FIREFLY_OFF
        and FIREFLY_ON based on the BLINK_FREQUENCY
        """
        # Set duration to a known value for testing purposes
        self.firefly.duration = 100

        # Set attributes to known values
        self.firefly.set_prim_group(FIREFLY_OFF)
        self.firefly.set_attr(BLINK_FREQUENCY, 10)
        self.firefly.set_attr(LAST_BLINKED_AT, 0)

        # Run the target function
        firefly_blink(self.firefly)

        # Last blink time needs to be updated
        self.assertEqual(
            self.firefly.get_attr(LAST_BLINKED_AT), self.firefly.duration
        )

        # The agent should be "blinked" since we were well over its
        # blinking frequency
        self.assertEqual(self.firefly.group_name(), FIREFLY_ON)

    def test_blink_turn_off(self):
        """
        Test if firefly_blink function immediately turns OFF an ON firefly
        """
        # Set duration to a known value for testing purposes
        self.firefly.duration = 100

        # Set attributes to known values
        self.firefly.set_prim_group(FIREFLY_ON)
        self.firefly.set_attr(BLINK_FREQUENCY, 10)
        self.firefly.set_attr(LAST_BLINKED_AT, 0)

        # Run the target function
        firefly_blink(self.firefly)

        # The firefly needs to be turned off immediately, if it is ON
        self.assertEqual(self.firefly.group_name(), FIREFLY_OFF)

    def test_adjust_blink_frequency(self):
        """
        Test adjust_blink_frequency function to see if it initializes the 
        BLINK_FREQUENCY
        """
        # Set attributes to known values
        self.firefly.duration = 100
        self.firefly.set_attr(BLINK_FREQUENCY, None)
        self.firefly.set_attr(LAST_BLINKED_AT, None)

        # Run the target function
        adjust_blink_frequency(self.firefly)

        # A random blink frequency should have been generated
        self.assertGreater(self.firefly.get_attr(BLINK_FREQUENCY), 0)

        # Last blink time should be updated
        self.assertEqual(
            self.firefly.get_attr(LAST_BLINKED_AT), self.firefly.duration
        )
