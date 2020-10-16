namespace UnitTestRm02

import RelationshipManager.Interfaces

import System
import System.Collections
import NUnit.Framework

/*
For testing the more advanced, high level RM1 class
*/

class BO:
    static protected RM as IRM
    static public def SetRm(rm):
        RM = rm
    
class X(BO):
    def constructor():
        RM.ER("xtoy", Cardinality.OneToOne, Directionality.DirectionalWithBackPointer)
    def setY(y):
        RM.R(self, y, "xtoy")
    def getY():
        return RM.P(self, "xtoy")
    def clearY():
        RM.NR(self, self.getY(), "xtoy")
    
class Y(BO):
    pass

[TestFixture]
class TestCase01_OneToOne:

    private RM as IRM

    [SetUp]
    def SetUp():
        BO.SetRm(RmFactory.GetRM())
        
    [Test]    
    def OneToOne_XSingularApi_YNoApi():
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
            
        x1 = X()
        x2 = X()
        y1 = Y()
        y2 = Y()
        # Initial situation
        assert x1.getY() == null
        assert x2.getY() == null

        # After clearing pointers
        x1.clearY()
        assert x1.getY() == null
        assert x2.getY() == null
            
        # After setting one pointer, x1 -> y1
        x1.setY(y1)
        assert x1.getY() == y1
        assert x2.getY() == null

        # After setting x2 -> y1, we cannot allow a situation where
        # both x's to point to the same y, since this would be "many to one".
        # The existing x1 -> y1 must be auto deleted by the relationship manager
        # relationship enforcer.
        assert x1.getY() == y1
        x2.setY(y1)
        assert x1.getY() == null  # relationship should have been auto removed
        assert x2.getY() == y1

        # Clear one pointer
        x1.clearY()
        assert x1.getY() == null
        assert x2.getY() == y1
            
        # Clear other pointer
        x2.clearY()
        assert x1.getY() == null
        assert x2.getY() == null

        # Change from pointing to one thing then point to another
        x1.setY(y1)
        x1.setY(y2)
        assert x1.getY() == y2
            
        # Ensure repeat settings do not disturb things
        x1.clearY()
        x2.clearY()
        # x1 -> y1, x2 -> null
        x1.setY(y1)
        assert x1.getY() == y1
        assert x2.getY() == null
        # repeat
        x1.setY(y1)
        assert x1.getY() == y1
        assert x2.getY() == null
        
        # x1 -> null, x2 -> y1
        x2.setY(y1)
        assert x1.getY() == null
        assert x2.getY() == y1
        # repeat
        x2.setY(y1)
        assert x1.getY() == null
        assert x2.getY() == y1
        
        # x1 -> y2, x2 -> y1
        x1.setY(y2)
        assert x1.getY() == y2
        assert x2.getY() == y1
        # repeat
        x1.setY(y2)
        assert x1.getY() == y2
        assert x2.getY() == y1



