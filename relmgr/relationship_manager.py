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
`RelationshipManager.target_of()` as needed.

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

    def _get_relationships(self) -> List[Tuple[object, object, Union[int, str]]]:
        """Getter"""
        return self.rm._get_relationships()

    def _set_relationships(self, listofrelationshiptuples: List[Tuple[object, object, Union[int, str]]]) -> None:
        self.rm._set_relationships(listofrelationshiptuples)
        """Setter"""

    relationships = property(_get_relationships, _set_relationships)
    """Property to get flat list of relationships tuples"""

    def add_rel(self, source, target, rel_id=1) -> None:
        """Add relationships between ... """
        self.rm.add_rel(source, target, rel_id)

    def remove_rel(self, source, target, rel_id=1) -> None:
        """Remove all relationships between ... """
        self.rm.remove_rel(source, target, rel_id)

    def _find_objects(self, source=None, target=None, rel_id=1) -> Union[List[object], bool]:
        """Find first object - low level"""
        return self.rm._find_objects(source, target, rel_id)

    def _find_object(self, source=None, target=None, rel_id=1) -> object:
        """Find first object - low level"""
        return self.rm._find_object(source, target, rel_id)

    def targets_of(self, source, rel_id) -> List:
        """Find all objects pointed to by me - all the things 'source' is pointing at."""
        pass  # TODO 

    def target_of(self, source, relId=1) -> object:
        """Find first object pointed to by me - first target"""
        return self.rm._find_object(source, None, relId)

    def sources_to(self, target, rel_id) -> List:  # Back pointer query 
        """Find all objects pointing to me. Perhaps rename 'pointers_to'."""
        pass  # TODO 

    def source_to(self, target, relId=1) -> object:  # Back pointer query
        """Find first object pointing to me - first source. Perhaps rename 'pointer_to'."""
        return self.rm._find_object(None, target, relId)

    def enforce(self, relId, cardinality, directionality="directional"):
        """Enforce a relationship by auto creating reciprocal relationships in the case of 
        bidirectional relationships, and by overwriting existing relationships if in the case
        of one-to-one cardinality?
        """
        self.rm.enforce(relId, cardinality, directionality)

    def dumps(self) -> bytes:
        """Dump relationship tuples and objects to pickled bytes.
        The `objects` attribute and all objects stored therein
        (within the instance of `RelationshipManager.objects`) also get persisted."""
        return pickle.dumps(PersistenceWrapper(
            objects=self.objects, relationships=self.relationships))

    @staticmethod
    def loads(asbytes: bytes):  # -> RelationshipManager:
        """Load relationship tuples and objects from pickled bytes. 
        Returns a `RelationshipManager` instance.
        """
        data: PersistenceWrapper = pickle.loads(asbytes)
        rm = RelationshipManager()
        rm.objects = data.objects
        rm.relationships = data.relationships
        return rm  

    def clear(self) -> None:
        """Clear all relationships, does not affect .objects - if you want to clear that too then
        assign a new empty object to it.  E.g. rm.objects = Namespace()
        """
        self.rm.clear()
        self.objects = Namespace()

    ## Short API

    def ER(self, relId, cardinality, directionality="directional"):
        self.enforce(relId, cardinality, directionality)

    def R(self, source, target, relId=1):
        self.add_rel(source, target, relId)

    def P(self, source, relId=1):
        return self._find_object(source, None, relId)

    def B(self, target, relId=1):
        return self._find_object(None, target, relId)

    def PS(self, source, relId=1):
        return self._find_objects(source, None, relId)

    def NR(self, source, target, relId=1):
        self.remove_rel(source, target, relId)

    def CL(self):
        self.clear()

    # Util

    def debug_print_rels(self):
        """Just a diagnostic method to print the relationships in the rm.
        See also the `RelationshipManager.relationships` property."""
        print()
        pprint.pprint(self.relationships)
