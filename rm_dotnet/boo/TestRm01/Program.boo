import System
//import System.Collections
import RelationshipManager56
import RelationshipManager.Interfaces

print "Hello, World!"


rm = EfficientRelationshipManager()
print rm
rm.AddRelationship('a','b', 'r1')
rm.AddRelationship('a','b', 'r2')
rm.AddRelationship('a','c', 'r1')
rm.AddRelationship('b','a', 'r1')
rm.AddRelationship('c','b', 'r9')

r = rm.Relationships
assert len(r) == 5
assert 3 > 1

x = ('a', 'b', 'r1'); assert x in r
x = ('a', 'b', 'r2'); assert x in r
x = ('a', 'c', 'r1'); assert x in r
x = ('b', 'a', 'r1'); assert x in r
x = ('c', 'b', 'r9'); assert x in r
        
if ('a', 'b', 'r1') in r:
	print 'ok'
	
/*
assert rm.FindObjects('a','b','r1') == true
assert rm.FindObjects('a','b','r2') == true
assert rm.FindObjects('a','c','r1') == true
assert rm.FindObjects('b','a','r1') == true
assert rm.FindObjects('c','b','r9') == true
*/
assert rm.DoesRelIdExistBetween('a','b','r1')
assert rm.DoesRelIdExistBetween('a','b','r2')
assert rm.DoesRelIdExistBetween('a','c','r1')
assert rm.DoesRelIdExistBetween('b','a','r1')
assert rm.DoesRelIdExistBetween('c','b','r9')


print null

//res as duck

//print "find with relid of null", rm.FindObjects('a','b',null)
print "find with relid of null viz. FindRelIdsBetween", rm.FindRelIdsBetween('a','b')

//print "find with relid of 1", rm.FindObjects('a','b',1)
print "find with relid of 1 viz. DoesRelIdExistBetween", rm.DoesRelIdExistBetween('a','b',1)

print rm.FindObjects('a',null)
print rm.FindObjects(null,'b')	

print rm.FindObjects('a',null,'r1')
print rm.FindObjects(null,'b','r2')	

// -------------------

rm2 = RM1()
print rm2
rm2.ER("xtoy", Cardinality.OneToOne, Directionality.DirectionalWithBackPointer)

print 'all done'

Console.ReadLine()
