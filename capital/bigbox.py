
"""
This is a minimal model that inherits from model.py
and just sets up a couple of agents in two groups that
do nothing except move around randomly.
"""

from lib.agent import MOVE, Agent
from lib.display_methods import BLACK, BLUE, GREEN, RED, ORANGE, PURPLE
from lib.model import Model
from lib.model import NUM_MBRS, MBR_ACTION, NUM_MBRS_PROP, COLOR, MBR_CREATOR
from lib.utils import Debug
from lib.space import get_neighbor
import random

DEBUG = Debug()

MODEL_NAME = "bigbox"
NUM_OF_CONSUMERS = 50
NUM_OF_MP = 8
DEBUG = False

CONSUMER_GROUP = 0
MP_GROUP = 1
BB_GROUP = 2

MIN_CONSUMER_SPENDING = 50
MAX_CONSUMER_SPENDING = 70

BIG_BOX = "Big box"
CONSUMER = "Consumer"
HOOD_SIZE = 2
MP_PREF = 0.1
PERIOD = 7
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
    consumer_books = {"spending power": spending_power,
                      "last util": 0.0,
                      "item needed": get_rand_good()}
    return Agent(name + str(i),
                 action=consumer_action,
                 attrs=consumer_books, **kwargs)


def create_mp(store_grp, i, action=None, **kwargs):
    """
    Create a mom and pop store.
    """
    store_num = i % len(mp_stores)
    return Agent(name=str(store_grp) + " " + str(i),
                 action=common_action,
                 attrs={"expense":
                        mp_stores[mp_stores_type[store_num]]["per_expense"],
                        "capital":
                        mp_stores[mp_stores_type[store_num]]["init_capital"]},
                 **kwargs)


def create_bb(name, i, action=None, **kwargs):
    """
    Create a big box store.
    """
    return Agent(name=name + str(i),
                 action=common_action,
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
    item_needed = consumer.get_attr("item needed")
    shop_at = get_neighbor(consumer, pred=sells_good)
    if shop_at is None:
        return MOVE

    transaction(shop_at, consumer)
    if DEBUG:
        print("     someone shopped at ",   shop_at)
    consumer["item needed"] = get_rand_good()
    return MOVE


# action for mom and pop, and big box
def common_action(business):
    """
    Common action to deduct expenses and
    check whether the entity goes out of business
    """
    print(business.attrs)
    business["capital"] -= business["expense"]
    if DEBUG:
        print("       ", business, "has a capital of ", business["capital"])
    if business["capital"] <= 0:
        business.die()
        if DEBUG:
            print("       ", business, "is out of business.")


def sells_good(store):
    """
    will be finished in the next meeting
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


def transaction(store, consumer):
    """
    Add money to the store's capital from consumer.
    """
    store["capital"] += consumer["spending power"]


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
        MBR_ACTION: common_action,
        NUM_MBRS: NUM_OF_MP,
        NUM_MBRS_PROP: "num_mp",
        COLOR: RED
    },
    "bb_grp": {
        MBR_CREATOR: create_bb,
        MBR_ACTION: common_action,
        COLOR: BLACK
    },
}


class BigBox(Model):
    """
    This class should just create a basic model that runs, has
    some agents that move around, and allows us to test if
    the system as a whole is working.
    It turns out that so far, we don't really need to subclass anything!
    """
    def __init__(self, model_nm="bigbox", props=None,
                 grp_struct=bigbox_grps,
                 env_action=None,
                 serial_obj=None, exec_key=None):
        super().__init__(model_nm=model_nm, props=props,
                         grp_struct=grp_struct,
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
