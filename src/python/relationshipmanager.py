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

import copy

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
class RelationshipManager(EfficientRelationshipManager1):
    pass

"""
import pprint

class RelationshipManagerPersistent(RelationshipManager):
    def __init__(self):
        RelationshipManager.__init__(self)

    def __repr__(self):
        return pprint.pformat(self.Relationships)

    def LoadFromStr(self, str):
        self.Relationships = eval(str)

    def LoadFromList(self, L):
        self.Relationships = L

P.S.  There may be more stuff like this to integrate back into the main
      relationshipmanager.py module found in oobtree.py
      e.g.
        self._ConvertRelations(self.oobtreeAllies.relations.Relationships)
        LoadFromReprStr(self, strdict):
        __repr__(self):
        __str__(self):
        LoadFromDict
        etc.
"""

#-----------------------------

import unittest, random, time

class TestCase01(unittest.TestCase):
    def setUp(self):
        self.rm = RelationshipManager()
    def checkBasic00(self):
        self.rm.AddRelationship('a','b')
        self.rm.AddRelationship('a','c')

        result = self.rm.FindObjects('a',None)
        assert result == ['b','c'] or result == ['c','b']
        assert self.rm.FindObjects(None,'a') == []
        assert self.rm.FindObjects(None,'b') == ['a']
        assert self.rm.FindObjects(None,'c') == ['a']
    def checkBasic01Singular(self):
        self.rm.AddRelationship('a','b')
        self.rm.AddRelationship('a','c')
        assert self.rm.FindObject(None,'b') == 'a'
        assert self.rm.FindObject(None,'c') == 'a'

        result = self.rm.FindObject('a',None) # could be 'b' or 'c' - arbitrary
        assert result == 'b' or result == 'c'


