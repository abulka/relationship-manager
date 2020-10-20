import copy
import pickle
import pprint
from dataclasses import dataclass
from functools import lru_cache
from typing import Dict, List, Optional, Set, Tuple, Union
from relmgr._core import _CoreRelationshipManager


class _EnforcingRelationshipManager(_CoreRelationshipManager):
    """
    A stricter Relationship Manager which adds the method 'enforce'
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

    def enforce(self, relId, cardinality, directionality="directional"):
        self.enforcer[relId] = (cardinality, directionality)

    def _RemoveExistingRelationships(self, fromObj, toObj, relId):
        def ExtinguishOldFrom():
            oldFrom = self.source_to(toObj, relId)
            self.remove_rel(oldFrom, toObj, relId)

        def ExtinguishOldTo():
            oldTo = self.target_of(fromObj, relId)
            self.remove_rel(fromObj, oldTo, relId)
        if relId in list(self.enforcer.keys()):
            cardinality, directionality = self.enforcer[relId]
            if cardinality == "onetoone":
                ExtinguishOldFrom()
                ExtinguishOldTo()
            elif cardinality == "onetomany":  # and directionality == "directional":
                ExtinguishOldFrom()

    def add_rel(self, fromObj, toObj, relId=1):
        self._RemoveExistingRelationships(fromObj, toObj, relId)
        super().add_rel(fromObj, toObj, relId)
        if relId in list(self.enforcer.keys()):
            cardinality, directionality = self.enforcer[relId]
            if directionality == "bidirectional":
                super().add_rel(toObj, fromObj, relId)

    def remove_rel(self, fromObj, toObj, relId=1):
        super().remove_rel(fromObj, toObj, relId)
        if relId in list(self.enforcer.keys()):
            cardinality, directionality = self.enforcer[relId]
            if directionality == "bidirectional":
                super().remove_rel(toObj, fromObj, relId)

    def clear(self) -> None:
        super().clear()
        self.enforcer = {}
