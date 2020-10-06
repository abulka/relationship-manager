namespace UnitTestRm02

import RelationshipManager56

import System
import System.Collections
import NUnit.Framework
//import unittest, random, time

[TestFixture]
class SampleFixture:
	
	[Test]
	def PassTest():
		assert 1 == 1
		assert true == true
		assert "McDonalds sucks!" == "McDonalds sucks!"

[TestFixture]
class LowLevelRm_TestCase01:
	
	public rm as EfficientRelationshipManager
	
	[SetUp]
	def SetUp():		
		self.rm = EfficientRelationshipManager()
		
	[Test]
	def checkBasic00():
		self.rm.AddRelationship('a','b')
		self.rm.AddRelationship('a','c')

		result = self.rm.FindObjects('a',null)
		assert result == ['b','c'] or result == ['c','b']
		assert self.rm.FindObjects(null,'a') == []
		assert self.rm.FindObjects(null,'b') == ['a']
		assert self.rm.FindObjects(null,'c') == ['a']
		
	[Test]
	def checkBasic01Singular():
		self.rm.AddRelationship('a','b')
		self.rm.AddRelationship('a','c')
		assert self.rm.FindObject(null,'b') == 'a'
		assert self.rm.FindObject(null,'c') == 'a'

		result = self.rm.FindObject('a',null) # could be 'b' or 'c' - arbitrary
		assert result == 'b' or result == 'c'

