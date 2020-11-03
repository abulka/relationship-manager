import unittest
import pprint
from relmgr import RelationshipManager
# from relmgr.relationship_manager import RelationshipManagerCaching as RelationshipManager  # test caching version
from tests.python.settings import USE_RM_CACHE

# creating a global variable makes referring to the RM instance more succinct than e.g. self.RM
rm = None


class TestCase01_OneToOne(unittest.TestCase):

    def setUp(self):
        global rm
        rm = RelationshipManager(caching=USE_RM_CACHE)

    def test_scenario_1_OneToOne_XSingularApi_YNoApi(self):
        """"""  # trick unit tests not to print first line of multiline comment by adding empty multiline comment here
        """
         ______________        ______________
        |       X      |      |       Y      |
        |______________|      |______________|
        |              |      |              |
        |void  setY(y) |1    1|              |
        |Y     getY()  |----->|              |
        |void  clearY()|      |              |
        |______________|      |______________|

        """
        class X:
            def __init__(self):        rm.enforce("xtoy", "onetoone", "directional")
            def setY(self, y):         rm.add_rel(self, y, "xtoy")
            def getY(self):     return rm.find_target(source=self, rel_id="xtoy")
            def clearY(self):          rm.remove_rel(self, self.getY(), "xtoy")

        class Y:
            pass

        x1 = X()
        x2 = X()
        y1 = Y()
        y2 = Y()
        # Initial situation
        self.assertIsNone(x1.getY())
        self.assertIsNone(x2.getY())

        # After clearing pointers
        x1.clearY()
        self.assertIsNone(x1.getY())
        self.assertIsNone(x2.getY())

        # After setting one pointer, x1 -> y1
        x1.setY(y1)
        # RM.debug_print_rels()
        self.assertEqual(x1.getY(), y1)
        self.assertIsNone(x2.getY())

        # After setting x2 -> y1, we cannot allow a situation where
        # both x's to point to the same y, since this would be "many to one".
        # The existing x1 -> y1 must be auto deleted by the relationship manager
        # relationship enforcer.
        self.assertEqual(x1.getY(), y1)
        x2.setY(y1)
        self.assertIsNone(x1.getY())  # relationship should have been auto removed
        self.assertEqual(x2.getY(), y1)

        # Clear one pointer
        x1.clearY()
        self.assertIsNone(x1.getY())
        self.assertEqual(x2.getY(), y1)

        # Clear other pointer
        x2.clearY()
        self.assertIsNone(x1.getY())
        self.assertIsNone(x2.getY())

        # Change from pointing to one thing then point to another
        x1.setY(y1)
        x1.setY(y2)
        self.assertEqual(x1.getY(), y2)

        # Ensure repeat settings do not disturb things
        x1.clearY()
        x2.clearY()
        # x1 -> y1, x2 -> None
        x1.setY(y1)
        self.assertEqual(x1.getY(), y1)
        self.assertIsNone(x2.getY())
        # repeat
        x1.setY(y1)
        self.assertEqual(x1.getY(), y1)
        self.assertIsNone(x2.getY())

        # x1 -> None, x2 -> y1
        x2.setY(y1)
        self.assertIsNone(x1.getY())
        self.assertEqual(x2.getY(), y1)
        # repeat
        x2.setY(y1)
        self.assertIsNone(x1.getY())
        self.assertEqual(x2.getY(), y1)

        # x1 -> y2, x2 -> y1
        x1.setY(y2)
        self.assertEqual(x1.getY(), y2)
        self.assertEqual(x2.getY(), y1)
        # repeat
        x1.setY(y2)
        self.assertEqual(x1.getY(), y2)
        self.assertEqual(x2.getY(), y1)

    def test_scenario_2_OneToOne_XNoApi_YSingularApi(self):
        """"""  # trick unit tests not to print first line of multiline comment by adding empty multiline comment here
        """
         ______________        ______________
        |       X      |      |       Y      |
        |______________|      |______________|
        |              |      |              |
        |              |1    1|setX(self, x) |
        |              |----->|getX(self)    |
        |              |      |clearX(self)  |
        |______________|      |______________|        

        """
        class X:
            pass

        class Y:
            def __init__(self):        rm.enforce("xtoy", "onetoone", "directional")
            def setX(self, x):         rm.add_rel(x, self, "xtoy")
            def getX(self):     return rm.find_source(target=self, rel_id="xtoy")
            def clearX(self):          rm.remove_rel(self.getX(), self, "xtoy")

        x1 = X()
        x2 = X()
        y1 = Y()
        y2 = Y()

        # Initial situation
        self.assertIsNone(y1.getX())
        self.assertIsNone(y2.getX())

        # After clearing pointers
        y1.clearX()
        self.assertIsNone(y1.getX())
        self.assertIsNone(y2.getX())

        # After setting one pointer, thus x1 -> y1
        y1.setX(x1)
        self.assertEqual(y1.getX(), x1)
        self.assertIsNone(y2.getX())

        # Want to show two x's pointing to same y
        # Cannot do this since need access to an x api to do the 2nd link
        # but this unit test assumes that the X has no API at all.
        pass

        # A y can be pointed to by many x's
        # An x can only point at one y at a time
        # So if x1 -> y1 and then x1 -> y2 then y1 is being pointed to by no-one.
        # After setting other pointer, both x's pointing to same y, thus x1 & x2 -> y1
        y2.setX(x1)
        self.assertIsNone(y1.getX())  # should be auto cleared
        self.assertEqual(y2.getX(), x1)

        # Clear one pointer
        y1.clearX()
        self.assertIsNone(y1.getX())
        self.assertEqual(y2.getX(), x1)

        # Clear other pointer
        y2.clearX()
        self.assertIsNone(y1.getX())
        self.assertIsNone(y2.getX())

        # Change from x1 -> y1 to x2 -> y1 (pointing to one thing then point to another)
        y1.clearX()
        y2.clearX()
        y1.setX(x1)
        y1.setX(x2)
        self.assertEqual(y1.getX(), x2)
        self.assertIsNone(y2.getX())

        # Ensure repeat settings do not disturb things
        y1.clearX()
        y2.clearX()
        y1.setX(x1)
        self.assertEqual(y1.getX(), x1)
        self.assertIsNone(y2.getX())
        # repeat
        y1.setX(x1)
        self.assertEqual(y1.getX(), x1)
        self.assertIsNone(y2.getX())

    def onetooneasserts(self, x1, x2, y1, y2):

        def assertallclear():
            self.assertIsNone(x1.getY())
            self.assertIsNone(x2.getY())
            self.assertIsNone(y1.getX())
            self.assertIsNone(y2.getX())

        # Initial situation
        assertallclear()

        # After clearing pointers
        x1.clearY()
        x2.clearY()
        y1.clearX()
        y2.clearX()
        assertallclear()

        # After setting one pointer, x1 <-> y1
        x1.setY(y1)
        self.assertEqual(x1.getY(), y1)
        self.assertIsNone(x2.getY())
        self.assertEqual(y1.getX(), x1)
        self.assertIsNone(y2.getX())
        # rm.debug_print_rels()

        # After clearing that one pointer, x1 <-> y1
        x1.clearY()
        assertallclear()

        # After setting one pointer, via y API, x1 <-> y1
        y1.setX(x1)
        self.assertEqual(x1.getY(), y1)
        self.assertIsNone(x2.getY())
        self.assertEqual(y1.getX(), x1)
        self.assertIsNone(y2.getX())
        y1.clearX()
        assertallclear()

        # After setting one pointer, via y API, x1 <-> y1
        # then change it via x API, to          x1 <-> y2
        # thus the old x1 <-> y1 must extinguish.
        y1.setX(x1)
        x1.setY(y2)
        self.assertEqual(x1.getY(), y2)
        self.assertIsNone(x2.getY())
        self.assertIsNone(y1.getX())
        self.assertEqual(y2.getX(), x1)
        # repeat
        y1.setX(x1)
        x1.setY(y2)
        self.assertEqual(x1.getY(), y2)
        self.assertIsNone(x2.getY())
        self.assertIsNone(y1.getX())
        self.assertEqual(y2.getX(), x1)
        # clear
        x1.clearY()
        assertallclear()

        # Do same trick using opposite API's
        x1.setY(y1)                             # instead of y1.setX(x1)
        y2.setX(x1)                             # instead of x1.setY(y2)
        # exactly the same assertions
        self.assertEqual(x1.getY(), y2)
        self.assertIsNone(x2.getY())
        self.assertIsNone(y1.getX())
        self.assertEqual(y2.getX(), x1)
        # repeat
        x1.setY(y1)
        y2.setX(x1)
        self.assertEqual(x1.getY(), y2)
        self.assertIsNone(x2.getY())
        self.assertIsNone(y1.getX())
        self.assertEqual(y2.getX(), x1)

        y2.clearX()
        assertallclear()

        # Wire both x1-y1, x2-y2 using x API
        x1.setY(y1)
        x2.setY(y2)
        self.assertEqual(x1.getY(), y1)
        self.assertEqual(x2.getY(), y2)
        self.assertEqual(y1.getX(), x1)
        self.assertEqual(y2.getX(), x2)
        # repeat wiring using opposite Y api, same asserts
        y1.setX(x1)
        y2.setX(x2)
        self.assertEqual(x1.getY(), y1)
        self.assertEqual(x2.getY(), y2)
        self.assertEqual(y1.getX(), x1)
        self.assertEqual(y2.getX(), x2)
        # Now set x2-y1 using x API, should yield x1-None, x2-y1
        x2.setY(y1)
        self.assertIsNone(x1.getY())
        self.assertEqual(x2.getY(), y1)
        self.assertEqual(y1.getX(), x2)
        self.assertIsNone(y2.getX())
        # Repeat above set x2-y1 using y API, same asserts
        y1.setX(x2)
        self.assertIsNone(x1.getY())
        self.assertEqual(x2.getY(), y1)
        self.assertEqual(y1.getX(), x2)
        self.assertIsNone(y2.getX())
        # Now set x1-y2, using y API, should yield x1-y2, x2-y1
        y2.setX(x1)
        self.assertEqual(x1.getY(), y2)
        self.assertEqual(x2.getY(), y1)
        self.assertEqual(y1.getX(), x2)
        self.assertEqual(y2.getX(), x1)
        # Repeat above set x1-y2, using x API, same asserts
        x1.setY(y2)
        self.assertEqual(x1.getY(), y2)
        self.assertEqual(x2.getY(), y1)
        self.assertEqual(y1.getX(), x2)
        self.assertEqual(y2.getX(), x1)

        x1.clearY()
        self.assertIsNone(x1.getY())
        self.assertEqual(x2.getY(), y1)
        self.assertEqual(y1.getX(), x2)
        self.assertIsNone(y2.getX())
        y1.clearX()
        assertallclear()

    def test_scenario_3_OneToOne_XSingularApi_YSingularApi(self):
        """"""  # trick unit tests not to print first line of multiline comment by adding empty multiline comment here
        """
        Since both sides have an API, then this is bidirectional
         ______________        ______________
        |       X      |      |       Y      |
        |______________|      |______________|
        |              |      |              |
        |void  setY(y) |1    1|setX(self, x) |
        |Y     getY()  |<---->|getX(self)    |
        |void  clearY()|      |clearX(self)  |
        |______________|      |______________|        
        """
        class X:
            def __init__(self):        rm.enforce("xy", "onetoone", "bidirectional")
            def setY(self, y):         rm.add_rel(self, y, "xy")
            def getY(self):     return rm.find_target(self, "xy")
            def clearY(self):          rm.remove_rel(self, self.getY(), "xy")

        class Y:
            def __init__(self):        rm.enforce("xy", "onetoone", "bidirectional")  # redundant call since already called in X's constructor
            def setX(self, x):         rm.add_rel(self, x, "xy")
            def getX(self):     return rm.find_target(self, "xy")
            def clearX(self):          rm.remove_rel(self, self.getX(), "xy")

        x1 = X()
        x2 = X()
        y1 = Y()
        y2 = Y()
        self.onetooneasserts(x1, x2, y1, y2)

    def test_scenario_3A_OneToOne_XSingularApi_YSingularApi_Alt_Backpointer(self):
        """"""  # trick unit tests not to print first line of multiline comment by adding empty multiline comment here
        """
        Alternative implementation of same API, One to one, with back pointer

         ______________        ______________
        |       X      |      |       Y      |
        |______________|      |______________|
        |              |      |              |
        |void  setY(y) |1    1|setX(self, x) |
        |Y     getY()  |<---->|getX(self)    |
        |void  clearY()|      |clearX(self)  |
        |______________|      |______________|        
        
        Proves that the bidirectional one to one - API using only P()
         (whether implemented as two synchronised relationships,
          or whether implemented as a smart single bi relationship)
        can also be imlpemented as directional one to one - API using B() and P()
         (whether implemented as a single relationship,
          or whether implemented as two synchronised (more efficient) relationships).
        
        Note that the above alternative API implementation is a pure 
        combination of the two directional APIs from unit tests
            XSingularApi_YNoApi
            XNoApi_YSingularApi
        using the directional relationship "xtoy".
        """
        class X:
            def __init__(self):        rm.enforce("xtoy", "onetoone", "directional")
            def setY(self, y):         rm.add_rel(self, y, "xtoy")
            def getY(self):     return rm.find_target(self, "xtoy")
            def clearY(self):          rm.remove_rel(self, self.getY(), "xtoy")

        class Y:
            def __init__(self):        rm.enforce("xtoy", "onetoone", "directional")  # redundant call since already called in X's constructor
            def setX(self, x):         rm.add_rel(x, self, "xtoy")
            def getX(self):     return rm.find_source(self, "xtoy")
            def clearX(self):          rm.remove_rel(self.getX(), self, "xtoy")

        x1 = X()
        x2 = X()
        y1 = Y()
        y2 = Y()
        self.onetooneasserts(x1, x2, y1, y2)


