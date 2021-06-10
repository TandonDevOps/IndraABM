from unittest import TestCase

import db.menus_db as mdb


class MenuTests(TestCase):
    def test_get_model_menu(self):
        self.assertTrue(isinstance(mdb.get_model_menu(), dict))

    def test_get_run_menu(self):
        self.assertTrue(isinstance(mdb.get_run_menu(), dict))
        self.assertGreater(len(mdb.get_run_menu()), 1)
