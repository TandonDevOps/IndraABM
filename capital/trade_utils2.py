"""
This file contains general functions useful in trading goods.
"""
import random
import copy
# import math

from registry.registry import get_env
from lib.utils import Debug

DEBUG = Debug()

TRADE_STATUS = 0

OFFER_FROM_1 = 5
OFFER_FROM_2 = 4
INIT1 = 3
INIT2 = 2
ACCEPT = 1
INADEQ = 0
REJECT = -1
NO_TRADER = -2

AMT_AVAIL = "amt_available"
GOODS = "goods"

trade_state_dict = {
    OFFER_FROM_1: "Offer 1",
    OFFER_FROM_2: "Offer 2",
    INIT1: "Init 1",
    INIT2: "Init 2",
    ACCEPT: "Accept",
    INADEQ: "Inadequate",
    REJECT: "Reject",
    NO_TRADER: "No Trader",
}

COMPLEMENTS = "complementaries"
DEF_MAX_UTIL = 20  # this should be set by the models that use this module
DIM_UTIL_BASE = 1.1  # we should experiment with this!

ESSENTIALLY_ZERO = .0001

DIGITS_TO_RIGHT = 2

max_util = DEF_MAX_UTIL

"""
All utility functions must be registered here!
"""
UTIL_FUNC = "util_func"
GEN_UTIL_FUNC = "gen_util_func"
STEEP_GRADIENT = 20


def gen_util_func(qty, divisibility):
    return max_util * ((DIM_UTIL_BASE) ** (-qty*divisibility))


def penguin_util_func(qty, divisibility=None):
    return 25 * (1 ** (-qty))


def cat_util_func(qty, divisibility=None):
    return 10 * (1 ** (-qty))


def bear_util_func(qty, divisibility=None):
    return 15 * (1 ** (-qty))


def steep_util_func(qty, divisibility=None):
    return 20 * (2 ** (-qty))


def test_util_func(f, max, d):
    for q in range(0, max):
        print(f"Utility: {f(q, d)}")


util_funcs = {
    GEN_UTIL_FUNC: gen_util_func,
    "penguin_util_func": penguin_util_func,
    "cat_util_func": cat_util_func,
    "bear_util_func": bear_util_func,
    "steep_util_func": steep_util_func
}


def get_util_func(fname):
    return util_funcs[fname]


"""
    We expect goods dictionaries to look like:
        goods = {
            "houses": { AMT_AVAIL: int, "maybe more fields": vals ... },
            "trucks": { AMT_AVAIL: int, "maybe more fields": vals ... },
            "etc.": { AMT_AVAIL: int, "maybe more fields": vals ... },
        }
    A trader is an object that can be indexed to yield a goods dictionary.
"""


def trade_debug(agent1, agent2, good1, good2, amt1, amt2, gain, loss):
    if DEBUG.debug and (good1 == "gold" or good1 == "gold"):
        print(f"       {agent1.name} is offering {amt1} of {good1} to "
              + f"{agent2.name} for {amt2} of {good2} with a "
              + f"gain of {round(gain, 2)} and "
              + f"a loss of {round(loss, 2)}")


def is_complement(trader, good, comp):
    """
    see if 'comp' is complement of 'good'
    """
    if comp in trader[GOODS][good][COMPLEMENTS]:
        return True
    else:
        return False


def check_complement(trader):
    """
    see if COMPLEMENT is an attribute in trader
    """
    if COMPLEMENTS in trader[GOODS]:
        return True
    else:
        return False


def is_depleted(goods_dict):
    """
    See if `goods_dict` has any non-zero amount of goods in it.
    """
    for good in goods_dict:
        if goods_dict[good][AMT_AVAIL] > 0:
            return False
    # if all goods are 0 (or less) dict is empty:
    return True


def transfer(to_goods, from_goods, good_nm, amt=None, comp=False):
    """
    Transfer goods between two goods dicts.
    Use `amt` if it is not None.
    """
    nature = copy.deepcopy(from_goods)
    if not amt:
        amt = from_goods[good_nm][AMT_AVAIL]
    for good in from_goods:
        if good in to_goods:
            amt_before_add = to_goods[good][AMT_AVAIL]
        else:
            amt_before_add = 0
        to_goods[good] = nature[good]
        if good != good_nm:
            to_goods[good][AMT_AVAIL] = amt_before_add
        else:
            from_goods[good][AMT_AVAIL] -= amt
            to_goods[good][AMT_AVAIL] = amt_before_add + amt
    if comp:
        for g in to_goods:
            if to_goods[g][AMT_AVAIL] > 0:
                to_goods[g]['incr'] += amt * STEEP_GRADIENT
                comp_list = to_goods[g][COMPLEMENTS]
                for comp in comp_list:
                    to_goods[comp]['incr'] += STEEP_GRADIENT * amt


