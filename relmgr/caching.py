import copy
import pickle
import pprint
from dataclasses import dataclass
from functools import lru_cache
from typing import Dict, List, Optional, Set, Tuple, Union
from relmgr.enforcing import EnforcingRelationshipManager


class RelationshipManagerCaching(EnforcingRelationshipManager):
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

    def AddRelationship(self, from_, to, rel_id=1) -> None:
        super().AddRelationship(from_, to, rel_id)
        self._clearCaches()

    def RemoveRelationships(self, from_, to, rel_id=1) -> None:
        super().RemoveRelationships(from_, to, rel_id)
        self._clearCaches()

    @lru_cache(maxsize=None)
    def FindObjects(self, from_=None, to=None, rel_id=1) -> Union[List[object], bool]:
        return super().FindObjects(from_, to, rel_id)

    @lru_cache(maxsize=None)
    def FindObject(self, from_=None, to=None, rel_id=1) -> object:
        return super().FindObject(from_, to, rel_id)

    @lru_cache(maxsize=None)
    def FindObjectPointedToByMe(self, from_, relId=1) -> object:
        return super().FindObject(from_, None, relId)

    @lru_cache(maxsize=None)
    def FindObjectPointingToMe(self, toObj, relId=1) -> object:  # Back pointer query
        return super().FindObject(None, toObj, relId)

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
        self.FindObjectPointedToByMe.cache_clear()
