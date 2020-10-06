namespace UnitTestRm07

import RelationshipManager55
import System
import System.Collections
import NUnit.Framework

import UnitTestRm02  # for BO class

class X(BO):
    def constructor():
        RM.ER("xtoy", "onetomany", "bidirectional")
    def addY(y):
        RM.R(self, y, "xtoy")
    def getAllY():
        return RM.PS(self, "xtoy")
    def removeY(y):
        RM.NR(self, y, "xtoy")
            
class Y(BO):
    ##  def setX(x):         RM.R(self, x, "xy")
    def setX(x):
        RM.R(x, self, "xtoy")  # though bi, there is still a direction!
    def getX():
        return RM.P(self, "xtoy")
    def clearX():
        RM.NR(self, self.getX(), "xtoy")
            
            
[TestFixture]
class TestCase01_OneToOne7:

    private RM as RM1
    private compareUtil as UnittestCompareStuffUtility

    [SetUp]
    def SetUp():
        BO.SetRm(RM1())
        self.compareUtil = UnittestCompareStuffUtility()
        
    [Test]
    def checkOneToMany_XPluralApi_YSingularApi():
    """
    One to Many, BI
    
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
        x1 = X()
        x2 = X()
        y1 = Y()
        y2 = Y()
        self.compareUtil.onetomanyasserts(x1,x2,y1,y2,true)

