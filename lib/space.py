"""
This file defines Space, which is a collection
of agents related spatially.
"""
import json
import math
import random

import lib.agent as agt
import lib.group as grp
import lib.utils as utl

DEBUG = utl.Debug()

DEF_WIDTH = 10
DEF_HEIGHT = 10

MAX_WIDTH = 200
MAX_HEIGHT = 200

DEF_MAX_MOVE = 2

MAX_PLACE_ATTEMPTS = 100

FAR_AWAY = 100000000  # Just some very big number!

ALL_FULL = "Can't fit more agents in this space!"

MAX_TEMP_NUM = 2 ** 64

MOORE = "Moore"
VON_N = "VonNeumann"

Y = agt.Y
X = agt.X

region_dict = {}


def gen_temp_grp_nm(s):
    """
    This makes "sure" that grp names are unique.
    Of course, roughly 1 / MAX_TEMP_NUM times we will
    create a duplicate name... but that shouldn't happen
    before the heat death of the universe.
    """
    return s + str(random.randint(0, MAX_TEMP_NUM))


class SpaceFull(Exception):
    """
    Exception to raise when a space fills up.
    """
    def __init__(self, message):
        self.message = message


def out_of_bounds(x, y, x1, y1, x2, y2):
    """
    Is point x, y off the grid defined by x1, y1, x2, y2
    x1 and y1 are inclusive, and in bounds
    x2 and y2 are exclusive, and out of bounds
    """
    return (x < x1 or x >= x2
            or y < y1 or y >= y2)


def debug_agent_pos(agent):
    """
    Prints agent id and position
    """
    if DEBUG.debug_lib:
        print(str(agent), "with id", id(agent), "is at", agent.get_pos())


def bound(point, lower, upper):
    """
    Input:  a point to check against the upper and lower bounds
    Output: If the point is in the range of lower and upper, inclusive, the
            value of the point is returned

            If the point is out of bounds, then the value of
            the closest bounds is returned
    """
    return min(max(point, lower), upper)


def distance(a1, a2):
    """
    We're going to return the distance between two objects. That calculation
    is easy if they are both located in space, but what if one of them is
    not? For now, we will return FAR_AWAY, but is that right?
    """
    if (not a1.is_located()) or (not a2.is_located()):
        return FAR_AWAY
    else:
        debug_agent_pos(a1)
        debug_agent_pos(a2)
        return math.sqrt(
            ((a2.get_x() - a1.get_x()) ** 2)
            + ((a2.get_y() - a1.get_y()) ** 2)
        )


def in_hood(agent, other, hood_sz):
    """
    Check whether agent and other are within a certain distance
    of each other.
    """
    d = distance(agent, other)
    if DEBUG.debug2_lib:
        print("Distance between " + str(agent)
              + " and " + str(other) + " is "
              + str(d))
    return d <= hood_sz


def get_xy_from_str(coord_str):
    """
    Return x and y integers from a string coordinate tuple ex."(5, 6)"
    """
    x, y = coord_str[1:-1].split(",")
    return int(x), int(y)


def exists_neighbor(agent, pred=None, exclude_self=True, size=1,
                    region_type=None, **kwargs):
    import lib.actions as acts
    env = acts.get_even()
    return env.exists_neighbor(agent,
                               pred=pred,
                               exclude_self=exclude_self,
                               size=size,
                               region_type=region_type)


def get_neighbors(agent, pred=None, exclude_self=True, size=1,
                  region_type=MOORE, model_name=None):
    """
    Get the Moore neighbors for an agent.
    We might expand this in the future to allow von Neumann hoods!
    Also, we have a messed up situation with some funcs taking
    `include_self` and some taking `exclude_self`: for sweet love of Jesus, let
    us use one or the other!
    """
    import lib.actions as acts
    env = acts.get_even()
    if region_type == MOORE:
        return env.get_moore_hood(agent, pred=pred, size=size,
                                  model_name=model_name)
    else:
        return env.get_vonneumann_hood(agent, pred=pred, size=size)


def get_neighbor(agent, pred=None, exclude_self=True, size=1,
                 region_type=None, **kwargs):
    import lib.actions as acts
    env = acts.get_even()
    return env.get_neighbor(agent,
                            pred=pred,
                            exclude_self=exclude_self,
                            size=size,
                            region_type=region_type)


