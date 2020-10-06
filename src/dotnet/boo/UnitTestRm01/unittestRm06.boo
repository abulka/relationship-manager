namespace UnitTestRm06

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
	pass

[TestFixture]
class TestCase01_OneToOne6:

	private RM as IRM
	private compareUtil as UnittestCompareStuffUtility

	[SetUp]
	def SetUp():
		BO.SetRm(RmFactory.GetRM())
		self.compareUtil = UnittestCompareStuffUtility()
		
	[Test]
	def checkOneToMany_XPluralApi_YNoApi():
	"""
	One to Many
	
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

		x1 = X()
		x2 = X()
		y1 = Y()
		y2 = Y()
		self.compareUtil.onetomanyasserts(x1,x2,y1,y2)
