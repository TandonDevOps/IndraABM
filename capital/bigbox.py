"""
Big Box: studies under what conditions the entry of a big box store
will drive small retailers out of business.
"""

from lib.agent import MOVE, Agent, join
from lib.display_methods import BLACK, BLUE, GREEN, RED, ORANGE, PURPLE
from lib.model import Model
from lib.model import NUM_MBRS, MBR_ACTION, COLOR, MBR_CREATOR
from lib.space import get_neighbors
from registry.registry import get_model, get_group
import random

DEBUG = True
NOT_DEBUG = False

MODEL_NAME = "bigbox"
DEF_BB_PERIOD = 7
DEF_DIM = 30
DEF_NUM_AGENTS = DEF_DIM * DEF_DIM
CONSUMERS_DENSITY = 0.05
MP_DENSITY = 0.3
NUM_OF_CONSUMERS = DEF_NUM_AGENTS * CONSUMERS_DENSITY
NUM_OF_MP = DEF_NUM_AGENTS * MP_DENSITY
MULTIPLIER = 10
DEF_HOOD_SIZE = 2
DEF_MP_PREF = 0.1
NO_PREF = 0.0

MIN_CONSUMER_SPENDING = 50
MAX_CONSUMER_SPENDING = 70
AVG_MP_INIT_CAP = 100

BIG_BOX = "bb_grp"
CONSUMER = "consumer_grp"
MP_STORE = "mp_grp"
NOT_AVAIL = -1.0

bb_expense = 100
bb_capital = MULTIPLIER * AVG_MP_INIT_CAP
item_needed = None

# attributes
SPENDING_POWER = "spending_power"
LAST_UTIL = "last_util"
ITEM_NEEDED = "item_needed"
GOODS_SOLD = "goods_sold"
UTIL_ADJ = "util_adj"
EXPENSE = "expense"
CAPITAL = "capital"
PER_EXPENSE = "per_expense"
INIT_CAPITAL = "init_capital"
PERIOD = "period"

# initialize mp stores type and attributes
cons_goods = ["books", "coffee", "groceries", "hardware", "meals"]
mp_stores_type = ["Bookshop", "Coffeeshop", "Grocery store",
                  "Hardware", "Restaurant"]
mp_stores = {"Bookshop": {COLOR: ORANGE,
                          PER_EXPENSE: 20,
                          INIT_CAPITAL: AVG_MP_INIT_CAP - 10,
                          GOODS_SOLD: ["books"],
                          UTIL_ADJ: 0.1},
             "Coffeeshop": {COLOR: BLACK,
                            PER_EXPENSE: 22,
                            INIT_CAPITAL: AVG_MP_INIT_CAP,
                            GOODS_SOLD: ["coffee"],
                            UTIL_ADJ: 0.2},
             "Grocery store": {COLOR: GREEN,
                               PER_EXPENSE: 23,
                               INIT_CAPITAL: AVG_MP_INIT_CAP,
                               GOODS_SOLD: ["groceries"],
                               UTIL_ADJ: 0.3},
             "Hardware": {COLOR: RED,
                          PER_EXPENSE: 18,
                          INIT_CAPITAL: AVG_MP_INIT_CAP + 10,
                          GOODS_SOLD: ["hardware"],
                          UTIL_ADJ: 0.4},
             "Restaurant": {COLOR: PURPLE,
                            PER_EXPENSE: 25,
                            INIT_CAPITAL: AVG_MP_INIT_CAP,
                            GOODS_SOLD: ["meals"],
                            UTIL_ADJ: 0.5}}


def debug_retailer(grp):
    for member in grp:
        print(member, "expense:",
              grp[member].get_attr(EXPENSE),
              "capital:", grp[member].get_attr(CAPITAL))


# =============================
# CONSUMER functions
#     get_rand_good
#     create_consumer
#     consumer_action
#     sells_good
#     choose_seller
# =============================
def get_rand_good():
    """
    Randomly select consumer's item needed
    after each run.
    """
    return random.choice(cons_goods)


