namespace UnitTestRm08

import RelationshipManager.Interfaces

import System
import System.Collections
import NUnit.Framework

import UnitTestRm02  # for BO class

          
class X(BO):
    def constructor():
        RM.ER("xtoy", Cardinality.OneToMany, Directionality.DirectionalWithBackPointer)
    def addY(y):
        RM.R(self, y, "xtoy")
    def getAllY():
        return RM.PS(self, "xtoy")
    def removeY(y):
        RM.NR(self, y, "xtoy")
            
class Y(BO):
    def setX(x):
        RM.R(x, self, "xtoy")
    def getX():
        return RM.B(self, "xtoy")
    def clearX():
        RM.NR(self.getX(), self, "xtoy")
              
            
[TestFixture]
class TestCase01_OneToOne8:

    private RM as IRM
    private compareUtil as UnittestCompareStuffUtility

    [SetUp]
    def SetUp():
        BO.SetRm(RmFactory.GetRM())
        self.compareUtil = UnittestCompareStuffUtility()
        
    [Test]
    def OneToMany_XPluralApi_YSingularApi_Alt():
    """
    Alternative implentation, using Directionality.DirectionalWithBackPointer and B()
     _________________        ______________
    |        X        |      |       Y      |
    |_________________|      |______________|
    |                 |      |              |
    |addY(self, y)    |1    *|setX(self, x) |
    |getAllY(self)    |<---->|getX(self)    |
    |removeY(self, y) |      |clearX(self)  |
    |_________________|      |______________|
    
    """

        x1 = X()
        x2 = X()
        y1 = Y()
        y2 = Y()
        self.compareUtil.onetomanyasserts(x1,x2,y1,y2,true)

    
