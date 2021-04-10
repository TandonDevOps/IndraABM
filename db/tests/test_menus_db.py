from unittest import TestCase

import db.menus_db as mdb


class MenuTests(TestCase):
    def test_get_model_menu(self):
        self.assertTrue(isinstance(mdb.get_model_menu(), dict))
