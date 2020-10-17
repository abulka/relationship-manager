import unittest
import pprint
import random
import timeit

DEBUG = False

CACHING_ON = True

if CACHING_ON:
    from relmgr.relationship_manager import RelationshipManagerCaching as RelationshipManager  # test caching version
else:
    from relmgr.relationship_manager import RelationshipManagerPersistent as RelationshipManager  # test non caching version


# creating a global variable makes referring to the RM instance more succinct than e.g. self.RM
RM = None


class TestCaching(unittest.TestCase):

    def setUp(self):
        global RM
        RM = RelationshipManager()
        self.start_time = timeit.default_timer()

    def tearDown(self):
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
        STRESS_AMOUNT = 20000

        # build the relationships
        for i in range(NUM_RELS):
            RM.R(random.choice(fromIds), random.choice(toIds), relId="stress")

        # now access them repeadedly
        for i in range(STRESS_AMOUNT):
            for fromId in range(len(fromIds)):
                rels = RM.PS(fromId, "stress")
                if i == 0 and DEBUG:
                    print(rels)

        # report the results
        if DEBUG:
            if CACHING_ON:
                print(RM.PS.cache_info())
            else:
                print("no caching")
