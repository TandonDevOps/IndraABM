"""
This is the test suite for fashion.py.
"""

import math
import numpy as np
from unittest import TestCase, skip  # , main

from models.fashion import (
    MODEL_NAME,
    Fashion,
    fashion_grps,
    main,
    new_color_pref,
    env_unfavorable,
    NEUTRAL,
    TOO_SMALL,
    RED_SIN,
    BLUE_SIN,
)


class FashionTestCase(TestCase):
    def setUp(self):
        self.fashion = Fashion(MODEL_NAME, grp_struct=fashion_grps)

    def tearDown(self):
        self.fashion = None

    def test_run(self):
        """
        Does running the model work? (return of 0)
        """
        self.assertEqual(0, self.fashion.run())

    def test_main(self):
        """
        Does the main func of the model work? (return of 0)
        """
        self.assertEqual(0, main())

    def test_new_color_pref(self):
        old_pref = 1
        env_color = 0.6

        # Calculate true value
        true_value = math.sin(
            np.average(
                [math.asin(old_pref), math.asin(env_color)],
                weights=[1.0, 0.6],
            )
        )

        # Test the function
        result = new_color_pref(old_pref, env_color)

        # They need to be within 2 decimal places
        self.assertAlmostEqual(result, true_value, 2)

    def test_env_unfavorable(self):
        def op1(my_pref, arg1):
            # Dummy operation for testing
            return "op1"

        def op2(my_pref, arg1):
            # Dummy operation for testing
            return "op2"

        # Check when color is red
        my_color = RED_SIN
        result_1 = env_unfavorable(my_color, None, op1, op2)
        self.assertEqual(result_1, "op1")

        # Check when color is blue
        my_color = BLUE_SIN
        result_2 = env_unfavorable(my_color, None, op1, op2)
        self.assertEqual(result_2, "op2")
