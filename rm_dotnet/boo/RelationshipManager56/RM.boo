namespace RelationshipManager56
import System
import RelationshipManager.Interfaces

class RM1(RelationshipManagerConstrained, IRM):
"""
	For compatibility with older tests.
	Shorthand method names
"""
	def ER(relId as string, cardinality as Cardinality):
		self.EnforceRelationship(relId, cardinality)

	def ER(relId as string, cardinality as Cardinality, directionality as Directionality):
		self.EnforceRelationship(relId, cardinality, directionality)

	def R(fromObj, toObj, relId as string):
		self.AddRelationship(fromObj, toObj, relId)

	def PS(fromObj, relId as string):
		return self.FindObjectsPointedToByMe(fromObj, relId)

	def P(fromObj, relId as string):
		return self.FindObjectPointedToByMe(fromObj, relId)

	def BS(toObj, relId as string):
	 	return FindObjectsPointingToMe(toObj, relId)

	def B(toObj, relId as string):
		return self.FindObjectPointingToMe(toObj, relId)

	def NR(fromObj, toObj, relId as string):
		self.RemoveRelationship(fromObj, toObj, relId as string)

	def NRS(obj, relId as string):
		self.RemoveAllRelationshipsInvolving(obj, relId)

	def QR(fromObj, toObj, relId as string) as bool:
		return self.DoesRelIdExistBetween(fromObj, toObj, relId)

	def Count():
		return self.Count()
		
	def CountRelationships(relId as string):
		return self.CountRelationships(relId)
		
	def Clear():
		self.Clear()		
		
