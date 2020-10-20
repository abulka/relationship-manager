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
        for from_ in self.Relations:
            to_dict = self.Relations[from_]
            for to in to_dict:
                for relId in to_dict[to]:
                    result.append((from_, to, relId))
        return result

    def SetRelations(self, list_of_relationship_tuples: List[Tuple[object, object, Union[int, str]]]):
        for r in list_of_relationship_tuples:
            self.AddRelationship(from_=r[0], to=r[1], rel_id=r[2])
    Relationships = property(GetRelations, SetRelations)

    def AddRelationship(self, from_, to, rel_id=1) -> None:
        def AddEntry(relationsDict, from_, to, rel_id):
            if from_ not in relationsDict:
                relationsDict[from_] = {}
            if to not in relationsDict[from_]:
                relationsDict[from_][to] = []
            if rel_id not in relationsDict[from_][to]:
                relationsDict[from_][to].append(rel_id)
        AddEntry(self.Relations, from_, to, rel_id)
        AddEntry(self.InverseOfRelations, to, from_, rel_id)

    def RemoveRelationships(self, from_, to, rel_id=1) -> None:
        """
        Specifying None as a parameter means 'any'
        """
        def have_specified_all_params(): return (
                from_ is not None and to is not None and rel_id is not None)

        def number_of_wildcard_params():
            result = 0  # number of None params, which represent a wildcard match
            if from_ is None:
                result += 1
            if to is None:
                result += 1
            if rel_id is None:
                result += 1
            return result

        if number_of_wildcard_params() > 1:
            raise RuntimeError(
                'Only one parameter can be left as None, (indicating a match with anything).')

        def ZapRelId(from_, to, rel_id):
            def _ZapRelationId(rdict, from_, to, rel_id):
                assert (from_ is not None and to is not None and rel_id is not None)
                rel_list = rdict[from_][to]
                if rel_id in rel_list:
                    rel_list.remove(rel_id)
                if not rel_list:     # no more relationships, so remove the entire mapping
                    del rdict[from_][to]
            _ZapRelationId(self.Relations,          from_, to,   rel_id)
            _ZapRelationId(self.InverseOfRelations, to,   from_, rel_id)

        if have_specified_all_params():
            if self.FindObjects(from_, to, rel_id):  # returns T/F
                ZapRelId(from_, to, rel_id)
        else:
            # this list will be either 'from_' or 'to' or RelIds depending on which param was set as None (meaning match anything)
            lzt = self.FindObjects(from_, to, rel_id)
            if lzt:
                for objOrRelid in lzt:
                    if from_ == None:
                        # lzt contains all the things that point to 'to' with relid 'rel_id'
                        # objOrRelid is the specific thing during this iteration that point to 'to', so delete it
                        ZapRelId(objOrRelid, to, rel_id)
                    elif to == None:
                        ZapRelId(from_, objOrRelid, rel_id)
                    elif rel_id == None:
                        ZapRelId(from_, to, objOrRelid)

    def FindObjects(self, from_=None, to=None, rel_id=1) -> Union[List[object], bool]:
        """
        Specifying None as a parameter means 'any'
        Can specify
          # 'from_' is None - use normal relations dictionary
          from_=None to=blah rel_id=blah  anyone pointing to 'to' of specific rel_id
          from_=None to=blah rel_id=None  anyone pointing to 'to'

          # 'to' is None - use inverse relations dictionary
          from_=blah to=None rel_id=blah  anyone 'from_' points to, of specific rel_id
          from_=blah to=None rel_id=None  anyone 'from_' points to

          # Both 'to' & 'from_' specified, use any e.g. use normal relations dictionary
          from_=blah to=blah rel_id=None  all rel_id's between blah and blah
          from_=blah to=blah rel_id=blah  T/F does this specific relationship exist

          from_=None to=None rel_id=blah  error (though you could implement returning a list of from_,to pairs using the R blah e.g. [('a','b'),('a','c')]
          from_=None to=None rel_id=None  error
        """
        if from_ is None and to is None:
            raise RuntimeError("Either 'from_' or 'to' has to be specified")

        def havespecifiedallParams(): return (
            from_ != None and to != None and rel_id != None)
        resultlist = []

        if from_ == None:
            subdict = self.InverseOfRelations.get(to, {})
            resultlist = [k for k, v in subdict.items() if (
                rel_id in v or rel_id == None)]

        elif to == None:
            # returns a list of all the matching tos
            subdict = self.Relations.get(from_, {})
            resultlist = [k for k, v in subdict.items() if (
                rel_id in v or rel_id == None)]

        else:
            """
            # Both 'to' & 'from_' specified, use any e.g. use normal relations dictionary
            from_=blah to=blah rel_id=None  all rel_id's between blah and blah
            from_=blah to=blah rel_id=blah  T/F does this specific relationship exist
            """
            subdict = self.Relations.get(from_, {})
            relationIdsList = subdict.get(to, [])
            if rel_id == None:
                # return the entire list of relationship ids between these two.
                resultlist = relationIdsList
            else:
                return rel_id in relationIdsList  # return T/F
        return copy.copy(resultlist)

    def FindObject(self, from_=None, to=None, rel_id=1) -> object:
        lzt = self.FindObjects(from_, to, rel_id)
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
