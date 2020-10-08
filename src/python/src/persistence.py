import pprint
import copy
import random
import time
from typing import List, Set, Dict, Tuple, Optional
from dataclasses import dataclass  # requires 3.7
import pickle
from src.relationship_manager import EnforcingRelationshipManager as RelationshipManager

"""
Persistence for Relationship Manager

EXPERIMENTAL

"""


@dataclass
class Namespace:
    """Just want a namespace to store vars/attrs in. Could use a dictionary."""


@dataclass
class PersistenceWrapper:
    """Holds both objects and relationships. Could use a dictionary."""
    objects: Namespace  # Put all your objects involved in relationships as attributes of this object
    relations: List  # Relationship Manager relationship List will go here


class RelationshipManagerPersistent(RelationshipManager):
    def __init__(self):
        RelationshipManager.__init__(self)
        self.objects = Namespace()  # assign to this namespace directly to record your objects

    def Clear(self):
        RelationshipManager.Clear(self)
        self.objects = Namespace()

    def dumps(self):
        return pickle.dumps(PersistenceWrapper(
            objects=self.objects, relations=self.Relationships))

    @staticmethod
    def loads(asbytes):
        data: PersistenceWrapper = pickle.loads(asbytes)
        rm = RelationshipManager()
        rm.objects = data.objects
        rm.Relationships = data.relations
        return rm
