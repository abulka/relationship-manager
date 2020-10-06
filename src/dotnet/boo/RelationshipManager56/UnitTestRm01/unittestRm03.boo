namespace UnitTestRm03

import RelationshipManager55
import System
import System.Collections
import NUnit.Framework

import UnitTestRm02

	
class X(BO):
	pass
	
class Y(BO):
	def constructor():
		RM.ER("xtoy", "onetoone", "directional")
	def setX(x):
		RM.R(x, self, "xtoy")
	def getX():
		return RM.B(self, "xtoy")
	def clearX():
		RM.NR(self.getX(), self, "xtoy")

[TestFixture]
class TestCase01_OneToOne3:

	private RM as RM1

	[SetUp]
	def SetUp():
		BO.SetRm(RM1())
		
	[Test]
	def checkOneToOne_XNoApi_YSingularApi():
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

		x1 = X()
		x2 = X()
		y1 = Y()
		y2 = Y()

		# Initial situation
		assert y1.getX() == null
		assert y2.getX() == null

		# After clearing pointers
		y1.clearX()
		assert y1.getX() == null
		assert y2.getX() == null
			
		# After setting one pointer, thus x1 -> y1
		y1.setX(x1)
		assert y1.getX() == x1
		assert y2.getX() == null

		# Want to show two x's pointing to same y
		# Cannot do this since need access to an x api to do the 2nd link
		# but this unit test assumes that the X has no API at all.
		#pass

		# A y can be pointed to by many x's
		# An x can only point at one y at a time
		# So if x1 -> y1 and then x1 -> y2 then y1 is being pointed to by no-one.
		# After setting other pointer, both x's pointing to same y, thus x1 & x2 -> y1
		y2.setX(x1)
		assert y1.getX() == null  # should be auto cleared
		assert y2.getX() == x1

		# Clear one pointer
		y1.clearX()
		assert y1.getX() == null
		assert y2.getX() == x1
			
		# Clear other pointer
		y2.clearX()
		assert y1.getX() == null
		assert y2.getX() == null

		# Change from x1 -> y1 to x2 -> y1 (pointing to one thing then point to another)
		y1.clearX()
		y2.clearX()
		y1.setX(x1)
		y1.setX(x2)
		assert y1.getX() == x2
		assert y2.getX() == null

		# Ensure repeat settings do not disturb things
		y1.clearX()
		y2.clearX()
		y1.setX(x1)
		assert y1.getX() == x1
		assert y2.getX() == null
		# repeat
		y1.setX(x1)
		assert y1.getX() == x1
		assert y2.getX() == null


