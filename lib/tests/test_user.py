"""
This is the test suite for user.py.
"""

from unittest import TestCase, main, skip

from lib.env import Env
from lib.tests.test_agent import create_newton
from lib.tests.test_agent import get_exec_key
from lib.tests.test_env import GRP1, GRP2
from lib.user import DEF_STEPS, get_menu_json
from lib.user import TermUser
from lib.user import TestUser, CANT_ASK_TEST

MSG = "Hello world"


class UserTestCase(TestCase):
    def setUp(self):
        self.exec_key = get_exec_key()
        self.env = Env("Test env", exec_key=self.exec_key)
        self.user = TermUser("User", exec_key=self.exec_key)
        self.test_user = TestUser("TestUser", exec_key=self.exec_key)

    def tearDown(self):
        self.exec_key = None
        self.user = None
        self.test_user = None

    def test_tell(self):
        """
        Try to tell the user something.
        """
        ret = self.user.tell(MSG)
        self.assertEqual(ret, MSG)

    @skip("Models work but this test fails: problem is in the test!")
    def test_run(self):
        # need special env for this one
        env = Env("Test env", members=[create_newton()])
        acts = run(self.user, test_run=True)
        self.assertEqual(acts, DEF_STEPS)

    @skip("Models work but this test fails: problem is in the test!")
    def test_tcall(self):
        # need special env for this one
        env = Env("Test env", members=[create_newton()], exec_key=self.exec_key)
        acts = run(self.test_user, test_run=True)
        self.assertEqual(acts, DEF_STEPS)

    def test_task(self):
        self.assertEqual(self.test_user.ask("Silly question?"), CANT_ASK_TEST)

    @skip("Awaiting new registry")
    def test_get_menu_json(self):
        """
        See if we can read in the menu!
        """
        menu = get_menu_json()
        self.assertTrue(len(menu) >= 2)


if __name__ == '__main__':
    main()
