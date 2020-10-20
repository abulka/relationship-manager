import copy
import pickle
import pprint
from dataclasses import dataclass
from functools import lru_cache
from typing import Dict, List, Optional, Set, Tuple, Union
from relmgr.core import CoreRelationshipManager


class EnforcingRelationshipManager(CoreRelationshipManager):
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
                super().AddRelationship(toObj, fromObj, relId)

    def RemoveRelationships(self, fromObj, toObj, relId=1):
        super().RemoveRelationships(fromObj, toObj, relId)
        if relId in list(self.enforcer.keys()):
            cardinality, directionality = self.enforcer[relId]
            if directionality == "bidirectional":
                super().RemoveRelationships(toObj, fromObj, relId)

    def Clear(self) -> None:
        super().Clear()
        self.enforcer = {}