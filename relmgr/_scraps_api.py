from relmgr.relationship_manager import Namespace
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

Possible revised API
--------------------

def add(self, source, target, rel_id: Union[int,str]=1) -> None: pass
def remove(self, source, target, rel_id=1) -> None: pass
def targets_of(self, source, rel_id) -> List: pass
def sources_to(self, target, rel_id) -> List: pass # Back pointer query
def enforce(self, rel_id, cardinality, directionality="directional"): pass
def clear(self) -> None: pass

# convenience - return the first object 
def target_of(self, source, rel_id) -> object: pass
def source_to(self, target, rel_id) -> object: pass # Back pointer query

# low level
def _find_objects(self, source=None, target=None, rel_id=1) -> Union[List[object], bool]: pass
def _find_object(self, source=None, target=None, rel_id=1) -> object: pass

# persistence related
objects: Namespace
relationships = property(_get_relationships, _set_relationships)  # flat list of rel. tuples
def dumps(self) -> bytes:
def loads(asbytes: bytes) -> RelationshipManager:  # @staticmethod

# potential replacement or extension to persisting objects
objects_dict: Dict  # alternative place for storing objects

# potential extension to persistence objects
add_obj(self, obj, obj_id: str)
get_obj(self, obj_id: str) -> object:
remove_obj(self, obj) -> None:

"""


class IRelationshipManagerAPI:
    """API of Relationship Manager - for documentaton purposes"""

    """Optional place for storing objects involved in relationships, so the objects are saved"""
    objects: Namespace

    def GetRelations(self) -> List[Tuple[object, object, Union[int, str]]]:
        """Getter"""

    def SetRelations(self, listofrelationshiptuples: List[Tuple[object, object, Union[int, str]]]) -> None:
        """Setter"""

    """Property to get flat list of relationships tuples"""
    Relationships = property(GetRelations, SetRelations)
    
    def AddRelationship(self, from_, to, rel_id=1) -> None:
        """Add relationships between ... """

    def RemoveRelationships(self, from_, to, rel_id=1) -> None:
        """Remove all relationships between ... """

    def FindObjects(self, from_=None, to=None, rel_id=1) -> Union[List[object], bool]:
        """Find all objects - low level"""

    def FindObject(self, from_=None, to=None, rel_id=1) -> object:
        """Find first object - low level"""

    def FindObjectPointedToByMe(self, from_, relId=1) -> object:
        """Find first object pointed to by me - first target"""

    def FindObjectPointingToMe(self, toObj, relId=1) -> object:  # Back pointer query
        """Find first object pointed to me - first source"""

    def Clear(self) -> None:
        """Clear all relationships, does not affect .objects - if you want to clear that too then
        assign a new empty object to it.  E.g. rm.objects = Namespace()
        """

    def EnforceRelationship(self, relId, cardinality, directionality="directional"):
        """Enforce a relationship by auto creating reciprocal relationships in the case of 
        bidirectional relationships, and by overwriting existing relationships if in the case
        of one-to-one cardinality?
        """

    def dumps(self) -> bytes:
        """Dump relationship tuples and objects to pickled bytes"""

    @staticmethod
    def loads(asbytes: bytes) -> RelationshipManager:
        """Load relationship tuples and objects from pickled bytes"""

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