def create_consumer(name, i, action=None, **kwargs):
    """
    Create consumers
    """
    spending_power = random.randint(MIN_CONSUMER_SPENDING,
                                    MAX_CONSUMER_SPENDING)
    return Agent(name + str(i),
                 action=consumer_action,
                 attrs={SPENDING_POWER: spending_power,
                        LAST_UTIL: 0.0,
                        ITEM_NEEDED: get_rand_good()}, **kwargs)


# action for consumer
def consumer_action(consumer, **kwargs):
    """
    Check shops near consumer and
    consumer decide where to shop at.
    """
    global item_needed
    item_needed = consumer.get_attr(ITEM_NEEDED)
    box = get_model(consumer.exec_key)
    hood_size = box.hood_size
    sellers = get_neighbors(consumer, pred=sells_good, size=hood_size)
    shop_at = choose_store(consumer, sellers.members.items())

    if shop_at is None:
        return MOVE
    transaction(shop_at, consumer)
    consumer[ITEM_NEEDED] = get_rand_good()
    return MOVE


def sells_good(store):
    """
    Return True if store sells the good the consumer needs
        Bigbox: always sells item needed, thus return True
        Consumer: does not sell, thus return False
        MP store: needs to check if it sells item needed
    """
    global item_needed
    grp = str(store.primary_group())
    if grp == BIG_BOX:
        return True
    elif grp == CONSUMER:
        return False
    else:
        if store.is_active() and store.get_attr(GOODS_SOLD) is not None:
            if item_needed in store.get_attr(GOODS_SOLD):
                if NOT_DEBUG:
                    print("store is chosen", store.name)
                return True
    return False


def choose_store(consumer, sellers):
    """
    The Consumer determines who, of those who sell the good he desires,
    he will buy from.
    Args:
        sellers: a list of tuples of seller (name, agent)
            with type (str, Agent)
        consumer: who shops for good
    Returns:
        a top store (with max util) selling that good
    """
    top_seller = None
    max_util = 0.0
    for seller in sellers:
        this_util = utils_from_good(seller[1], consumer.get_attr(ITEM_NEEDED))
        if this_util >= max_util:
            max_util = this_util
            top_seller = seller[1]
    consumer.set_attr(LAST_UTIL, max_util)
    return top_seller


# =============================
# RETAILER fucntions
#     create_mp
#     create_bb
#     retailer_action
#     transaction
# =============================
def create_mp(store_grp, i, action=None, **kwargs):
    """
    Create a mom and pop store.
    """
    store_num = i % len(mp_stores)
    store = mp_stores[mp_stores_type[store_num]]
    return Agent(name=str(store_grp) + " " + str(i),
                 action=retailer_action,
                 attrs={EXPENSE: store[PER_EXPENSE],
                        CAPITAL: store[INIT_CAPITAL],
                        GOODS_SOLD: cons_goods[store_num],
                        UTIL_ADJ: store[UTIL_ADJ]},
                 **kwargs)


def create_bb(name, mbr_id, bb_capital, action=None, **kwargs):
    """
    Create a big box store.
    """
    return Agent(name=name + str(mbr_id),
                 action=retailer_action,
                 attrs={EXPENSE: bb_expense,
                        CAPITAL: bb_capital},
                 **kwargs)


# action for mom and pop, and big box
def retailer_action(store):
    """
    Common action to deduct expenses and
    check whether the entity goes out of business
    """
    capital = store.get_attr(CAPITAL) - store.get_attr(EXPENSE)
    store.set_attr(CAPITAL, capital)
    if store.get_attr(CAPITAL) <= 0:
        store.die()


def transaction(store, consumer):
    """
    Add money to the store's capital from consumer.
    """
    capital = store.get_attr(CAPITAL) + consumer.get_attr(SPENDING_POWER)
    store.set_attr(CAPITAL, capital)
    if NOT_DEBUG:
        print(store.name, store.get_attr(CAPITAL))
        bb_grp = get_group(BIG_BOX, store.exec_key)
        mp_grp = get_group(MP_STORE, store.exec_key)
        debug_retailer(bb_grp)
        debug_retailer(mp_grp)


