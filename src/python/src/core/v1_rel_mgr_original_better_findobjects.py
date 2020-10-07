class RelationshipManagerOriginalBetterFindObjects:
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
      havespecifiedallParams = lambda : (From!=None and To!=None and RelId!=None)
      def NumberOfNonWildcardParamsSupplied():
          numberOfNoneParams = 0
          if From == None: numberOfNoneParams+=1
          if To == None: numberOfNoneParams+=1
          if RelId == None: numberOfNoneParams+=1
          return numberOfNoneParams

      if NumberOfNonWildcardParamsSupplied() > 1:
          raise RuntimeError('Only one parameter can be left as None, (match anything).')

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
          raise RuntimeError("Either 'From' or 'To' has to be specified")
      resultlist = []
      havespecifiedallParams = lambda : (From!=None and To!=None and RelId!=None)
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