# a little test data for `get_rand_good()`:
TEST_GOODS_DICT = {
    "sugar": {AMT_AVAIL: 10},
    "honey": {AMT_AVAIL: 20},
    "molasses": {AMT_AVAIL: 30},
    "stevia": {AMT_AVAIL: 0},
}


def get_rand_good(goods_dict, nonzero=False):
    """
    What should this do with empty dict?
    """
    if goods_dict is None or not len(goods_dict):
        return None
    else:
        if nonzero and is_depleted(goods_dict):
            # we can't allocate what we don't have!
            print("Goods are depleted!")
            return None

        return random.choice([good for good in
                              goods_dict if goods_dict[good][AMT_AVAIL] > 0])


def incr_util(good_dict, good, amt=None, agent=None, graph=False, comp=None):
    '''
    if graph=True, increase the utility according to
    the weight of edge in the graph
    '''
    if graph:
        good_graph = agent["graph"]
        if comp:
            incr = good_graph.get_weight(good, comp)
        else:
            incr = good_graph.max_neighbors(good, good_dict)
        good_dict[good]["incr"] += incr
    else:
        if amt:
            good_dict[good]["incr"] += amt
        else:
            good_dict[good]["incr"] += 1


def endow(trader, avail_goods, equal=False, rand=False, comp=False):
    """
    This function is going to pick a good at random, and give the
    trader all of it, by default. We will write partial distributions
    later.
    """
    if equal:
        # each trader get equal amount of good
        equal_dist(comp=comp)
    elif rand:
        # each trader get random amt of good
        rand_dist(trader[GOODS], avail_goods, comp=comp)
    else:
        # pick an item at random
        # stick all of it in trader's goods dictionary
        good2endow = get_rand_good(avail_goods, nonzero=True)
        if good2endow is not None:
            # get some of the good
            transfer(trader[GOODS], avail_goods, good2endow, comp=comp)


def equal_dist(num_trader, to_goods, from_goods, comp=False):
    """
    each trader get equal amount of goods
    to_goods = trader[GOODS], from_goods = avail_goods
    """
    for good in from_goods:
        amt = from_goods[good][AMT_AVAIL] / num_trader
        transfer(to_goods, from_goods, good, amt, comp=comp)


def rand_dist(to_goods, from_goods, comp=False):
    """
    Pick a random good and transfer a random amount of it to trader.
    """
    selected_good = get_rand_good(from_goods, nonzero=True)
    amt = random.randrange(0, from_goods[selected_good][AMT_AVAIL], 1)
    transfer(to_goods, from_goods, selected_good, amt, comp=comp)


def goods_to_str(goods):
    """
    take a goods dict to string
    """
    string = ', '.join([str(goods[k][AMT_AVAIL]) + " " + str(k)
                        for k in goods.keys()])
    return string


def trade_state_to_str(state):
    """
    convert integer value of ans to string
    """
    return trade_state_dict[state]


def rand_goods_list(goods):
    rand_list = list(goods.keys())
    random.shuffle(rand_list)
    return rand_list


TRADER1 = 0
TRADER2 = 1


class TradeState():
    """
    A class to track the state of a trade.
    """
    def __init__(self, trader1, trader2, good1=None,
                 amt1=0, good2=None, amt2=0, status=INIT1):
        """
        Args:
            good1: the name of the good offered first
            amt1: the amount of that good offered at this point
                in negotiations
            good2: the name of the good offered in return for good1
            amt2: the amount of that good offered at this point
                in negotiations
            status: current state of this trade
        """
        self.status = status
        self.traders = [
                        {"trader": trader1, "good": good1, "amt": amt1},
                        {"trader": trader2, "good": good2, "amt": amt2},
                       ]

    def get_good(self, which_side):
        return self.traders[which_side]["good"]

    def __str__(self):
        return (f"Trade between {str(self.traders[TRADER1]['trader'])} "
                + f"and {str(self.traders[TRADER2]['trader'])} "
                + f"in state {trade_state_to_str(self.status)}")

    def __repr__(self):
        return (
            str(self)
            + f"; good1 is {self.traders[TRADER1]['good']}"
            + f"; amt1 is {self.traders[TRADER1]['amt']}"
            + f"; good2 is {self.traders[TRADER2]['good']}"
            + f"; amt2 is {self.traders[TRADER2]['amt']}"
        )

    def get_side(self, which_side):
        return self.traders[which_side]

    def get_other(self, which_side):
        return abs(which_side - 1)


