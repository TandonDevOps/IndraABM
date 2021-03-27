"""
This file defines a Group, which is composed
of one or more Agents (see agent.py).
(A group might have its membership reduced to one!)
"""
import json
from collections import OrderedDict
from copy import copy
from random import choice

from lib.agent import Agent, join, INF, is_group, AgentEncoder
from lib.utils import get_func_name, Debug

DEBUG = Debug()


def grp_from_nm_dict(nm, dictionary):
    grp = Group(nm)
    grp.members = dictionary
    return grp


class Group(Agent):
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
                 duration=INF, action=None, mbr_creator=None,
                 mbr_action=None, color=None,
                 num_mbrs=None, serial_obj=None,
                 **kwargs):

        self.num_mbrs_ever = 0
        self.members = OrderedDict()

        super().__init__(name, attrs=attrs, duration=duration,
                         action=action, serial_obj=serial_obj,
                         **kwargs)
        self.type = type(self).__name__

        if serial_obj is not None:
            self.restore(serial_obj)
        else:
            if members is not None:
                for member in members:
                    join(self, member)
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
                    join(self, mbr_creator(self.name, i,
                                           action=mbr_action,
                                           exec_key=self.exec_key))
                    # skip passing kwargs for now: **kwargs))

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
        rep["members"] = self.members
        rep["mbr_creator"] = get_func_name(self.mbr_creator)
        return rep

    def from_json(self, serial_obj):
        # from registry.run_dict import mbr_creator_dict
        super().from_json(serial_obj)
        self.color = serial_obj["color"]
        self.num_mbrs_ever = serial_obj["num_mbrs_ever"]
        # we loop through the members of this group
        for nm in serial_obj["members"]:
            member = serial_obj["members"][nm]
            if member["type"] == "Agent":
                self.members[nm] = Agent(name=nm, serial_obj=member,
                                         exec_key=member['exec_key'])
            elif member["type"] == "Group":
                self.members[nm] = Group(name=nm, serial_obj=member,
                                         exec_key=member['exec_key'])
        mem_create_nm = serial_obj["mbr_creator"]
        self.mbr_creator = mem_create_nm

    def __repr__(self):
        return json.dumps(self.to_json(), cls=AgentEncoder, indent=4)

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
        join(self, member)

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
            for (key, member) in self.members.items():
                if member.is_active():
                    (acted, moved) = member(**kwargs)
                    total_acts += acted
                    total_moves += moved
                else:
                    # delete agents but not group:
                    if not is_group(member):
                        del_list.append(key)
        for key in del_list:
            del self.members[key]
        return total_acts, total_moves

    def __add__(self, other):
        """
        This implements set union and returns
        a new Group that is self union other.
        If other is an atomic agent, just add it to
        this group.
        """
        if other is None:
            return self

        new_dict = copy(self.members)
        if is_group(other):
            new_dict.update(other.members)
        else:
            new_dict[other.name] = other
        new_grp = grp_from_nm_dict(self.name + "+" + other.name, new_dict)
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

        if is_group(other):
            for key in other:
                join(self, other[key])
        else:
            join(self, other)
        return self

    def __mul__(self, other):
        """
        This implements set intersection and returns
        a new Group that is self intersect other.
        This has no useful meaning if `other` is an
        atom.
        """
        new_dict = copy(self.members)
        for mbr in self.members:
            if mbr not in other.members:
                del new_dict[mbr]
        return grp_from_nm_dict(str(self) + "X" + str(other), new_dict)

    def __imul__(self, other):
        """
        When `other` is a Group,
        this implements set intersection and makes the current
        Group equal to self intersect other.
        """
        del_list = []
        for mbr in self.members:
            if mbr not in other.members:
                del_list.append(mbr)
        for mbr in del_list:
            del self.members[mbr]
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

    def subset(self, predicate, *args, name=None):  # noqa E999
        new_dict = OrderedDict()
        for mbr in self:
            if predicate(self[mbr], *args):
                new_dict[mbr] = self[mbr]
        return grp_from_nm_dict(name, new_dict)

    def is_active(self):
        """
        For now, group just stay active.
        """
        return True
        # we should look at bringing back this logic at some point,
        # but the problem is it will block pending
        # actions like deleting dead members from the group.
        #        for member in self.members.values():
        #            if member.is_active():
        #                return True
        #        return False

    def ismember(self, agent):
        return str(agent) in self.members

    def is_mbr_comp(self, mbr):
        return is_group(self.members[mbr])

    def pop_count(self, mbr):
        if self.is_mbr_comp(mbr):
            return len(self.members[mbr])
        else:
            return 1

    def magnitude(self):
        pass

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
