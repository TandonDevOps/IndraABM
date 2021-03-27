"""
This is a minimal model that inherits from model.py
and just sets up a couple of agents in two groups that
do nothing except move around randomly.
"""
import os

from lib.agent import Agent, MOVE
from lib.display_methods import GREEN
from lib.model import Model, MBR_CREATOR, NUM_MBRS, MBR_ACTION
from lib.model import NUM_MBRS_PROP, COLOR
from lib.env import PopHist
# import capital.trade_utils as tu
from capital.trade_utils2 import seek_a_trade, GEN_UTIL_FUNC, ACCEPT
from capital.trade_utils2 import AMT_AVAIL, endow, UTIL_FUNC, TRADER1, TRADER2

MODEL_NAME = "money"
DUR = "durability"
TRADE_COUNT = "trade_count"
INCR = "incr"
DIVISIBILITY = "divisibility"
IS_ALLOC = "is_allocated"
AGE = "age"
GOODS = "goods"

DEF_NUM_TRADERS = 4
MONEY_MAX_UTIL = 100
INIT_COUNT = 0  # a starting point for trade_count

START_GOOD_AMT = 5
EQUILIBRIUM_DECLARED = 10

# a counter for counting number of continuous periods with no trade
eq_count = 0
# a dictionary storing the "trade_count" for each good from the last period
prev_trade = {'cow': 0,
              'gold': 0,
              'cheese': 0,
              'banana': 0,
              'diamond': 0,
              'avocado': 0,
              'stone': 0,
              'milk': 0,
              }

# these are the goods we hand out at the start:
natures_goods = {
    # add initial value to this data?
    # color choice isn't working yet, but we want to build it in
    "cow": {AMT_AVAIL: START_GOOD_AMT, UTIL_FUNC: GEN_UTIL_FUNC,
            INCR: 0, DUR: 0.8, DIVISIBILITY: 1.0,
            TRADE_COUNT: 0, IS_ALLOC: False,
            AGE: 1, },
    "cheese": {AMT_AVAIL: START_GOOD_AMT, UTIL_FUNC: GEN_UTIL_FUNC,
               INCR: 0, DUR: 0.5, DIVISIBILITY: 0.4,
               TRADE_COUNT: 0, IS_ALLOC: False,
               AGE: 1, },
    "gold": {AMT_AVAIL: START_GOOD_AMT, UTIL_FUNC: GEN_UTIL_FUNC,
             INCR: 0, DUR: 1.0, DIVISIBILITY: 0.05,
             TRADE_COUNT: 0, IS_ALLOC: False,
             AGE: 1, },
    "banana": {AMT_AVAIL: START_GOOD_AMT, UTIL_FUNC: GEN_UTIL_FUNC,
               INCR: 0, DUR: 0.2, DIVISIBILITY: 0.2,
               TRADE_COUNT: 0, IS_ALLOC: False,
               AGE: 1, },
    "diamond": {AMT_AVAIL: START_GOOD_AMT, UTIL_FUNC: GEN_UTIL_FUNC,
                INCR: 0, DUR: 1.0, DIVISIBILITY: 0.8,
                TRADE_COUNT: 0, IS_ALLOC: False,
                AGE: 1, },
    "avocado": {AMT_AVAIL: START_GOOD_AMT, UTIL_FUNC: GEN_UTIL_FUNC,
                INCR: 0, DUR: 0.3, DIVISIBILITY: 0.5,
                TRADE_COUNT: 0, IS_ALLOC: False,
                AGE: 1, "color": GREEN},
    "stone": {AMT_AVAIL: START_GOOD_AMT, UTIL_FUNC: GEN_UTIL_FUNC,
              INCR: 0, DUR: 1.0, DIVISIBILITY: 1.0,
              TRADE_COUNT: 0, IS_ALLOC: False,
              AGE: 1, },
    "milk": {AMT_AVAIL: START_GOOD_AMT, UTIL_FUNC: GEN_UTIL_FUNC,
             INCR: 0, DUR: 0.2, DIVISIBILITY: 0.15,
             TRADE_COUNT: 0, IS_ALLOC: False,
             AGE: 1, },
}


class Good:
    def __init__(self, name, amt, age=0):
        self.amt = amt
        self.dur_decr = natures_goods[name][DUR]
        self.util_func = natures_goods[name][UTIL_FUNC]
        self.age = age

    def get_decr_amt(self):
        return self.dur_decr * self.age

    def decay(self):
        self.age += 1


