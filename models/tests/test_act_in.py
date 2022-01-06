"""
This is the test suite for basic.py.
"""

from unittest import TestCase, skip
from models import act_in as AI 

class ActInTestCase(TestCase):
    def setUp(self):
        import lib.space as spc
        spc.region_dict = {}
        self.act_in = AI.ActIn(AI.MODEL_NAME, grp_struct=AI.act_in_grps)

    def tearDown(self):
        self.act_in = None

    def test_get_near_and_far_grps(self):
        pass

    def test_act_val(self):
       act_power = 0
       in_power = 0
       act_in_calc = (act_power * AI.act_in_grps[AI.ACTIVE][AI.ACT_STRENGTH]
                      + in_power * AI.act_in_grps[AI.INACTIVE][AI.IN_STRENGTH] 
                      + AI.act_in_grps[AI.INACTIVE][AI.BIAS])
       self.assertEqual(AI.act_val(act_power,in_power), act_in_calc), 

    def test_run(self):
        """
        Does running the model work? (return of 0)
        """
        self.assertEqual(0, self.act_in.run())

    def test_main(self):
        """
        Does the main func of the model work? (return of 0)
        """
        self.assertEqual(0, AI.main())
