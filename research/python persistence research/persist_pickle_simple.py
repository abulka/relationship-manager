import pprint
import random
from dataclasses import dataclass  # requires 3.7
import copy
import pickle
from typing import List, Set, Dict, Tuple, Optional
from relmgr import RelationshipManager

"""
Persist a bunch of objects and Relationship Manager
based relationships using pickle.
"""


@dataclass
class Entity:
    strength: int = 0
    wise: bool = False
    experience: int = 0

    def __hash__(self):
        hash_value = hash(self.strength) ^ hash(
            self.wise) ^ hash(self.experience)
        return hash_value


@dataclass
class Namespace:
    """Just want a namespace to store vars/attrs in. Could use a dictionary."""


@dataclass
class PersistenceWrapper:
    """Holds both objects and relationships. Could use a dictionary."""
    objects: Namespace  # Put all your objects involved in relationships as attributes of this object
    relations: List  # Relationship Manager relationship List will go here


objects = Namespace()  # create a namespace for the variables
objects.id1 = Entity(strength=1, wise=True, experience=80)
objects.id2 = Entity(strength=2, wise=False, experience=20)
objects.id3 = Entity(strength=3, wise=True, experience=100)
rm = RelationshipManager()
rm.add_rel(objects.id1, objects.id2)
rm.add_rel(objects.id1, objects.id3)
assert rm._find_objects(objects.id1) == [objects.id2, objects.id3]

# persist
asbytes = pickle.dumps(PersistenceWrapper(
    objects=objects, relations=rm.relationships))

# resurrect
data: PersistenceWrapper = pickle.loads(asbytes)
rm2 = RelationshipManager()
objects2 = data.objects
rm2.relationships = data.relations

# check things worked
assert rm2._find_objects(objects2.id1) == [objects2.id2, objects2.id3]

print('done, all OK')