def create_trader(name, i, action=None, **kwargs):
    """
    A func to create a trader.
    """
    return Agent(name + str(i),
                 action=action,
                 # goods will now be a dictionary like:
                 # goods["cow"] = [cowA, cowB, cowC, etc.]
                 attrs={GOODS: {},
                        "util": 0,
                        "pre_trade_util": 0},
                 **kwargs)


def trader_action(agent, **kwargs):
    """
    A simple default agent action.
    """
    outcome = seek_a_trade(agent, **kwargs)
    if outcome.status is ACCEPT:
        good1 = outcome.get_good(TRADER1)
        good2 = outcome.get_good(TRADER2)
        # update current period's trade count in natures_good
        natures_goods[good1][TRADE_COUNT] += 1
        natures_goods[good2][TRADE_COUNT] += 1
        # why do goods only age if trade is accepted?
        agent[GOODS][good1][AGE] += 1
        agent[GOODS][good2][AGE] += 1
    return MOVE


money_grps = {
    "traders": {
        MBR_CREATOR: create_trader,
        MBR_ACTION: trader_action,
        NUM_MBRS: DEF_NUM_TRADERS,
        NUM_MBRS_PROP: "num_traders",
        COLOR: GREEN,
    },
}


def amt_adjust(nature):
    """
    A func to adjust good amount with divisibility
    """
    for good in nature:
        nature[good][AMT_AVAIL] = nature[good][AMT_AVAIL] / \
                                  nature[good][DIVISIBILITY]


def nature_to_traders(traders, nature):
    """
    A func to do the initial endowment from nature to all traders
    """
    # before endowment from nature to trader,
    # first adjust the good amt by divisibility
    amt_adjust(nature)
    for trader in traders:
        endow(traders[trader], nature)
        for good in traders[trader][GOODS]:
            if traders[trader][GOODS][good][AMT_AVAIL] != 0:
                nature[good][IS_ALLOC] = True
        print(repr(traders[trader]))


TRADER_GRP = 0


class Money(Model):
    """
    The model class for the Menger money model.
    """
    def __init__(self, model_nm="money", props=None,
                 grp_struct=money_grps,
                 env_action=None,
                 serial_obj=None, exec_key=None):
        super().__init__(model_nm=model_nm, props=props,
                         grp_struct=grp_struct,
                         serial_obj=serial_obj,
                         exec_key=exec_key)
        self.prev_trades = 0
        self.no_trade_periods = 0

    def handle_props(self, props, model_dir=None):
        super().handle_props(props, model_dir='capital')

    def create_groups(self):
        grps = super().create_groups()
        nature_to_traders(grps[TRADER_GRP], natures_goods)
        return grps

    def create_pop_hist(self):
        """
        Set up our pop hist object to record amount traded per period.
        Directly accessing self.env.pop_hist breaks encapsulation.
        But that's OK since we plan to move pop_hist into model.
        """
        self.env.pop_hist = PopHist()  # this will record pops across time
        for good in natures_goods:
            if natures_goods[good]["is_allocated"] is True:
                self.env.pop_hist.record_pop(good, INIT_COUNT)

    def update_pop_hist(self):
        """
        This is our hook into the env to record the number of trades each
        period.
        Directly accessing self.env.pop_hist breaks encapsulation.
        But that's OK since we plan to move pop_hist into model.
        """
        for good in natures_goods:
            if natures_goods[good]["is_allocated"] is True:
                self.env.pop_hist.record_pop(good,
                                             natures_goods[good][TRADE_COUNT])

    def rpt_census(self, acts, moves):
        """
        This is where we override the default census report.
        """
        global prev_trade, eq_count
        # get_env(execution_key=execution_key)
        trade_count_dic = {x: natures_goods[x]["trade_count"]
                           for x in natures_goods}
        if trade_count_dic == prev_trade:
            eq_count += 1
        else:
            eq_count = 0
        # EQUILIBRIUM_DECLARED may be changed
        if eq_count >= EQUILIBRIUM_DECLARED:
            print("No trade between agents for", eq_count,
                  "periods. Equilibrium may have been reached.")
        prev_trade = trade_count_dic
        return "Number of trades last period: \n" \
            + str(trade_count_dic) + "\n"


def create_model(serial_obj=None, props=None):
    """
    This is for the sake of the API server:
    """
    if serial_obj is not None:
        return Money(serial_obj=serial_obj)
    else:
        return Money(MODEL_NAME, grp_struct=money_grps, props=props)


def main():
    model = create_model()
    model.run()
    return 0


if __name__ == "__main__":
    if os.environ["user_type"] == "test":
        os.environ["user_type"] = "terminal"
        import cProfile
        cProfile.run('main()')
        exit()
    main()
