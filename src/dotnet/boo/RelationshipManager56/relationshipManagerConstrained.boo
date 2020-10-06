namespace RelationshipManager56
import System
import System.Collections  # for IList
import RelationshipManager.Interfaces

/*
		Relationship manager revisited.
		Version 1.5
		Boo .NET 2.0 port
		Jan 2006. 
		(c) Andy Bulka
		http://www.atug.com/andypatterns
		
		  ____	    _	    _   _			      _	    _
		 |  _ \ ___| | __ _| |_(_) ___  _ __  ___| |__ (_)_ __
		 | |_) / _ \ |/ _` | __| |/ _ \| '_ \/ __| '_ \| | '_ \
		 |  _ <  __/ | (_| | |_| | (_) | | | \__ \ | | | | |_) |
		 |_| \_\___|_|\__,_|\__|_|\___/|_| |_|___/_| |_|_| .__/
														 |_|
		  __  __
		 |  \/  | __ _ _ __   __ _  __ _  ___ _ __
		 | |\/| |/ _` | '_ \ / _` |/ _` |/ _ \ '__|
		 | |  | | (_| | | | | (_| | (_| |  __/ |
		 |_|  |_|\__,_|_| |_|\__,_|\__, |\___|_|
								   |___/
		
*/


class RelationshipManagerConstrained(IRelationshipManager):
"""
	The Constrained relationship manager is the recommended interface
	to relationship manager.
	
	You don't need to call EnforceRelationship() if you don't want to.
	
	The cardinality options are (Cardinality.OneToOne, "onetomany").  The default is
	no enforcement of cardinality.  The result
	of breaking these rules is simple overwrite behaviour (no exceptions are raised).
	In other words, if you have a "onetotone" enforcement then try to break it by
	trying to create a one to many, then the new relationship will simply replace 
	the old one, thus maintaining the constraint of one to one.
	
	The directionality options are (Directionality.DirectionalWithBackPointer, Directionality.DoubleDirectional).  The default is
	Directionality.DirectionalWithBackPointer.  Directionality.DoubleDirectional automatically adds a second relationship of 
	the same relId in the reverse direction.  Thus you get two relationships for every
	call to AddRelationship().  Similarly, when removing relationships, 
	two relationships are removed for every call to RemoveRelationship().
	
	Note that the ability to use the backpointer feature of relationship manager
	i.e. calling FindObjectsPointingToMe() is not affected by the directionality
	setting.  You can always get the backpointer, no matter what what the direction
	of the relationship is.  Why bother with Directionality.DoubleDirectional then?  Well you may
	prefer to formalise you relationships and make things explicit, rather than
	relying on the magic powers of the relationship manager engine.  Thus in a 
	bidirectional situation you would not need to call for the backpointer, 
	you would instead ask for the appropriate official forward pointer 
	(two official forward pointers exist, remember).
"""
	private rm as EfficientRelationshipManager
	private constraints as Hash
	private useEnforcement = true   // makes things slower, though.  50% slower!
	
	def constructor():
		self.rm = EfficientRelationshipManager()
		self.constraints = {}

	public def UseCache(flag):
		self.rm.UseCache(flag)

	public def UseEnforcement(flag):
		self.useEnforcement = flag

	private def ValidateEnums(cardinality as Cardinality, directionality as Directionality):
		assert directionality in (Directionality.DirectionalWithBackPointer, Directionality.DoubleDirectional)
		assert cardinality in (Cardinality.OneToOne, Cardinality.OneToMany)
		
	private def ExtinguishOldFrom(toObj, relId as string):
		oldFrom = self.FindObjectPointingToMe(toObj, relId)
		self.RemoveRelationship(oldFrom, toObj, relId)
		
	private def ExtinguishOldTo(fromObj, relId as string):
		oldTo = self.FindObjectPointedToByMe(fromObj, relId)
		self.RemoveRelationship(fromObj, oldTo, relId)

	private def _RemoveExistingRelationships(fromObj, toObj, relId as string):
		if relId in self.constraints.Keys:
			cardinality as Cardinality, directionality = self.constraints[relId]
			self.ValidateEnums(cardinality, directionality)
			if cardinality == Cardinality.OneToOne:
				ExtinguishOldFrom(toObj, relId)
				ExtinguishOldTo(fromObj, relId)
			elif cardinality == Cardinality.OneToMany: # and directionality == Directionality.DirectionalWithBackPointer:
				ExtinguishOldFrom(toObj, relId)

	def EnforceRelationship(relId as string, cardinality as Cardinality):
	"""
		directionality is either Directionality.DirectionalWithBackPointer or Directionality.DoubleDirectional
		cardinality is either "onetoone" or "onetomany".  "manytomany" is not supported (yet?).
	"""
		self.EnforceRelationship(relId, cardinality, Directionality.DirectionalWithBackPointer)
		
	def EnforceRelationship(relId as string, cardinality as Cardinality, directionality as Directionality):
	"""
		directionality is either Directionality.DirectionalWithBackPointer or Directionality.DoubleDirectional
		cardinality is either "onetoone" or "onetomany".  "manytomany" is not supported (yet?).
	"""
		self.constraints[relId] = (cardinality, directionality)
		
	def AddRelationship(fromObj, toObj):
		self.AddRelationship(fromObj, toObj, "")
		
	def AddRelationship(fromObj, toObj, relId as string):
		if self.useEnforcement:
			self._RemoveExistingRelationships(fromObj, toObj, relId)  // slow
		self.rm.AddRelationship(fromObj, toObj, relId)

		if relId in self.constraints.Keys:
			cardinality as Cardinality, directionality as Directionality = self.constraints[relId]
			self.ValidateEnums(cardinality, directionality)
			if directionality == Directionality.DoubleDirectional:
				self.rm.AddRelationship(toObj, fromObj, relId)
		
	def FindObjectPointedToByMe(fromObj, relId as string):
		return self.rm.FindObject(fromObj, null, relId)
		
	def FindObjectPointingToMe(toObj, relId as string):
		return self.rm.FindObject(null, toObj, relId)

	def FindObjectsPointedToByMe(fromObj, relId as string):
		return self.rm.FindObjects(fromObj, null, relId)

	def FindObjectsPointingToMe(toObj, relId as string):
	    return self.rm.FindObjects(null, toObj, relId)
    
	def RemoveRelationship(fromObj, toObj, relId as string):
		self.rm.RemoveRelationships(fromObj, toObj, relId)
		
		if relId in self.constraints.Keys:
			cardinality as Cardinality, directionality as Directionality = self.constraints[relId]
			self.ValidateEnums(cardinality, directionality)
			if directionality == Directionality.DoubleDirectional:
				self.rm.RemoveRelationships(toObj, fromObj, relId)

	def RemoveAllRelationshipsInvolving(obj, relId as string):
		list = self.rm.FindObjects(obj, null, relId)
		for o in list:
			self.RemoveRelationship(obj, o, relId)

		list = self.rm.FindObjects(null, obj, relId)
		for o in list:
			self.RemoveRelationship(o, obj, relId)

	def CountRelationships(relId as string):
	"""
	Returns a count of all the relationships matching the given relId 
	in the relationship manager.

	Warning: There will be double the amount of relationships if you are using
	a Directionality.DoubleDirectional relationship i.e. For each AddRelationship() two
	relationships are added (both with the same relId).  One is [from, to]
	and the other is [to, from].
	
	If you want to avoid this, then use a Directionality.DirectionalWithBackPointer relationship.  You
	can still get backpointers using the usual FindObjectsPointingToMe()
	method, even with simple Directionality.DirectionalWithBackPointer relationships.  See the main doco
	on why you would use Directionality.DirectionalWithBackPointer relationships when simple Directionality.DirectionalWithBackPointer
	give you all the facilities you want...
	"""
		return self.rm.CountRelationships(relId)
	
	def Count():
	"""
	<summary>
	Returns a count of all the relationship entries in the relationship manager.
	</summary>

	Warning: There will be double the amount of relationships if you are using
	a Directionality.DoubleDirectional relationship i.e. For each AddRelationship() two
	relationships are added (both with the same relId).  One is [from, to]
	and the other is [to, from].
	
	If you want to avoid this, then use a Directionality.DirectionalWithBackPointer relationship.  You
	can still get backpointers using the usual FindObjectsPointingToMe()
	method, even with simple Directionality.DirectionalWithBackPointer relationships.  See the main doco
	on why you would use Directionality.DirectionalWithBackPointer relationships when simple Directionality.DirectionalWithBackPointer
	give you all the facilities you want...
	"""
		return self.rm.Count()

	def Clear():
		self.rm.Clear()

	public def DoesRelIdExistBetween(From, To, RelId as string) as bool:
		return self.rm.DoesRelIdExistBetween(From, To, RelId)
		
	public def FindRelIdsBetween(From, To) as IList:
		return self.rm.FindRelIdsBetween(From, To)
		