class TestCase02(unittest.TestCase):
    def setUp(self):
        """
        A --r1-> B
        A <-r1-- B
        A --r2-> B
        A --r1-> C
        """
        self.rm = RelationshipManager()

        self.rm.AddRelationship('a','b', 'r1')
        self.rm.AddRelationship('a','b', 'r2')

        self.rm.AddRelationship('b','a', 'r1')

        self.rm.AddRelationship('a','c', 'r1')

    def checkIfRelIdIsWorking01(self):
        result = self.rm.FindObject('a',None,'r1') # could be 'b' or 'c' - arbitrary
        assert result == 'b' or result == 'c'

        assert self.rm.FindObject('a',None, 'r2') == 'b'
        assert self.rm.FindObject('a',None, 'r3') == None

        assert self.rm.FindObject(None,'b', 'r1') == 'a'
        assert self.rm.FindObject(None,'b', 'r2') == 'a'


        assert self.rm.FindObject(None,'c') <> 'a' # default relationshipid is integer 1 which is not the string 'r1' nor is it 'r2'
        assert self.rm.FindObject(None,'c','r1') == 'a'

    def checkMultipleReturns01(self):
        #assert self.rm.FindObjects('a',None,'r1').sort() == ['b', 'c']
        res = self.rm.FindObjects('a',None,'r1')
        res.sort()
        assert res == ['b', 'c']

        assert self.rm.FindObjects(None,'b','r1') == ['a']
        assert self.rm.FindObjects(None,'b') == []  # cos no relationships with id integer 1 have been created

        ok = False
        try:
          assert self.rm.FindObjects(None,None) == []   # invalid - must specify at least either from or to
        except RuntimeError:
          ok = True
        assert ok


    def checkNonExistent01(self):
        assert self.rm.FindObjects('aa',None,'r1') == []
        assert self.rm.FindObjects('a',None,'r1111') == []
        assert self.rm.FindObjects('az',None,None) == []
        assert self.rm.FindObjects(None,'bb','r1') == []
        assert self.rm.FindObjects(None,'b','r1111') == []
        assert self.rm.FindObjects('a',None,'r1111') == []
        assert self.rm.FindObjects(None,'bb',None) == []

    def checkFindRelationshipIds_NewFeatureFeb2005_01(self):
        # ***
        # *** Original behaviour was to return the actual relationship tuples (bad cos implementation dependent!)
        # ***
        # *** New behaviour is to return a boolean.
        # ***
        # When specify both sides of a relationship, PLUS the relationship itself,
        # then there is nothing to find, so return a boolean T/F if that relationship exists.
        #
        assert self.rm.FindObjects('a','b','r1') == True
        assert self.rm.FindObjects('a','b','r2') == True
        assert self.rm.FindObjects('a','b','zzz') == False

        """
        This next one is a bit subtle - we are in fact specifying all parameters, because the
        default relId is integer 1 (allowing you to create simple relationships easily).
        Thus the question we are asking is "is there a R of type 'integer 1' between a and b?"
        """
        assert self.rm.FindObjects('a','b') == False # cos no relationships with id integer 1 have been created

    def checkFindRelationshipIds_NewFeatureFeb2005_02(self):
        # ***
        # *** Original behaviour was to return the actual relationship tuples (bad cos implementation dependent!)
        # ***
        # *** New behaviour is to return a list of the relationship ids.
        # ***
        # When specify both sides of the relationship but leave the relationship None, you get a list of the relationships.
        #
        assert self.rm.FindObjects('a','b',None) == ['r1', 'r2']

    def checkRemoval_01(self):
        # Specify wildcard RelId
        assert self.rm.FindObjects('a','b',None) == ['r1', 'r2']
        assert self.rm.FindObjects('a','b','r1') == True
        assert self.rm.FindObjects('a','b','r2') == True
        self.rm.RemoveRelationships('a','b',None)  # remove all R's between a and b
        assert self.rm.FindObjects('a','b',None) == [], 'Getting ' + str(self.rm.FindObjects('a','b',None))
        assert self.rm.FindObjects('a','b','r1') == False
        assert self.rm.FindObjects('a','b','r2') == False

    def checkRemoval_02(self):
        # Specify all params
        self.rm.RemoveRelationships('a','b','r1')
        assert self.rm.FindObjects('a','b',None) == ['r2']
        assert self.rm.FindObjects('a','b','r1') == False
        assert self.rm.FindObjects('a','b','r2') == True

    def checkRemoval_03(self):
        # Specify 'from' param
        assert self.rm.FindObjects('a','b','r1') == True
        assert self.rm.FindObjects('a','b','r2') == True
        assert self.rm.FindObjects('a','c','r1') == True
        self.rm.RemoveRelationships('a',None,'r1')
        assert self.rm.FindObjects('a','b','r1') == False # zapped
        assert self.rm.FindObjects('a','b','r2') == True
        assert self.rm.FindObjects('a','c','r1') == False # zapped

        assert self.rm.FindObject(None,'b','r1') == None
        assert self.rm.FindObject(None,'b','r2') == 'a'
        assert self.rm.FindObject(None,'c',None) == None

    def checkRemoval_04(self):
        # Specify 'to' param
        assert self.rm.FindObjects('a','b','r1') == True
        assert self.rm.FindObjects('a','b','r2') == True
        assert self.rm.FindObjects('a','c','r1') == True
        self.rm.RemoveRelationships(None,'b','r1')
        assert self.rm.FindObjects('a','b','r1') == False # zapped
        assert self.rm.FindObjects('a','b','r2') == True
        assert self.rm.FindObjects('a','c','r1') == True

        self.rm.RemoveRelationships(None,'c','r1')
        assert self.rm.FindObjects('a','b','r2') == True
        assert self.rm.FindObjects('a','c','r1') == False # zapped

        self.rm.RemoveRelationships(None,'b','r2')
        assert self.rm.FindObjects('a','b','r2') == False # zapped
        assert self.rm.FindObjects('a','c','r1') == False