class UnittestCompareStuffUtility:
    
    def assertallclear(x1 as duck, x2 as duck, y1 as duck, y2 as duck):
        assert x1.getY() == null
        assert x2.getY() == null
        assert y1.getX() == null
        assert y2.getX() == null

    def onetooneasserts(x1 as duck, x2 as duck, y1 as duck, y2 as duck):
        
        # Initial situation
        assertallclear(x1, x2, y1, y2)

        # After clearing pointers
        x1.clearY()
        x2.clearY()
        y1.clearX()
        y2.clearX()
        assertallclear(x1, x2, y1, y2)

        # After setting one pointer, x1 <-> y1
        x1.setY(y1)
        assert x1.getY() == y1
        assert x2.getY() == null
        
        assert y1.getX() == x1
        assert y2.getX() == null

        # After clearing that one pointer, x1 <-> y1
        x1.clearY()
        assertallclear(x1, x2, y1, y2)

        # After setting one pointer, via y API, x1 <-> y1
        y1.setX(x1)
        assert x1.getY() == y1
        assert x2.getY() == null
        assert y1.getX() == x1
        assert y2.getX() == null
        y1.clearX()
        assertallclear(x1, x2, y1, y2)

        # After setting one pointer, via y API, x1 <-> y1
        # then change it via x API, to          x1 <-> y2
        # thus the old x1 <-> y1 must extinguish.
        y1.setX(x1)
        x1.setY(y2)
        assert x1.getY() == y2
        assert x2.getY() == null
        assert y1.getX() == null
        assert y2.getX() == x1
        # repeat
        y1.setX(x1)
        x1.setY(y2)
        assert x1.getY() == y2
        assert x2.getY() == null
        assert y1.getX() == null
        assert y2.getX() == x1
        # clear
        x1.clearY()
        assertallclear(x1, x2, y1, y2)
        
        # Do same trick using opposite API's
        x1.setY(y1)                             # instead of y1.setX(x1)
        y2.setX(x1)                             # instead of x1.setY(y2)
        # exactly the same assertions
        assert x1.getY() == y2
        assert x2.getY() == null
        assert y1.getX() == null
        assert y2.getX() == x1
        # repeat
        x1.setY(y1)
        y2.setX(x1)
        assert x1.getY() == y2
        assert x2.getY() == null
        assert y1.getX() == null
        assert y2.getX() == x1

        y2.clearX()
        assertallclear(x1, x2, y1, y2)


        # Wire both x1-y1, x2-y2 using x API
        x1.setY(y1)
        x2.setY(y2)
        assert x1.getY() == y1
        assert x2.getY() == y2
        assert y1.getX() == x1
        assert y2.getX() == x2
        # repeat wiring using opposite Y api, same asserts
        y1.setX(x1)
        y2.setX(x2)
        assert x1.getY() == y1
        assert x2.getY() == y2
        assert y1.getX() == x1
        assert y2.getX() == x2
        # Now set x2-y1 using x API, should yield x1-null, x2-y1
        x2.setY(y1)
        assert x1.getY() == null
        assert x2.getY() == y1
        assert y1.getX() == x2
        assert y2.getX() == null
        # Repeat above set x2-y1 using y API, same asserts
        y1.setX(x2)
        assert x1.getY() == null
        assert x2.getY() == y1
        assert y1.getX() == x2
        assert y2.getX() == null
        # Now set x1-y2, using y API, should yield x1-y2, x2-y1
        y2.setX(x1)
        assert x1.getY() == y2
        assert x2.getY() == y1
        assert y1.getX() == x2
        assert y2.getX() == x1
        # Repeat above set x1-y2, using x API, same asserts
        x1.setY(y2)
        assert x1.getY() == y2
        assert x2.getY() == y1
        assert y1.getX() == x2
        assert y2.getX() == x1
        
        x1.clearY()
        assert x1.getY() == null
        assert x2.getY() == y1
        assert y1.getX() == x2
        assert y2.getX() == null
        y1.clearX()
        assertallclear(x1, x2, y1, y2)
    
    
    def assertallclear(x1 as duck, x2 as duck, y1 as duck, y2 as duck, yapi as bool):
    """
    	Don't use Assert.Equals() in Boo - I don't know why but the compiler complains.

    	Both ArrayList and Boo.Lang.List inherit from the same interface "IList." 
		How do I compare ArrayLists and lists (Boo.Lang.List) ?  They don't
		seem to be compatible.  THEY AREN'T (yet) see my boo google post at
		http://tinyurl.com/p4q6b
		Workaround: wrap all calls to RM that return IList with List() which
		converts them into python compatible [] lists, which the unit tests use.
    """
        assert SameAs(x1.getAllY(), [])
        assert SameAs(x2.getAllY(), [])
        if yapi:
            assert y1.getX() == null
            assert y2.getX() == null
            
    def assertSituation00(x1 as duck, x2 as duck, y1 as duck, y2 as duck, yapi as bool):
        assert SameAs(x1.getAllY(), [y1])
        if yapi:
            assert y1.getX() == x1
            
    def assertSituation01(x1 as duck, x2 as duck, y1 as duck, y2 as duck, yapi as bool):
    """
     ,-----.      ,-----.
    (  x1   )--->(  y1   )
     `-----'.     `-----'
            |
             \      ,-----.
              `--->(  y2   )
                    `-----'
    """
        rez = SameAs(x1.getAllY(), [y1, y2]) or SameAs(x1.getAllY(), [y2, y1])
        assert rez, "Actual situation {0} should be {1}" % (x1.getAllY(), [y1, y2])
        if yapi:
            assert y1.getX() == x1
            assert y2.getX() == x1
            
    def assertSituation02(x1 as duck, x2 as duck, y1 as duck, y2 as duck, yapi as bool):
    """
     ,-----.      ,-----.
    (  x1   )    (  y1   )
     `-----'.     `-----'
            |
             \      ,-----.
              `--->(  y2   )
                    `-----'
    """
        assert SameAs(x1.getAllY(), [y2])
        if yapi:
            assert y1.getX() == null
            assert y2.getX() == x1

    def assertSituation03(x1 as duck, x2 as duck, y1 as duck, y2 as duck, yapi as bool):
        assert SameAs(x1.getAllY(), [y1])
        if yapi:
            assert y1.getX() == x1
            
    def assertSituation04(x1 as duck, x2 as duck, y1 as duck, y2 as duck, yapi as bool):
        rez = SameAs(x1.getAllY(), [y1, y2]) or SameAs(x1.getAllY(), [y2, y1])
        assert rez, "assert error"
        if yapi:
            assert y2.getX() == x1
            
    def assertSituation05(x1 as duck, x2 as duck, y1 as duck, y2 as duck, yapi as bool):
        if yapi:
            assert y1.getX() == null
        assert SameAs(x1.getAllY(), [y2])

    def assertSituation06(x1 as duck, x2 as duck, y1 as duck, y2 as duck, yapi as bool):
        assert SameAs(x1.getAllY(), [])
        assert SameAs(x2.getAllY(), [y1])
        if yapi:
            assert y1.getX() == x2


    def onetomanyasserts(x1 as duck, x2 as duck, y1 as duck, y2 as duck):
        self.onetomanyasserts(x1, x2, y1, y2, false)
        
    def onetomanyasserts(x1 as duck, x2 as duck, y1 as duck, y2 as duck, yapi as bool):

        # Initial situation
        assertallclear(x1, x2, y1, y2, yapi)
        # clearing pointers that do not exist, should be ok.
        x1.removeY(y1)
        assertallclear(x1, x2, y1, y2, yapi)
        x1.removeY(y2)
        assertallclear(x1, x2, y1, y2, yapi)
        x2.removeY(y1)
        assertallclear(x1, x2, y1, y2, yapi)
        x2.removeY(y2)
        assertallclear(x1, x2, y1, y2, yapi)
        if yapi:
            y1.clearX()
            assertallclear(x1, x2, y1, y2, yapi)
            y2.clearX()
            assertallclear(x1, x2, y1, y2, yapi)


	    /*
	    +--------------------------------+
	    |Add a single X to Y relationship|
	    +--------------------------------+
	    */
        x1.addY(y1)
        
	    /*
	     ,-----.      ,-----.
	    (  x1   )--->(  y1   )
	     `-----'      `-----'
	    */
        assertSituation00(x1, x2, y1, y2, yapi)
        # now remove it
        x1.removeY(y1)
        assertallclear(x1, x2, y1, y2, yapi)

        # Add initial relationship, from the y side
        if yapi:
            y1.setX(x1)
            assertSituation00(x1, x2, y1, y2, yapi)
            # now remove it, from the y side
            y1.clearX()
            assertallclear(x1, x2, y1, y2, yapi)


        /*
        +--------------------------------------------+
        |Add two relationships coming from a single X|
        |to multiple Y's.                            |
        +--------------------------------------------+
        */

        # Add two relationships, from x API
        x1.addY(y1)
        x1.addY(y2)
        assertSituation01(x1, x2, y1, y2, yapi)
        # now remove y1
        x1.removeY(y1)
        assertSituation02(x1, x2, y1, y2, yapi)
        # now remove y2
        x1.removeY(y2)
        assertallclear(x1, x2, y1, y2, yapi)

        # Add two relationships, from the y api side.
        if yapi:
            assertallclear(x1, x2, y1, y2, yapi)
            y1.setX(x1)
            y2.setX(x1)
            assertSituation01(x1, x2, y1, y2, yapi)
            # now remove y1
            y1.clearX()
            assertSituation02(x1, x2, y1, y2, yapi)
            # now remove y1
            y2.clearX()
            assertallclear(x1, x2, y1, y2, yapi)



        /*
        +---------------------------+
        |Add same relationship twice|
        +---------------------------+
        */
        x1.addY(y1)
        x1.addY(y1)
        
        /*
         ,-----.      ,-----.
        (  x1   )--->(  y1   )
         `-----'      `-----'

                        ,-----.
                       (  y2   )
                        `-----'        
        */
        assertSituation03(x1, x2, y1, y2, yapi)
        
        x1.addY(y2)
        x1.addY(y2)
        
        /*
         ,-----.      ,-----.
        (  x1   )--->(  y1   )
         `-----' `.   `-----'
                   `-.
                      `>,-----.
                       (  y2   )
                        `-----'
        */
        assertSituation04(x1, x2, y1, y2, yapi)
        # now remove y1 (again, twice, just to check robustness)
        x1.removeY(y1)
        x1.removeY(y1)
        
        /*
         ,-----.      ,-----.
        (  x1   )--->(  y1   )
         `-----'      `-----'

                        ,-----.
                       (  y2   )
                        `-----'        
        */
        assertSituation05(x1, x2, y1, y2, yapi)
        # now remove y2 twice
        x1.removeY(y2)
        x1.removeY(y2)

        assertallclear(x1, x2, y1, y2, yapi)
        

        /*
        +----------------------------------------+
        |Add same relationship twice, from Y side|
        +----------------------------------------+
        */
        if yapi:
            y1.setX(x1)
            y1.setX(x1)
            /*
             ,-----.      ,-----.
            (  x1   )--->(  y1   )
             `-----'      `-----'

                            ,-----.
                           (  y2   )
                            `-----'        
            */
            assertSituation03(x1, x2, y1, y2, yapi)
            y2.setX(x1)
            y2.setX(x1)
            /*
             ,-----.      ,-----.
            (  x1   )--->(  y1   )
             `-----' `.   `-----'
                       `-.
                          `>,-----.
                           (  y2   )
                            `-----'
            */
            assertSituation04(x1, x2, y1, y2, yapi)
            # now remove y1, from Y side (again, twice, just to check robustness)
            y1.clearX()
            y1.clearX()
            /*
             ,-----.      ,-----.
            (  x1   )--->(  y1   )
             `-----'      `-----'

                            ,-----.
                           (  y2   )
                            `-----'        
            */
            assertSituation05(x1, x2, y1, y2, yapi)
            # now remove y2 twice, from Y side
            y2.clearX()
            y2.clearX()

            assertallclear(x1, x2, y1, y2, yapi)
        

        /*
        +----------------------------------------------------+
        |Add two relationships, then add a third             |
        |relationship which effects an previous relationship.|
        +----------------------------------------------------+
        */
        # Make x1 -> y1,y2
        assertallclear(x1, x2, y1, y2, yapi)
        x1.addY(y1)
        x1.addY(y2)
        /*
          ,-----.      ,-----.
         (  x1   )--->(  y1   )
          `-----' `.   `-----'
                    `-.
            ,-----.    `>,-----.
           (  x2   )    (  y2   )
            `-----'      `-----'
        */
        # Now make x2 -> y1
        x2.addY(y1)
        /*
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
        */
        assert SameAs(x1.getAllY(), [y2])
        assert SameAs(x2.getAllY(), [y1])
        if yapi:
            assert y1.getX() == x2
            assert y2.getX() == x1

        x1.removeY(y2)
        x2.removeY(y1)
        assertallclear(x1, x2, y1, y2, yapi)
        

        /*
        +---------------------------------------------------+
        |Two different X's point to the same Y.             |
        |Again enforcement that y only pointed to by one X, |
        |and that the original relationship is extinguished.|
        +---------------------------------------------------+
        */

        x1.addY(y1)
        /*
         ,-----.      ,-----.
        (  x1   )--->(  y1   )
         `-----'      `-----'
          ,-----.
         (  x2   )
          `-----'
        */
        x2.addY(y1)
        
        /*
         ,-----.      ,-----.
        (  x1   )  .>(  y1   )
         `-----'   |  `-----'
          ,-----.  |
         (  x2   --+
          `-----'        
        */
        assertSituation06(x1, x2, y1, y2, yapi)

        x2.removeY(y1)
        assertallclear(x1, x2, y1, y2, yapi)


        # Same as above, except wired via Y's API
        if yapi:
            y1.setX(x1)
            y1.setX(x2)
            assertSituation06(x1, x2, y1, y2, yapi)
            y1.clearX()
            assertallclear(x1, x2, y1, y2, yapi)

        assertallclear(x1, x2, y1, y2, yapi)
           
