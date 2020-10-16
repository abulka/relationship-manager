namespace UnitTestRm05

import RelationshipManager.Interfaces

import System
import System.Collections
import NUnit.Framework

import UnitTestRm02  # for BO class, and for UnittestCompareStuffUtility

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
	def constructor():
		RM.ER("xtoy", Cardinality.OneToOne, Directionality.DirectionalWithBackPointer)
	def setX(x):
		RM.R(x, self, "xtoy")
	def getX():
		return RM.B(self, "xtoy")
	def clearX():
		RM.NR(self.getX(), self, "xtoy")
		


[TestFixture]
class TestCase01_OneToOne5:

	private RM as IRM
	private compareUtil = UnittestCompareStuffUtility()

	[SetUp]
	def SetUp():
		BO.SetRm(RmFactory.GetRM())
		
	[Test]
	def OneToOne_XSingularApi_YSingularApi_Alt():
	"""
	Alternative implementation of same API.
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

		x1 = X()
		x2 = X()
		y1 = Y()
		y2 = Y()
		self.compareUtil.onetooneasserts(x1,x2,y1,y2)
	
