"""
This is the test suite for trade.py.
"""

from unittest import TestCase, main, skip
from registry.registry import create_exec_env
import capital.bigbox as bigbox
from capital.bigbox import (
    MODEL_NAME,
    bigbox_grps,
    BigBox,
    create_consumer,
    create_mp,
    create_bb,
    get_rand_good,
    town_action,
    # sells_good,
    # consumer_action,
    # retailer_action,
    MIN_CONSUMER_SPENDING,
    MAX_CONSUMER_SPENDING,
    bb_capital,
    bb_expense,
)


def header(s):
    print("\n==================")
    print(s)
    print("==================")


class BigBoxTestCase(TestCase):
    def setUp(self):
        header("Setting up")
        self.bigbox = BigBox(MODEL_NAME, grp_struct=bigbox_grps,
                             env_action=town_action)
        self.consumer = create_consumer("consumer", 0,
                                        exec_key=self.bigbox.exec_key)
        self.mp = create_mp("mp", 0,
                            exec_key=self.bigbox.exec_key)

    def tearDown(self):
        header("Tearing down")
        self.bigbox = None
        self.consumer = None
        self.mp = None

    def test_create_consumer(self):
        self.assertTrue(isinstance(self.consumer.name, str))
        spending_power = self.consumer["spending_power"]
        self.assertTrue(spending_power >= MIN_CONSUMER_SPENDING and
                        spending_power <= MAX_CONSUMER_SPENDING)
        self.assertEqual(self.consumer["last_util"], 0.0)
        self.assertTrue(isinstance(self.consumer["item_needed"], str))

    def test_create_mp(self):
        self.assertTrue(isinstance(self.mp.name, str))
        self.assertTrue(self.mp["expense"] >= 0.0)
        self.assertTrue(self.mp["capital"] >= 0.0)
        self.assertTrue(isinstance(self.mp["goods_sold"], str))

    def test_create_bb(self):
        exec_key = create_exec_env()
        self.bb = create_bb("bb", 0, exec_key=exec_key)
        self.assertTrue(isinstance(self.bb.name, str))
        # to be changed when read props from user
        self.assertEqual(self.bb["expense"], bb_expense)
        self.assertEqual(self.bb["capital"], bb_capital)

    def test_get_rand_good(self):
        rand_good = get_rand_good()
        self.assertTrue(isinstance(rand_good, str))

    @skip
    def test_sell_goods(self):
        pass
        # item_needed = self.consumer["item_needed"]

    @skip
    def test_town_action(self):
        pass

    @skip
    def test_consumer_action(self):
        pass

    @skip
    def test_retailer_action(self):
        pass

    @skip
    def test_transaction(self):
        pass

    def test_main(self):
        self.assertEqual(bigbox.main(), 0)

    if __name__ == '__main__':
        main()