[TestFixture]
class LowLevelRm_TestCase02:
	public rm as EfficientRelationshipManager
	[SetUp]
	def SetUp():		
		/*
		A --r1-> B
		A <-r1-- B
		A --r2-> B
		A --r1-> C
		*/
		self.rm = EfficientRelationshipManager()

		self.rm.AddRelationship('a','b', 'r1')
		self.rm.AddRelationship('a','b', 'r2')

		self.rm.AddRelationship('b','a', 'r1')

		self.rm.AddRelationship('a','c', 'r1')
		
	[Test]
	def checkIfRelIdIsWorking01():
		result = self.rm.FindObject('a',null,'r1') # could be 'b' or 'c' - arbitrary
		assert result == 'b' or result == 'c'

		assert self.rm.FindObject('a',null, 'r2') == 'b'
		assert self.rm.FindObject('a',null, 'r3') == null

		assert self.rm.FindObject(null,'b', 'r1') == 'a'
		assert self.rm.FindObject(null,'b', 'r2') == 'a'


		assert self.rm.FindObject(null,'c') != 'a' # default relationshipid is integer 1 which is not the string 'r1' nor is it 'r2'
		assert self.rm.FindObject(null,'c','r1') == 'a'

	[Test]
	def checkMultipleReturns01():
		#assert self.rm.FindObjects('a',null,'r1').sort() == ['b', 'c']
		res as Boo.Lang.List
		res = self.rm.FindObjects('a',null,'r1')
		res.Sort()
		assert res == ['b', 'c']

		assert self.rm.FindObjects(null,'b','r1') == ['a']
		assert self.rm.FindObjects(null,'b') == []  # cos no relationships with id integer 1 have been created

		ok = false
		try:
		  assert self.rm.FindObjects(null,null) == []   # invalid - must specify at least either from or to
		except RuntimeError:
		  ok = true
		assert ok

	[Test]
	def checkNonExistent01():
		assert self.rm.FindObjects('aa',null,'r1') == []
		assert self.rm.FindObjects('a',null,'r1111') == []
		assert self.rm.FindObjects('az',null,null) == []
		assert self.rm.FindObjects(null,'bb','r1') == []
		assert self.rm.FindObjects(null,'b','r1111') == []
		assert self.rm.FindObjects('a',null,'r1111') == []
		assert self.rm.FindObjects(null,'bb',null) == []

	[Test]
	def FindRelIds_NewFeatureFeb2005_01():
		# ***
		# *** Original behaviour was to return the actual relationship tuples (bad cos implementation dependent!)
		# ***
		# *** New behaviour is to return a boolean.
		# ***
		# When specify both sides of a relationship, PLUS the relationship itself,
		# then there is nothing to find, so return a boolean T/F if that relationship exists.
		#
		//assert self.rm.FindObjects('a','b','r1') == true
		assert self.rm.DoesRelIdExistBetween('a','b','r1') == true
		//assert self.rm.FindObjects('a','b','r2') == true
		assert self.rm.DoesRelIdExistBetween('a','b','r2') == true
		//assert self.rm.FindObjects('a','b','zzz') == false
		assert self.rm.DoesRelIdExistBetween('a','b','zzz') == false

		/*
		This next one is a bit subtle - we are in fact specifying all parameters, because the
		default relId is integer 1 (allowing you to create simple relationships easily).
		Thus the question we are asking is "is there a R of type 'integer 1' between a and b?"
		*/
		//assert self.rm.FindObjects('a','b') == false # cos no relationships with id integer 1 have been created
		assert self.rm.DoesRelIdExistBetween('a','b') == false # cos no relationships with id integer 1 have been created

	[Test]
	def FindRelIds_NewFeatureFeb2005_02():
		# ***
		# *** Original behaviour was to return the actual relationship tuples (bad cos implementation dependent!)
		# ***
		# *** New behaviour is to return a list of the relationship ids.
		# ***
		# When specify both sides of the relationship but leave the relationship None, you get a list of the relationships.
		#
		//assert self.rm.FindObjects('a','b',null) == ['r1', 'r2']
		assert self.rm.FindRelIdsBetween('a','b') == ['r1', 'r2']
		

	[Test]
	def checkRemoval_01():
		# Specify wildcard RelId
		/*
		assert self.rm.FindObjects('a','b',null) == ['r1', 'r2']
		assert self.rm.FindObjects('a','b','r1') == true
		assert self.rm.FindObjects('a','b','r2') == true
		self.rm.RemoveRelationships('a','b',null)  # remove all R's between a and b
		assert self.rm.FindObjects('a','b',null) == [] //, 'Getting ' + str(self.rm.FindObjects('a','b',null))
		assert self.rm.FindObjects('a','b','r1') == false
		assert self.rm.FindObjects('a','b','r2') == false
		*/
		assert self.rm.FindRelIdsBetween('a','b') == ['r1', 'r2']
		assert self.rm.DoesRelIdExistBetween('a','b','r1') == true
		assert self.rm.DoesRelIdExistBetween('a','b','r2') == true
		self.rm.RemoveRelationships('a','b',null)  # remove all R's between a and b
		assert self.rm.FindRelIdsBetween('a','b') == [] //, 'Getting ' + str(self.rm.FindObjects('a','b',null))
		assert self.rm.DoesRelIdExistBetween('a','b','r1') == false
		assert self.rm.DoesRelIdExistBetween('a','b','r2') == false

	[Test]
	def checkRemoval_02():
		# Specify all params
		/*
		self.rm.RemoveRelationships('a','b','r1')
		assert self.rm.FindObjects('a','b',null) == ['r2']
		assert self.rm.FindObjects('a','b','r1') == false
		assert self.rm.FindObjects('a','b','r2') == true
		*/
		self.rm.RemoveRelationships('a','b','r1')
		assert self.rm.FindRelIdsBetween('a','b') == ['r2']
		assert self.rm.DoesRelIdExistBetween('a','b','r1') == false
		assert self.rm.DoesRelIdExistBetween('a','b','r2') == true

	[Test]
	def checkRemoval_03():
		# Specify 'from' param
		/*
		assert self.rm.FindObjects('a','b','r1') == true
		assert self.rm.FindObjects('a','b','r2') == true
		assert self.rm.FindObjects('a','c','r1') == true
		self.rm.RemoveRelationships('a',null,'r1')
		assert self.rm.FindObjects('a','b','r1') == false # zapped
		assert self.rm.FindObjects('a','b','r2') == true
		assert self.rm.FindObjects('a','c','r1') == false # zapped

		assert self.rm.FindObject(null,'b','r1') == null
		assert self.rm.FindObject(null,'b','r2') == 'a'
		assert self.rm.FindObject(null,'c',null) == null
		*/
		
		assert self.rm.DoesRelIdExistBetween('a','b','r1') == true
		assert self.rm.DoesRelIdExistBetween('a','b','r2') == true
		assert self.rm.DoesRelIdExistBetween('a','c','r1') == true
		self.rm.RemoveRelationships('a',null,'r1')
		assert self.rm.DoesRelIdExistBetween('a','b','r1') == false # zapped
		assert self.rm.DoesRelIdExistBetween('a','b','r2') == true
		assert self.rm.DoesRelIdExistBetween('a','c','r1') == false # zapped

		assert self.rm.FindObject(null,'b','r1') == null
		assert self.rm.FindObject(null,'b','r2') == 'a'
		assert self.rm.FindObject(null,'c',null) == null
	
	[Test]
	def checkRemoval_04():
		# Specify 'to' param
		assert self.rm.DoesRelIdExistBetween('a','b','r1') == true
		assert self.rm.DoesRelIdExistBetween('a','b','r2') == true
		assert self.rm.DoesRelIdExistBetween('a','c','r1') == true
		self.rm.RemoveRelationships(null,'b','r1')
		assert self.rm.DoesRelIdExistBetween('a','b','r1') == false # zapped
		assert self.rm.DoesRelIdExistBetween('a','b','r2') == true
		assert self.rm.DoesRelIdExistBetween('a','c','r1') == true

		self.rm.RemoveRelationships(null,'c','r1')
		assert self.rm.DoesRelIdExistBetween('a','b','r2') == true
		assert self.rm.DoesRelIdExistBetween('a','c','r1') == false # zapped

		self.rm.RemoveRelationships(null,'b','r2')
		assert self.rm.DoesRelIdExistBetween('a','b','r2') == false # zapped
		assert self.rm.DoesRelIdExistBetween('a','c','r1') == false

