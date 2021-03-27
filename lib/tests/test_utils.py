"""
This is the test suite for utils.py.
"""

import os
from unittest import TestCase

from lib.utils import Debug
from lib.utils import INDRA_DEBUG_VAR, INDRA_DEBUG2_VAR, INDRA_DEBUG3_VAR
from lib.utils import INDRA_DEBUG_LIB_VAR, INDRA_DEBUG2_LIB_VAR


class DebugTestCase(TestCase):
    """
    NOTE/README:
    Here we initialize a new Debug object each time we test, because we keep
    changing the environment variables for testing. The Debug class reads the
    environment variables when it was created and thus a new Debug object needs
    to be created whenever we change the environment variables for testing.
    """

    def setUp(self):
        self.true_values = ["1", "True", "true"]
        self.false_values = ["0", "False", "false", "", "None"]

    def test_debug(self):
        env_var = INDRA_DEBUG_VAR

        # Remove related environment variable for this test
        # Test the default value without any environment variable set
        os.environ.pop(env_var, None)
        self.assertFalse(Debug().debug)

        # Test debugging statement when it is set to various true values
        for value in self.true_values:
            os.environ[env_var] = value
            self.assertTrue(Debug().debug)

        # Test debugging statement when it is set to various false values
        for value in self.false_values:
            os.environ[env_var] = value
            self.assertFalse(Debug().debug)

    def test_debug2(self):
        env_var = INDRA_DEBUG2_VAR

        # Remove related environment variable for this test
        # Test the default value without any environment variable set
        os.environ.pop(env_var, None)
        self.assertFalse(Debug().debug2)

        # Test debugging statement when it is set to various true values
        for value in self.true_values:
            os.environ[env_var] = value
            self.assertTrue(Debug().debug2)

        # Test debugging statement when it is set to various false values
        for value in self.false_values:
            os.environ[env_var] = value
            self.assertFalse(Debug().debug2)

    def test_debug3(self):
        env_var = INDRA_DEBUG3_VAR

        # Remove related environment variable for this test
        # Test the default value without any environment variable set
        os.environ.pop(env_var, None)
        self.assertFalse(Debug().debug3)

        # Test debugging statement when it is set to various true values
        for value in self.true_values:
            os.environ[env_var] = value
            self.assertTrue(Debug().debug3)

        # Test debugging statement when it is set to various false values
        for value in self.false_values:
            os.environ[env_var] = value
            self.assertFalse(Debug().debug3)

    def test_debug_lib(self):
        env_var = INDRA_DEBUG_LIB_VAR

        # Remove related environment variable for this test
        # Test the default value without any environment variable set
        os.environ.pop(env_var, None)
        self.assertFalse(Debug().debug_lib)

        # Test debugging statement when it is set to various true values
        for value in self.true_values:
            os.environ[env_var] = value
            self.assertTrue(Debug().debug_lib)

        # Test debugging statement when it is set to various false values
        for value in self.false_values:
            os.environ[env_var] = value
            self.assertFalse(Debug().debug_lib)

    def test_debug2_lib(self):
        env_var = INDRA_DEBUG2_LIB_VAR

        # Remove related environment variable for this test
        # Test the default value without any environment variable set
        os.environ.pop(env_var, None)
        self.assertFalse(Debug().debug2_lib)

        # Test debugging statement when it is set to various true values
        for value in self.true_values:
            os.environ[env_var] = value
            self.assertTrue(Debug().debug2_lib)

        # Test debugging statement when it is set to various false values
        for value in self.false_values:
            os.environ[env_var] = value
            self.assertFalse(Debug().debug2_lib)
