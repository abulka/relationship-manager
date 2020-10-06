import copy

"""
Core Implementations of Relationship Manager - various:
    - RelationshipManagerOriginal
    - RelationshipManagerOriginal2
    - BigRelationshipManager1
    - EfficientRelationshipManager1 (latest)

Note that the actual RelationshipManager adds a little bit of functionality too.
"""

class RelationshipManagerOriginal:
  def __init__(self):		# Constructor
      self.Relationships = []
  def AddRelationship(self, From, To, RelId=1):
      if not self.FindObjects(From, To, RelId):
        self.Relationships.append( (From, To, RelId) ) # assoc obj
  def RemoveRelationships(self, From, To, RelId=1):
      if not From or not To:
          return
      lzt = self.FindObjects(From, To, RelId)
      if lzt:
          for association in lzt:
              self.Relationships.remove(association)
  def FindObjects(self, From=None, To=None, RelId=1):
      resultlist = []
      match = lambda obj,list,index : obj==list[index] or obj==None
      for association in self.Relationships:
          if match(From,association,0) and match(To,association,1) and RelId==association[2]:
              if From==None:
                  resultlist.append(association[0])
              elif To==None:
                  resultlist.append(association[1])
              else:
                  resultlist.append(association)
      return resultlist
  def FindObject(self, From=None, To=None, RelId=1):
      lzt = self.FindObjects(From, To, RelId)
      if lzt:
        return lzt[0]
      else:
        return None
  def Clear(self):
      del self.Relationships[0:]

#-----------------------------------

class RelationshipManagerOriginal2:
  """
  Slightly altered version of original that has improved FindObjects().
   1. Specifying RelId=None means return a list of any matching relationships ids
   2. No longer returns relationship tuples (cos thats implementation dependent).
  """
  def __init__(self):		# Constructor
      self.Relationships = []
  def AddRelationship(self, From, To, RelId=1):
      if not self.FindObjects(From, To, RelId):
        self.Relationships.append( (From, To, RelId) ) # assoc obj
  def RemoveRelationships(self, From, To, RelId=1):
      """ Specifying None as a parameter means 'any' """
      havespecifiedallParams = lambda : (From<>None and To<>None and RelId<>None)
      def NumberOfNonWildcardParamsSupplied():
          numberOfNoneParams = 0
          if From == None: numberOfNoneParams+=1
          if To == None: numberOfNoneParams+=1
          if RelId == None: numberOfNoneParams+=1
          return numberOfNoneParams

      if NumberOfNonWildcardParamsSupplied() > 1:
          raise RuntimeError, 'Only one parameter can be left as None, (match anything).'

      if havespecifiedallParams():
          association = (From, To, RelId)  # this is implementation dependent.
          if association in self.Relationships:
            self.Relationships.remove(association)
      else:
          lzt = self.FindObjects(From, To, RelId) # lzt contains either From or To or RelIds
          if lzt:        # depending on which param was set as None (meaning match anything)
              for objOrRelid in lzt:
                  if From==None:
                    association = (objOrRelid, To, RelId)
                  elif To==None:
                    association = (From, objOrRelid, RelId)
                  elif RelId==None:
                    association = (From, To, objOrRelid)

                  if association in self.Relationships:
                    self.Relationships.remove(association)

  def FindObjects(self, From=None, To=None, RelId=1):
      """ Specifying None as a parameter means 'any' """
      if From==None and To==None:
          raise RuntimeError, "Either 'From' or 'To' has to be specified"
      resultlist = []
      havespecifiedallParams = lambda : (From<>None and To<>None and RelId<>None)
      match = lambda obj,list,index : obj==list[index] or obj==None
      for association in self.Relationships:
          if match(From,association,0) and match(To,association,1) and match(RelId,association,2):
              if havespecifiedallParams():
                return True   # Found the only match, so stop looking
              if From==None:
                  resultlist.append(association[0])
              elif To==None:
                  resultlist.append(association[1])
              elif RelId==None:
                  resultlist.append(association[2])
      if havespecifiedallParams():
        return False
      return resultlist
  def FindObject(self, From=None, To=None, RelId=1):
      lzt = self.FindObjects(From, To, RelId)
      if lzt:
        return lzt[0]
      else:
        return None
  def Clear(self):
      del self.Relationships[0:]

