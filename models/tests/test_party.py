"""
This is the tests for the party model
"""

from unittest import TestCase
from models.party import MODEL_NAME, Party, party_grps, main
from models.party import create_female, create_male


class PartyTestCase(TestCase):
    def setUp(self):
        """
        Initializing agents
        """
        self.party = Party(MODEL_NAME, grp_struct=party_grps)
        self.male = create_male("male", 0)
        self.female = create_female("female", 0)

    def tearDown(self):
        self.party = None
        self.male = None
        self.female = None
    
    def test_run(self):
        """
        Does running the mode work? (return of 0)
        """
        self.assertEqual(0, self.party.run())
    
    def test_main(self):
        """
        Does running the main method work? (return of 0)
        """
        self.assertEqual(0, main())
    