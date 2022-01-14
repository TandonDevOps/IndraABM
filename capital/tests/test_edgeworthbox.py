"""
This is the test suite for edgeworthbox.py.
"""

from unittest import TestCase, main
import capital.edgeworthbox as edge
from capital.edgeworthbox import UTIL, PRE_TRADE_UTIL, TRADE_WITH, GOODS
from capital.edgeworthbox import create_cheese, create_wine


class EdgeworthboxTestCase(TestCase):

    def test_create_cheese(self):
        self.trader = create_cheese("cheese", 0)
        self.assertTrue(isinstance(self.trader.name, str))
        self.assertTrue(isinstance(self.trader[GOODS], dict))
        self.assertEqual(self.trader[UTIL], 0)
        self.assertEqual(self.trader[PRE_TRADE_UTIL], 0)
        self.assertTrue(isinstance(self.trader[TRADE_WITH], str))

    def test_create_wine(self):
        self.trader = create_wine("wine", 0)
        self.assertTrue(isinstance(self.trader.name, str))
        self.assertTrue(isinstance(self.trader[GOODS], dict))
        self.assertEqual(self.trader[UTIL], 0)
        self.assertEqual(self.trader[PRE_TRADE_UTIL], 0)
        self.assertTrue(isinstance(self.trader[TRADE_WITH], str))

    def test_main(self):
        self.assertEqual(edge.main(), 0)

    if __name__ == '__main__':
        main()