#-----------------------------------

class BigRelationshipManager1(object):
    """
     Efficient RM using hash
     
     The faster RM does not support relationship Id's properly, so causes errors
     in saving me mappings, which require 'S' and 'G' relationships.

     Note the reason it doesn't support relationship Id's is that when adding an entry
     any subsequent relationship Id clobbers the previous relationship Id, since dictionaries
     cannot have duplicate keys.
    """
    def __init__(self):     # Constructor
        self.Relations = {}
        self.InverseOfRelations = {}

    def GetRelations(self):
        result = []
        for fromobj in self.Relations:
            todict = self.Relations[fromobj]
            for toobj in todict:
                result.append((fromobj, toobj, '1')) # since BigRelationshipManager1 doesn't support relId properly, fake it.
        return result
    def SetRelations(self, listofrelationshiptuples):
        for r in listofrelationshiptuples:
            self.AddRelationship(From=r[0], To=r[1], RelId=r[2])
    Relationships = property(GetRelations, SetRelations) # ANDY

    def AddRelationship(self, From, To, RelId=1):
        if From not in self.Relations:
            self.Relations[From] = {}
        self.Relations[From][To] = RelId

        if To not in self.InverseOfRelations:
            self.InverseOfRelations[To] = {}
        self.InverseOfRelations[To][From] = RelId
    def RemoveRelationships(self, From, To, RelId=1):
        del self.Relations[From][To]
        if not self.Relations[From]:
            del self.Relations[From]

        del self.InverseOfRelations[To][From]
        if not self.InverseOfRelations[To]:
            del self.InverseOfRelations[To]
    def FindObjects(self, From=None, To=None, RelId=1):
        resultlist = []

        if From==None:
            subdict = self.InverseOfRelations.get(To, {})
            resultlist = [ k for k, v in subdict.iteritems() if v == RelId]
        elif To==None:
            # returns a list of all the matching tos
            subdict = self.Relations.get(From, {})
            resultlist = [ k for k, v in subdict.iteritems() if v == RelId]
        else:
            # returns a list of all the matching (from, to, relid)
            subdict = self.Relations.get(From, {})
            relid = subdict.get(To, None)
            if relid == None:
                resultlist = []
            else:
                resultlist = [(From, To, RelId)]
        return resultlist
    def Clear(self):
        self.Relations.clear()
        self.InverseOfRelations.clear()
    def FindObject(self, From=None, To=None, RelId=1):    # ANDY
        lzt = self.FindObjects(From, To, RelId)
        if lzt:
            return lzt[0]
        else:
            return None

#-----------------------------------

