"""
Relationship manager.
(c) Andy Bulka 2003-2020 (wow that's a long time!)
https://github.com/abulka/relationship-manager

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
from dataclasses import dataclass  # requires at least 3.7
import copy
from functools import lru_cache
import pprint


class CoreRelationshipManager(object):
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

    core - for older core versions see misc/old orginal/
    """

    def __init__(self):     # Constructor
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


class RMCoreImplementation(CoreRelationshipManager):
    pass




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


class RelationshipManagerCaching(RelationshipManagerPersistent):

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

    ## Persistence

    # (not necessary to override) self.objects

    # (not necessary to override) def dumps(self) -> bytes:

    @staticmethod
    def loads(asbytes: bytes):  # -> RelationshipManagerCaching:
        data: PersistenceWrapper = pickle.loads(asbytes)
        rm = RelationshipManagerCaching()  # could we use super() here to determine class to create?
        rm.objects = data.objects
        rm.Relationships = data.relations
        # rm._clearCaches()  # not needed cos its a new instance
        return rm    

    def _clearCaches(self):
        self.FindObjects.cache_clear()
        self.FindObject.cache_clear()
        self.GetRelations.cache_clear()
        self.FindObjectPointingToMe.cache_clear()
        self.FindObjectPointedToByMe.cache_clear()

        """
        Alternative cache clear 
        https://www.geeksforgeeks.org/clear-lru-cache-in-python/

        But it might other caches - unless we can 
        limit it to those used by RM

            gc.collect() 
            
            # All objects collected 
            objects = [i for i in gc.get_objects()  
                    if isinstance(i, functools._lru_cache_wrapper)] 
            
            # All objects cleared 
            for object in objects: 
                object.cache_clear() 

        """


class RelationshipManager():
    """Main Relationship Manager to use in your projects."""

    def __init__(self, caching=True) -> None:
        if caching:
            self.rm = RelationshipManagerCaching()
        else:
            self.rm = RelationshipManagerPersistent()
        self.objects = Namespace()  # assign to this namespace directly to record your objects

    def GetRelations(self) -> List[Tuple[object, object, Union[int, str]]]:
        return self.rm.GetRelations()

    def SetRelations(self, listofrelationshiptuples: List[Tuple[object, object, Union[int, str]]]) -> None:
        self.rm.SetRelations(listofrelationshiptuples)

    Relationships = property(GetRelations, SetRelations)

    def AddRelationship(self, from_, to, rel_id=1) -> None:
        self.rm.AddRelationship(from_, to, rel_id)

    def RemoveRelationships(self, from_, to, rel_id=1) -> None:
        self.rm.RemoveRelationships(from_, to, rel_id)

    def FindObjects(self, from_=None, to=None, rel_id=1) -> Union[List[object], bool]:
        return self.rm.FindObjects(from_, to, rel_id)

    def FindObject(self, from_=None, to=None, rel_id=1) -> object:
        return self.rm.FindObject(from_, to, rel_id)

    def FindObjectPointedToByMe(self, fromObj, relId=1) -> object:
        return self.rm.FindObject(fromObj, None, relId)

    def FindObjectPointingToMe(self, toObj, relId=1) -> object:  # Back pointer query
        return self.rm.FindObject(None, toObj, relId)

    def EnforceRelationship(self, relId, cardinality, directionality="directional"):
        self.rm.EnforceRelationship(relId, cardinality, directionality)

    def dumps(self) -> bytes:
        # Unfortunately have to re-implement here to ensure .objects gets persisted not the inner rm.objects
        return pickle.dumps(PersistenceWrapper(
            objects=self.objects, relations=self.Relationships))

    @staticmethod
    def loads(asbytes: bytes):  # -> RelationshipManager:
        # Unfortunately have to re-implement here to ensure get a `RelationshipManager` returned
        data: PersistenceWrapper = pickle.loads(asbytes)
        rm = RelationshipManager()  # could we use super() here to determine class to create?
                    # how to create a caching or not version - save some options too? getting complex
        rm.objects = data.objects
        rm.Relationships = data.relations
        return rm  

    def Clear(self) -> None:
        self.rm.Clear()

    ## Short API

    def ER(self, relId, cardinality, directionality="directional"):
        self.EnforceRelationship(relId, cardinality, directionality)

    def R(self, fromObj, toObj, relId=1):
        self.AddRelationship(fromObj, toObj, relId)

    def P(self, fromObj, relId=1):
        return self.FindObject(fromObj, None, relId)

    def B(self, toObj, relId=1):
        return self.FindObject(None, toObj, relId)

    def PS(self, fromObj, relId=1):
        return self.FindObjects(fromObj, None, relId)

    def NR(self, fromObj, toObj, relId=1):
        self.RemoveRelationships(fromObj, toObj, relId)

    def CL(self):
        self.Clear()

    # Util

    def debug_print_rels(self):
        print()
        pprint.pprint(self.Relationships)
