class RelationshipManager:
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

import unittest, random

class TestCase00(unittest.TestCase):
    def setUp(self):
        self.rm = RelationshipManager()
    def checkBasic00(self):
        self.rm.AddRelationship('a','b')
        self.rm.AddRelationship('a','c')
        assert self.rm.FindObjects('a',None) == ['b','c']
        assert self.rm.FindObjects(None,'a') == []
        assert self.rm.FindObjects(None,'b') == ['a']
        assert self.rm.FindObjects(None,'c') == ['a']
    def checkBasic01Singular(self):
        self.rm.AddRelationship('a','b')
        self.rm.AddRelationship('a','c')
        assert self.rm.FindObject(None,'b') == 'a'
        assert self.rm.FindObject(None,'c') == 'a'
        assert self.rm.FindObject('a',None) == 'b' # could have been 'c' - arbitrary
        
def suite():
    suite1 = unittest.makeSuite(TestCase00,'check')
    alltests = unittest.TestSuite( (suite1,) )
    return alltests
    
def main():
    """ Run all the suites.  To run via a gui, then
            python unittestgui.py NestedDictionaryTest.suite
        Note that I run with VERBOSITY on HIGH  :-) just like in the old days
        with pyUnit for python 2.0
        Simply call
          runner = unittest.TextTestRunner(descriptions=0, verbosity=2)
        The default arguments are descriptions=1, verbosity=1
    """
    runner = unittest.TextTestRunner(descriptions=0, verbosity=2) # default is descriptions=1, verbosity=1
    #runner = unittest.TextTestRunner(descriptions=0, verbosity=1) # default is descriptions=1, verbosity=1
    runner.run( suite() )

if __name__ == '__main__':
    main()
