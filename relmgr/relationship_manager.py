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

    def add_rel(self, source, target, rel_id=1) -> None:
        """Add relationships between ... """
        self.rm.add_rel(source, target, rel_id)

    def remove_rel(self, source, target, rel_id=1) -> None:
        """Remove all relationships between ... """
        self.rm.remove_rel(source, target, rel_id)

    def FindObjects(self, source=None, target=None, rel_id=1) -> Union[List[object], bool]:
        """Find first object - low level"""
        return self.rm.FindObjects(source, target, rel_id)

    def FindObject(self, source=None, target=None, rel_id=1) -> object:
        """Find first object - low level"""
        return self.rm.FindObject(source, target, rel_id)

    def FindObjectPointedToByMe(self, source, relId=1) -> object:
        """Find first object pointed to by me - first target"""
        return self.rm.FindObject(source, None, relId)

    def FindObjectPointingToMe(self, target, relId=1) -> object:  # Back pointer query
        """Find first object pointed to me - first source"""
        return self.rm.FindObject(None, target, relId)

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

    def R(self, source, target, relId=1):
        self.add_rel(source, target, relId)

    def P(self, source, relId=1):
        return self.FindObject(source, None, relId)

    def B(self, target, relId=1):
        return self.FindObject(None, target, relId)

    def PS(self, source, relId=1):
        return self.FindObjects(source, None, relId)

    def NR(self, source, target, relId=1):
        self.remove_rel(source, target, relId)

    def CL(self):
        self.Clear()

    # Util

    def debug_print_rels(self):
        """Just a diagnostic method to print the relationships in the rm.
        See also the `RelationshipManager.Relationships` property."""
        print()
        pprint.pprint(self.Relationships)