def trade_acceptable(trade_state, which_side):
    """
    Is the trade acceptable to `which_side`?
    """
    other_side = trade_state.get_other(which_side)
    my_side = trade_state.get_side(which_side)
    other_side = trade_state.get_side(other_side)
    # side 1 gains goods from side 2:
    my_side_gain = utility_delta(my_side["trader"], other_side["good"],
                                 other_side["amt"])
    # but gives up some of its own:
    my_side_loss = utility_delta(my_side["trader"], my_side["good"],
                                 my_side["amt"])
    if DEBUG.debug:
        print(f"my gain: {my_side_gain}; my loss: {my_side_loss}")
    if my_side_gain > my_side_loss:
        return True


def negotiate(trade):
    """
    See if these two traders (held in `trade` can strike a deal.
    """
    if DEBUG.debug2:
        pass
        # print(f"Attempting {str(trade)}")
    while trade.status != ACCEPT and trade.status != REJECT:
        if DEBUG.debug2:
            pass
            # print(f"{repr(trade)}")
        side1 = trade.get_side(TRADER1)
        side2 = trade.get_side(TRADER2)
        if trade.status == INIT1:
            side1["good"] = get_rand_good(side1["trader"]["goods"])
            if side1["good"] is None:
                trade.status = REJECT
            else:
                side1["amt"] = 1
                trade.status = INIT2
        elif trade.status == INIT2:
            side2["good"] = get_rand_good(side2["trader"]["goods"])
            if side2["good"] is None:
                trade.status = REJECT
            else:
                side2["amt"] = 1
                # eval trade from side2 POV:
                if trade_acceptable(trade, TRADER2):
                    trade.status = OFFER_FROM_2
                else:
                    trade.status = INADEQ
        elif trade.status == OFFER_FROM_2:
            # eval trade from side1 POV:
            if trade_acceptable(trade, TRADER1):
                if DEBUG.debug:
                    print("Accepting trade!")
                trade.status = ACCEPT
            else:
                trade.status = REJECT
        elif trade.status == INADEQ:
            # check whether the incremented amount exceed the AMT_AVAIL
            trader = side1["trader"]
            good = side1["good"]
            amt_incr = side1["amt"] + 1
            if (amt_incr <= trader[GOODS][good][AMT_AVAIL]):
                side1["amt"] += 1
                if trade_acceptable(trade, TRADER1):
                    trade.status = OFFER_FROM_1
                else:
                    trade.status = REJECT
            else:
                # not enough good to offer
                trade.status = REJECT
        elif trade.status == OFFER_FROM_1:
            # eval trade from side2 POV:
            if trade_acceptable(trade, TRADER2):
                trade.status = ACCEPT
            else:
                trade.status = INADEQ

    return trade


def seek_a_trade(agent, comp=False):
    nearby_agent = get_env(exec_key=agent.exec_key).get_closest_agent(agent)
    if nearby_agent is not None:
        trade = TradeState(agent, nearby_agent)
        trade = negotiate(trade)
        if trade.status == ACCEPT:
            exec_trade(trade)
        return trade
    else:
        return NO_TRADER


def seek_a_trade_w_comp(agent, **kwargs):
    return seek_a_trade(agent, comp=True, **kwargs)


def exec_trade(trade_state):
    side1 = trade_state.get_side(TRADER1)
    side2 = trade_state.get_side(TRADER2)
    trade(side1["trader"], side1["good"], side1["amt"],
          side2["trader"], side2["good"], side2["amt"])


def trade(agent, my_good, my_amt,
          counterparty, their_good, their_amt, comp=None):
    adj_add_good(agent, my_good, -my_amt, comp=comp)
    adj_add_good(agent, their_good, their_amt, comp=comp)
    adj_add_good(counterparty, their_good, -their_amt, comp=comp)
    adj_add_good(counterparty, my_good, my_amt, comp=comp)


