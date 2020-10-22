class RelationshipManagerOriginal:
    def __init__(self):
        self.Relationships = []

    def AddRelationship(self, From, To, RelId=1):
        if not self.FindObjects(From, To, RelId):
            self.Relationships.append((From, To, RelId))  # assoc obj

    def RemoveRelationships(self, From, To, RelId=1):
        if not From or not To:
            return
        lzt = self.FindObjects(From, To, RelId)
        if lzt:
            for association in lzt:
                self.Relationships.remove(association)

    def FindObjects(self, From=None, To=None, RelId=1):
        resultlist = []
        def match(obj, list, index): return obj == list[index] or obj == None
        for association in self.Relationships:
            if match(From, association, 0) and match(To, association, 1) and RelId == association[2]:
                if From == None:
                    resultlist.append(association[0])
                elif To == None:
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

"""
and you could use it like this:

```python
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
```
"""