class TestCase02_OneToMany(unittest.TestCase):

    def setUp(self):
        global rm
        rm = RelationshipManager()

    def tearDown(self):
        RM = None

    def test_scenario_4_OneToMany_XPluralApi_YNoApi(self):
        """"""  # trick unit tests not to print first line of multiline comment by adding empty multiline comment here

        """
        One to Many, directional, all methods on lhs X side.
        
         _________________        ______________
        |        X        |      |       Y      |
        |_________________|      |______________|
        |                 |      |              |
        |addY(self, y)    |1    *|              |
        |getAllY(self)    |----->|              |
        |removeY(self, y) |      |              |
        |_________________|      |______________|

        X has the required plural API, 
        Y has no API.
        """
        class X:
            def __init__(self):        rm.enforce(
                "xtoy", "onetomany", "directional")

            def addY(self, y):         rm.add_rel(self, y, "xtoy")
            def getAllY(self):  return rm.find_targets(self, "xtoy")
            def removeY(self, y):      rm.remove_rel(self, y, "xtoy")

        class Y:
            pass

        x1 = X()
        x2 = X()
        y1 = Y()
        y2 = Y()
        self.onetomanyasserts(x1, x2, y1, y2)

    def test_scenario_5_OneToMany_XPluralApi_YSingularApi(self):
        """"""  # trick unit tests not to print first line of multiline comment by adding empty multiline comment here
        """
        One to Many, bidirectional, methods on both X and Y
        
         _________________        ______________
        |        X        |      |       Y      |
        |_________________|      |______________|
        |                 |      |              |
        |addY(self, y)    |1    *|setX(self, x) |
        |getAllY(self)    |<---->|getX(self)    |
        |removeY(self, y) |      |clearX(self)  |
        |_________________|      |______________|

        X has the required plural API, 
        Y has the reciprocal singular API
        
        Since there are two API's, one on each class, this makes it a bidirectional relationship.
        
        However !! there still remains a strong sense of directionality since the one to many
        is directional i.e. the one is the X and the many is the Y.

        Thus RM.R on both API's must be always done from the X to the Y.
        
        So in a sense, the relationships should be named "xtoy" even though it is bi.
        
        
                               ___               ___
          _________        ___d888b___       ___d888
         d888888888b______d88888888888b_____d8888888
        d8888888888888888888888888888888888888888888
        Y88P     Y8888888888P       Y888888888P
        
        ASIDE:
        Only in the many to many case would you consider using a name like "xy" for a 
        relationshipId.  ??
        
        But even then, you often have a many to many that is directional
        e.g. many brothers to many sisters - you must get the directionality right 
        e.g. "brothertosister" is one relationship
             X (brother)                                Y (sister)
             addSister(s)  RM.R(this,s,'btos')          addBrother(b)  RM.R(b,this,'btos')
             getSisters()                               getBrothers()
             
        Notice the directionality is always the one way.
        
        Will there ever be a many to many where directionality DOESN'T matter?
        Perhaps if there are two different objects pointing to each other, there
        are going to be the 'attachment points' - thus you ALWAYS need to know
        who is on what side of the relationship.
        
        END ASIDE.
        
        h88b     h8888888888b       h888888888b
        q8888888888888888888888888888888888888888888
         q888888888p""   "q88888888888p""q8888888
                           ""q888p""       ""q888
        
        This too, has two implementations, do it as a BI, with proper pointers
        from y to x (rather than relying on backpointers).  
        Note that implementationally, both cases can be done with a single relationship
        or both cases can be done with a pair of relationships.
        one relationship, a bi
        """
        class X:
            def __init__(self):        rm.enforce(
                "xtoy", "onetomany", "bidirectional")

            def addY(self, y):         rm.add_rel(self, y, "xtoy")
            def getAllY(self):  return rm.find_targets(self, "xtoy")
            def removeY(self, y):      rm.remove_rel(self, y, "xtoy")

        class Y:
            # though bi, there is still a direction!
            def setX(self, x):         rm.add_rel(x, self, "xtoy")
            def getX(self):     return rm.find_target(self, "xtoy")
            def clearX(self):          rm.remove_rel(self, self.getX(), "xtoy")

        x1 = X()
        x2 = X()
        y1 = Y()
        y2 = Y()
        self.onetomanyasserts(x1, x2, y1, y2, yapi=1)

    def test_scenario_5A_OneToMany_XPluralApi_YSingularApi_Alt(self):
        """"""  # trick unit tests not to print first line of multiline comment by adding empty multiline comment here
        """
        Alternative implementation of scenario 5, using "directional" and B() backpointer method
         _________________        ______________
        |        X        |      |       Y      |
        |_________________|      |______________|
        |                 |      |              |
        |addY(self, y)    |1    *|setX(self, x) |
        |getAllY(self)    |<---->|getX(self)    |
        |removeY(self, y) |      |clearX(self)  |
        |_________________|      |______________|       
        """
        class X:
            def __init__(self):        rm.enforce(
                "xtoy", "onetomany", "directional")

            def addY(self, y):         rm.add_rel(self, y, "xtoy")
            def getAllY(self):  return rm.find_targets(source=self, rel_id="xtoy")
            def removeY(self, y):      rm.remove_rel(self, y, "xtoy")

        class Y:
            def setX(self, x):         rm.add_rel(x, self, "xtoy")
            def getX(self):     return rm.find_source(target=self, rel_id="xtoy")
            def clearX(self):          rm.remove_rel(self.getX(), self, "xtoy")

        x1 = X()
        x2 = X()
        y1 = Y()
        y2 = Y()
        self.onetomanyasserts(x1, x2, y1, y2, yapi=1)


    def onetomanyasserts(self, x1, x2, y1, y2, yapi=0):

        def assertallclear():
            self.assertEqual(x1.getAllY(), [])
            self.assertEqual(x2.getAllY(), [])
            if yapi:
                self.assertIsNone(y1.getX())
                self.assertIsNone(y2.getX())

        def assertSituation00():
            self.assertEqual(x1.getAllY(), [y1])
            if yapi:
                self.assertEqual(y1.getX(), x1)

        # Initial situation
        assertallclear()

        # clearing pointers that do not exist, should be ok.
        x1.removeY(y1)
        assertallclear()
        x1.removeY(y2)
        assertallclear()
        x2.removeY(y1)
        assertallclear()
        x2.removeY(y2)
        assertallclear()
        if yapi:
            y1.clearX()
            assertallclear()
            y2.clearX()
            assertallclear()

        """
        +--------------------------------+
        |Add a single X to Y relationship|
        +--------------------------------+
        """
        x1.addY(y1)
        """
         ,-----.      ,-----.
        (  x1   )--->(  y1   )
         `-----'      `-----'
        """
        assertSituation00()
        # now remove it
        x1.removeY(y1)
        assertallclear()

        # Add initial relationship, from the y side
        if yapi:
            y1.setX(x1)
            assertSituation00()
            # now remove it, from the y side
            y1.clearX()
            assertallclear()

        """
        +--------------------------------------------+
        |Add two relationships coming from a single X|
        |to multiple Y's.                            |
        +--------------------------------------------+
        """
        def assertSituation01():
            """
             ,-----.      ,-----.
            (  x1   )--->(  y1   )
             `-----'.     `-----'
                    |
                     \      ,-----.
                      `--->(  y2   )
                            `-----'
            """
            # this way of testing is dependent on a certain order which sometimes fails: self.assertEqual(x1.getAllY(), [y1, y2], "Actual situation %s" % x1.getAllY())
            self.assertEqual(len(x1.getAllY()), 2)
            self.assertIn(y1, x1.getAllY())
            self.assertIn(y2, x1.getAllY())
            if yapi:
                self.assertEqual(y1.getX(), x1)
                self.assertEqual(y2.getX(), x1)

        def assertSituation02():
            """
             ,-----.      ,-----.
            (  x1   )    (  y1   )
             `-----'.     `-----'
                    |
                     \      ,-----.
                      `--->(  y2   )
                            `-----'
            """
            self.assertEqual(x1.getAllY(), [y2])
            if yapi:
                self.assertIsNone(y1.getX())
                self.assertEqual(y2.getX(), x1)
        # Add two relationships, from x API
        x1.addY(y1)
        x1.addY(y2)
        assertSituation01()
        # now remove y1
        x1.removeY(y1)
        assertSituation02()
        # now remove y2
        x1.removeY(y2)
        assertallclear()

        # Add two relationships, from the y api side.
        if yapi:
            assertallclear()
            y1.setX(x1)
            y2.setX(x1)
            assertSituation01()
            # now remove y1
            y1.clearX()
            assertSituation02()
            # now remove y1
            y2.clearX()
            assertallclear()

        """
        +---------------------------+
        |Add same relationship twice|
        +---------------------------+
        """
        def assertSituation03():
            self.assertEqual(x1.getAllY(), [y1])
            if yapi:
                self.assertEqual(y1.getX(), x1)

        def assertSituation04():
            # this way of testing is dependent on a certain order which sometimes fails: self.assertEqual(x1.getAllY(), [y1, y2])
            self.assertEqual(len(x1.getAllY()), 2)
            self.assertIn(y1, x1.getAllY())
            self.assertIn(y2, x1.getAllY())
            if yapi:
                self.assertEqual(y2.getX(), x1)

        def assertSituation05():
            if yapi:
                self.assertIsNone(y1.getX())
            self.assertEqual(x1.getAllY(), [y2])
        x1.addY(y1)
        x1.addY(y1)
        """
         ,-----.      ,-----.
        (  x1   )--->(  y1   )
         `-----'      `-----'

                        ,-----.
                       (  y2   )
                        `-----'        
        """
        assertSituation03()

        x1.addY(y2)
        x1.addY(y2)
        """
         ,-----.      ,-----.
        (  x1   )--->(  y1   )
         `-----' `.   `-----'
                   `-.
                      `>,-----.
                       (  y2   )
                        `-----'
        """
        assertSituation04()
        # now remove y1 (again, twice, just to check robustness)
        x1.removeY(y1)
        x1.removeY(y1)
        """
         ,-----.      ,-----.
        (  x1   )--->(  y1   )
         `-----'      `-----'

                        ,-----.
                       (  y2   )
                        `-----'        
        """
        assertSituation05()
        # now remove y2 twice
        x1.removeY(y2)
        x1.removeY(y2)

        assertallclear()

        """
        +----------------------------------------+
        |Add same relationship twice, from Y side|
        +----------------------------------------+
        """
        if yapi:
            y1.setX(x1)
            y1.setX(x1)
            """
             ,-----.      ,-----.
            (  x1   )--->(  y1   )
             `-----'      `-----'

                            ,-----.
                           (  y2   )
                            `-----'        
            """
            assertSituation03()
            y2.setX(x1)
            y2.setX(x1)
            """
             ,-----.      ,-----.
            (  x1   )--->(  y1   )
             `-----' `.   `-----'
                       `-.
                          `>,-----.
                           (  y2   )
                            `-----'
            """
            assertSituation04()
            # now remove y1, from Y side (again, twice, just to check robustness)
            y1.clearX()
            y1.clearX()
            """
             ,-----.      ,-----.
            (  x1   )--->(  y1   )
             `-----'      `-----'

                            ,-----.
                           (  y2   )
                            `-----'        
            """
            assertSituation05()
            # now remove y2 twice, from Y side
            y2.clearX()
            y2.clearX()

            assertallclear()

        """
        +----------------------------------------------------+
        |Add two relationships, then add a third             |
        |relationship which effects an previous relationship.|
        +----------------------------------------------------+
        """
        # Make x1 -> y1,y2
        assertallclear()
        x1.addY(y1)
        x1.addY(y2)
        """
          ,-----.      ,-----.
         (  x1   )--->(  y1   )
          `-----' `.   `-----'
                    `-.
            ,-----.    `>,-----.
           (  x2   )    (  y2   )
            `-----'      `-----'
        """
        # Now make x2 -> y1
        x2.addY(y1)
        """
         ,-----.        ,-----.
        (  x1   )     >(  y1   )
         `-----' `. ,'  `-----'
                   /-.
           ,-----,'   `>,-----.
          (  x2   )    (  y2   )
           `-----'      `-----'        
        After much thought, I believe the addition of the x2 -> y1 relationship
         should extinguish the existing x1 -> y1 since y's can only be pointed to by one x.
        If you want to keep the existing x1 -> y1 then you actually are describing the
         many to many, directional, no y api, scenario.        
        """
        self.assertEqual(x1.getAllY(), [y2])
        self.assertEqual(x2.getAllY(), [y1])
        if yapi:
            self.assertEqual(y1.getX(), x2)
            self.assertEqual(y2.getX(), x1)

        x1.removeY(y2)
        x2.removeY(y1)
        assertallclear()

        """
        +---------------------------------------------------+
        |Two different X's point to the same Y.             |
        |Again enforcement that y only pointed to by one X, |
        |and that the original relationship is extinguished.|
        +---------------------------------------------------+
        """
        def assertSituation06():
            self.assertEqual(x1.getAllY(), [])
            self.assertEqual(x2.getAllY(), [y1])
            if yapi:
                self.assertEqual(y1.getX(), x2)

        x1.addY(y1)
        """
         ,-----.      ,-----.
        (  x1   )--->(  y1   )
         `-----'      `-----'
          ,-----.
         (  x2   )
          `-----'
        """
        x2.addY(y1)
        """
         ,-----.      ,-----.
        (  x1   )  .>(  y1   )
         `-----'   |  `-----'
          ,-----.  |
         (  x2   --+
          `-----'        
        """
        assertSituation06()

        x2.removeY(y1)
        assertallclear()

        # Same as above, except wired via Y's API
        if yapi:
            y1.setX(x1)
            y1.setX(x2)
            assertSituation06()
            y1.clearX()
            assertallclear()

        assertallclear()


