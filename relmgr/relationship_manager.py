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

    def __init__(self, caching=True) -> None:
        if caching:
            self.rm = _RelationshipManagerCaching()
        else:
            self.rm = _EnforcingRelationshipManager()

        self.objects = Namespace()
        """Assign to this `.objects` namespace directly to record your objects
        for persistence puposes.
        """

    def GetRelations(self) -> List[Tuple[object, object, Union[int, str]]]:
        return self.rm.GetRelations()

    def SetRelations(self, listofrelationshiptuples: List[Tuple[object, object, Union[int, str]]]) -> None:
        self.rm.SetRelations(listofrelationshiptuples)

    Relationships = property(GetRelations, SetRelations)

    def AddRelationship(self, from_, to, rel_id=1) -> None:
        self.rm.AddRelationship(from_, to, rel_id)

    def RemoveRelationships(self, from_, to, rel_id=1) -> None:
        self.rm.RemoveRelationships(from_, to, rel_id)

    def FindObjects(self, from_=None, to=None, rel_id=1) -> Union[List[object], bool]:
        return self.rm.FindObjects(from_, to, rel_id)

    def FindObject(self, from_=None, to=None, rel_id=1) -> object:
        return self.rm.FindObject(from_, to, rel_id)

    def FindObjectPointedToByMe(self, fromObj, relId=1) -> object:
        return self.rm.FindObject(fromObj, None, relId)

    def FindObjectPointingToMe(self, toObj, relId=1) -> object:  # Back pointer query
        return self.rm.FindObject(None, toObj, relId)

    def EnforceRelationship(self, relId, cardinality, directionality="directional"):
        self.rm.EnforceRelationship(relId, cardinality, directionality)

    def dumps(self) -> bytes:
        # Unfortunately have to re-implement here to ensure .objects gets persisted not the inner rm.objects
        return pickle.dumps(PersistenceWrapper(
            objects=self.objects, relations=self.Relationships))

    @staticmethod
    def loads(asbytes: bytes):  # -> RelationshipManager:
        # Unfortunately have to re-implement here to ensure get a `RelationshipManager` returned
        data: PersistenceWrapper = pickle.loads(asbytes)
        rm = RelationshipManager()  # could we use super() here to determine class to create?
                    # how to create a caching or not version - save some options too? getting complex
        rm.objects = data.objects
        rm.Relationships = data.relations
        return rm  

    def Clear(self) -> None:
        self.rm.Clear()
        self.objects = Namespace()

    ## Short API

    def ER(self, relId, cardinality, directionality="directional"):
        self.EnforceRelationship(relId, cardinality, directionality)

    def R(self, fromObj, toObj, relId=1):
        self.AddRelationship(fromObj, toObj, relId)

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