class EfficientRelationshipManager1(object):
    """
    e.g.
    relations {
                from1 : {to1:[rel1]}
                from2 : {to5:[rel1,rel2], to6:[rel1]}
              }
    inverseRelations {
                same as above except meaning is reversed.
              }
    """
    def __init__(self):     # Constructor
        self.Relations = {}
        self.InverseOfRelations = {}

    def GetRelations(self):
        result = []
        for fromobj in self.Relations:
            todict = self.Relations[fromobj]
            for toobj in todict:
                for relId in todict[toobj]:
                  result.append((fromobj, toobj, relId))
        return result
    def SetRelations(self, listofrelationshiptuples):
        for r in listofrelationshiptuples:
            self.AddRelationship(From=r[0], To=r[1], RelId=r[2])
    Relationships = property(GetRelations, SetRelations) # ANDY

    def AddRelationship(self, From, To, RelId=1):
        def AddEntry(relationsDict, From, To, RelId):
            if From not in relationsDict:
                relationsDict[From] = {}
            if To not in relationsDict[From]:
                relationsDict[From][To] = []
            if RelId not in relationsDict[From][To]:
                relationsDict[From][To].append(RelId)
        AddEntry(self.Relations, From, To, RelId)
        AddEntry(self.InverseOfRelations, To, From, RelId)


    def RemoveRelationships(self, From, To, RelId=1):
      """
      Specifying None as a parameter means 'any'
      """
      havespecifiedallParams = lambda : (From<>None and To<>None and RelId<>None)
      def NumberOfNonWildcardParamsSupplied():
          numberOfNoneParams = 0
          if From == None: numberOfNoneParams+=1
          if To == None: numberOfNoneParams+=1
          if RelId == None: numberOfNoneParams+=1
          return numberOfNoneParams

      if NumberOfNonWildcardParamsSupplied() > 1:
          raise RuntimeError, 'Only one parameter can be left as None, (indicating a match with anything).'

      def ZapRelId(From, To, RelId):
          def _ZapRelationId(rdict, From, To, RelId):
              assert (From<>None and To<>None and RelId<>None)
              relList = rdict[From][To]
              if RelId in relList:
                  relList.remove(RelId)
              if relList == []:     # no more relationships, so remove the entire mapping
                  del rdict[From][To]
          _ZapRelationId(self.Relations,          From, To,   RelId)
          _ZapRelationId(self.InverseOfRelations, To,   From, RelId)

      if havespecifiedallParams():
          if self.FindObjects(From, To, RelId):  # returns T/F
              ZapRelId(From, To, RelId)
      else:
          lzt = self.FindObjects(From, To, RelId) # this list will be either From or To or RelIds depending on which param was set as None (meaning match anything)
          if lzt:
              for objOrRelid in lzt:
                  if From==None:
                    # lzt contains all the things that point to 'To' with relid 'RelId'
                    # objOrRelid is the specific thing during this iteration that point to 'To', so delete it
                    ZapRelId(objOrRelid, To, RelId)
                  elif To==None:
                    ZapRelId(From, objOrRelid, RelId)
                  elif RelId==None:
                    ZapRelId(From, To, objOrRelid)


    def FindObjects(self, From=None, To=None, RelId=1):
        """
        Specifying None as a parameter means 'any'
        Can specify
          # 'From' is None - use normal relations dictionary
          From=None To=blah RelId=blah  anyone pointing to 'To' of specific RelId
          From=None To=blah RelId=None  anyone pointing to 'To'

          # 'To' is None - use inverse relations dictionary
          From=blah To=None RelId=blah  anyone 'From' points to, of specific RelId
          From=blah To=None RelId=None  anyone 'From' points to

          # Both 'To' & 'From' specified, use any e.g. use normal relations dictionary
          From=blah To=blah RelId=None  all RelId's between blah and blah
          From=blah To=blah RelId=blah  T/F does this specific relationship exist

          From=None To=None RelId=blah  error (though you could implement returning a list of From,To pairs using the R blah e.g. [('a','b'),('a','c')]
          From=None To=None RelId=None  error
        """
        if From==None and To==None:
            raise RuntimeError, "Either 'From' or 'To' has to be specified"

        havespecifiedallParams = lambda : (From<>None and To<>None and RelId<>None)
        resultlist = []

        if From==None:
            subdict = self.InverseOfRelations.get(To, {})
            resultlist = [ k for k, v in subdict.iteritems() if (RelId in v or RelId == None)]

        elif To==None:
            # returns a list of all the matching tos
            subdict = self.Relations.get(From, {})
            resultlist = [ k for k, v in subdict.iteritems() if (RelId in v or RelId == None)]

        else:
          """
          # Both 'To' & 'From' specified, use any e.g. use normal relations dictionary
          From=blah To=blah RelId=None  all RelId's between blah and blah
          From=blah To=blah RelId=blah  T/F does this specific relationship exist
          """
          subdict = self.Relations.get(From, {})
          relationIdsList = subdict.get(To, [])
          if RelId==None:
              resultlist = relationIdsList  # return the entire list of relationship ids between these two.
          else:
              return RelId in relationIdsList # return T/F
        return copy.copy(resultlist)

    def Clear(self):
        self.Relations.clear()
        self.InverseOfRelations.clear()

    def FindObject(self, From=None, To=None, RelId=1):    # ANDY
        lzt = self.FindObjects(From, To, RelId)
        if lzt:
            return lzt[0]
        else:
            return None

# -------------------------

#class RelationshipManager(RelationshipManagerOriginal):
#class RelationshipManager(RelationshipManagerOriginal2):
#class RelationshipManager(BigRelationshipManager1):
# class RelationshipManager(EfficientRelationshipManager1):
#     pass
