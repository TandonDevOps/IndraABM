
"""
This is a minimal model that inherits from model.py
and just sets up a couple of agents in two groups that
do nothing except move around randomly.
"""
import lib.actions as actions
import lib.model as mdl
import lib.env as env
import capital.trade_utils as utl

DEBUG = actions.DEBUG

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

wine_goods = {"wine": {utl.AMT_AVAIL: DEF_NUM_WINE,
                       utl.UTIL_FUNC: utl.GEN_UTIL_FUNC, INCR: 0},
              "cheese": {utl.AMT_AVAIL: 0,
                         utl.UTIL_FUNC: utl.GEN_UTIL_FUNC, INCR: 0}}
cheese_goods = {"wine": {utl.AMT_AVAIL: 0,
                         utl.UTIL_FUNC: utl.GEN_UTIL_FUNC, INCR: 0},
                "cheese": {utl.AMT_AVAIL: DEF_NUM_CHEESE,
                           utl.UTIL_FUNC: utl.GEN_UTIL_FUNC, INCR: 0}}


def create_wine(name, i, action=None, **kwargs):
    return actions.agt.Agent(WINE_AGENT,
                             action=utl.seek_a_trade,
                             attrs={GOODS: wine_goods,
                                    UTIL: 0,
                                    PRE_TRADE_UTIL: 0,
                                    TRADE_WITH: "Cheese holders"},
                             **kwargs)


def create_cheese(name, i, action=None, **kwargs):
    return actions.agt.Agent(CHEESE_AGENT,
                             action=utl.seek_a_trade,
                             attrs={GOODS: cheese_goods,
                                    UTIL: 0,
                                    PRE_TRADE_UTIL: 0,
                                    TRADE_WITH: "Wine holders"},
                             **kwargs)


edge_grps = {
    "wine_grp": {
        mdl.MBR_CREATOR: create_wine,
        mdl.MBR_ACTION: utl.seek_a_trade,
        mdl.NUM_MBRS: DEF_WINE_MBRS,
        mdl.COLOR: actions.RED
    },
    "cheese_grp": {
        mdl.MBR_CREATOR: create_cheese,
        mdl.MBR_ACTION: utl.seek_a_trade,
        mdl.NUM_MBRS: DEF_CHEESE_MBRS,
        mdl.COLOR: actions.BLUE
    },
}


class EdgeworthBox(mdl.Model):
    """
    This class should just create a basic model that runs, has
    some agents that move around, and allows us to test if
    the system as a whole is working.
    It turns out that so far, we don't really need to subclass anything!
    """
    def handle_props(self, props, model_dir=None):
        super().handle_props(props, model_dir='capital')
        wine_goods["wine"][utl.AMT_AVAIL] = self.props.get(START_WINE)
        cheese_goods["cheese"][utl.AMT_AVAIL] = self.props.get(START_CHEESE)
        self.last_cheese_amt = cheese_goods["cheese"][utl.AMT_AVAIL]

    def create_pop_hist(self):
        """
        Set up our pop hist object to record amount traded per period.
        Directly accessing self.env.pop_hist breaks encapsulation.
        But that's OK since we plan to move pop_hist into model.
        """
        self.env.pop_hist = env.PopHist()  # this will record pops across time
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
        cheesey = actions.get_agent(CHEESE_AGENT, exec_key=self.exec_key)
        self.env.pop_hist.record_pop("cheese",
                                     cheesey[GOODS]['cheese'][utl.AMT_AVAIL])
        self.env.pop_hist.record_pop("wine",
                                     cheesey[GOODS]['wine'][utl.AMT_AVAIL])
        if self.last_cheese_amt == cheesey[GOODS]['cheese'][utl.AMT_AVAIL]:
            print("At equilibrium")
        else:
            self.last_cheese_amt = cheesey[GOODS]['cheese'][utl.AMT_AVAIL]

    def rpt_census(self, acts, moves):
        """
        This is where we override the default census report.
        Report the amount of cheese and wine of cheese_agent
        """
        cheesey = actions.get_agent(CHEESE_AGENT, exec_key=self.exec_key)
        cheese_rpt = f"Holdings of cheese agent\n\
                      cheese amount: {cheesey[GOODS]['cheese'][utl.AMT_AVAIL]}\
                      \nwine amount: {cheesey[GOODS]['wine'][utl.AMT_AVAIL]}"
        winey = actions.get_agent(WINE_AGENT, exec_key=self.exec_key)
        wine_rpt = f"Holdings of wine agent\n\
                    cheese amount: {winey[GOODS]['cheese'][utl.AMT_AVAIL]}\
                    \nwine amount: {winey[GOODS]['wine'][utl.AMT_AVAIL]}"
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
