import copy
import pickle
import pprint
from dataclasses import dataclass
from functools import lru_cache
from typing import Dict, List, Optional, Set, Tuple, Union


class _CoreRelationshipManager(object):
    """
    Good efficient implementation in that it maps forward and reverse pointers
    for better performance of backpointer lookups e.g.

        relations {
            from1 : {to1:[rel1]}
            from2 : {to5:[rel1,rel2], to6:[rel1]}
        }
        inverseRelations {
            same as above except meaning is reversed.
        }

    Adds Relationships property for setting and getting the relationships
    which helps if persisting.

    """

    def __init__(self):
        self.Relations = {}
        self.InverseOfRelations = {}

    def GetRelations(self) -> List[Tuple[object, object, Union[int, str]]]:
        result = []
        for source in self.Relations:
            to_dict = self.Relations[source]
            for to in to_dict:
                for relId in to_dict[to]:
                    result.append((source, to, relId))
        return result

    def SetRelations(self, list_of_relationship_tuples: List[Tuple[object, object, Union[int, str]]]):
        for r in list_of_relationship_tuples:
            self.add_rel(source=r[0], to=r[1], rel_id=r[2])
    Relationships = property(GetRelations, SetRelations)

    def add_rel(self, source, to, rel_id=1) -> None:
        def AddEntry(relationsDict, source, to, rel_id):
            if source not in relationsDict:
                relationsDict[source] = {}
            if to not in relationsDict[source]:
                relationsDict[source][to] = []
            if rel_id not in relationsDict[source][to]:
                relationsDict[source][to].append(rel_id)
        AddEntry(self.Relations, source, to, rel_id)
        AddEntry(self.InverseOfRelations, to, source, rel_id)

    def RemoveRelationships(self, source, to, rel_id=1) -> None:
        """
        Specifying None as a parameter means 'any'
        """
        def have_specified_all_params(): return (
                source is not None and to is not None and rel_id is not None)

        def number_of_wildcard_params():
            result = 0  # number of None params, which represent a wildcard match
            if source is None:
                result += 1
            if to is None:
                result += 1
            if rel_id is None:
                result += 1
            return result

        if number_of_wildcard_params() > 1:
            raise RuntimeError(
                'Only one parameter can be left as None, (indicating a match with anything).')

        def ZapRelId(source, to, rel_id):
            def _ZapRelationId(rdict, source, to, rel_id):
                assert (source is not None and to is not None and rel_id is not None)
                rel_list = rdict[source][to]
                if rel_id in rel_list:
                    rel_list.remove(rel_id)
                if not rel_list:     # no more relationships, so remove the entire mapping
                    del rdict[source][to]
            _ZapRelationId(self.Relations,          source, to,   rel_id)
            _ZapRelationId(self.InverseOfRelations, to,   source, rel_id)

        if have_specified_all_params():
            if self.FindObjects(source, to, rel_id):  # returns T/F
                ZapRelId(source, to, rel_id)
        else:
            # this list will be either 'source' or 'to' or RelIds depending on which param was set as None (meaning match anything)
            lzt = self.FindObjects(source, to, rel_id)
            if lzt:
                for objOrRelid in lzt:
                    if source == None:
                        # lzt contains all the things that point to 'to' with relid 'rel_id'
                        # objOrRelid is the specific thing during this iteration that point to 'to', so delete it
                        ZapRelId(objOrRelid, to, rel_id)
                    elif to == None:
                        ZapRelId(source, objOrRelid, rel_id)
                    elif rel_id == None:
                        ZapRelId(source, to, objOrRelid)

    def FindObjects(self, source=None, to=None, rel_id=1) -> Union[List[object], bool]:
        """
        Specifying None as a parameter means 'any'
        Can specify
          # 'source' is None - use normal relations dictionary
          source=None to=blah rel_id=blah  anyone pointing to 'to' of specific rel_id
          source=None to=blah rel_id=None  anyone pointing to 'to'

          # 'to' is None - use inverse relations dictionary
          source=blah to=None rel_id=blah  anyone 'source' points to, of specific rel_id
          source=blah to=None rel_id=None  anyone 'source' points to

          # Both 'to' & 'source' specified, use any e.g. use normal relations dictionary
          source=blah to=blah rel_id=None  all rel_id's between blah and blah
          source=blah to=blah rel_id=blah  T/F does this specific relationship exist

          source=None to=None rel_id=blah  error (though you could implement returning a list of source,to pairs using the R blah e.g. [('a','b'),('a','c')]
          source=None to=None rel_id=None  error
        """
        if source is None and to is None:
            raise RuntimeError("Either 'source' or 'to' has to be specified")

        def havespecifiedallParams(): return (
            source != None and to != None and rel_id != None)
        resultlist = []

        if source == None:
            subdict = self.InverseOfRelations.get(to, {})
            resultlist = [k for k, v in subdict.items() if (
                rel_id in v or rel_id == None)]

        elif to == None:
            # returns a list of all the matching tos
            subdict = self.Relations.get(source, {})
            resultlist = [k for k, v in subdict.items() if (
                rel_id in v or rel_id == None)]

        else:
            """
            # Both 'to' & 'source' specified, use any e.g. use normal relations dictionary
            source=blah to=blah rel_id=None  all rel_id's between blah and blah
            source=blah to=blah rel_id=blah  T/F does this specific relationship exist
            """
            subdict = self.Relations.get(source, {})
            relationIdsList = subdict.get(to, [])
            if rel_id == None:
                # return the entire list of relationship ids between these two.
                resultlist = relationIdsList
            else:
                return rel_id in relationIdsList  # return T/F
        return copy.copy(resultlist)

    def FindObject(self, source=None, to=None, rel_id=1) -> object:
        lzt = self.FindObjects(source, to, rel_id)
        if lzt:
            return lzt[0]
        else:
            return None

    def FindObjectPointedToByMe(self, fromObj, relId=1) -> object:
        return self.FindObject(fromObj, None, relId)

    def FindObjectPointingToMe(self, toObj, relId=1) -> object:  # Back pointer query
        return self.FindObject(None, toObj, relId)

    def Clear(self):
        self.Relations.clear()
        self.InverseOfRelations.clear()
