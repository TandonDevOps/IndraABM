"""
This is the test suite for wolfsheep.py.
"""

from unittest import TestCase, skip  # , main
from lib.agent import Agent
from models.wolfsheep import WolfSheep, main, MODEL_NAME, wolfsheep_grps
from models.wolfsheep import WOLF_GRP_NM, SHEEP_GRP_NM
from models.wolfsheep import TIME_TO_REPRODUCE, WOLF_REPRO_PERIOD, SHEEP_REPRO_PERIOD
from models.wolfsheep import DEF_TIME_TO_REPRO
from models.wolfsheep import sheep_action, wolf_action, reproduce


class WolfSheepTestCase(TestCase):
    def setUp(self):
        self.wolfsheep = WolfSheep(MODEL_NAME, grp_struct=wolfsheep_grps)
        self.wolf = Agent(name=WOLF_GRP_NM, exec_key=self.wolfsheep.exec_key)
        self.sheep = Agent(name=SHEEP_GRP_NM, exec_key=self.wolfsheep.exec_key)

    def tearDown(self):
        self.wolfsheep = None

    def test_run(self):
        """
        Does running the model work? (return of 0)
        """
        self.assertEqual(0, self.wolfsheep.run())

    def test_main(self):
        """
        Does the main func of the model work? (return of 0)
        """
        self.assertEqual(0, main())

    def test_wolf_action(self):
        """
        Wolves act by eating a random sheep from the meadow
        """

        # Run once to initialize the attributes
        wolf_action(self.wolf)

        # Get TIME_TO_REPRODUCE attribute
        time_to_repro = self.wolf.get_attr(TIME_TO_REPRODUCE)

        # Run again
        wolf_action(self.wolf)

        if time_to_repro == 1:
            self.assertEqual(self.wolf.get_attr(TIME_TO_REPRODUCE), WOLF_REPRO_PERIOD)
        else:
            self.assertEqual(self.wolf.get_attr(TIME_TO_REPRODUCE), time_to_repro - 1)

    def test_sheep_action(self):
        """
        Sheep act by moving around the meadow and reproducing
        """

        # Run once to initialize the attributes
        sheep_action(self.sheep)

        # Get TIME_TO_REPRODUCE attribute
        time_to_repro = self.sheep.get_attr(TIME_TO_REPRODUCE)

        # Run again
        sheep_action(self.sheep)

        if time_to_repro == 1:
            self.assertEqual(self.sheep.get_attr(TIME_TO_REPRODUCE), SHEEP_REPRO_PERIOD)
        else:
            self.assertEqual(self.sheep.get_attr(TIME_TO_REPRODUCE), time_to_repro - 1)

    @skip("This test is nonsense: can't ask a sheep to act outside of model.")
    def test_sheep_reproduce(self):
        """
        Check if sheep can reproduce
        """

        # Run once to initialize the attributes
        sheep_action(self.sheep)

        # Set TIME_TO_REPRODUCE to 0 for triggering reproduction
        self.sheep.set_attr(TIME_TO_REPRODUCE, 0)

        # Let sheep reproduce
        reproduce(self.sheep)

        self.assertEqual(
            self.sheep.get_attr(TIME_TO_REPRODUCE), DEF_TIME_TO_REPRO
        )

    @skip("This test is nonsense: can't ask a wolf to act outside of model.")
    def test_wolf_reproduce(self):
        """
        Check if wolf can reproduce
        """

        # Run once to initialize the attributes
        wolf_action(self.wolf)

        # Set TIME_TO_REPRODUCE to 0 for triggering reproduction
        self.wolf.set_attr(TIME_TO_REPRODUCE, 0)

        # Let wolf reproduce
        reproduce(self.wolf)

        self.assertEqual(
            self.wolf.get_attr(TIME_TO_REPRODUCE), DEF_TIME_TO_REPRO
        )
