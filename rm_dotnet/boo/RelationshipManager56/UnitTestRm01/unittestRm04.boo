namespace UnitTestRm04

import RelationshipManager55
import System
import System.Collections
import NUnit.Framework

import UnitTestRm02  # for BO class, and for UnittestCompareStuffUtility

class X(BO):
	def constructor():
		RM.ER("xy", "onetoone", "bidirectional")
	def setY(y):
		RM.R(self, y, "xy")
	def getY():
		return RM.P(self, "xy")
	def clearY():
		RM.NR(self, self.getY(), "xy")
	
class Y(BO):
	def constructor():
		RM.ER("xy", "onetoone", "bidirectional")
	def setX(x):
		RM.R(self, x, "xy")
	def getX():
		return RM.P(self, "xy")
	def clearX():
		RM.NR(self, self.getX(), "xy")

[TestFixture]
class TestCase01_OneToOne4:

	private RM as RM1
	private compareUtil = UnittestCompareStuffUtility()

	[SetUp]
	def SetUp():
		BO.SetRm(RM1())
		
	[Test]
	def checkOneToOne_XSingularApi_YSingularApi():
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
			
		x1 = X()
		x2 = X()
		y1 = Y()
		y2 = Y()
		self.compareUtil.onetooneasserts(x1,x2,y1,y2)

