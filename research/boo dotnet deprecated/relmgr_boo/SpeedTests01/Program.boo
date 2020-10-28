namespace SpeedTests01

import System
import System.Collections
import System.DateTime

import RelationshipManager.Interfaces
import RelationshipManager56
import RelationshipManager.Turbo


def SpeedTest(rm as IRelationshipManager):
	basicTest = false
	removalTest = false
	findCacheTest = false
	onetooneTest = true
	
	if basicTest:
		rm.AddRelationship('a','b', 'r1')
		rm.AddRelationship('a','b', 'r2')
		rm.AddRelationship('a','c', 'r1')
	
	if basicTest:
		for i in range(1,500):
			System.Console.Write(".")
			fromobj = "a"+i
			toobj = 'b'+i
			rm.AddRelationship(fromobj, toobj, 'r3')
			rm.AddRelationship(fromobj, 'b', 'r3')
			rm.AddRelationship('a', toobj, 'r3')
		
			for j in range(1,10):
				rm.AddRelationship(fromobj, toobj, 'r4')
				rm.AddRelationship(fromobj, 'b', 'r4')
				rm.AddRelationship('a', toobj, 'r4')
			
				rm.RemoveRelationship(fromobj, toobj, 'r4')
				rm.RemoveRelationship(fromobj, 'b', 'r4')
				rm.RemoveRelationship('a', toobj, 'r4')

	if removalTest:
		rm.EnforceRelationship('r77', Cardinality.OneToMany)
		for i in range(1,500):
			System.Console.Write(".")
			a = DateTime()
			b = DateTime()
			n = rm.Count()
			rm.AddRelationship('zzzzz', 'qqqq', 'r77')
			rm.AddRelationship(a, b, 'r77')
			rm.AddRelationship(a, 'c', 'r77')
			rm.AddRelationship(b, 'ddd', 'r77')
			rm.AddRelationship(b, 'eee', 'r77')
			rm.AddRelationship(b, 'rrrrr', 'r77')
			rm.AddRelationship(b, 'ggggg', 'r77')
			rm.Count()
			rm.CountRelationships('r77')
			rm.RemoveRelationship(b, 'eee', 'r77')
			rm.RemoveRelationship(b, 'rrrrr', 'r77')
			rm.RemoveRelationship(b, 'ggggg', 'r77')
			rm.RemoveAllRelationshipsInvolving(a, 'r77')
			rm.RemoveAllRelationshipsInvolving(b, 'r77')
			assert rm.Count() > n
			rm.RemoveAllRelationshipsInvolving('zzzzz', 'r77')
			assert rm.Count() == n
		
	
	if basicTest:
		//rm2.EnforceRelationship('relA', Cardinality.OneToMany, Directionality.DoubleDirectional)
		for i in range(1,51):
			System.Console.Write(".")
			for b in range(1,20):
				toobj = 'b'+b
				rm.AddRelationship('a', b, 'relA')
				rm.AddRelationship('a', toobj, 'relA')
				for n in range(1,15):
					list = rm.FindObjectsPointedToByMe('a', 'relA')
					list = rm.FindObjectsPointingToMe(b, 'relA')
					list = rm.FindObjectsPointingToMe(toobj, 'relA')
			for n in range(1,15):
				list = rm.FindObjectsPointedToByMe('b', 'relA')
				list = rm.FindObjectsPointedToByMe('b1', 'relA')
				list = rm.FindObjectsPointedToByMe('b2', 'relA')
				
				o = rm.FindObjectPointingToMe('b', 'relA')
				o = rm.FindObjectPointingToMe('b1', 'relA')
				o = rm.FindObjectPointingToMe('b2', 'relA')
	
			for n in range(1,15):
				list = rm.FindObjectPointedToByMe('b', 'relA')
				list = rm.FindObjectPointedToByMe('b1', 'relA')
				list = rm.FindObjectPointedToByMe('b2', 'relA')

	if findCacheTest:
		rm.AddRelationship('a', 'b', 'rel1')
		rm.AddRelationship('b', 'c', 'rel1')
		rm.AddRelationship('c', 'd', 'rel1')
		rm.AddRelationship('d', 'e', 'rel1')
		rm.AddRelationship('e', 'f', 'rel1')
		for i in range(1,999000):
			if i % 1000 == 0:
				System.Console.Write(".")
			o = rm.FindObjectPointedToByMe('b', 'rel1')
			assert o == 'c'
		
	if onetooneTest:
		System.Console.Write(".")
		rm.EnforceRelationship('r88', Cardinality.OneToOne)
		for i in range(1,200):
			if i % 20 == 0:
				System.Console.Write(".")
			rm.AddRelationship("aaaaaa", "bbbbbb", 'r88')
			o = rm.FindObjectPointedToByMe("aaaaaa", 'r88')
			assert o == "bbbbbb"
			rm.AddRelationship("aaaaaa", "cccccc", 'r88')
			for j in range(1,9999):
				o = rm.FindObjectPointedToByMe("aaaaaa", 'r88')
				assert o == "cccccc"
				o = rm.FindObjectPointingToMe("cccccc", 'r88')
				assert o == "aaaaaa"
				//o = rm.FindObjectPointingToMe("bbbbbb", 'r88')
				//assert o == null
			assert not rm.DoesRelIdExistBetween("aaaaaa", "bbbbbb", 'r88')
			
	print "!"
	print

def PrintPercentFaster(old as double, new as double):
	# =(C2-C1)/C1*100
	result as int
	times as int
	
	if new == old:
		result = 0
		print(old + " to " + new + " = no change")
	elif new < old:
		diff = (old-new)
		times = old/new
		result = diff/new * 100
		print(old + " to " + new + " diff is " + diff + " = " + result + "% or " + times + "x faster ")
	else:
		diff = (new-old)
		times = new/old
		result = diff/old * 100
		print(old + " to " + new + " diff is " + diff + " = " + result + "% or " + times + "x slower")
	return result

print "---- INTRO ----"

PrintPercentFaster(1,2)
PrintPercentFaster(2,1)
print
	
print "---- SPEED TESTS ----"

start = date.Now
SpeedTest(RelationshipManagerConstrained())
duration1 = date.Now - start

start = date.Now
SpeedTest(RelationshipMgrTurbo())
duration2 = date.Now - start

print
print 'RelationshipManagerConstrained', duration1
print 'RelationshipMgrTurbo', duration2
PrintPercentFaster(duration1.Ticks, duration2.Ticks)
print

print 'all done'
Console.ReadLine()