def get_num_of_neighbors(agent, exclude_self=False, pred=None, size=1,
                         region_type=None, **kwargs):
    import lib.actions as acts
    env = acts.get_even()
    return env.get_num_of_neighbors(agent,
                                    exclude_self=True,
                                    pred=None,
                                    size=size,
                                    region_type=region_type)


def neighbor_ratio(agent, pred_one, pred_two=None, size=1, region_type=None,
                   **kwargs):
    import lib.actions as acts
    env = acts.get_even()
    return env.neighbor_ratio(agent, pred_one,
                              pred_two=pred_two,
                              size=size,
                              region_type=region_type)


def degrees_between(x_dif, y_dif):
    return math.degrees(math.atan(y_dif / x_dif))


def opposing_angle(pos1, pos2):
    '''
    Returns the inverse of the angle of
    the other_agent relative to the agent.
    '''
    x_dif = pos2[X] - pos1[X]
    y_dif = pos2[Y] - pos1[Y]
    if (x_dif != 0 and y_dif != 0):
        if (x_dif > 0):
            new_angle = 180 + degrees_between(x_dif, y_dif)
        else:
            new_angle = degrees_between(x_dif, y_dif)
    elif (y_dif != 0):
        if (y_dif > 0):
            new_angle = 270
        else:
            new_angle = 90
    else:
        if (x_dif > 0):
            new_angle = 180
        else:
            new_angle = 0
    return new_angle


def get_move_angle(agent, agents_in_range):
    vector_x = 0
    vector_y = 0
    for curr_agent in agents_in_range:
        if (curr_agent.get_x() != agent.get_x()):
            if ((curr_agent.get_x() - agent.get_x()) < 0):
                vector_x -= 1 / ((curr_agent.get_x() - agent.get_x()) ** 2)
            else:
                vector_x += 1 / ((curr_agent.get_x() - agent.get_x()) ** 2)
        if (curr_agent.get_y() != agent.get_y()):
            if ((curr_agent.get_y() - agent.get_y()) < 0):
                vector_y -= 1 / ((curr_agent.get_y() - agent.get_y()) ** 2)
            else:
                vector_y += 1 / ((curr_agent.get_y() - agent.get_y()) ** 2)
    return opposing_angle([0, 0], [vector_x, vector_y])


