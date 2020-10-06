namespace UnitTestRm02

import System
import System.Collections

import RelationshipManager56
import RelationshipManager.Interfaces
import RelationshipManager.Turbo

class RmFactory:
	static useTurbo as bool = true
	
	static def GetRelationshipManager():
		if useTurbo:
			return RelationshipManager.Turbo.RelationshipMgrTurbo()
		else:
			return RelationshipManager56.RelationshipManagerConstrained()
		
	static def GetRM():
		if useTurbo:
			return RelationshipManager.Turbo.RM()
		else:
			return RelationshipManager56.RM1()

def SameAs2(self1 as IList, other as IList, other2 as IList) as bool:
	pass
	
def SameAs(self1 as IList, other as IList) as bool:
	if self1 is other:
		//Console.Out.WriteLine("SameAs: IS   :-)")
		return true

	if len(self1) != len(other):
		Console.Out.WriteLine("SameAs FAILS: LIST LENGTH DIFFERENCE!   " + len(self1) + " vs. " + len(other))

		Console.Out.WriteLine("List 1 length " + len(self1))
		for o in self1:
			Console.Out.WriteLine("o id = " + (o.GetHashCode)())

		Console.Out.WriteLine("List 2 length " + len(other))
		for o in other:
			Console.Out.WriteLine("o id = " + (o.GetHashCode)())
			
		return false

	i=0
	while i< len(self1):
		if self1[i] != other[i]:
			//Console.Out.WriteLine("SameAs FAILS: lhs id = " + (self1[i].GetHashCode)() + "  rhs id = " + (other[i].GetHashCode)())
			return false
		++i
	//Console.Out.WriteLine("SameAs: ==   :-)")
	return true 

