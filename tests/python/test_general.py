import unittest
import random
import time
import os
import sys
from relmgr import RelationshipManager
from tests.python.settings import USE_RM_CACHE


class TestCase00(unittest.TestCase):
    def test_example(self):
        # FRED FRED FRED <-- this doesn't get printed
        """"""  # trick unit tests not to print first line of multiline comment by adding empty multiline comment here

        """
        sdfsdfsdfsdfsdfdsf <-- this does get printed, unless we do the above multiline trick
        """
        pass


class TestCase01(unittest.TestCase):
    def setUp(self):
        self.rm = RelationshipManager(caching=USE_RM_CACHE)

    def test_Basic00(self):
        self.rm.add_rel('a', 'b')
        self.rm.add_rel('a', 'c')

        result = self.rm.find_targets('a')
        self.assertTrue(result == ['b', 'c'] or result == ['c', 'b'])
        self.assertEqual(self.rm.find_sources('a'), [])
        self.assertEqual(self.rm.find_sources('b'), ['a'])
        self.assertEqual(self.rm.find_sources('c'), ['a'])

    def test_Basic01Singular(self):
        self.rm.add_rel('a', 'b')
        self.rm.add_rel('a', 'c')
        self.assertEqual(self.rm.find_source('b'), 'a')
        self.assertEqual(self.rm.find_source('c'), 'a')

        # could be 'b' or 'c' - arbitrary
        result = self.rm.find_target('a')
        self.assertTrue(result == 'b' or result == 'c')


