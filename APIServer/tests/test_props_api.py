"""
"""
import json
from unittest import TestCase, main, skip

from APIServer.props_api import get_props
from APIServer.api_utils import ERROR

from lib.utils import PA_INDRA_NET, get_indra_home

BASIC_MODEL_ID = 0
BAD_MODEL_ID = -999
indra_dir = get_indra_home(PA_INDRA_NET)


class TestPropsAPI(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_props(self):
        """
        See if props can be gotten!
        We will try both the error case and a good case.
        """
        ret = get_props(BAD_MODEL_ID, "nonsense")
        print("Ret = ", ret)
        self.assertTrue(ERROR in ret)
        ret = get_props(BASIC_MODEL_ID, indra_dir)
        print("Ret = ", ret)
        self.assertTrue(ERROR not in ret)

if __name__ == "__main__":
    main()
