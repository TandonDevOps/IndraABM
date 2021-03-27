
"""
This is a minimal model that inherits from model.py
and just sets up a couple of agents in two groups that
do nothing except move around randomly.
"""

from lib.agent import Agent
from lib.display_methods import RED, BLUE
from lib.model import Model, NUM_MBRS, MBR_CREATOR, MBR_ACTION, COLOR
from lib.env import PopHist
from registry.registry import get_agent
from capital.trade_utils2 import GEN_UTIL_FUNC, UTIL_FUNC, AMT_AVAIL
from capital.trade_utils2 import seek_a_trade
from lib.utils import Debug

DEBUG = Debug()

MODEL_NAME = "edgeworthbox"
DEF_WINE_MBRS = 1
DEF_CHEESE_MBRS = 1
DEF_NUM_CHEESE = 4
DEF_NUM_WINE = 4

UTIL = "util"
PRE_TRADE_UTIL = "pre_trade_util"
TRADE_WITH = "trades_with"

GOODS = "goods"
INCR = "incr"

WINE_AGENT = "Wine agent"
START_WINE = "start_wine"
CHEESE_AGENT = "Cheese agent"
START_CHEESE = "start_cheese"

wine_goods = {"wine": {AMT_AVAIL: DEF_NUM_WINE,
                       UTIL_FUNC: GEN_UTIL_FUNC, INCR: 0},
              "cheese": {AMT_AVAIL: 0,
                         UTIL_FUNC: GEN_UTIL_FUNC, INCR: 0}}
cheese_goods = {"wine": {AMT_AVAIL: 0,
                         UTIL_FUNC: GEN_UTIL_FUNC, INCR: 0},
                "cheese": {AMT_AVAIL: DEF_NUM_CHEESE,
                           UTIL_FUNC: GEN_UTIL_FUNC, INCR: 0}}


def create_wine(name, i, action=None, **kwargs):
    return Agent(WINE_AGENT,
                 action=seek_a_trade,
                 attrs={GOODS: wine_goods,
                        UTIL: 0,
                        PRE_TRADE_UTIL: 0,
                        TRADE_WITH: "Cheese holders"},
                 **kwargs)


def create_cheese(name, i, action=None, **kwargs):
    return Agent(CHEESE_AGENT,
                 action=seek_a_trade,
                 attrs={GOODS: cheese_goods,
                        UTIL: 0,
                        PRE_TRADE_UTIL: 0,
                        TRADE_WITH: "Wine holders"},
                 **kwargs)


edge_grps = {
    "wine_grp": {
        MBR_CREATOR: create_wine,
        MBR_ACTION: seek_a_trade,
        NUM_MBRS: DEF_WINE_MBRS,
        COLOR: RED
    },
    "cheese_grp": {
        MBR_CREATOR: create_cheese,
        MBR_ACTION: seek_a_trade,
        NUM_MBRS: DEF_CHEESE_MBRS,
        COLOR: BLUE
    },
}


class EdgeworthBox(Model):
    """
    This class should just create a basic model that runs, has
    some agents that move around, and allows us to test if
    the system as a whole is working.
    It turns out that so far, we don't really need to subclass anything!
    """
    def handle_props(self, props, model_dir=None):
        super().handle_props(props, model_dir='capital')
        wine_goods["wine"][AMT_AVAIL] = self.props.get(START_WINE)
        cheese_goods["cheese"][AMT_AVAIL] = self.props.get(START_CHEESE)
        self.last_cheese_amt = cheese_goods["cheese"][AMT_AVAIL]

    def create_pop_hist(self):
        """
        Set up our pop hist object to record amount traded per period.
        Directly accessing self.env.pop_hist breaks encapsulation.
        But that's OK since we plan to move pop_hist into model.
        """
        self.env.pop_hist = PopHist()  # this will record pops across time
        self.env.pop_hist.record_pop("cheese", DEF_NUM_CHEESE)
        self.env.pop_hist.record_pop("wine", 0)

    def update_pop_hist(self):
        """
        This is our hook into the env to record the number of trades each
        period.
        Directly accessing self.env.pop_hist breaks encapsulation.
        But that's OK since we plan to move pop_hist into model.
        """
        if DEBUG.debug2:
            print(repr(self))
        cheesey = get_agent(CHEESE_AGENT, exec_key=self.exec_key)
        self.env.pop_hist.record_pop("cheese",
                                     cheesey[GOODS]['cheese'][AMT_AVAIL])
        self.env.pop_hist.record_pop("wine",
                                     cheesey[GOODS]['wine'][AMT_AVAIL])
        if self.last_cheese_amt == cheesey[GOODS]['cheese'][AMT_AVAIL]:
            print("At equilibrium")
        else:
            self.last_cheese_amt = cheesey[GOODS]['cheese'][AMT_AVAIL]

    def rpt_census(self, acts, moves):
        """
        This is where we override the default census report.
        Report the amount of cheese and wine of cheese_agent
        """
        cheesey = get_agent(CHEESE_AGENT, exec_key=self.exec_key)
        cheese_rpt = f"Holdings of cheese agent\
                      \ncheese amount: {cheesey[GOODS]['cheese'][AMT_AVAIL]}\
                      \nwine amount: {cheesey[GOODS]['wine'][AMT_AVAIL]}"
        winey = get_agent(WINE_AGENT, exec_key=self.exec_key)
        wine_rpt = f"Holdings of wine agent\
                    \ncheese amount: {winey[GOODS]['cheese'][AMT_AVAIL]}\
                    \nwine amount: {winey[GOODS]['wine'][AMT_AVAIL]}"
        return cheese_rpt + "\n" + wine_rpt


def create_model(serial_obj=None, props=None):
    """
    This is for the sake of the API server:
    """
    if serial_obj is not None:
        return EdgeworthBox(serial_obj=serial_obj)
    else:
        return EdgeworthBox(MODEL_NAME, grp_struct=edge_grps, props=props)


def main():
    model = create_model()
    model.run()
    return 0


if __name__ == "__main__":
    main()