class TestCase03(unittest.TestCase):
    def setUp(self):
        """
        Lots of relationsips. Check the speed.
        """
        self.rm = RelationshipManager()
        #self.THINGS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJLMNOPQRSTUVWXYZ'    # ori takes MINUTES   efficient1 takes 1.7
        self.THINGS = 'abcdefghijk'                                             # ori takes 4.6       efficient1 takes 0.38

        for c in self.THINGS:
          for c2 in self.THINGS:
            self.rm.AddRelationship(c,c2,'r1')
            self.rm.AddRelationship(c,c2,'r2')
            self.rm.AddRelationship(c2,c,'r3')

    def checkSpeed01(self):
        t = time.time()

        for c in self.THINGS:
          for c2 in self.THINGS:
            assert c2 in self.rm.FindObjects(c,None,'r1')
            assert c2 in self.rm.FindObjects(c,None,'r2')
            assert c in self.rm.FindObjects(c2,None,'r3')

        timetook = time.time() -t
        #print "Relationship lookups took", timetook, 'seconds'

        assert timetook < 0.05, 'Relationship manager not fast enough! ' + str(timetook)


class TestCase04(unittest.TestCase):
    def setUp(self):
        """
        A --r1-> B
        A --r1-> B   # attempt to add a second R of the same type
        A --r2-> B
        A --r1-> C
        """
        self.rm = RelationshipManager()

        self.rm.AddRelationship('a','b', 'r1')
        self.rm.AddRelationship('a','b', 'r1')
        self.rm.AddRelationship('a','b', 'r2')
        self.rm.AddRelationship('a','c', 'r1')

    def checkDuplicates01(self):
        assert self.rm.FindObjects('a','b','r1') == True # [('a', 'b', 'r1')]
        assert self.rm.FindObjects('a','b',None) == ['r1','r2']
        assert self.rm.FindObjects('a','c','r1') == True # [('a', 'c', 'r1')]
        assert self.rm.FindObjects('a','c',None) == ['r1']

class TestCase05(unittest.TestCase):
    def setUp(self):
        """
        Check getting and setting the 'Relationships' property, which,
        despite the implementation, should look the same.
        In the original RM the property is actually accessed directly (naughty)
        and the implementation is the same as the spec, namely a list of tuples (from,to,relid)

        A --r1-> B
        A --r2-> B
        A --r1-> C
        B --r1-> A
        C --r9-> B
        """
        self.rm = RelationshipManager()

        self.rm.AddRelationship('a','b', 'r1')
        self.rm.AddRelationship('a','b', 'r2')
        self.rm.AddRelationship('a','c', 'r1')
        self.rm.AddRelationship('b','a', 'r1')
        self.rm.AddRelationship('c','b', 'r9')

    def checkGet01(self):
        r = self.rm.Relationships
        #assert r == [('a', 'b', 'r1'), ('a', 'b', 'r2'), ('a', 'c', 'r1'), ('b', 'a', 'r1'), ('c', 'b', 'r9')]
        assert len(r) == 5
        assert ('a', 'b', 'r1') in r
        assert ('a', 'b', 'r2') in r
        assert ('a', 'c', 'r1') in r
        assert ('b', 'a', 'r1') in r
        assert ('c', 'b', 'r9') in r


    def checkSet01(self):
        r = [('a', 'b', 'r1'), ('a', 'b', 'r2'), ('a', 'c', 'r1'), ('b', 'a', 'r1'), ('c', 'b', 'r9')]
        newrm = RelationshipManager()
        newrm.Relationships = r

        assert self.rm.FindObjects('a','b','r1') == True
        assert self.rm.FindObjects('a','b','r2') == True
        assert self.rm.FindObjects('a','c','r1') == True
        assert self.rm.FindObjects('b','a','r1') == True
        assert self.rm.FindObjects('c','b','r9') == True


def suite():
    suite1 = unittest.makeSuite(TestCase01,'check')
    suite2 = unittest.makeSuite(TestCase02,'check')
    suite3 = unittest.makeSuite(TestCase03,'check')
    suite4 = unittest.makeSuite(TestCase04,'check')
    suite5 = unittest.makeSuite(TestCase05,'check')
    alltests = unittest.TestSuite( (suite1,suite2,suite3,suite4,suite5) )
    return alltests

def main():
    runner = unittest.TextTestRunner(descriptions=0, verbosity=2) # default is descriptions=1, verbosity=1
    runner.run( suite() )

if __name__ == '__main__':
    main()
