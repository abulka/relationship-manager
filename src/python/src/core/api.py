from typing import List, Set, Dict, Tuple, Optional, Union

"""
Core Implementations of Relationship Manager - various:
    - RelationshipManagerOriginal
    - RelationshipManagerOriginal2
    - BigRelationshipManager1
    - EfficientRelationshipManager1 (latest)

Note that the actual RelationshipManager uses this core implementation and 
adds a little bit of functionality too (the Relationships property), 
as does EnforcingRelationshipManager (the EnforceRelationship method).

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

"""

# These interfaces aren't actually used in code, they are just for documentation purposes

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
