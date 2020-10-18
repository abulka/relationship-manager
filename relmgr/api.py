from typing import List, Set, Dict, Tuple, Optional, Union
from relmgr import RelationshipManager


"""
What is a relationship RelId?
    Type RelId can be an integer or descriptive string

Note on the FindObjects(self, From=None, To=None, RelId=1) method:
    Specifying None as a parameter means 'any'. E.g. when you specify:

        # 'From' is None - use normal relations dictionary
        From=None To=blah RelId=blah  anyone pointing to 'To' of specific RelId
        From=None To=blah RelId=None  anyone pointing to 'To'

        # 'To' is None - use inverse relations dictionary
        From=blah To=None RelId=blah  anyone 'From' points to, of specific RelId
        From=blah To=None RelId=None  anyone 'From' points to

        # Both 'To' & 'From' specified, use any e.g. use normal relations dictionary
        From=blah To=blah RelId=None  all RelId's between blah and blah
        From=blah To=blah RelId=blah  T/F does this specific relationship exist  <--- bool returned, yuk

        From=None To=None RelId=blah  error (though you could implement returning 
                                            a list of From,To pairs using the R blah e.g. [('a','b'),('a','c')]
        From=None To=None RelId=None  error

Other uses of None as a parameter value
    RemoveRelationships(self, From, To, RelId=1) -> None: Specifying None as a parameter means 'any'

These interfaces aren't actually used in code, they are just for documentation purposes
------------------

class InterfaceCoreRelationshipManager:
    def AddRelationship(self, From, To, RelId: Union[int,str]=1) -> None: pass
    def RemoveRelationships(self, From, To, RelId=1) -> None: pass
    def FindObjects(self, From=None, To=None, RelId=1) -> Union[List[object], bool]: pass
    def FindObject(self, From=None, To=None, RelId=1) -> object: pass
    def Clear(self) -> None: pass

class InterfaceRelationshipManager(InterfaceCoreRelationshipManager):
    def FindObjectPointedToByMe(self, fromObj, relId) -> object: pass
    def FindObjectPointingToMe(self, toObj, relId) -> object: pass # Back pointer query
    def GetRelations(self) -> List[Tuple[object, object, Union[int, str]]]: pass
    def SetRelations(self, listofrelationshiptuples: List[Tuple[object, object, Union[int, str]]]) -> None: pass
    Relationships = property(GetRelations, SetRelations)

class InterfaceEnforcingRelationshipManager(InterfaceRelationshipManager):
    def EnforceRelationship(self, relId, cardinality, directionality="directional"): pass

"""


class IRelationshipManagerAPI(RelationshipManager):
    """API of Relationship Manager - for documentaton purposes"""

    def GetRelations(self) -> List[Tuple[object, object, Union[int, str]]]:
        return super().GetRelations()

    def SetRelations(self, listofrelationshiptuples: List[Tuple[object, object, Union[int, str]]]) -> None:
        super().SetRelations(listofrelationshiptuples)

    Relationships = property(GetRelations, SetRelations)

    def AddRelationship(self, from_, to, rel_id=1) -> None:
        super().AddRelationship(from_, to, rel_id)

    def RemoveRelationships(self, from_, to, rel_id=1) -> None:
        super().RemoveRelationships(from_, to, rel_id)

    def FindObjects(self, from_=None, to=None, rel_id=1) -> Union[List[object], bool]:
        return super().FindObjects(from_, to, rel_id)

    def FindObject(self, from_=None, to=None, rel_id=1) -> object:
        return super().FindObject(from_, to, rel_id)

    def FindObjectPointedToByMe(self, from_, relId=1) -> object:
        return super().FindObject(from_, None, relId)

    def FindObjectPointingToMe(self, toObj, relId=1) -> object:  # Back pointer query
        return super().FindObject(None, toObj, relId)

    def Clear(self) -> None:
        super().Clear()

    ## Enforcing

    def EnforceRelationship(self, relId, cardinality, directionality="directional"):
        self.enforcer[relId] = (cardinality, directionality)

    ## Persistence

    # self.objects

    def dumps(self) -> bytes:
        super().dumps()

    @staticmethod
    def loads(asbytes: bytes) -> RelationshipManager:
        return super().loads(asbytes)

    ## Short API

    def ER(self, relId, cardinality, directionality="directional"):
        super().ER(relId, cardinality, directionality)

    def R(self, fromObj, toObj, relId=1):
        super().R(fromObj, toObj, relId)

    def P(self, fromObj, relId=1):
        return super().P(fromObj, relId)

    def B(self, toObj, relId=1):
        return super().B(toObj, relId)

    def PS(self, fromObj, relId=1):
        return super().PS(fromObj, relId)

    def NR(self, fromObj, toObj, relId=1):
        super().NR(fromObj, toObj, relId)

    def CL(self):
        super()


# cannot seem to run this as 
# if __name__ == "__main__":
#     import pprint

#     rm = RelationshipManagerAPI()
#     rm.AddRelationship('a', 'b', 1)
#     rm.AddRelationship('a', 'b', 2)
#     pprint.pprint(rm.Relations)
#     pprint.pprint(rm.Relationships)
