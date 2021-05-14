
"""
This is a minimal model that inherits from model.py
and just sets up a couple of agents in two groups that
do nothing except move around randomly.
"""

from lib.agent import MOVE, Agent
from lib.display_methods import BLACK, BLUE, GREEN, RED, ORANGE, PURPLE
from lib.model import Model
from lib.model import NUM_MBRS, MBR_ACTION, NUM_MBRS_PROP, COLOR, MBR_CREATOR
from lib.space import get_neighbor
from registry.registry import get_env
import random

DEBUG = True
NOT_DEBUG = False

MODEL_NAME = "bigbox"
NUM_OF_CONSUMERS = 10
NUM_OF_MP = 5
NUM_OF_BB = 0

CONSUMER_GROUP = 0
MP_GROUP = 1
BB_GROUP = 2

MIN_CONSUMER_SPENDING = 50
MAX_CONSUMER_SPENDING = 70

BIG_BOX = "Big box"
CONSUMER = "Consumer"
HOOD_SIZE = 2
MP_PREF = 0.1
NUM_PERIOD = 20
STANDARD = 200
MULTIPLIER = 10

bb_capital = 1000
bb_expense = 100
item_needed = None

cons_goods = ["books", "coffee", "groceries", "hardware", "meals"]
mp_stores_type = ["Bookshop", "Coffeeshop", "Grocery store",
                  "Hardware", "Restaurant"]
mp_stores = {"Bookshop": {"color": ORANGE,
                          "per_expense": 20,
                          "init_capital": 90,
                          "goods_sold": ["books"]},
             "Coffeeshop": {"color": BLACK,
                            "per_expense": 22,
                            "init_capital": 100,
                            "goods_sold": ["coffee"]},
             "Grocery store": {"color": GREEN,
                               "per_expense": 23,
                               "init_capital": 100,
                               "goods_sold": ["groceries"]},
             "Hardware": {"color": RED,
                          "per_expense": 18,
                          "init_capital": 110,
                          "goods_sold": ["hardware"]},
             "Restaurant": {"color": PURPLE,
                            "per_expense": 25,
                            "init_capital": 100,
                            "goods_sold": ["meals"]}}


def get_rand_good():
    """
    Randomly select consumer's item needed
    after each run.
    """
    return random.choice(cons_goods)


# create consumer, mom and pop, and big box
def create_consumer(name, i, action=None, **kwargs):
    """
    Create consumers
    """
    spending_power = random.randint(MIN_CONSUMER_SPENDING,
                                    MAX_CONSUMER_SPENDING)
    consumer_books = {"spending_power": spending_power,
                      "last_util": 0.0,
                      "item_needed": get_rand_good()}
    return Agent(name + str(i),
                 action=consumer_action,
                 attrs=consumer_books, **kwargs)


def create_mp(store_grp, i, action=None, **kwargs):
    """
    Create a mom and pop store.
    """
    store_num = i % len(mp_stores)
    return Agent(name=str(store_grp) + " " + str(i),
                 action=retailer_action,
                 attrs={"expense":
                        mp_stores[mp_stores_type[store_num]]["per_expense"],
                        "capital":
                        mp_stores[mp_stores_type[store_num]]["init_capital"],
                        "goods_sold": cons_goods[store_num], },
                 **kwargs)


def create_bb(name, i, action=None, **kwargs):
    """
    Create a big box store.
    """
    return Agent(name=name + str(i),
                 action=retailer_action,
                 attrs={"expense": bb_expense,
                        "capital": bb_capital},
                 **kwargs)


# action for consumer
def consumer_action(consumer, **kwargs):
    """
    Check shops near consumer and
    consumer decide where to shop at.
    """
    global item_needed
    item_needed = consumer.get_attr("item_needed")
    shop_at = get_neighbor(consumer, pred=sells_good, size=10)
    if NOT_DEBUG:
        print("item_needed:", item_needed)
        print("shop_at:", shop_at)
    if shop_at is None:
        return MOVE

    transaction(shop_at, consumer)
    if NOT_DEBUG:
        print("     someone shopped at ",   shop_at)
    consumer["item_needed"] = get_rand_good()
    return MOVE


def sells_good(store):
    """
    Return True if store sells the good the consumer needs
    """
    global item_needed
    if str(store.primary_group()) == BIG_BOX:
        return True
    elif str(store.primary_group()) == CONSUMER:
        return False
    else:
        if store.is_active():
            if store.get_attr("goods_sold") is not None:
                if item_needed in store.get_attr("goods_sold"):
                    return True
        return False


def choose_store(consumer, store):
    pass


# action for mom and pop, and big box
def retailer_action(business):
    """
    Common action to deduct expenses and
    check whether the entity goes out of business
    """
    business["capital"] -= business["expense"]
    if NOT_DEBUG:
        print("       ", business, "has a capital of ", business["capital"])
    if business["capital"] <= 0:
        business.die()
        if NOT_DEBUG:
            print("       ", business, "is out of business.")


def transaction(store, consumer):
    """
    Add money to the store's capital from consumer.
    """
    store["capital"] += consumer["spending_power"]


bigbox_grps = {
    "consumer_grp": {
        MBR_CREATOR: create_consumer,
        MBR_ACTION: consumer_action,
        NUM_MBRS: NUM_OF_CONSUMERS,
        NUM_MBRS_PROP: "num_consumers",
        COLOR: BLUE
    },
    "mp_grp": {
        MBR_CREATOR: create_mp,
        MBR_ACTION: retailer_action,
        NUM_MBRS: NUM_OF_MP,
        NUM_MBRS_PROP: "num_mp",
        COLOR: RED
    },
    "bb_grp": {
        MBR_CREATOR: create_bb,
        MBR_ACTION: retailer_action,
        NUM_MBRS: NUM_OF_BB,
        COLOR: BLACK
    },
}


def town_action(town):
    """
    To be filled in: create big box store at appropriate turn.
    You should have town.exec_key available.
    """
    box = get_env(town.exec_key)
    periods = town.get_periods()
    if periods > 0 and periods % NUM_PERIOD == 0:
        box.add_child("bb_grp")


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

    def handle_props(self, props, model_dir=None):
        super().handle_props(props, model_dir='capital')


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
