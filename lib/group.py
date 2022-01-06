"""
This file defines a Group, which is composed
of zero or more Agents (see agent.py).
(A group might have its membership reduced to zero!)
"""
import json
from copy import copy
from random import choice

import lib.agent as agt
import lib.utils as utl

DEBUG = utl.Debug()


def grp_from_nm_mbrs(nm, mbrs, exec_key=None):
    assert nm is not None, "Cannot pass None as name to grp_from_nm_mbrs"
    grp = Group(nm, exec_key=exec_key, members=list(mbrs.values()))
    # grp.members = mbrs
    return grp


class Members():
    """
    group.members was once simply a dictionary; now we are going to wrap the
    dict in a class so we can give it the same color interface as pop hist.
    """
    def __init__(self, serial_mbrs=None):
        self.mbr_dict = {}
        if serial_mbrs is not None:
            self.from_json(serial_mbrs)

    def has_color(self, name):
        """
        See if a pop has a specific color.
        """
        return self.mbr_dict[name].has_color()

    def get_color(self, name):
        """
        See if a pop has a specific color.
        """
        return self.mbr_dict[name].get_color()

    def from_json(self, serial_mbrs):
        # we loop through the members of this group
        for nm in serial_mbrs:
            member = serial_mbrs[nm]
            if member["type"] == "Agent":
                self.mbr_dict[nm] = agt.Agent(name=nm, serial_obj=member,
                                              exec_key=member['exec_key'])
            elif member["type"] == "Group":
                self.mbr_dict[nm] = Group(name=nm, serial_obj=member,
                                          exec_key=member['exec_key'])

    def to_json(self):
        return self.mbr_dict

    def items(self):
        return self.mbr_dict.items()

    def values(self):
        return self.mbr_dict.values()

    def keys(self):
        return self.mbr_dict.keys()

    def update(self, other):
        """
        Implements set union of members.
        """
        return self.mbr_dict.update(other.mbr_dict)

    def __repr__(self):
        return json.dumps(self.to_json(), cls=agt.AgentEncoder, indent=4)

    def __eq__(self, other):
        # now check the unique fields here:
        for mbr in self:
            if mbr not in other:
                return False
            else:
                if self[mbr] != other[mbr]:
                    return False
        return True

    def __len__(self):
        return len(self.mbr_dict)

    def __getitem__(self, key):
        """
        We are going to return the 'key' member
        of our member dictionary.
        """
        return self.mbr_dict[key]

    def __setitem__(self, key, member):
        """
        In contrast to agent, which sets a val
        for setitem, for groups, we are going to set
        the 'key' member.
        """
        self.mbr_dict[key] = member

    def __delitem__(self, key):
        """
        This will delete a member from this group.
        """
        del self.mbr_dict[key]

    def __contains__(self, item):
        """
        A test whether item is a member of this set.
        """
        return item in self.mbr_dict

    def __iter__(self):
        return iter(self.mbr_dict)

    def __reversed__(self):
        return reversed(self.mbr_dict)


