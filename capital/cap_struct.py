"""
A model for capital structure.
Places two groups of agents in the enviornment randomly
and moves them around randomly.
"""
import copy

from lib.agent import Agent
from lib.display_methods import RED, BLUE
from lib.model import Model, MBR_CREATOR, NUM_MBRS, MBR_ACTION
from lib.model import NUM_MBRS_PROP, COLOR

MODEL_NAME = "capital"

DEF_NUM_ENTR = 10
DEF_NUM_RHOLDER = 10
DEF_TOTAL_RESOURCES_ENTR_WANT = 20000
DEF_TOTAL_RESOURCES_RHOLDER_HAVE = 30000

DEF_ENTR_CASH = 100000
DEF_RHOLDER_CASH = 0
DEF_K_PRICE = 1


DEF_RESOURCE_HOLD = {"land": 1000, "truck": 500, "building": 200}
DEF_CAP_WANTED = {"land": 1000, "truck": 500, "building": 200}
DEF_EACH_CAP_PRICE = {"land": DEF_K_PRICE,
                      "truck": DEF_K_PRICE,
                      "building": DEF_K_PRICE}

resource_holders = None  # list of resource holders
entrepreneurs = None  # list of entrepreneur


def dict_to_string(dict):
    return " ".join(good + " {0:.2f}".format(amt)
                    for good, amt in dict.items())


def create_rholder(name, i, action=None, **kwargs):
    """
    Create an agent.
    """
    # TO BE FIXED
    # k_price = DEF_K_PRICE
    resources = copy.deepcopy(DEF_CAP_WANTED)
    # num_resources = len(resources)
    price_list = copy.deepcopy(DEF_EACH_CAP_PRICE)
    starting_cash = DEF_RHOLDER_CASH
    return Agent(name + str(i),
                 action=rholder_action,
                 attrs={"cash": starting_cash,
                        "resources": resources,
                        "price": price_list},
                 **kwargs)


def rholder_action(agent, **kwargs):
    if agent["resources"]:
        print("I'm " + agent.name
              + " and I've got resources. I have "
              + str(agent["cash"]) + " dollars now."
              + " I have " + str(agent["resources"]) + ".")
    else:
        print("I'm " + agent.name
              + " and I've got resources. I have "
              + str(agent["cash"]) + " dollars now."
              + " I ran out of resources!")
    # resource holder dont move
    return True


def create_entr(name, i, action=None, **kwargs):
    """
    Create an agent.
    """
    # TO BE FIXED
    starting_cash = DEF_ENTR_CASH
    resources = copy.deepcopy(DEF_CAP_WANTED)
    return Agent(name + str(i),
                 action=entr_action,
                 attrs={"cash": starting_cash,
                        "wants": resources,
                        "have": {}},
                 **kwargs)


def entr_action(agent, **kwargs):
    if agent["cash"] > 0:
        # TO BE FIXED
        # nearby_rholder = get_env().get_neighbor_of_groupX(agent,
        #                                         resource_holders,
        #                                         hood_size=4)
        nearby_rholder = None
        if nearby_rholder is not None:
            # try to buy a resource if you have cash
            for good in agent["wants"].keys():
                price = nearby_rholder["price"][good]
                entr_max_buy = min(agent["cash"], agent["wants"][good] * price)
                # if find the resources entr want
                if good in nearby_rholder["resources"].keys():
                    trade_amt = min(entr_max_buy,
                                    nearby_rholder["resources"][good])
                    # update resources for the two groups
                    if good not in agent["have"].keys():
                        agent["have"][good] = trade_amt
                    agent["have"][good] += trade_amt
                    agent["wants"][good] -= trade_amt
                    nearby_rholder["resources"][good] -= trade_amt
                    nearby_rholder["cash"] += trade_amt * price
                    agent["cash"] -= trade_amt * price
                    if agent["wants"][good] <= 0:
                        agent["wants"].pop(good)
                    if nearby_rholder["resources"][good] <= 0:
                        nearby_rholder["resources"].pop(good)
                    break

            if agent["wants"] and agent["have"]:
                print("I'm " + agent.name
                      + " and I will buy resources from "
                      + str(nearby_rholder) + ". I have "
                      + "{0:.2f}".format(agent["cash"])
                      + " dollars left."
                      + " I want "
                      + dict_to_string(agent["wants"])
                      + ", and I have "
                      + dict_to_string(agent["have"]) + ".")
            elif agent["wants"]:
                print("I'm " + agent.name
                      + " and I will buy resources from "
                      + str(nearby_rholder) + ". I have "
                      + "{0:.2f}".format(agent["cash"])
                      + " dollars left."
                      + " I want "
                      + dict_to_string(agent["wants"])
                      + ", and I don't have any capital.")
            elif agent["have"]:
                print("I'm " + agent.name
                      + " and I will buy resources from "
                      + str(nearby_rholder) + ". I have "
                      + "{0:.2f}".format(agent["cash"])
                      + " dollars left."
                      + " I got all I need, and I have "
                      + dict_to_string(agent["have"]) + "!")
            return False
            # move to find resource holder

        else:
            print("I'm " + agent.name + " and I'm broke!")
    else:
        print("I'm " + agent.name
              + " and I can't find resources.")
    return True


cap_grps = {
    "entrepreneurs": {
        MBR_CREATOR: create_entr,
        MBR_ACTION: entr_action,
        NUM_MBRS: DEF_NUM_ENTR,
        NUM_MBRS_PROP: "num_entr",
        COLOR: BLUE,
    },
    "resource_holders": {
        MBR_CREATOR: create_rholder,
        MBR_ACTION: rholder_action,
        NUM_MBRS: DEF_NUM_RHOLDER,
        NUM_MBRS_PROP: "num_rholder",
        COLOR: RED,
    }
}


class CapStruct(Model):
    def handle_props(self, props, model_dir=None):
        super().handle_props(props, model_dir='capital')

    def create_groups(self):
        grps = super().create_groups()
        return grps


def create_model(serial_obj=None, props=None):
    if serial_obj is not None:
        return CapStruct(serial_obj=serial_obj)
    else:
        return CapStruct(MODEL_NAME, grp_struct=cap_grps, props=props)


def main():
    model = create_model()
    model.run()
    return 0


if __name__ == "__main__":
    main()