class TestCase02(unittest.TestCase):
    def setUp(self):
        """
        A --r1-> B
        A <-r1-- B
        A --r2-> B
        A --r1-> C
        """
        self.rm = RelationshipManager(caching=USE_RM_CACHE)

        self.rm.add_rel('a', 'b', 'r1')
        self.rm.add_rel('a', 'b', 'r2')

        self.rm.add_rel('b', 'a', 'r1')

        self.rm.add_rel('a', 'c', 'r1')

    def test_IfRelIdIsWorking01(self):
        # could be 'b' or 'c' - arbitrary
        result = self.rm.find_target('a', 'r1')
        self.assertTrue(result == 'b' or result == 'c')

        self.assertEqual(self.rm.find_target('a', 'r2'), 'b')
        self.assertIsNone(self.rm.find_target('a', 'r3'))

        self.assertEqual(self.rm.find_source(target='b', rel_id='r1'), 'a')
        self.assertEqual(self.rm.find_source(target='b', rel_id='r2'), 'a')

        # default relationshipid is integer 1 which is not the string 'r1' nor is it 'r2'
        self.assertNotEqual(self.rm.find_source(target='c'), 'a')
        self.assertEqual(self.rm.find_source(target='c', rel_id='r1'), 'a')

    def test_MultipleReturns01(self):
        res = self.rm.find_targets('a', rel_id='r1')
        res.sort()
        self.assertEqual(res, ['b', 'c'])

        self.assertEqual(self.rm.find_sources('b', rel_id='r1'), ['a'])
        # cos no relationships with id integer 1 have been created
        self.assertEqual(self.rm.find_sources('b'), [])

    def test_NonExistent01(self):
        self.assertEqual(self.rm.find_targets('aa', rel_id='r1'), [])
        self.assertEqual(self.rm.find_targets('a', rel_id='r1111'), [])
        self.assertEqual(self.rm.find_targets('az', rel_id=None), [])
        self.assertEqual(self.rm.find_sources('bb', rel_id='r1'), [])
        self.assertEqual(self.rm.find_sources('b', rel_id='r1111'), [])
        self.assertEqual(self.rm.find_targets('a', rel_id='r1111'), [])
        self.assertEqual(self.rm.find_sources('bb', rel_id=None), [])

    def test_FindRelationshipIds_NewFeatureFeb2005_01(self):
        """Test if relationships exist"""
        self.assertTrue(self.rm.is_rel('a', 'b', 'r1'))
        self.assertTrue(self.rm.is_rel('a', 'b', 'r2'))
        self.assertFalse(self.rm.is_rel('a', 'b', 'zzz'))

        # No relationships with rel_id integer 1 (the default rel) have been created.
        self.assertFalse(self.rm.is_rel('a', 'b', rel_id=1))
        self.assertFalse(self.rm.is_rel('a', 'b'))

    def test_FindRelationshipIds_NewFeatureFeb2005_02(self):
        # Get a list of the relationships between source and target.
        self.assertEqual(self.rm.find_rels('a', 'b'), ['r1', 'r2'])

    def test_Removal_01(self):
        # print()
        # Specify wildcard RelId
        self.assertEqual(self.rm.find_rels('a', 'b'), ['r1', 'r2'])
        self.assertTrue(self.rm.is_rel('a', 'b', 'r1'))
        self.assertTrue(self.rm.is_rel('a', 'b', 'r2'))
        # remove all R's between a and b
        self.rm.remove_rel('a', 'b', None)
        self.assertEqual(self.rm.find_rels('a', 'b'), [], 'Getting ' + str(self.rm.find_rels('a', 'b')))
        self.assertFalse(self.rm.is_rel('a', 'b', 'r1'))
        self.assertFalse(self.rm.is_rel('a', 'b', 'r2'))

    def test_Removal_02(self):
        # Specify all params
        self.rm.remove_rel('a', 'b', 'r1')
        self.assertEqual(self.rm.find_rels('a', 'b'), ['r2'])
        self.assertFalse(self.rm.is_rel('a', 'b', 'r1'))
        self.assertTrue(self.rm.is_rel('a', 'b', 'r2'))

    def test_Removal_03(self):
        # Specify 'from' param
        self.assertTrue(self.rm.is_rel('a', 'b', 'r1'))
        self.assertTrue(self.rm.is_rel('a', 'b', 'r2'))
        self.assertTrue(self.rm.is_rel('a', 'c', 'r1'))
        self.rm.remove_rel('a', None, 'r1')
        self.assertFalse(self.rm.is_rel('a', 'b', 'r1'))  # zapped
        self.assertTrue(self.rm.is_rel('a', 'b', 'r2'))
        self.assertFalse(self.rm.is_rel('a', 'c', 'r1'))  # zapped

        self.assertIsNone(self.rm.find_source('b', 'r1'))
        self.assertEqual(self.rm.find_source('b', 'r2'), 'a')
        self.assertIsNone(self.rm.find_source('c', None))

    def test_Removal_04(self):
        # Specify 'to' param
        self.assertTrue(self.rm.is_rel('a', 'b', 'r1'))
        self.assertTrue(self.rm.is_rel('a', 'b', 'r2'))
        self.assertTrue(self.rm.is_rel('a', 'c', 'r1'))
        self.rm.remove_rel(None, 'b', 'r1')
        self.assertFalse(self.rm.is_rel('a', 'b', 'r1'))  # zapped
        self.assertTrue(self.rm.is_rel('a', 'b', 'r2'))
        self.assertTrue(self.rm.is_rel('a', 'c', 'r1'))

        self.rm.remove_rel(None, 'c', 'r1')
        self.assertTrue(self.rm.is_rel('a', 'b', 'r2'))
        self.assertFalse(self.rm.is_rel('a', 'c', 'r1'))  # zapped

        self.rm.remove_rel(None, 'b', 'r2')
        self.assertFalse(self.rm.is_rel('a', 'b', 'r2'))  # zapped
        self.assertFalse(self.rm.is_rel('a', 'c', 'r1'))


class TestCase03(unittest.TestCase):
    def setUp(self):
        """
        Lots of relationsips. Check the speed.
        """
        self.rm = RelationshipManager(caching=USE_RM_CACHE)
        # self.THINGS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJLMNOPQRSTUVWXYZ'    # ori takes MINUTES   efficient1 takes 1.7
        # ori takes 4.6       efficient1 takes 0.38
        self.THINGS = 'abcdefghijk'

        for c in self.THINGS:
            for c2 in self.THINGS:
                self.rm.add_rel(c, c2, 'r1')
                self.rm.add_rel(c, c2, 'r2')
                self.rm.add_rel(c2, c, 'r3')

    def test_Speed01(self):
        t = time.time()

        for c in self.THINGS:
            for c2 in self.THINGS:
                self.assertIn(c2, self.rm.find_targets(c, 'r1'))
                self.assertIn(c2, self.rm.find_targets(c, 'r2'))
                self.assertIn(c, self.rm.find_targets(c2, 'r3'))

        timetook = time.time() - t
        # print "Relationship lookups took", timetook, 'seconds'

        self.assertTrue(timetook < 0.05, 'Relationship manager not fast enough! ' + \
            str(timetook))


