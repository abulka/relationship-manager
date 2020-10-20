import unittest
import pprint
import random
import timeit
from relmgr.relationship_manager import RelationshipManager
from tests.python.settings import USE_RM_CACHE

DEBUG = False

# creating a global variable makes referring to the RM instance more succinct than e.g. self.RM
RM = None


class TestCaching(unittest.TestCase):

    def setUp(self):
        global RM
        RM = RelationshipManager(caching=USE_RM_CACHE)
        self.start_time = timeit.default_timer()

    def tearDown(self):
        global RM
        RM = None
        elapsed = timeit.default_timer() - self.start_time
        if DEBUG:
            print(f"{elapsed=}")

    def test_BigOne(self):
        """"""
        """
        Create large number of random relationships
        """

        fromIds = list(range(100))
        toIds = list(range(100))
        NUM_RELS = 300
        STRESS_AMOUNT = 10000

        # build the relationships
        for i in range(NUM_RELS):
            RM.R(random.choice(fromIds), random.choice(toIds), relId="stress")

        # now access them repeatedly
        for i in range(STRESS_AMOUNT):
            for fromId in range(len(fromIds)):
                rels = RM.PS(fromId, "stress")
                if i == 0 and DEBUG:
                    print(rels)

        # report the results
        if DEBUG:
            if USE_RM_CACHE:
                print(RM.PS.cache_info())
            else:
                print("no caching")
