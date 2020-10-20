import copy
import pickle
import pprint
from dataclasses import dataclass
from functools import lru_cache
from typing import Dict, List, Optional, Set, Tuple, Union
from relmgr._enforcing import _EnforcingRelationshipManager


class _RelationshipManagerCaching(_EnforcingRelationshipManager):
    # no persistence in this

    def __init__(self):
        super().__init__()

    @lru_cache(maxsize=None)
    def GetRelations(self) -> List[Tuple[object, object, Union[int, str]]]:
        return super().GetRelations()

    def SetRelations(self, listofrelationshiptuples: List[Tuple[object, object, Union[int, str]]]) -> None:
        super().SetRelations(listofrelationshiptuples)
        self._clearCaches()

    # (not necessary to override) Relationships = property(GetRelations, SetRelations)

    def add_rel(self, source, target, rel_id=1) -> None:
        super().add_rel(source, target, rel_id)
        self._clearCaches()

    def remove_rel(self, source, target, rel_id=1) -> None:
        super().remove_rel(source, target, rel_id)
        self._clearCaches()

    @lru_cache(maxsize=None)
    def FindObjects(self, source=None, target=None, rel_id=1) -> Union[List[object], bool]:
        return super().FindObjects(source, target, rel_id)

    @lru_cache(maxsize=None)
    def FindObject(self, source=None, target=None, rel_id=1) -> object:
        return super().FindObject(source, target, rel_id)

    @lru_cache(maxsize=None)
    def target_of(self, source, relId=1) -> object:
        return super().FindObject(source, None, relId)

    @lru_cache(maxsize=None)
    def FindObjectPointingToMe(self, target, relId=1) -> object:  # Back pointer query
        return super().FindObject(None, target, relId)

    def Clear(self) -> None:
        super().Clear()
        self._clearCaches()

    ## Enforcing

    def EnforceRelationship(self, relId, cardinality, directionality="directional"):
        self.enforcer[relId] = (cardinality, directionality)

    def _clearCaches(self):
        self.FindObjects.cache_clear()
        self.FindObject.cache_clear()
        self.GetRelations.cache_clear()
        self.FindObjectPointingToMe.cache_clear()
        self.target_of.cache_clear()