[TestFixture]
class LowLevelRm_TestCase03:
	
	public rm as EfficientRelationshipManager
	
	private THINGS as string = "abcdefghijk" 										 # ori takes 4.6	   efficient1 takes 0.38  boo version 0.015625 seconds
	//private THINGS as string = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJLMNOPQRSTUVWXYZ" # ori takes MINUTES   efficient1 takes 1.7
	//private THINGS as string = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJLMNOPQRSTUVWXYZ1234567890!@#$%^&*()_-=+|}{][;:'><.,`~"
	
	[SetUp]
	def SetUp():		
		//
		//Lots of relationsips. Check the speed.
		//
		self.rm = EfficientRelationshipManager()

		for c in self.THINGS:
			for c2 in self.THINGS:
				self.rm.AddRelationship(c,c2,'r1')
				self.rm.AddRelationship(c,c2,'r2')
				self.rm.AddRelationship(c2,c,'r3')

	[Test]
	def checkSpeed01():
		t as DateTime = DateTime.Now
		
		for c in self.THINGS:
			for c2 in self.THINGS:
				assert c2 in self.rm.FindObjects(c,null,'r1')
				assert c2 in self.rm.FindObjects(c,null,'r2')
				assert c in self.rm.FindObjects(c2,null,'r3')

		timetook as TimeSpan = DateTime.Now -t
		#print "Relationship lookups took", timetook.TotalSeconds, 'seconds'

		assert timetook.TotalSeconds < 0.05, ('Relationship manager not fast enough! timetook={0} TotalMilliseconds={1} TotalSeconds={2}' % (timetook.ToString(),timetook.TotalMilliseconds,timetook.TotalSeconds))

[TestFixture]
class LowLevelRm_TestCase04:
	
	public rm as EfficientRelationshipManager
	//public rm as RelationshipMgrTurbo //RelationshipManager
	
	[SetUp]
	def SetUp():		
		/*
		A --r1-> B
		A --r1-> B   # attempt to add a second R of the same type
		A --r2-> B
		A --r1-> C
		*/
		self.rm = EfficientRelationshipManager()
		//self.rm = RelationshipMgrTurbo()

		self.rm.AddRelationship('a','b', 'r1')
		self.rm.AddRelationship('a','b', 'r1')
		self.rm.AddRelationship('a','b', 'r2')
		self.rm.AddRelationship('a','c', 'r1')
		
	[Test]
	def checkDuplicates01():
		assert self.rm.DoesRelIdExistBetween('a','b','r1') == true # [('a', 'b', 'r1')]
		assert self.rm.FindRelIdsBetween('a','b') == ['r1','r2']
		assert self.rm.DoesRelIdExistBetween('a','c','r1') == true # [('a', 'c', 'r1')]
		assert self.rm.FindRelIdsBetween('a','c') == ['r1']
		
[TestFixture]
class LowLevelRm_TestCase05:
	
	public rm as EfficientRelationshipManager
	
	[SetUp]
	def SetUp():
		/*
		Check getting and setting the 'Relationships' property, which,
		despite the implementation, should look the same.
		In the original RM the property is actually accessed directly (naughty)
		and the implementation is the same as the spec, namely a list of tuples (from,to,relid)

		A --r1-> B
		A --r2-> B
		A --r1-> C
		B --r1-> A
		C --r9-> B
		*/
		self.rm = EfficientRelationshipManager()

		self.rm.AddRelationship('a','b', 'r1')
		self.rm.AddRelationship('a','b', 'r2')
		self.rm.AddRelationship('a','c', 'r1')
		self.rm.AddRelationship('b','a', 'r1')
		self.rm.AddRelationship('c','b', 'r9')
		
	[Test]
	def checkGet01():
		r = self.rm.Relationships
		#assert r == [('a', 'b', 'r1'), ('a', 'b', 'r2'), ('a', 'c', 'r1'), ('b', 'a', 'r1'), ('c', 'b', 'r9')]
		assert len(r) == 5
		/*
		assert ('a', 'b', 'r1') in r
		assert ('a', 'b', 'r2') in r
		assert ('a', 'c', 'r1') in r
		assert ('b', 'a', 'r1') in r
		assert ('c', 'b', 'r9') in r
		*/
		x = ('a', 'b', 'r1'); assert x in r
		x = ('a', 'b', 'r2'); assert x in r
		x = ('a', 'c', 'r1'); assert x in r
		x = ('b', 'a', 'r1'); assert x in r
		x = ('c', 'b', 'r9'); assert x in r
		
	[Test]
	def checkSet01():
		r = [('a', 'b', 'r1'), ('a', 'b', 'r2'), ('a', 'c', 'r1'), ('b', 'a', 'r1'), ('c', 'b', 'r9')]
		newrm = EfficientRelationshipManager()
		newrm.Relationships = r

		assert self.rm.DoesRelIdExistBetween('a','b','r1') == true
		assert self.rm.DoesRelIdExistBetween('a','b','r2') == true
		assert self.rm.DoesRelIdExistBetween('a','c','r1') == true
		assert self.rm.DoesRelIdExistBetween('b','a','r1') == true
		assert self.rm.DoesRelIdExistBetween('c','b','r9') == true