class TestCase04(unittest.TestCase):
    def setUp(self):
        """
        A --r1-> B
        A --r1-> B   # attempt to add a second R of the same type
        A --r2-> B
        A --r1-> C
        """
        self.rm = RelationshipManager(caching=USE_RM_CACHE)

        self.rm.add_rel('a', 'b', 'r1')
        self.rm.add_rel('a', 'b', 'r1')
        self.rm.add_rel('a', 'b', 'r2')
        self.rm.add_rel('a', 'c', 'r1')

    def test_Duplicates01(self):
        self.assertTrue(self.rm.is_rel(
            'a', 'b', 'r1'))  # [('a', 'b', 'r1')]
        self.assertEqual(self.rm.find_rels('a', 'b'), ['r1', 'r2'])
        self.assertTrue(self.rm.is_rel(
            'a', 'c', 'r1'))  # [('a', 'c', 'r1')]
        self.assertEqual(self.rm.find_rels('a', 'c'), ['r1'])


class TestCase05(unittest.TestCase):
    def setUp(self):
        """
        Check getting and setting the 'relationships' property, which,
        despite the implementation, should look the same.
        In the original RM the property is actually accessed directly (naughty)
        and the implementation is the same as the spec, namely a list of tuples (from,to,relid)

        A --r1-> B
        A --r2-> B
        A --r1-> C
        B --r1-> A
        C --r9-> B
        """
        self.rm = RelationshipManager(caching=USE_RM_CACHE)

        self.rm.add_rel('a', 'b', 'r1')
        self.rm.add_rel('a', 'b', 'r2')
        self.rm.add_rel('a', 'c', 'r1')
        self.rm.add_rel('b', 'a', 'r1')
        self.rm.add_rel('c', 'b', 'r9')

    def test_Get01(self):
        r = self.rm.relationships
        #self.assertEqual(r, [('a', 'b', 'r1'), ('a', 'b', 'r2'), ('a', 'c', 'r1'), ('b', 'a', 'r1'), ('c', 'b', 'r9')])
        self.assertEqual(len(r), 5)
        self.assertIn(('a', 'b', 'r2'), r)
        self.assertIn(('a', 'c', 'r1'), r)
        self.assertIn(('a', 'b', 'r1'), r)
        self.assertIn(('b', 'a', 'r1'), r)
        self.assertIn(('c', 'b', 'r9'), r)

    def test_Set01(self):
        r = [('a', 'b', 'r1'), ('a', 'b', 'r2'), ('a', 'c', 'r1'),
             ('b', 'a', 'r1'), ('c', 'b', 'r9')]
        newrm = RelationshipManager()
        newrm.relationships = r

        self.assertTrue(self.rm.is_rel('a', 'b', 'r1'))
        self.assertTrue(self.rm.is_rel('a', 'b', 'r2'))
        self.assertTrue(self.rm.is_rel('a', 'c', 'r1'))
        self.assertTrue(self.rm.is_rel('b', 'a', 'r1'))
        self.assertTrue(self.rm.is_rel('c', 'b', 'r9'))


def suite():
    # This suite only gets used by an explicit test runner when executing this file as a program
    # For CLI unit test discovery launching, use 'python -m unittest tests.test_core' or for verbosity
    # python -m unittest -v tests.test_core
    suite0 = unittest.makeSuite(TestCase00, 'test')
    suite1 = unittest.makeSuite(TestCase01, 'test')
    suite2 = unittest.makeSuite(TestCase02, 'test')
    suite3 = unittest.makeSuite(TestCase03, 'test')
    suite4 = unittest.makeSuite(TestCase04, 'test')
    suite5 = unittest.makeSuite(TestCase05, 'test')
    alltests = unittest.TestSuite(
        (suite0, suite1, suite2, suite3, suite4, suite5))
    return alltests


def main():
    # runner = unittest.TextTestRunner(descriptions=0, verbosity=2) # default is descriptions=1, verbosity=1
    # default is descriptions=1, verbosity=1
    runner = unittest.TextTestRunner(descriptions=False, verbosity=0)
    runner.run(suite())


if __name__ == '__main__':
    main()

