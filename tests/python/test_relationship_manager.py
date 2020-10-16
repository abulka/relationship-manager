import unittest
import random
import time
import os
import sys
from relmgr import RelationshipManager


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
        self.rm = RelationshipManager()

    def test_Basic00(self):
        self.rm.AddRelationship('a', 'b')
        self.rm.AddRelationship('a', 'c')

        result = self.rm.FindObjects('a', None)
        assert result == ['b', 'c'] or result == ['c', 'b']
        assert self.rm.FindObjects(None, 'a') == []
        assert self.rm.FindObjects(None, 'b') == ['a']
        assert self.rm.FindObjects(None, 'c') == ['a']

    def test_Basic01Singular(self):
        self.rm.AddRelationship('a', 'b')
        self.rm.AddRelationship('a', 'c')
        assert self.rm.FindObject(None, 'b') == 'a'
        assert self.rm.FindObject(None, 'c') == 'a'

        # could be 'b' or 'c' - arbitrary
        result = self.rm.FindObject('a', None)
        assert result == 'b' or result == 'c'


class TestCase02(unittest.TestCase):
    def setUp(self):
        """
        A --r1-> B
        A <-r1-- B
        A --r2-> B
        A --r1-> C
        """
        self.rm = RelationshipManager()

        self.rm.AddRelationship('a', 'b', 'r1')
        self.rm.AddRelationship('a', 'b', 'r2')

        self.rm.AddRelationship('b', 'a', 'r1')

        self.rm.AddRelationship('a', 'c', 'r1')

    def test_IfRelIdIsWorking01(self):
        # could be 'b' or 'c' - arbitrary
        result = self.rm.FindObject('a', None, 'r1')
        assert result == 'b' or result == 'c'

        assert self.rm.FindObject('a', None, 'r2') == 'b'
        assert self.rm.FindObject('a', None, 'r3') == None

        assert self.rm.FindObject(None, 'b', 'r1') == 'a'
        assert self.rm.FindObject(None, 'b', 'r2') == 'a'

        # default relationshipid is integer 1 which is not the string 'r1' nor is it 'r2'
        assert self.rm.FindObject(None, 'c') != 'a'
        assert self.rm.FindObject(None, 'c', 'r1') == 'a'

    def test_MultipleReturns01(self):
        #assert self.rm.FindObjects('a',None,'r1').sort() == ['b', 'c']
        res = self.rm.FindObjects('a', None, 'r1')
        res.sort()
        assert res == ['b', 'c']

        assert self.rm.FindObjects(None, 'b', 'r1') == ['a']
        # cos no relationships with id integer 1 have been created
        assert self.rm.FindObjects(None, 'b') == []

        ok = False
        try:
            # invalid - must specify at least either from or to
            assert self.rm.FindObjects(None, None) == []
        except RuntimeError:
            ok = True
        assert ok

    def test_NonExistent01(self):
        assert self.rm.FindObjects('aa', None, 'r1') == []
        assert self.rm.FindObjects('a', None, 'r1111') == []
        assert self.rm.FindObjects('az', None, None) == []
        assert self.rm.FindObjects(None, 'bb', 'r1') == []
        assert self.rm.FindObjects(None, 'b', 'r1111') == []
        assert self.rm.FindObjects('a', None, 'r1111') == []
        assert self.rm.FindObjects(None, 'bb', None) == []

    def test_FindRelationshipIds_NewFeatureFeb2005_01(self):
        # ***
        # *** Original behaviour was to return the actual relationship tuples (bad cos implementation dependent!)
        # ***
        # *** New behaviour is to return a boolean.
        # ***
        # When specify both sides of a relationship, PLUS the relationship itself,
        # then there is nothing to find, so return a boolean T/F if that relationship exists.
        #
        assert self.rm.FindObjects('a', 'b', 'r1') == True
        assert self.rm.FindObjects('a', 'b', 'r2') == True
        assert self.rm.FindObjects('a', 'b', 'zzz') == False

        """
        This next one is a bit subtle - we are in fact specifying all parameters, because the
        default relId is integer 1 (allowing you to create simple relationships easily).
        Thus the question we are asking is "is there a R of type 'integer 1' between a and b?"
        """
        assert self.rm.FindObjects(
            'a', 'b') == False  # cos no relationships with id integer 1 have been created

    def test_FindRelationshipIds_NewFeatureFeb2005_02(self):
        # ***
        # *** Original behaviour was to return the actual relationship tuples (bad cos implementation dependent!)
        # ***
        # *** New behaviour is to return a list of the relationship ids.
        # ***
        # When specify both sides of the relationship but leave the relationship None, you get a list of the relationships.
        #
        assert self.rm.FindObjects('a', 'b', None) == ['r1', 'r2']

    def test_Removal_01(self):
        # Specify wildcard RelId
        assert self.rm.FindObjects('a', 'b', None) == ['r1', 'r2']
        assert self.rm.FindObjects('a', 'b', 'r1') == True
        assert self.rm.FindObjects('a', 'b', 'r2') == True
        # remove all R's between a and b
        self.rm.RemoveRelationships('a', 'b', None)
        assert self.rm.FindObjects(
            'a', 'b', None) == [], 'Getting ' + str(self.rm.FindObjects('a', 'b', None))
        assert self.rm.FindObjects('a', 'b', 'r1') == False
        assert self.rm.FindObjects('a', 'b', 'r2') == False

    def test_Removal_02(self):
        # Specify all params
        self.rm.RemoveRelationships('a', 'b', 'r1')
        assert self.rm.FindObjects('a', 'b', None) == ['r2']
        assert self.rm.FindObjects('a', 'b', 'r1') == False
        assert self.rm.FindObjects('a', 'b', 'r2') == True

    def test_Removal_03(self):
        # Specify 'from' param
        assert self.rm.FindObjects('a', 'b', 'r1') == True
        assert self.rm.FindObjects('a', 'b', 'r2') == True
        assert self.rm.FindObjects('a', 'c', 'r1') == True
        self.rm.RemoveRelationships('a', None, 'r1')
        assert self.rm.FindObjects('a', 'b', 'r1') == False  # zapped
        assert self.rm.FindObjects('a', 'b', 'r2') == True
        assert self.rm.FindObjects('a', 'c', 'r1') == False  # zapped

        assert self.rm.FindObject(None, 'b', 'r1') == None
        assert self.rm.FindObject(None, 'b', 'r2') == 'a'
        assert self.rm.FindObject(None, 'c', None) == None

    def test_Removal_04(self):
        # Specify 'to' param
        assert self.rm.FindObjects('a', 'b', 'r1') == True
        assert self.rm.FindObjects('a', 'b', 'r2') == True
        assert self.rm.FindObjects('a', 'c', 'r1') == True
        self.rm.RemoveRelationships(None, 'b', 'r1')
        assert self.rm.FindObjects('a', 'b', 'r1') == False  # zapped
        assert self.rm.FindObjects('a', 'b', 'r2') == True
        assert self.rm.FindObjects('a', 'c', 'r1') == True

        self.rm.RemoveRelationships(None, 'c', 'r1')
        assert self.rm.FindObjects('a', 'b', 'r2') == True
        assert self.rm.FindObjects('a', 'c', 'r1') == False  # zapped

        self.rm.RemoveRelationships(None, 'b', 'r2')
        assert self.rm.FindObjects('a', 'b', 'r2') == False  # zapped
        assert self.rm.FindObjects('a', 'c', 'r1') == False