def adjust_dura(trader, good, val):
    """
    This function will check if durability is an attribute of
    the goods. If so, utility will be adjusted by durability.
    """
    item = list(trader["goods"])[0]
    if "durability" in trader["goods"][item]:
        return val*(trader["goods"][good]["durability"] **
                    (trader["goods"][good]["age"]/5))
    else:
        return val


def get_lowest(agent, my_good, their_good, bidder=True):
    """
    This function will get the max a bidder want to give up or
    the min a reciever want to accept.
    """
    if bidder is True:
        # agent is bidder and is getting "my_good"
        util = utility_delta(agent, my_good, 1)
        # print("     Bidder will get utility of", util)
        # agent is losing "their_good"
        change_amt = -1
    else:
        # agent is reciever and is losing "my_good"
        util = utility_delta(agent, my_good, -1)
        # print("     Reciever will get utility of", util)
        # agent is getting "their_good"
        change_amt = 1
    # Exhaustive method to find lowest (inefficient and to be changed)
    change = change_amt
    # u_delta(gain) must >=  u_delta(loss)
    if bidder is True:
        # print("Bidder",their_good, agent["goods"][their_good][AMT_AVAIL])
        while abs(change) < agent["goods"][their_good][AMT_AVAIL]:
            # print("B     current amt is", change, "utility is",
            #       abs(utility_delta(agent, their_good, change)))
            if abs(utility_delta(agent, their_good, change)) >= abs(util):
                return abs(change-change_amt)
            change += change_amt
    else:
        while True:
            # print("R     current amt is", change, "utility is",
            #       abs(utility_delta(agent, their_good, change)))
            if abs(utility_delta(agent, their_good, change)) >= abs(util):
                return abs(change)
            change += change_amt
    return 0


def check_div(trader, good):
    """
    This function will check if divisibility is an attribute of
    the goods. If so, the function will return divisibility;
    else, the function will return 1.
    """
    item = list(trader["goods"])[0]
    if "divisibility" in trader["goods"][item]:
        # if the good is too old, set the avaliable amount to 0
        # (good is no longer valid for trading)
        amt = trader["goods"][good]["divisibility"]
        return amt
    else:
        return 1


def utility_delta(agent, good, change):
    """
    We are going to determine the utility of goods gained
    (amt is positive) or lost (amt is negative).
    `change` will be fractional if good divisibility < 1
    """
    curr_good = agent["goods"][good]
    ufunc_name = curr_good[UTIL_FUNC]
    curr_amt = curr_good[AMT_AVAIL]
    curr_div = check_div(agent, good)
    curr_util = adjust_dura(agent, good,
                            get_util_func(ufunc_name)(curr_amt, curr_div))
    new_util = adjust_dura(agent, good,
                           get_util_func(ufunc_name)((curr_amt + change),
                                                     curr_div))
    return ((new_util + curr_util) / 2) * change


def adj_add_good(agent, good, amt, comp=None):
    agent["util"] += utility_delta(agent, good, amt)
    old_amt = agent["goods"][good][AMT_AVAIL]
    agent["goods"][good][AMT_AVAIL] += amt
    if comp:
        adj_add_good_w_comp(agent, good, amt, old_amt)


def new_good(old_amt, amt):
    return old_amt == 0 and amt > 0


def is_compl_good(agent, good):
    '''
    check if this good is a comp of other goods that the agent have
    '''
    return agent[GOODS][good]['incr'] != 0


def good_all_gone(agent, g):
    '''
    Check if this agent no longer has this good
    '''
    return agent[GOODS][g][AMT_AVAIL] == 0


def compl_lst(agent, good):
    '''
    return the complimentary list of this good
    '''
    return agent[GOODS][good][COMPLEMENTS]


def adj_add_good_w_comp(agent, good, amt, old_amt):
    if new_good(old_amt, amt):
        if is_compl_good(agent, good):
            incr_util(agent[GOODS], good,
                      amt=amt * STEEP_GRADIENT, agent=agent,
                      graph=True)
        # now increase utility of this good's complements:
        for comp in compl_lst(agent, good):
            incr_util(agent[GOODS], comp,
                      amt=amt * STEEP_GRADIENT, agent=agent,
                      graph=True, comp=good)
        print(agent[GOODS])

    if good_all_gone(agent, good):
        for comp in compl_lst(agent, good):
            agent[GOODS][comp]['incr'] = 0