def utils_from_good(store, good):
    '''
    Return util for each choice of retailers
    with preference for mom-and-pop
    '''
    grp = str(store.primary_group())
    box = get_model(store.exec_key)
    mp_pref = box.mp_pref
    # add preference if good sold in mom and pop
    if grp == MP_STORE:
        if good in store.get_attr(GOODS_SOLD):
            return (random.random() + store.get_attr(UTIL_ADJ)) * mp_pref
    elif grp == BIG_BOX:
        return NO_PREF
    return NOT_AVAIL


# big box groups
bigbox_grps = {
    CONSUMER: {
        MBR_CREATOR: create_consumer,
        MBR_ACTION: consumer_action,
        NUM_MBRS: NUM_OF_CONSUMERS,
        COLOR: BLUE
    },
    MP_STORE: {
        MBR_CREATOR: create_mp,
        MBR_ACTION: retailer_action,
        NUM_MBRS: NUM_OF_MP,
        COLOR: RED
    },
    BIG_BOX: {
        MBR_CREATOR: create_bb,
        MBR_ACTION: retailer_action,
        NUM_MBRS: 0,
        COLOR: BLACK
        # INIT_CAPITAL: bb_capital,
        # PERIOD: DEF_BB_PERIOD
    },
}


def town_action(town):
    """
    Create big box store at appropriate turn.
    """
    bb_grp = get_group(BIG_BOX, town.exec_key)
    box = get_model(town.exec_key)
    bb_period = box.bb_period
    bb_init_capital = box.multiplier * AVG_MP_INIT_CAP
    # if no big box exists, make them:
    num_bbs = len(bb_grp)
    if num_bbs == 0:
        if town.get_periods() >= bb_period:
            new_bb = bb_grp.mbr_creator(BIG_BOX, num_bbs, bb_init_capital,
                                        exec_key=town.exec_key)
            join(bb_grp, new_bb)
            town.place_member(new_bb)


class BigBox(Model):
    """
    This class should just create a basic model that runs, has
    some agents that move around, and allows us to test if
    the system as a whole is working.
    It turns out that so far, we don't really need to subclass anything!
    """
    def __init__(self, model_nm="bigbox", props=None,
                 grp_struct=bigbox_grps,
                 env_action=town_action,
                 serial_obj=None, exec_key=None):
        super().__init__(model_nm=model_nm, props=props,
                         grp_struct=grp_struct,
                         env_action=env_action,
                         serial_obj=serial_obj,
                         exec_key=exec_key)

    def from_json(self, jrep):
        super().from_json(jrep)
        self.hood_size = jrep["hood_size"]
        self.mp_pref = jrep["mp_pref"]
        self.bb_period = jrep["bb_period"]
        self.multiplier = jrep["multiplier"]

    def to_json(self):
        jrep = super().to_json()
        jrep["hood_size"] = self.hood_size
        jrep["mp_pref"] = self.mp_pref
        jrep["bb_period"] = self.bb_period
        jrep["multiplier"] = self.multiplier
        return jrep

    def handle_props(self, props, model_dir=None):
        """
        Handle our models special properties.
        Our super handles height and width.
        """
        super().handle_props(props, model_dir='capital')
        self.hood_size = self.props.get("hood_size", DEF_HOOD_SIZE)
        self.mp_pref = self.props.get("mp_pref", DEF_MP_PREF)
        self.multiplier = self.props.get("multiplier", MULTIPLIER)
        self.bb_period = self.props.get("bb_period", DEF_BB_PERIOD)
        num_agents = (self.height * self.width)
        consumer_density = self.props.get("consumer_density",
                                          CONSUMERS_DENSITY)
        mp_density = self.props.get("mp_density", MP_DENSITY)

        self.grp_struct[CONSUMER][NUM_MBRS] = int(num_agents *
                                                  consumer_density)
        self.grp_struct[MP_STORE][NUM_MBRS] = int(num_agents * mp_density)
        # self.grp_struct[BIG_BOX][INIT_CAPITAL] = int(multiplier
        #                                              * AVG_MP_INIT_CAP)


def create_model(serial_obj=None, props=None):
    """
    This is for the sake of the API server:
    """
    if serial_obj is not None:
        return BigBox(serial_obj=serial_obj)
    else:
        return BigBox(MODEL_NAME, grp_struct=bigbox_grps, props=props)


def main():
    model = create_model()
    model.run()
    return 0


if __name__ == "__main__":
    main()
