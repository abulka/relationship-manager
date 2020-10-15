namespace RelationshipManager56

import System
//import copy
import System.Collections  # for IList

class EfficientRelationshipManager:
	#region Bigcomment
	/*
	e.g.
	relations {
				from1 : {to1:[rel1]}
				from2 : {to5:[rel1,rel2], to6:[rel1]}
			  }
	inverseRelations {
				same as above except meaning is reversed.
			  }
			  
	Real Sample:
	-----------
		relations = {
						"from1" : {"to1":["rel1"]},
						"from2" : {"to5":["rel1","rel2"], "to6":["rel1"]}
					  }
		print relations
		print relations.Keys
		
	*/
	#endregion

	public Relations = {}
	public InverseOfRelations = {}
	
	private _cacheFindObjects = {}
	private _cacheFindRels = {}
	public useCache = false  // cahc makes things slower
	
	def constructor():
		pass

	public def UseCache(flag):
		self.useCache = flag
		
	private def InvalidateCaches():
		self._cacheFindObjects.Clear()
		self._cacheFindRels.Clear()

	def Count():
		result = 0
		todict as Hash
		for fromobj in self.Relations.Keys:
			todict = self.Relations[fromobj]
			for toobj in todict.Keys:
				for relId in todict[toobj]:
					result+=1					// THIS IS THE CHANGING LINE
		return result
		
	def CountRelationships(matchingRelId):
		result = 0
		todict as Hash
		for fromobj in self.Relations.Keys:
			todict = self.Relations[fromobj]
			for toobj in todict.Keys:
				for relId in todict[toobj]:
					if relId == matchingRelId:  // THIS IS THE CHANGING LINE
						result+=1    			// THIS IS THE CHANGING LINE
		return result
		
	#region Code For the Future Perhaps
	/*
	def CountRelationshipIds():
		return self.GetRelationshipIds().Count()
		
	def GetRelationshipIds():
		result = []
		for fromobj in self.Relations.Keys:
			todict = self.Relations[fromobj]
			for toobj in todict.Keys:
				for relId in todict[toobj]:
					if relId not in result:  // THIS IS THE CHANGING LINE
						result.Add(relId)    // THIS IS THE CHANGING LINE
		return result
	*/	
	#endregion	
		
	def GetRelations():
		result = []
		todict as Hash     // new
		for fromobj in self.Relations.Keys:
			todict = self.Relations[fromobj]
			for toobj in todict.Keys:
				//relationsList as IList = todict[toobj]
				//for relId in relationsList:
				for relId in todict[toobj]:
					result.Add((fromobj, toobj, relId))	// THIS IS THE CHANGING LINE
		return result
		
	def SetRelations(listofrelationshiptuples):
		for r as IList in listofrelationshiptuples:
			self.AddRelationship(r[0], r[1], r[2])
			
	//Relationships = property(GetRelations, SetRelations) # ANDY
	Relationships as IList:
	      get:
	          return self.GetRelations()
	      set:
	          self.SetRelations(value)
          
	private def AddEntry(relationsDict as Hash, From, To, RelId):
		
		if useCache:
			self.InvalidateCaches()
			
		if From not in relationsDict:
			relationsDict[From] = {}
		if To not in relationsDict[From] as Hash:
			//relationsDict[From][To] = []
			entry as Hash = relationsDict[From]
			entry[To] = []
		entry1 as Hash = relationsDict[From]
		entry2 as IList = entry1[To]
		if RelId not in entry2:
		//if RelId not in relationsDict[From][To]:
			//relationsDict[From][To].append(RelId)
			entry2.Add(RelId)

	def AddRelationship(From, To):
		self.AddRelationship(From, To, 1)
		
	def AddRelationship(From, To, RelId):
		AddEntry(self.Relations, From, To, RelId)
		AddEntry(self.InverseOfRelations, To, From, RelId)


	private def _ZapRelationId(rdict as Hash, From, To, RelId):
		if useCache:
			self.InvalidateCaches()
			
		assert _HavespecifiedallParams(From, To, RelId)
		relList as IList = (rdict[From] as Hash)[To]
		if RelId in relList:
			relList.Remove(RelId)
		if relList == []:	 # no more relationships, so remove the entire mapping
			//del rdict[From][To]
			(rdict[From] as Hash).Remove(To)
	
	private def ZapRelId(From, To, RelId):
		_ZapRelationId(self.Relations,		  From, To,   RelId)
		_ZapRelationId(self.InverseOfRelations, To,   From, RelId)


	private def _HavespecifiedallParams(From, To, RelId):
		return (From != null and To != null and RelId != null)

	private def _NumberOfNonWildcardParamsSupplied(From, To, RelId):
		numberOfNoneParams = 0
		if From == null:
			numberOfNoneParams+=1
		if To == null:
			numberOfNoneParams+=1
		if RelId == null:
			numberOfNoneParams+=1
		return numberOfNoneParams

	def RemoveRelationships(From, To, RelId):
		/*
		Specifying None as a parameter means 'any'
		*/
		lzt as IList
		
		if _NumberOfNonWildcardParamsSupplied(From, To, RelId) > 1:
			raise "RuntimeError " + "Only one parameter can be left as None, (indicating a match with anything)."

		if _HavespecifiedallParams(From, To, RelId):
			if self.DoesRelIdExistBetween(From, To, RelId):  # returns T/F
				ZapRelId(From, To, RelId)
		else:
			if From==null:
				lzt = self.FindObjects(null, To, RelId) # result is list of From objects i.e. things that point to 'To' with relid 'RelId'
				for obj in lzt:
					ZapRelId(obj, To, RelId)
			elif To==null:
				lzt = self.FindObjects(From, null, RelId) # result is list of To objects i.e. things that point from 'From' with relid 'RelId'
				for obj in lzt:
					ZapRelId(From, obj, RelId)
			elif RelId==null:
				lzt = self.FindRelIdsBetween(From, To) # result is RelIds
				for relid in lzt:
					ZapRelId(From, To, relid)
			else:
				raise "impossible else"
		
		/*
		if _HavespecifiedallParams(From, To, RelId):
			if self.FindObjects(From, To, RelId):  # returns T/F
				ZapRelId(From, To, RelId)
		else:
			lzt = self.FindObjects(From, To, RelId) # this list will be either From or To or RelIds depending on which param was set as None (meaning match anything)
			if lzt.Count > 0:
				for objOrRelid in lzt:
					if From==null:
						# lzt contains all the things that point to 'To' with relid 'RelId'
						# objOrRelid is the specific thing during this iteration that point to 'To', so delete it
						ZapRelId(objOrRelid, To, RelId)
					elif To==null:
						ZapRelId(From, objOrRelid, RelId)
					elif RelId==null:
						ZapRelId(From, To, objOrRelid)
		*/
			
	private def _FindRels(subdict as Hash, RelId) as Boo.Lang.List:
		if false and useCache:
			key = (subdict, RelId)
			//print 'key ' + key.ToString()
			if _cacheFindRels.ContainsKey(key):
			//if key in self._cacheFindRels.Keys:
				//System.Console.Write("*")
				return self._cacheFindRels[key]
			//else:
			//	System.Console.Write("_")
				
		resultlist = []
		for k in subdict.Keys:
			v as IList = subdict[k]
			if ((RelId in v) or (RelId == null)):
				resultlist.Add(k)

		if false and useCache:
			key = (subdict, RelId)
			self._cacheFindRels[key] = resultlist

		return resultlist


	public def FindRelIdsBetween(From, To) as IList:
		# Find all RelId's between blah and blah
		# Used to be FindObjects() where From=blah To=blah RelId=None
		subdict as Hash
		subdict = self.Relations[From] or {}
		relationIdsList as Boo.Lang.List = subdict[To] or []
		return relationIdsList[:]  # return the entire list of relationship ids between these two.
		
	public def DoesRelIdExistBetween(From, To) as bool:
		return self.DoesRelIdExistBetween(From, To, 1) # return T/F
		
	public def DoesRelIdExistBetween(From, To, RelId) as bool:
		# T/F does this specific relationship exist
		# Used to be FindObjects() where From=blah To=blah RelId=blah  
		subdict as Hash
		subdict = self.Relations[From] or {}
		relationIdsList as IList= subdict[To] or []
		return RelId in relationIdsList # return T/F


	def FindObjects(From, To) as IList:
		return self.FindObjects(From, To, 1)
			
	def FindObjects(From, To, RelId) as IList:
		/*
		Specifying None as a parameter means 'any'
		Can specify
		  # 'From' is None - use normal relations dictionary
		  From=None To=blah RelId=blah  anyone pointing to 'To' of specific RelId
		  From=None To=blah RelId=None  anyone pointing to 'To'

		  # 'To' is None - use inverse relations dictionary
		  From=blah To=None RelId=blah  anyone 'From' points to, of specific RelId
		  From=blah To=None RelId=None  anyone 'From' points to

		  # Both 'To' & 'From' specified, use any e.g. use normal relations dictionary
		  BOO VERSION DEPRECIATES THESE TWO SINCE RETURNING A LIST OR A BOOLEAN CONFUSING
		  From=blah To=blah RelId=None  all RelId's between blah and blah
		  From=blah To=blah RelId=blah  T/F does this specific relationship exist

		  From=None To=None RelId=blah  error (though you could implement returning a list of From,To pairs using the R blah e.g. [('a','b'),('a','c')]
		  From=None To=None RelId=None  error
		*/
		
		if useCache:
			key = (From, To, RelId)
			if _cacheFindObjects.ContainsKey(key):
				return self._cacheFindObjects[key]

		if From!=null and To!=null:
			if RelId == null:
				raise "Depreciated in boo version.  Use FindRelIdsBetween(From, To) instead"
			else:
				raise "Depreciated in boo version.  Use DoesRelIdExistBetween(From, To, RelId) instead"

		if From==null and To==null:
			raise "RuntimeError " + "Either 'From' or 'To' has to be specified"

		//havespecifiedallParams = lambda : (From<>None and To<>None and RelId<>None)
		//resultlist as IList
		resultlist = []
		subdict as Hash

		if From==null:
			//subdict = self.InverseOfRelations.get(To, {})
			subdict = self.InverseOfRelations[To] or {}

			//resultlist = [ k for k, v in subdict.iteritems() if (RelId in v or RelId == None)]
			resultlist = self._FindRels(subdict, RelId)
			
		elif To==null:
			# returns a list of all the matching tos
			//subdict = self.Relations.get(From, {})
			subdict = self.Relations[From] or {}
			
			//resultlist = [ k for k, v in subdict.iteritems() if (RelId in v or RelId == None)]
			resultlist = self._FindRels(subdict, RelId)

		else:
			raise "RuntimeError!! " + "Either 'From' or 'To' has to be specified"
			/*
			# Both 'To' & 'From' specified, use any e.g. use normal relations dictionary
			From=blah To=blah RelId=None  all RelId's between blah and blah
			From=blah To=blah RelId=blah  T/F does this specific relationship exist
			
			//subdict = self.Relations.get(From, {})
			subdict = self.Relations[From] or {}
			//relationIdsList = subdict.get(To, [])
			relationIdsList as IList= subdict[To] or []
			if RelId==null:
			  resultlist = relationIdsList  # return the entire list of relationship ids between these two.
			else:
			  return RelId in relationIdsList # return T/F
			*/
			  
		if useCache:
			key = (From, To, RelId)
			self._cacheFindObjects[key] = resultlist[:]

		//return copy.copy(resultlist)
		return resultlist[:]

	def Clear():
		self.Relations.Clear()
		self.InverseOfRelations.Clear()

	def FindObject(From, To):
		return self.FindObject(From, To, 1)
		
	def FindObject(From, To, RelId) as object:
		lzt as IList
		lzt = self.FindObjects(From, To, RelId)
		if lzt.Count > 0:
			return lzt[0]
		else:
			return null

# -------------------------