class Group(agt.Agent):
    """
    This is the base class of all collections
    of entities. It itself is an agent.
    Args:
        attrs: a dictionary of group properties
        members: a list of members, that will be turned
            into a dictionary
        mbr_creator: a function to create members
        num_mbrs: how many members to create
    """

    def __init__(self, name, attrs=None, members=None,
                 action=None, mbr_creator=None,
                 mbr_action=None, color=None,
                 num_mbrs=None,
                 **kwargs):

        self.num_mbrs_ever = 0
        self.members = Members()

        super().__init__(name, attrs=attrs, duration=agt.INF,
                         action=action,
                         **kwargs)
        self.type = type(self).__name__
        if members is not None:
            for member in members:
                agt.join(self, member)
        if num_mbrs is None:
            num_mbrs = 1  # A default if they forgot to pass this.
        self.num_mbrs_ever = num_mbrs
        self.mbr_creator = mbr_creator
        self.mbr_action = mbr_action
        self.color = color
        if mbr_creator is not None:
            # If we have a member creator function, call it
            # `num_mbrs` times to create group members.
            for i in range(num_mbrs):
                agt.join(self, mbr_creator(self.name, i,
                                           action=mbr_action))
                # skip passing kwargs for now: **kwargs))

    def set_mbr_action(self, new_action):
        """
        Usually members get assigned an action when they are
        created.
        But we can set a new action for our members.
        """
        for mbr in self.members.values():
            mbr.set_action(new_action)

    def restore(self, serial_obj):
        """
        Here we restore a group from a serialized object.
        """
        self.from_json(serial_obj)

    def to_json(self):
        """
        Here we turn a group into a serialized object.
        """
        rep = super().to_json()
        rep["num_mbrs_ever"] = self.num_mbrs_ever
        rep["type"] = self.type
        rep["color"] = self.color
        rep["members"] = self.members.to_json()
        return rep

    def from_json(self, serial_obj):
        """
        Turn a serilaized JSON stream back into a group:
        """
        super().from_json(serial_obj)
        self.mbr_creator = self._restore_func(serial_obj, "mbr_creator")
        self.color = serial_obj["color"]
        self.num_mbrs_ever = serial_obj["num_mbrs_ever"]
        self.members = Members(serial_mbrs=serial_obj["members"])

    def __repr__(self):
        return json.dumps(self.to_json(), cls=agt.AgentEncoder, indent=4)

    def __eq__(self, other):
        if not super().__eq__(other):
            return False
        # now check the unique fields here:
        for mbr in self:
            if mbr not in other:
                return False
            else:
                if self[mbr] != other[mbr]:
                    return False
        return True

    def __len__(self):
        return len(self.members)

    def __getitem__(self, key):
        """
        We are going to return the 'key' member
        of our member dictionary.
        """
        return self.members[key]

    def __setitem__(self, key, member):
        """
        In contrast to agent, which sets a val
        for setitem, for groups, we are going to set
        the 'key' member.
        """
        agt.join(self, member)

    def __delitem__(self, key):
        """
        This will delete a member from this group.
        """
        del self.members[key]

    def __contains__(self, item):
        """
        A test whether item is a member of this set.
        """
        return item in self.members

    def __iter__(self):
        return iter(self.members)

    def __reversed__(self):
        return reversed(self.members)

    def __call__(self, **kwargs):
        """
        Call the members' functions, and the group's
        action func if it has one.
        This should return the total of all
        agents who acted in a particular call.
        """
        if DEBUG.debug_lib:
            print("Calling {} to act.".format(self.name))
        total_acts = 0
        total_moves = 0
        del_list = []
        self.duration -= 1
        if self.duration > 0:
            if self.action is not None:
                # the action was defined outside this class, so pass self:
                self.action(self, **kwargs)
            for (mbr_nm, member) in self.members.items():
                if member.is_active():
                    (acted, moved) = member(**kwargs)
                    total_acts += acted
                    total_moves += moved
                else:
                    # delete agents but not group:
                    if not agt.is_group(member):
                        del_list.append(mbr_nm)
        for mbr_nm in del_list:
            del self.members[mbr_nm]
        return total_acts, total_moves

    def __sub__(self, other):
        """
        This implements set difference.
        """
        if other is None:
            return self
        new_members = copy(self.members)
        for mbr in other:
            if mbr in new_members:
                del new_members[mbr]
        new_grp = grp_from_nm_mbrs(self.name + "-" + other.name, new_members)
        return new_grp

    def __add__(self, other):
        """
        This implements set union and returns
        a new Group that is self union other.
        If other is an atomic agent, just add it to
        this group.
        """
        if other is None:
            return self

        new_members = copy(self.members)
        if agt.is_group(other):
            new_members.update(other.members)
        else:
            new_members[other.name] = other
        new_grp = grp_from_nm_mbrs(self.name + "+" + other.name, new_members)
        self.add_group(new_grp)
        other.add_group(new_grp)
        return new_grp

    def __iadd__(self, other):
        """
        Add other to set self.
        If other is a group, add all its members.
        If other is an atom, add it.
        """
        if other is None:
            return self

        if agt.is_group(other):
            for key in other:
                agt.join(self, other[key])
        else:
            agt.join(self, other)
        return self

    def add_member(self, member):
        """
        Should be called by join()
        """
        self.members[str(member)] = member
        return True

    def del_member(self, member):
        """
        Should be called by split()
        """
        if str(member) in self.members:
            del self.members[str(member)]
            # maybe this test should be using == instead of `is`
            if member.primary_group() is self:
                member.set_prim_group(None)
        else:
            print("Attempt to del non-existent mbr: " + str(member))

    def rand_member(self):
        if len(self) > 0:
            # this is expensive: maybe we can speed it up
            # by not going to list somehow
            key = choice(list(self.members.keys()))
            return self[key]
        else:
            return None

    def subset(self, predicate, *args, name=None, exec_key=None):  # noqa E999
        assert callable(predicate)
        new_dict = Members()
        for mbr in self:
            if predicate(self[mbr], *args):
                new_dict[mbr] = self[mbr]
        if name is None:
            name = str(predicate)  # get some name!
        return grp_from_nm_mbrs(name, new_dict, exec_key)

    def rand_subset(self, n, name="rand_subset", exec_key=None):  # noqa E999
        """
        Choose a random subset of N members from this group.
        """
        assert n > 0, "Must select a positive number of items for subset."
        assert n <= len(self), "Can't select random subset larger than set."
        name = name + str(n)
        rsubset = {}
        key_list = list(self.members.keys())
        while n > 0:
            a_mbr = choice(key_list)
            rsubset[a_mbr] = self[a_mbr]
            key_list.remove(a_mbr)
            n -= 1
        return grp_from_nm_mbrs(name, rsubset, exec_key)

    def is_active(self):
        """
        For now, groups just stay active.
        We might want to revisit later the question
        of whether a group with all inactive members
        should be inactivated.
        """
        return True

    def ismember(self, agent):
        return str(agent) in self.members

    def is_mbr_comp(self, mbr):
        return agt.is_group(self.members[mbr])

    def pop_count(self, mbr):
        if self.is_mbr_comp(mbr):
            return len(self.members[mbr])
        else:
            return 1

    def has_color(self):
        return self.color is not None

    def get_color(self):
        """
        Return this group's display color.
        """
        return self.color

    def get_marker(self):
        """
        Return this group's display marker.
        """
        return self.attrs.get("marker", None)

    def get_members(self):
        return self.members
