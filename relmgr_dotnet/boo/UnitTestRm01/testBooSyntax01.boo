import System.Collections
import System

interface IAA:
	def Do() as IList

class A(IAA):
	public def Do() as IList:
		return ArrayList()

class X:
	_a as A = A()
	def getAllY():
		return _a.Do()

a = A()
print a
print a.Do() == []
print List(a.Do()) == []

x = X()
print x.getAllY()
print x.getAllY() == []

x1 as duck = X()
print x1.getAllY()
print x1.getAllY() == []

print "************"
z = ArrayList()
print List(z) == []
#assert List(z) == []   # CRASH!!


//print Boo.Lang.List(x1.getAllY()) == []
//assert Boo.Lang.List(x1.getAllY()) == []   # CRASH!!

#print List(x1.getAllY()) == []
//print List(x1.getAllY()) == ["y1", "y2"]

zz = ArrayList()
print List(zz) == []
assert List(zz) == []

# .NET 2.0 version is             0.7.5.2013
# The latest command line version 0.7.6.2150
print BooVersion

qq = ArrayList()
qq.Add("hello")
print List(qq) == []
assert List(qq) == ["hello"]
print "List(qq) " + List(qq)

w = qq.GetHashCode
print(w())

w2 = (qq.GetHashCode)()
print w2

Console.Out.WriteLine("id = " + (qq.GetHashCode)())

print "ok"