def suite():
    # This suite only gets used by an explicit test runner when executing this file as a program
    # For CLI unit test discovery launching, use 'python -m unittest tests.test_rm'
    suite1 = unittest.makeSuite(TestCase01_OneToOne, 'test')
    suite2 = unittest.makeSuite(TestCase02_OneToMany, 'test')
    alltests = unittest.TestSuite((suite1, suite2))
    return alltests


def _suite():
    # test just one test
    suite = unittest.makeSuite(
        TestCase02_OneToMany, 'test_OneToMany_XPluralApi_YSingularApi_Alt')
    alltests = unittest.TestSuite((suite,))
    return alltests


def main():
    """ Run all the suites.  To run via a gui, then
            python unittestgui.py NestedDictionaryTest.suite
        Note that I run with VERBOSITY on HIGH  :-) just like in the old days
        with pyUnit for python 2.0
        Simply call
          runner = unittest.TextTestRunner(descriptions=0, verbosity=2)
        The default arguments are descriptions=1, verbosity=1
    """
    runner = unittest.TextTestRunner(
        descriptions=0, verbosity=2)  # default is descriptions=1, verbosity=1
    # runner = unittest.TextTestRunner(descriptions=0, verbosity=1) # default is descriptions=1, verbosity=1
    runner.run(suite())


if __name__ == '__main__':
    main()