class TestCase03(unittest.TestCase):
    def setUp(self):
        """
        Lots of relationsips. Check the speed.
        """
        self.rm = RelationshipManager()
        # self.THINGS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJLMNOPQRSTUVWXYZ'    # ori takes MINUTES   efficient1 takes 1.7
        # ori takes 4.6       efficient1 takes 0.38
        self.THINGS = 'abcdefghijk'

        for c in self.THINGS:
            for c2 in self.THINGS:
                self.rm.AddRelationship(c, c2, 'r1')
                self.rm.AddRelationship(c, c2, 'r2')
                self.rm.AddRelationship(c2, c, 'r3')

    def test_Speed01(self):
        t = time.time()

        for c in self.THINGS:
            for c2 in self.THINGS:
                assert c2 in self.rm.FindObjects(c, None, 'r1')
                assert c2 in self.rm.FindObjects(c, None, 'r2')
                assert c in self.rm.FindObjects(c2, None, 'r3')

        timetook = time.time() - t
        # print "Relationship lookups took", timetook, 'seconds'

        assert timetook < 0.05, 'Relationship manager not fast enough! ' + \
            str(timetook)


class TestCase04(unittest.TestCase):
    def setUp(self):
        """
        A --r1-> B
        A --r1-> B   # attempt to add a second R of the same type
        A --r2-> B
        A --r1-> C
        """
        self.rm = RelationshipManager()

        self.rm.AddRelationship('a', 'b', 'r1')
        self.rm.AddRelationship('a', 'b', 'r1')
        self.rm.AddRelationship('a', 'b', 'r2')
        self.rm.AddRelationship('a', 'c', 'r1')

    def test_Duplicates01(self):
        assert self.rm.FindObjects(
            'a', 'b', 'r1') == True  # [('a', 'b', 'r1')]
        assert self.rm.FindObjects('a', 'b', None) == ['r1', 'r2']
        assert self.rm.FindObjects(
            'a', 'c', 'r1') == True  # [('a', 'c', 'r1')]
        assert self.rm.FindObjects('a', 'c', None) == ['r1']


