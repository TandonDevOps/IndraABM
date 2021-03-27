"""
This is the test suite for trade.py.
"""

from unittest import TestCase, main
from registry.registry import create_exec_env
# from capital.trade_utils import AMT_AVAIL
# from indra.agent import Agent
# from capital.trade_utils import endow, get_rand_good,
# is_depleted, transfer
# from capital.trade_utils import rand_dist, equal_dist, GOODS
from capital.trade_utils import GOODS
import capital.money as mn
from capital.money import create_trader, natures_goods
# import capital.trade_utils as tu


def header(s):
    print("\n==================")
    print(s)
    print("==================")


class MoneyTestCase(TestCase):
    def setUp(self):
        header("Setting up")

    def tearDown(self):
        header("Tearing down")

    def test_create_trader(self):
        # header("Testing create_trader")
        exec_key = create_exec_env()
        self.trader = create_trader("trader", 0, exec_key=exec_key)
        self.assertTrue(isinstance(self.trader.name, str))
        self.assertTrue(isinstance(self.trader[GOODS], dict))
        self.assertEqual(self.trader["util"], 0)

    def test_trader_action(self):
        pass
        # need to check for exec key for the get_env in trade_utils

    def test_nature_to_traders(self):
        header("Testing nature_to_traders")
        exec_key = create_exec_env()
        self.goods = natures_goods
        self.traders = {}
        self.traders["trader0"] = create_trader("trader", 0, exec_key=exec_key)
        self.traders["trader1"] = create_trader("trader", 1, exec_key=exec_key)
        mn.nature_to_traders(self.traders, self.goods)
        # goods are depleted because of empty dicts
        self.assertEqual(self.traders["trader0"][GOODS], {})
        self.assertEqual(self.traders["trader1"][GOODS], {})

    def test_main(self):
        self.assertEqual(mn.main(), 0)

    if __name__ == '__main__':
        main()
