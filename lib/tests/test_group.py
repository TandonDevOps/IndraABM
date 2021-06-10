"""
This is the test suite for group.py.
"""

from IPython import embed
from unittest import TestCase, main, skip

from lib.agent import join, split, switch
from lib.group import Group
from lib.tests.test_agent import create_hardy, create_newton
from lib.tests.test_agent import create_ramanujan, create_littlewood
from lib.tests.test_agent import create_ramsey, create_leibniz
from lib.tests.test_agent import exec_key, get_exec_key

N = "Newton"
R = "Ramanujan"
L = "Leibniz"
H = "Hardy"
NL = N + L
LN = L + N
HR = H + R
LR = "LittlewoodRamsey"

CALC_GUYS = "Calculus guys"


def match_name(agent, name):
    return agent.name == name


def max_duration(agent, duration):
    return agent.duration <= duration


def create_calcguys(exec_key, members):
    return Group(CALC_GUYS, members=members, exec_key=exec_key)


def create_cambguys(exec_key):
    return Group("Cambridge guys",
                 members=[create_hardy(), create_ramanujan()],
                 exec_key=exec_key)


def create_cambguys2(exec_key):
    return Group("Other Cambridge guys",
                 members=[create_littlewood(), create_ramsey()],
                 exec_key=exec_key)


def create_mathgrp(exec_key, members):
    return Group("Math groups",
                 members=members,
                 exec_key=exec_key)


def create_mem_str(comp):
    s = ""
    for agent in comp:
        s += agent  # this will collect the names of the members
    return s


def print_mem_str(comp):
    print(create_mem_str(comp))


class GroupTestCase(TestCase):
    def setUp(self):
        self.exec_key = get_exec_key()
        self.hardy = create_hardy()
        self.newton = create_newton()
        self.calc = create_calcguys(self.exec_key, members=[self.newton, create_leibniz()])
        self.camb = create_cambguys(self.exec_key)
        self.mathgrp = create_mathgrp(self.exec_key, members=[self.calc,
                                                              self.camb])

    def tearDown(self):
        self.exec_key = None
        self.hardy = None
        self.newton = None
        self.calc = None
        self.camb = None
        self.mathgrp = None

    def test_ismember(self):
        self.assertTrue(self.calc.ismember(self.newton))

    def test_eq(self):
        self.assertEqual(self.calc, self.calc)
        self.assertNotEqual(self.camb, self.calc)

    def test_str(self):
        name = "Ramanujan"
        c = Group(name, exec_key=self.exec_key)
        self.assertEqual(name, str(c))

    def test_repr(self):
        # this test has to be written!
        # self.assertEqual(rep, repr(agent))
        pass

    def test_len(self):
        self.assertEqual(len(self.camb), 2)

    def test_get(self):
        self.assertEqual(self.camb[H], self.hardy)

    def test_set(self):
        self.camb[str(self.newton)] = self.newton
        self.assertEqual(self.camb[str(self.newton)], self.newton)

    def test_contains(self):
        self.assertTrue(H in self.camb)

    def test_iter(self):
        self.assertEqual(create_mem_str(self.calc), NL)

    def test_reversed(self):
        s = ""
        for guy in reversed(self.calc):
            s += guy
        self.assertEqual(s, LN)

    def test_mul(self):
        self.camb += self.newton
        math_inter = self.calc * self.camb
        print_mem_str(math_inter)
        self.assertEqual(create_mem_str(math_inter), N)

    @skip("Having some trouble with mathguys group.")
    def test_imul(self):
        self.assertEqual(create_mem_str(self.mathgrp), NL + HR)
        self.mathgrp *= self.camb  # should drop out calc!
        self.assertEqual(create_mem_str(self.mathgrp), HR)

    @skip("This test needs exec key.")
    def test_add(self):
        self.mathgrp = self.calc + self.camb + create_cambguys2()
        self.assertEqual(create_mem_str(self.mathgrp), NL + HR + LR)
        # ensure we did not change original group:
        self.assertEqual(create_mem_str(self.calc), NL)
        # let's make sure set union does not dupe members:
        camb_self_union = self.camb + self.camb
        self.assertEqual(create_mem_str(camb_self_union), HR)
        # now let's add an atom rather than a group:
        self.calch = self.calc + self.hardy
        self.assertEqual(create_mem_str(self.calch), NL + H)

    @skip("This test awaits the new registry.")
    def test_iadd(self):
        # let's make sure set union does not dupe members:
        self.camb += self.camb
        self.assertEqual(create_mem_str(self.camb), HR)
        # now test adding new members:
        self.camb += create_cambguys2()
        self.assertEqual(create_mem_str(self.camb), HR + LR)
        # now test adding an atomic entity:
        self.camb += create_newton()
        self.assertEqual(create_mem_str(self.camb), HR + LR + N)

    def test_call(self):
        (acts, moves) = self.mathgrp()
        self.assertEqual(acts, 3)  # hardy is passive!

    def test_subset(self):
        just_n = self.calc.subset(match_name, str(self.newton), name="Just Newton!")
        self.assertEqual(create_mem_str(just_n), N)
        just_l = self.calc.subset(max_duration, 25, name="Just Leibniz!")
        self.assertEqual(create_mem_str(just_n), N)

    def test_rand_member(self):
        rand_guy = self.calc.rand_member()
        self.assertIsNotNone(rand_guy)
        self.assertIn(str(rand_guy), self.calc)
        empty_set = Group("Empty", exec_key=self.exec_key)
        rand_guy = empty_set.rand_member()
        self.assertIsNone(rand_guy)

    def test_rand_subset(self):
        """
        Test creating a random subset of a group.
        2 is a completely arbitrary number of members to get.
        """
        rand_set = self.mathgrp.rand_subset(2)
        self.assertIsInstance(rand_set, Group)
        self.assertEquals(len(rand_set), 2)
        for member in rand_set:
            self.assertIn(member, self.mathgrp)

    def test_is_mbr_comp(self):
        self.assertTrue(self.mathgrp.is_mbr_comp(CALC_GUYS))
        self.assertFalse(self.calc.is_mbr_comp(str(self.newton)))

    def test_pop_count(self):
        self.assertEqual(self.mathgrp.pop_count(CALC_GUYS), 2)
        self.assertEqual(self.calc.pop_count(str(self.newton)), 1)

    def test_leave_group(self):
        """
        Test leaving a group.
        This test is here rather than in agent because it requires Group!
        """
        split(self.calc, self.newton)
        self.assertEqual(create_mem_str(self.calc), L)

    def test_join_group(self):
        """
        Test joining a group.
        This test is here rather than in agent because it requires Group!
        """
        join(self.calc, self.hardy)
        self.assertEqual(create_mem_str(self.calc), NL + H)

    @skip("switch() needs exec_key!")
    def test_switch_groups(self):
        """
        Test switching groups.
        This test is here rather than in agent because it requires Group!
        """
        switch(self.hardy.name, self.camb.name, self.calc.name)
        self.assertIn(str(self.hardy), self.calc)


if __name__ == '__main__':
    main()
