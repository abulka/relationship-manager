"""
Relationship manager.
Version 1.3
(c) Andy Bulka 2003-2020 (wow that's a long time!)
https://abulka.github.io/blog/2001/08/04/relationship-manager-design-pattern/

  ____      _       _   _                 _     _
 |  _ \ ___| | __ _| |_(_) ___  _ __  ___| |__ (_)_ __
 | |_) / _ \ |/ _` | __| |/ _ \| '_ \/ __| '_ \| | '_ \
 |  _ <  __/ | (_| | |_| | (_) | | | \__ \ | | | | |_) |
 |_| \_\___|_|\__,_|\__|_|\___/|_| |_|___/_| |_|_| .__/
                                                 |_|
  __  __
 |  \/  | __ _ _ __   __ _  __ _  ___ _ __
 | |\/| |/ _` | '_ \ / _` |/ _` |/ _ \ '__|
 | |  | | (_| | | | | (_| | (_| |  __/ |
 |_|  |_|\__,_|_| |_|\__,_|\__, |\___|_|
                           |___/
"""
from typing import List, Set, Dict, Tuple, Optional, Union
import pickle
from dataclasses import dataclass  # requires 3.7

# from src.core.v0_rel_mgr_original import RelationshipManagerOriginal as RMCoreImplementation  # 8 test failures
# from src.core.v1_rel_mgr_original_better_findobjects import RelationshipManagerOriginalBetterFindObjects as RMCoreImplementation  # 2 test failures
# from src.core.v2_rel_mgr_efficient_buggy import EfficientRelationshipManagerBuggy as RMCoreImplementation  # 12 test failures
from src.core.v3_rel_mgr_efficient import EfficientRelationshipManager as RMCoreImplementation  # 0 test failures


class RelationshipManager:
    """
    Main Relationship Manager to use in your projects.

    Could use a different core api implementation, though GetRelations() and SetRelations()
    only supported by the later core implementations.
    """

    def __init__(self) -> None:
        self.rm = RMCoreImplementation()

    def GetRelations(self) -> List[Tuple[object, object, Union[int, str]]]:
        return self.rm.GetRelations()

    def SetRelations(self, listofrelationshiptuples: List[Tuple[object, object, Union[int, str]]]) -> None:
        self.rm.SetRelations(listofrelationshiptuples)

    Relationships = property(GetRelations, SetRelations)

    def AddRelationship(self, From, To, RelId=1) -> None:
        self.rm.AddRelationship(From, To, RelId)

    def RemoveRelationships(self, From, To, RelId=1) -> None:
        self.rm.RemoveRelationships(From, To, RelId)

    def FindObjects(self, From=None, To=None, RelId=1) -> Union[List[object], bool]:
        return self.rm.FindObjects(From, To, RelId)

    def FindObject(self, From=None, To=None, RelId=1) -> object:
        return self.rm.FindObject(From, To, RelId)

    def FindObjectPointedToByMe(self, fromObj, relId=1) -> object:
        return self.rm.FindObject(fromObj, None, relId)

    def FindObjectPointingToMe(self, toObj, relId=1) -> object:  # Back pointer query
        return self.rm.FindObject(None, toObj, relId)

    def Clear(self) -> None:
        self.rm.Clear()


class EnforcingRelationshipManager(RelationshipManager):
    """
    A stricter Relationship Manager which adds the method 'EnforceRelationship'
    where you register the cardinality and directionality of each relationship.

    Benefits:

        - When adding and removing relationships, bi directional relationships 
        are automatically created. (though remember, back pointer queries are 
        also always possible in the case of regular RelationshipManager, I think
        this is more of an official wiring rather than using a back pointer concept?)

        - When adding the same relationship again (by mistake?) any previous 
        relationship is removed first.
    """

    def __init__(self):
        super().__init__()
        self.enforcer = {}

    def EnforceRelationship(self, relId, cardinality, directionality="directional"):
        self.enforcer[relId] = (cardinality, directionality)

    def _RemoveExistingRelationships(self, fromObj, toObj, relId):
        def ExtinguishOldFrom():
            oldFrom = self.FindObjectPointingToMe(toObj, relId)
            self.RemoveRelationships(oldFrom, toObj, relId)

        def ExtinguishOldTo():
            oldTo = self.FindObjectPointedToByMe(fromObj, relId)
            self.RemoveRelationships(fromObj, oldTo, relId)
        if relId in list(self.enforcer.keys()):
            cardinality, directionality = self.enforcer[relId]
            if cardinality == "onetoone":
                ExtinguishOldFrom()
                ExtinguishOldTo()
            elif cardinality == "onetomany":  # and directionality == "directional":
                ExtinguishOldFrom()

    def AddRelationship(self, fromObj, toObj, relId=1):
        self._RemoveExistingRelationships(fromObj, toObj, relId)
        super().AddRelationship(fromObj, toObj, relId)
        if relId in list(self.enforcer.keys()):
            cardinality, directionality = self.enforcer[relId]
            if directionality == "bidirectional":
                self.rm.AddRelationship(toObj, fromObj, relId)

    def RemoveRelationships(self, fromObj, toObj, relId=1):
        super().RemoveRelationships(fromObj, toObj, relId)
        if relId in list(self.enforcer.keys()):
            cardinality, directionality = self.enforcer[relId]
            if directionality == "bidirectional":
                self.rm.RemoveRelationships(toObj, fromObj, relId)

    def Clear(self) -> None:
        super().Clear()
        self.enforcer = {}


class EnforcingRelationshipManagerShortMethodNames:  # nicer for unit tests
    def __init__(self):
        self.rm = EnforcingRelationshipManager()

    def ER(self, relId, cardinality, directionality="directional"):
        self.rm.EnforceRelationship(relId, cardinality, directionality)

    def R(self, fromObj, toObj, relId=1):
        self.rm.AddRelationship(fromObj, toObj, relId)

    def P(self, fromObj, relId=1):
        # findObjectPointedToByMe(fromMe, id, cast)
        return self.rm.FindObject(fromObj, None, relId)

    def B(self, toObj, relId=1):
        # findObjectPointingToMe(toMe, id cast)
        return self.rm.FindObject(None, toObj, relId)

    def PS(self, fromObj, relId=1):
        # findObjectsPointedToByMe(fromMe, id, cast)
        return self.rm.FindObjects(fromObj, None, relId)

    def NR(self, fromObj, toObj, relId=1):
        self.rm.RemoveRelationships(fromObj, toObj, relId)


# Persistence

@dataclass
class Namespace:
    """Just want a namespace to store vars/attrs in. Could use a dictionary."""


@dataclass
class PersistenceWrapper:
    """Holds both objects and relationships. Could use a dictionary."""
    objects: Namespace  # Put all your objects involved in relationships as attributes of this object
    relations: List  # Relationship Manager relationship List will go here


class RelationshipManagerPersistent(EnforcingRelationshipManager):
    """
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
        # persist
        asbytes = rm.dumps()

        # resurrect
        rm2 = RelationshipManagerPersistent.loads(asbytes)
    """

    def __init__(self):
        super().__init__()
        self.objects = Namespace()  # assign to this namespace directly to record your objects

    def Clear(self):
        super().__init__()
        self.objects = Namespace()

    def dumps(self) -> bytes:
        return pickle.dumps(PersistenceWrapper(
            objects=self.objects, relations=self.Relationships))

    @staticmethod
    def loads(asbytes: bytes):  # -> RelationshipManagerPersistent:
        data: PersistenceWrapper = pickle.loads(asbytes)
        rm = EnforcingRelationshipManager()
        rm.objects = data.objects
        rm.Relationships = data.relations
        return rm
