import System

interface IDo:
	def Do1()
	def Do2()

class A:
	def Do1():
		pass

class B(A, IDo):
	#def Do1(): # Shouldn't need to implement again since
	#	pass    # Class B inherits Do1() from class A
	def Do2():
		pass

b = B()
print b

print "ok"