class Space(grp.Group):
    """
    A collection of entities that share a space.
    The way we handle space assignment is, default to random,
    and assign locations after we get our members.
    """

    def __init__(self, name, width=DEF_WIDTH, height=DEF_HEIGHT,
                 attrs=None, members=None, action=None,
                 random_placing=True, serial_obj=None, reg=True, **kwargs):
        super().__init__(name, attrs=attrs, members=members,
                         action=action, serial_obj=serial_obj,
                         reg=False, **kwargs)

        self.type = type(self).__name__
        if serial_obj is not None:
            self.restore(serial_obj)
        else:
            self.width = width
            self.height = height
            self.center = (width // 2, height // 2)
            # the location of members in the space {(tuple):Agent}
            self.locations = {}
            # by making two class methods for rand_place_members and
            # place_member, we allow two places to override
            self.random_placing = random_placing
            if random_placing:
                self.rand_place_members(self.members)
            else:
                self.consec_place_members(self.members)

    def get_center(self):
        return self.center

    def restore(self, serial_obj):
        self.from_json(serial_obj)

    def to_json(self):
        """
        We can order these as we wish to make debugging the API easier:
        """
        rep = {}
        rep["type"] = self.type
        rep["width"] = self.width
        rep["height"] = self.height
        rep["random_placing"] = self.random_placing
        rep.update(super().to_json())
        rep["locations"] = self.locations
        return rep

    def from_json(self, rep):
        """
        Recover a space from JSON.
        """
        super().from_json(rep)
        self.type = rep["type"]
        self.width = rep["width"]
        self.height = rep["height"]
        self.locations = rep["locations"]
        self.random_placing = rep["random_placing"]

    def __repr__(self):
        return json.dumps(self.to_json(), cls=agt.AgentEncoder, indent=4)

    def grid_size(self):
        """
        How big is the grid?
        """
        return self.width * self.height

    def is_full(self):
        """
        Is the grid full?
        """
        if len(self.locations) >= self.grid_size():
            if DEBUG.debug2_lib:
                print("num locations =", len(self.locations),
                      "; grid size =", self.grid_size())
            return True
        else:
            return False

    def rand_place_members(self, members, max_move=None):
        """
        Locate all members of this space in x, y grid.
        This randomly places members.
        """
        if members is not None:
            for nm, mbr in members.items():
                if not agt.is_group(mbr):  # by default don't locate groups
                    self.place_member(mbr, max_move)
                else:  # place composite's members
                    self.rand_place_members(mbr.members, max_move)

    def consec_place_members(self, members, curr_col=0, curr_row=0):
        """
        Locate all members of this space in x, y grid.
        Place members consecutively, starting from (0, 0) and
        moving to (1, 0), (2, 0), etc
        """
        print("Using consecutive placing of members.")
        if members is not None:
            for nm, mbr in members.items():
                if not agt.is_group(mbr):
                    if curr_col < self.width:
                        self.place_member(mbr, xy=(curr_col, curr_row))
                        if DEBUG.debug_lib:
                            print("Placing member at (" + str(curr_col) + ","
                                  + str(curr_row) + ")")
                        curr_col += 1
                    if curr_col == self.width:
                        if DEBUG.debug_lib:
                            print("Moving up a row from", curr_row,
                                  "to", curr_row + 1)
                        curr_col = 0
                        curr_row += 1
                else:  # place composite's members
                    self.consec_place_members(mbr.members, curr_col, curr_row)

    def rand_x(self, low=0, high=None):
        """
        Return a random x-value between 0 and this space's width,
        if no constraints are passed.
        With constraints, narrow to that range.
        """
        high = self.width if high is None else high
        return random.randint(low, high)

    def rand_y(self, low=0, high=None):
        """
        Return a random y-value between 0 and this space's height
        if no constraints are passed.
        With constraints, narrow to that range.
        """
        high = self.height if high is None else high
        return random.randint(low, high)

    def constrain_x(self, x):
        """
        Pull x in bounds if it ain't.
        """
        return bound(x, 0, self.width)

    def constrain_y(self, y):
        """
        Pull y in bounds if it ain't.
        """
        return bound(y, 0, self.height)

    def get_row_view(self, x, y, dist):
        pass

    def get_col_view(self, x, y, dist):
        pass

    def gen_new_pos(self, mbr, max_move):
        """
        Generate new random position within max_move of current pos.
        """
        low_x = 0
        high_x = self.width - 1
        low_y = 0
        high_y = self.height - 1
        if max_move is not None and mbr.is_located():
            low_x = self.constrain_x(mbr.get_x() - max_move)
            high_x = self.constrain_x(mbr.get_x() + max_move)
            low_y = self.constrain_y(mbr.get_y() - max_move)
            high_y = self.constrain_y(mbr.get_y() + max_move)
        x = self.rand_x(low_x, high_x)
        y = self.rand_y(low_y, high_y)
        return x, y

    def is_empty(self, x, y):
        """
        See if cell x,y is empty.
        Always make location a str for serialization.
        """
        return str((x, y)) not in self.locations

    def get_agent_at(self, x, y):
        """
        Return agent at cell x,y
        If cell is empty return None.
        Always make location a str for serialization.
        """
        import lib.actions as acts
        if self.is_empty(x, y):
            return None
        agent_nm = self.locations[str((x, y))]
        return acts.get_agent(agent_nm)

    def place_member(self, mbr, max_move=None, xy=None, attempts=0):
        """
        By default, locate a member at a random x, y spot in our grid.
        `max_move` constrains where that can be.
        Setting `xy` picks a particular spot to place member.
        `xy` must be a tuple!
        """
        if self.is_full():
            print(ALL_FULL)
            raise (SpaceFull(ALL_FULL))

        if attempts > MAX_PLACE_ATTEMPTS:
            # we should create a better exception here, but this will work for
            # now:
            print(ALL_FULL, "attempts=", attempts)
            raise (SpaceFull(ALL_FULL))

        if not agt.is_group(mbr):
            if xy is not None:
                (x, y) = xy
            else:
                (x, y) = self.gen_new_pos(mbr, max_move)
            if self.is_empty(x, y):
                if mbr.is_located():
                    self.move_location(x, y, mbr.get_x(),
                                       mbr.get_y(), mbr.name)
                else:
                    self.add_location(x, y, mbr)
                mbr.set_pos(x, y)
                return x, y
            elif (max_move is None) and (xy is None):
                # if the random position is already taken,x
                # find the member a new position
                # but if max_move is not None, the hood might be filled!
                # so we need something to detect
                # a full neighborhood as well.
                # and if xy is not None, the user asked for a particular
                # spot: don't give them another, but return None.
                return self.place_member(mbr, max_move, attempts=attempts + 1)
        else:
            return self.rand_place_members(mbr.members, max_move)

    def __iadd__(self, other):
        """
        This overrides the += operator
        Now the += operator can be used to add a member to the space
        """
        super().__iadd__(other)
        self.place_member(other)
        return self

    def add_location(self, x, y, member):
        """
        Add a new member to the locations of positions of members.
        locations{} stores agents by name, to look up in registry.
        """
        self.locations[str((x, y))] = member.name

    def get_locations(self):
        return self.locations

    def is_occupied(self, x, y):
        """
        See if (x, y) is occupied.
        """
        return str((x, y)) in self.locations

    def move_location(self, nx, ny, ox, oy, agent_name="NA"):
        """
        Move a member to a new position, if that position
        is not already occupied.
        """
        if not self.is_occupied(nx, ny):
            new_loc = str((nx, ny))
            old_loc = str((ox, oy))
            if not self.is_occupied(ox, oy):
                # must replace with proper logging call:
                print("Trying to move agent not in locations: "
                      + agent_name + " at " + old_loc)
            else:
                self.locations[new_loc] = self.locations[old_loc]
                del self.locations[old_loc]
        else:
            # must replace with proper logging call:
            print("Trying to place agent in occupied space.")

    def remove_location(self, coord):
        """
        Remove a member from locations.
        """
        str_coord = str(coord)
        if str_coord in self.locations:
            del self.locations[str_coord]
        else:
            # must replace with proper logging call:
            print("Trying to remove unlocated agent from space.")

    def get_row_hood(self, row_num, pred=None, save_neighbors=False):
        """
        Collects all agents in row `row_num` into a Group
        and returns it.
        """
        if row_num < 0 or row_num >= self.height:
            return None
        else:
            agent = self.get_agent_at(self.width // 2, row_num)
            row_hood = self.get_x_hood(agent, self.width - 1,
                                       include_self=True)
            row_hood.name = "Row neighbors"
            return row_hood

    def get_corners(self, start, size, orient=X):
        """
        Get the corners of an x or y run of cells.
        I think we could eliminate the if with enough cleverness.
        """
        NW = start
        if orient == X:
            first_coord = start[X]
            y_coord = start[Y]
            SW = (first_coord, y_coord + 1)
            NE = (first_coord + size, y_coord)
            SE = (first_coord + size, y_coord + 1)
        else:
            first_coord = start[Y]
            x_coord = start[X]
            SW = (x_coord, first_coord + size)
            NE = (x_coord + 1, first_coord)
            SE = (x_coord + 1, first_coord + size)
        return (NW, NE, SW, SE)

    def get_x_hood(self, agent, width=1, pred=None, include_self=False,
                   save_neighbors=False):
        """
        Takes in an agent and returns a Group
        of its x neighbors.
        For example, if the agent is located at (0, 0),
        get_x_hood would return neighbors between
        (-1, 0) and (1, 0).
        """
        (NW, NE, SW, SE) = self.get_corners(agent.get_pos(), width)
        x_hood = region_factory(self, size=1,
                                NW=NW, NE=NE, SW=SW, SE=SE,
                                agents_move=False)
        return x_hood.get_group()

    def get_y_hood(self, agent, height=1, pred=None, include_self=False,
                   save_neighbors=False):
        """
        Takes in an agent and returns a Group
        of its x neighbors.
        For example, if the agent is located at (0, 0),
        get_y_hood would return neighbors between
        (0, -1) and (0, 1).
        """
        (NW, NE, SW, SE) = self.get_corners(agent.get_pos(), height)
        y_hood = region_factory(self, size=1,
                                NW=NW, NE=NE, SW=SW, SE=SE,
                                agents_move=False)
        return y_hood.get_group()

    def get_vonneumann_hood(self, agent, pred=None, save_neighbors=False,
                            size=1):
        """
        Takes in an agent and returns a Group of its
        Von Neumann neighbors.
        `hood_size` is unused at present, but we should use it!
        """
        vonneumann_hood = (self.get_x_hood(agent, width=size)
                           + self.get_y_hood(agent, height=size))
        if agent.get("save_neighbors", False):
            agent.neighbors = vonneumann_hood
        return vonneumann_hood

    def get_moore_hood(self, agent, pred=None, save_neighbors=False,
                       include_self=False, size=1, model_name=None):
        """
        Takes in an agent and returns a Group of its Moore neighbors.
        Should call the region_factory!
        """

        region = region_factory(space=self,
                                center=(agent.get_x(), agent.get_y()),
                                size=size,
                                agents_move=not save_neighbors,
                                model_name=model_name)
        members = region.get_agents(exclude_self=not include_self, pred=pred)
        return grp.Group(gen_temp_grp_nm("Moore neighbors"),
                         members=members)

    def get_square_hood(self, agent, pred=None, save_neighbors=False,
                        include_self=False, hood_size=1):
        """
        Get a list of the nearby agents in a square neighborhood.
        The size of the hood is given by hood_size.
        We can filter with pred.
        We may or may not save this hood.
        """
        return self.get_moore_hood(agent,
                                   pred=pred,
                                   save_neighbors=save_neighbors,
                                   include_self=include_self,
                                   size=hood_size)

    def get_neighbor_of_groupX(self, agent, group, save_neighbors=False,
                               hood_size=1):
        """
        If the agent has any neighbors in group X, return the first one
        encountered.
        We may get the groupX object itself, or we may get passed
        its name.
        """
        hood = self.get_square_hood(agent, save_neighbors=save_neighbors,
                                    hood_size=hood_size)
        import lib.actions as acts
        if isinstance(group, str):
            # lookup group by name
            group = acts.get_agent(group)
            if group is None:
                return None
        for agent_name in hood:
            if group.ismember(agent_name):
                return group[agent_name]
        return None

    def get_closest_agent(self, agent, size=None):
        (agent, dist) = self.get_closest_agent_and_dist(agent, size=size)
        return agent

    def get_closest_agent_and_dist(self, agent, size=None):
        import lib.actions as acts
        """
        Get the agent' closest to agent on grid.
        """
        closest = None
        # set min much bigger than furthest possible agent:
        min_distance_seen = MAX_WIDTH * MAX_HEIGHT
        if size is None:
            size = max(MAX_WIDTH, MAX_HEIGHT)
        for other_nm in get_neighbors(agent, size=size):
            other = acts.get_agent(other_nm)
            d = distance(agent, other)
            if DEBUG.debug_lib:
                print("Distance to ", str(other), "is", d)
            if d < min_distance_seen:
                if DEBUG.debug_lib:
                    print("Replacing closest with", str(other))
                min_distance_seen = d
                closest = other
        return (closest, min_distance_seen)

    def get_max_distance(self):
        return math.sqrt((self.height ** 2) + (self.width ** 2))

    def point_from_vector(self, angle, max_move, xy, vector_start=(0, 0)):
        """
        Given a vector with one end at the origin, find
        the other end -- if off grid, pull it back onto the
        grid.
        """
        (prev_x, prev_y) = xy
        (new_x, new_y) = xy
        #  Calculate the new coordinates
        new_x += int(math.cos(math.radians(angle)) * max_move)
        new_y += int(math.sin(math.radians(angle)) * max_move)
        return self.constrain_x(new_x), self.constrain_y(new_y)

    def exists_neighbor(self, agent, pred=None, exclude_self=True, size=1,
                        region_type=None):
        if DEBUG.debug2_lib:
            print("agent save_neighbor false is", agent.get("save_neighbors",
                                                            False))
        region = region_factory(space=self, center=(agent.get_x(),
                                                    agent.get_y()),
                                size=size,
                                agents_move=not agent.get("save_neighbors",
                                                          False))
        return region.exists_neighbor(exclude_self=exclude_self, pred=pred)

    def get_num_of_neighbors(self, agent, exclude_self=True, pred=None,
                             size=1, region_type=None):
        region = region_factory(space=self, center=(agent.get_x(),
                                                    agent.get_y()),
                                size=size,
                                agents_move=not agent.get("save_neighbors",
                                                          False))
        return region.get_num_of_agents(exclude_self=exclude_self, pred=pred)

    def get_neighbor(self, agent, pred=None, exclude_self=True, size=1,
                     region_type=None):
        region = region_factory(space=self, center=(agent.get_x(),
                                                    agent.get_y()),
                                size=size,
                                agents_move=not agent.get("save_neighbors",
                                                          False))
        return region.get_neighbor(no_self=exclude_self, pred=pred)

    def neighbor_ratio(self, agent, pred_one, pred_two=None, size=1,
                       region_type=None):
        region = region_factory(space=self, center=(agent.get_x(),
                                                    agent.get_y()),
                                size=size,
                                agents_move=not agent.get("save_neighbors",
                                                          False))
        return region.get_ratio(pred_one, pred_two=pred_two)


def gen_region_name_for_model_at_exec_key(model_name, exec_key, NW=None,
                                          NE=None, SW=None,
                                          SE=None, center=None, size=None):
    return model_name + ":" + str(exec_key) + ":" + \
           gen_region_name(NW=NW,
                           NE=NE,
                           SW=SW,
                           SE=SE,
                           center=center,
                           size=size)


def gen_region_name(NW=None, NE=None, SW=None,
                    SE=None, center=None, size=None):
    if center is None:
        return str(NW) + "," + str(NE) + "," + str(SW) + "," + str(SE)
    else:
        return str(center) + "," + str(size)


def region_factory(space=None, NW=None, NE=None, SW=None,
                   SE=None, center=None, size=1, agents_move=True,
                   **kwargs):
    import lib.actions as acts
    region_name = gen_region_name(NW=NW, NE=NE, SW=SW, SE=SE,
                                  center=center, size=size)
    if 'model_name' in kwargs:
        model_name = kwargs['model_name']
        exec_key = acts.get_model().exec_key
        if exec_key is not None and model_name is not None:
            region_name = gen_region_name_for_model_at_exec_key(model_name,
                                                                exec_key,
                                                                NW=NW,
                                                                NE=NE,
                                                                SW=SW,
                                                                SE=SE,
                                                                center=center,
                                                                size=size)

    if region_name in region_dict:
        return region_dict[region_name]
    else:
        new_reg = Region(space=space, NW=NW, NE=NE, SW=SW, SE=SE,
                         center=center, size=size, agents_move=agents_move,
                         **kwargs)
        region_dict[region_name] = new_reg
        return new_reg


def circ_region_factory(space=None, center=None,
                        radius=None, agents_move=False, **kwargs):
    region_name = gen_region_name(center=center, size=radius)
    if region_name in region_dict:
        return region_dict[region_name]
    else:
        new_reg = CircularRegion(space=space, center=center, radius=radius,
                                 agents_move=agents_move, **kwargs)
        region_dict[region_name] = new_reg
        return new_reg


def return_region(space=None, NW=None, NE=None, SW=None,
                  SE=None, center=None, size=None, agents_move=True):
    region_name = gen_region_name(NW=NW, NE=NE, SW=SW, SE=SE,
                                  center=center, size=size)
    if region_name in region_dict:
        return region_dict[region_name]
    else:
        raise Exception("Attempting to return a region that doesn't exist")


class Region():
    """
    This is the base class for regions used for neighborhoods, obstacles,
    and other sub-divisions of space.
    """
    def __init__(self, space=None, NW=None, NE=None, SW=None,
                 SE=None, center=None, size=None, agents_move=True, **kwargs):
        """
        Construct a sub-region of a space.
        We expect the center to be a tuple in the form (x,y).

        NW, NE, SW, and SE are the corners of the region.
        Size is the distance from the center that will bound the region


        There are two ways to initializa a region:

        First way, specify its four corners.
        Region(space, NW=(0, 3), NE=(3, 3), SW=(0, 0), SE=(3, 0))

        The second way, give its center point and size.
        Region(space, center=(2, 3), size=7)
        """
        self.name = gen_region_name(NW, NE, SW, SE, center, size)
        self.space = space
        if (center is not None and size is not None):
            if not isinstance(center, tuple):
                raise TypeError("center of a region must be a tuple.")
            if not isinstance(size, int) and not isinstance(size, float):
                raise TypeError("size of a region must be a scalar.")
            self.NW = (center[X] - size, center[Y] + size)
            self.NE = (center[X] + size, center[Y] + size)
            self.SW = (center[X] - size, center[Y] - size)
            self.SE = (center[X] + size, center[Y] - size)
            self.center = center
            self.size = size
        else:
            self.NW = NW
            self.NE = NE
            self.SW = SW
            self.SE = SE
            self.center = None
            self.size = None
        self._constrain_corners()
        self.width = abs(self.NW[X] - self.NE[X])
        self.height = abs(self.NW[Y] - self.SW[Y])
        self.agents_move = agents_move
        self.my_agents = []
        self.my_sub_regs = []
        if not self.agents_move:
            self._load_agents()

    def _constrain_corners(self):
        """
        Constrains the bounds of the corners to the edges of the space
        """
        self.NW = (self.space.constrain_x(self.NW[X]),
                   self.space.constrain_y(self.NW[Y]))
        self.NE = (self.space.constrain_x(self.NE[X]),
                   self.space.constrain_y(self.NE[Y]))
        self.SW = (self.space.constrain_x(self.SW[X]),
                   self.space.constrain_y(self.SW[Y]))
        self.SE = (self.space.constrain_x(self.SE[X]),
                   self.space.constrain_y(self.SE[Y]))

    def __str__(self):
        return self.name

    def __repr__(self):
        s = "width: " + str(self.width) + " "
        s += "height: " + str(self.height) + "\n"
        s += "============" + "\n"
        s += "NW: " + str(self.NW) + "\n"
        s += "NE: " + str(self.NE) + "\n"
        s += "SW: " + str(self.SW) + "\n"
        s += "SE: " + str(self.SE) + "\n"
        s += "===========" + "\n"
        return s

    def contains(self, coord):
        if (coord[X] >= self.NW[X]) and (coord[X] < self.NE[X]):
            if (coord[Y] >= self.SW[Y]) and (coord[Y] < self.NE[Y]):
                return True
        return False

    def create_sub_reg(self, space=None, NW=None, NE=None, SW=None,
                       SE=None, center=None, size=None,
                       agents_move=True):
        if (size > self.size):
            raise Exception("Creating sub_region bigger than main region")
        self.my_sub_regs.append(region_factory(space=space, NW=NW, NE=NE,
                                               SW=SW, SE=SE, center=center,
                                               size=size,
                                               agents_move=agents_move))
        self._load_agents()
        return self.my_sub_regs[-1]

    def agents_move_switch(self):
        self.agents_move = not self.agents_move
        return self.agents_move

    def _load_sub_reg_agents(self, exclude_self=False):
        for region in self.my_sub_regs:
            for agent in self.my_agents:
                if (region.contains(agent.get_pos())):
                    region.my_agents.append(agent)

    def _load_agents(self, exclude_self=True):
        """
        This fills self.my_agents with all neighbors, and maybe the center
        agents, depending upon `exclude_self`.
        """
        if DEBUG.debug2_lib:
            print("calling _load_agents in space.py")
        for y in range(self.height):
            y_coord = self.SW[Y] + y + 1
            for x in range(self.width):
                x_coord = self.SW[X] + x
                if (x_coord, y_coord) == self.center and exclude_self is True:
                    continue
                potential_neighbor = self.space.get_agent_at(x_coord,
                                                             y_coord)
                if potential_neighbor is not None:
                    self.my_agents.append(potential_neighbor)
        self._load_sub_reg_agents(exclude_self=exclude_self)

    def _load_agents_if_necc(self, exclude_self=True, pred=None):
        """
        Load the neighboring agents if we ain't got 'em already.
        """
        if self.agents_move is True:
            self.my_agents = []
            self._load_agents(exclude_self=exclude_self)

    def _apply_pred_if_necc(self, pred):
        these_agents = []
        if pred is not None:
            these_agents = [agent for agent in self.my_agents if pred(agent)]
        else:
            these_agents = self.my_agents
        return these_agents

    def get_agents(self, exclude_self=False, pred=None):
        """
        Get agents in region filtered by `pred()`:
            if agents don't move, use saved set.
        """
        self._load_agents_if_necc(exclude_self=exclude_self)
        return self._apply_pred_if_necc(pred)

    def get_group(self):
        return grp.Group(self.name, members=self.get_agents())

    def get_num_of_agents(self, exclude_self=False, pred=None):
        self._load_agents_if_necc(exclude_self=exclude_self)
        return len(self._apply_pred_if_necc(pred))

    def get_neighbor(self, no_self=True, pred=None):
        self._load_agents_if_necc(exclude_self=no_self)
        if pred is None:
            if len(self.my_agents) > 0:
                return self.my_agents[0]
        else:
            for agent in self.my_agents:
                if pred(agent):
                    return agent
        return None

    def exists_neighbor(self, exclude_self=True, pred=None):
        return self.get_neighbor(no_self=exclude_self, pred=pred) is not None

    def get_ratio(self, pred_one, pred_two=None):
        if pred_one is None:
            raise Exception("Pass at least a single predicate to get_ratio")
        self._load_agents_if_necc(exclude_self=True)
        ratio_agents = self.my_agents
        numerator = len([agent for agent in ratio_agents if pred_one(agent)])
        if pred_two is not None:
            denominator = len([agent for agent in ratio_agents
                               if pred_two(agent)])
        else:
            denominator = len(ratio_agents)
        if denominator == 0:
            return 1
        return numerator / denominator


class CircularRegion(Region):
    """
    This is a subclass of Region.
    """
    def __init__(self, space=None, center=None, radius=None, agents_move=True,
                 **kwargs):
        self.space = space
        self.center = center
        self.radius = radius
        self.name = "Circle"
        self.agents_move = agents_move
        self.my_sub_regs = []
        if self.agents_move:
            self.my_agents = []
        else:
            self.my_agents = self._load_agents()

    def check_out_bounds(self, coord):
        """
        Calls the parent classes out of bounds to see if the coordinate is
        outside the space
        """
        return out_of_bounds(coord[X], coord[Y], 0, 0, self.space.width,
                             self.space.height)

    def contains(self, coord):
        """
        Checks to see if the coord is in the CircularRegion
        """
        if ((((coord[X] - self.center[X]) ** 2)
             + ((coord[Y] - self.center[Y]) ** 2) < self.radius ** 2)
                and not self.check_out_bounds(coord)):
            return True
        return False

    def create_sub_reg(self, space=None, center=None,
                       radius=None, agents_move=True, **kwargs):
        if (radius > self.radius):
            raise Exception("Creating sub_region bigger than main region")
        self.my_sub_regs.append(circ_region_factory(
            space=space, center=center, radius=radius,
            agents_move=agents_move, **kwargs))
        self._load_agents()
        return self.my_sub_regs[-1]

    def _load_agents(self, exclude_self=True):
        # We're going to loop across all locations
        for coord in self.space.locations:
            contain_counter = 0
            conv_coord = get_xy_from_str(coord)
            # and see if the location is in the region.
            if self.contains(conv_coord):
                contain_counter += 1
                potential_agent = self.space.get_agent_at(conv_coord[X],
                                                          conv_coord[Y])
                if ((conv_coord == list(self.center))
                        and (exclude_self is True)):
                    continue
                else:
                    self.my_agents.append(potential_agent)

    def _load_agents_if_necc(self, exclude_self=True, pred=None):
        if self.agents_move is True:
            self.my_agents = []
            self._load_agents(exclude_self=exclude_self)

    def _apply_pred_if_necc(self, pred):
        these_agents = []
        if pred is not None:
            these_agents = [agent for agent in self.my_agents if pred(agent)]
        else:
            these_agents = self.my_agents
        return these_agents

    def get_agents(self, exclude_self=True, pred=None):
        self._load_agents_if_necc(exclude_self=exclude_self)
        return self._apply_pred_if_necc(pred)


class CompositeRegion(Region):
    """
    Composite Region is a subclass of region
    It represents a sub area of a larger region
    """

    def __init__(self, region_set=None):
        if region_set is None:
            self.composite = {}
        else:
            self.composite = region_set

    def contains(self, coord):
        """
        Checks to see if a coord is in a saved region
        """
        for region in self.composite:
            if (region.contains(coord)):
                return True
        return False

    def get_agents(self, exclude_self=False, pred=None):
        """
        Returns all the agents placed in all saved regions
        """
        my_agents = []
        for region in self.composite:
            sub_my_agents = region.get_agents(exclude_self=False, pred=pred)
            my_agents.extend(sub_my_agents)
        return my_agents

    def exists_neighbor(self, exclude_self=False, pred=None):
        """
        Checks if there is a neighboring region
        """
        for region in self.composite:
            if region.exists_neighbor(exclude_self=False, pred=pred):
                return True
        return False

    def add_region(self, region):
        """
        Add a composite region to be saved
        """
        self.composite.add(region)

    def remove_region(self, region):
        """
        Remove a composite region from the saved regions
        """
        self.composite.remove(region)