class TestCase05(unittest.TestCase):
    def setUp(self):
        """
        Check getting and setting the 'Relationships' property, which,
        despite the implementation, should look the same.
        In the original RM the property is actually accessed directly (naughty)
        and the implementation is the same as the spec, namely a list of tuples (from,to,relid)

        A --r1-> B
        A --r2-> B
        A --r1-> C
        B --r1-> A
        C --r9-> B
        """
        self.rm = RelationshipManager()

        self.rm.AddRelationship('a', 'b', 'r1')
        self.rm.AddRelationship('a', 'b', 'r2')
        self.rm.AddRelationship('a', 'c', 'r1')
        self.rm.AddRelationship('b', 'a', 'r1')
        self.rm.AddRelationship('c', 'b', 'r9')

    def test_Get01(self):
        r = self.rm.Relationships
        #assert r == [('a', 'b', 'r1'), ('a', 'b', 'r2'), ('a', 'c', 'r1'), ('b', 'a', 'r1'), ('c', 'b', 'r9')]
        assert len(r) == 5
        assert ('a', 'b', 'r1') in r
        assert ('a', 'b', 'r2') in r
        assert ('a', 'c', 'r1') in r
        assert ('b', 'a', 'r1') in r
        assert ('c', 'b', 'r9') in r

    def test_Set01(self):
        r = [('a', 'b', 'r1'), ('a', 'b', 'r2'), ('a', 'c', 'r1'),
             ('b', 'a', 'r1'), ('c', 'b', 'r9')]
        newrm = RelationshipManager()
        newrm.Relationships = r

        assert self.rm.FindObjects('a', 'b', 'r1') == True
        assert self.rm.FindObjects('a', 'b', 'r2') == True
        assert self.rm.FindObjects('a', 'c', 'r1') == True
        assert self.rm.FindObjects('b', 'a', 'r1') == True
        assert self.rm.FindObjects('c', 'b', 'r9') == True


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


"""
SCRAPS

import pprint

class RelationshipManagerPersistent(RelationshipManager):
    def __init__(self):
        RelationshipManager.__init__(self)

    def __repr__(self):
        return pprint.pformat(self.Relationships)

    def LoadFromStr(self, str):
        self.Relationships = eval(str)

    def LoadFromList(self, L):
        self.Relationships = L

P.S.  There may be more stuff like this to integrate back into the main
      relationshipmanager.py module found in oobtree.py
      e.g.
        self._ConvertRelations(self.oobtreeAllies.relations.Relationships)
        LoadFromReprStr(self, strdict):
        __repr__(self):
        __str__(self):
        LoadFromDict
        etc.
"""

# -----------------------------
