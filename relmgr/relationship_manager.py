"""
Relationship Manager - Lightweight Object Database for Python.
(c) Andy Bulka 2003 - 2020.
https://github.com/abulka/relationship-manager
"""
import copy
import pickle
import pprint
from dataclasses import dataclass
from functools import lru_cache
from typing import Dict, List, Optional, Set, Tuple, Union
from relmgr._enforcing import _EnforcingRelationshipManager
from relmgr._caching import _RelationshipManagerCaching
from relmgr.persist_support import Namespace, PersistenceWrapper


__pdoc__ = {}

__pdoc__['RelationshipManager'] = """
# Welcome to Relationship Manager

Put simply, create an instance of this class, then call 
`RelationshipManager.add_rel()` to record relationships between
any two Python objects.

You can then make queries e.g. using 
`RelationshipManager.FindObjectPointedToByMe()` as needed.

## What is a relationship RelId?

Type RelId can be an integer or descriptive string e.g. `x-to-y`.

## Note on the low level FindObjects() method

```
FindObjects(self, From=None, To=None, RelId=1):
```

Specifying None as a parameter means 'any'. E.g. when you specify:

'From' is None - use normal relations dictionary
```
From=None To=blah RelId=blah  anyone pointing to 'To' of specific RelId
From=None To=blah RelId=None  anyone pointing to 'To'
```

'To' is None - use inverse relations dictionary
```
From=blah To=None RelId=blah  anyone 'From' points to, of specific RelId
From=blah To=None RelId=None  anyone 'From' points to
```

Both 'To' & 'From' specified, use any e.g. use normal relations dictionary
```
From=blah To=blah RelId=None  all RelId's between blah and blah
From=blah To=blah RelId=blah  T/F does this specific relationship exist  <--- bool returned, yuk
From=None To=None RelId=blah  error (though you could implement returning 
                                    a list of From,To pairs using the R blah e.g. [('a','b'),('a','c')]
From=None To=None RelId=None  error
```

## Other uses of None as a parameter value

RemoveRelationships(self, From, To, RelId=1) -> None: Specifying None as a parameter means 'any'
"""

__pdoc__['RelationshipManager.dumps'] = """
    Persistent Relationship Manager.  

    Provides an attribute object called `.objects` where you can keep all the
    objects involved in relationships e.g.

        rm.objects.obj1 = Entity(strength=1, wise=True, experience=80)

    Then when you persist the Relationship Manager both the objects and
    relations are pickled and later restored. This means your objects are
    accessible by attribute name e.g. rm.objects.obj1 at all times. You can
    assign these references to local variables for convenience e.g.

        obj1 = rm.objects.obj1

    Usage:
        ```
        # persist
        asbytes = rm.dumps()

        # resurrect
        rm2 = RelationshipManagerPersistent.loads(asbytes)
        ```
"""


class RelationshipManager():
    """Main Relationship Manager to use in your projects."""

    def __init__(self, caching: bool=True) -> None:
        """Constructor.  Set the option `caching` if you want
        faster performance using Python `lru_cache` technology 
        - defaults to True.
        """
        if caching:
            self.rm = _RelationshipManagerCaching()
        else:
            self.rm = _EnforcingRelationshipManager()

        self.objects = Namespace()
        """Optional place for storing objects involved in relationships, so the objects are saved.
        Assign to this `.objects` namespace directly to record your objects
        for persistence puposes.
        """

    def GetRelations(self) -> List[Tuple[object, object, Union[int, str]]]:
        """Getter"""
        return self.rm.GetRelations()

    def SetRelations(self, listofrelationshiptuples: List[Tuple[object, object, Union[int, str]]]) -> None:
        self.rm.SetRelations(listofrelationshiptuples)
        """Setter"""

    Relationships = property(GetRelations, SetRelations)
    """Property to get flat list of relationships tuples"""

    def add_rel(self, from_, to, rel_id=1) -> None:
        """Add relationships between ... """
        self.rm.add_rel(from_, to, rel_id)

    def RemoveRelationships(self, from_, to, rel_id=1) -> None:
        """Remove all relationships between ... """
        self.rm.RemoveRelationships(from_, to, rel_id)

    def FindObjects(self, from_=None, to=None, rel_id=1) -> Union[List[object], bool]:
        """Find first object - low level"""
        return self.rm.FindObjects(from_, to, rel_id)

    def FindObject(self, from_=None, to=None, rel_id=1) -> object:
        """Find first object - low level"""
        return self.rm.FindObject(from_, to, rel_id)

    def FindObjectPointedToByMe(self, fromObj, relId=1) -> object:
        """Find first object pointed to by me - first target"""
        return self.rm.FindObject(fromObj, None, relId)

    def FindObjectPointingToMe(self, toObj, relId=1) -> object:  # Back pointer query
        """Find first object pointed to me - first source"""
        return self.rm.FindObject(None, toObj, relId)

    def EnforceRelationship(self, relId, cardinality, directionality="directional"):
        """Enforce a relationship by auto creating reciprocal relationships in the case of 
        bidirectional relationships, and by overwriting existing relationships if in the case
        of one-to-one cardinality?
        """
        self.rm.EnforceRelationship(relId, cardinality, directionality)

    def dumps(self) -> bytes:
        """Dump relationship tuples and objects to pickled bytes.
        The `objects` attribute and all objects stored therein
        (within the instance of `RelationshipManager.objects`) also get persisted."""
        return pickle.dumps(PersistenceWrapper(
            objects=self.objects, relations=self.Relationships))

    @staticmethod
    def loads(asbytes: bytes):  # -> RelationshipManager:
        """Load relationship tuples and objects from pickled bytes. 
        Returns a `RelationshipManager` instance.
        """
        data: PersistenceWrapper = pickle.loads(asbytes)
        rm = RelationshipManager()
        rm.objects = data.objects
        rm.Relationships = data.relations
        return rm  

    def Clear(self) -> None:
        """Clear all relationships, does not affect .objects - if you want to clear that too then
        assign a new empty object to it.  E.g. rm.objects = Namespace()
        """
        self.rm.Clear()
        self.objects = Namespace()

    ## Short API

    def ER(self, relId, cardinality, directionality="directional"):
        self.EnforceRelationship(relId, cardinality, directionality)

    def R(self, fromObj, toObj, relId=1):
        self.add_rel(fromObj, toObj, relId)

    def P(self, fromObj, relId=1):
        return self.FindObject(fromObj, None, relId)

    def B(self, toObj, relId=1):
        return self.FindObject(None, toObj, relId)

    def PS(self, fromObj, relId=1):
        return self.FindObjects(fromObj, None, relId)

    def NR(self, fromObj, toObj, relId=1):
        self.RemoveRelationships(fromObj, toObj, relId)

    def CL(self):
        self.Clear()

    # Util

    def debug_print_rels(self):
        """Just a diagnostic method to print the relationships in the rm.
        See also the `RelationshipManager.Relationships` property."""
        print()
        pprint.pprint(self.Relationships)
