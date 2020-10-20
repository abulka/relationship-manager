import pprint
import random
from dataclasses import dataclass  # requires 3.7
import copy
import pickle
from typing import List, Set, Dict, Tuple, Optional
from relmgr import RelationshipManager

"""
Persist a bunch of objects and proper "object to object" Relationship Manager
based relationships using pickle. No dictionaries.
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
    """An alternative to a dictionary, just want a namespace to store vars/attrs
    in. Cannot use object() since instances don't allow arbitrary attribute
    assignment. We use a dataclass because it implements eq and hash for us, cos
    we compare namespaces later on.

    Unfortunately we don't get anything except "Namespace()" in the repr cos we
    haven't declared any attributes here. Lucky pickle is smarter and will pull
    out all the vars and put them back! To work around this we define repr here
    to burrow in and display any dynamically created attributes - nice. This repr
    here doesn't affect persistence because pickle looks at reality not repr.
    """

    def __repr__(self) -> str:
        return repr(vars(self))


@dataclass
class PersistenceWrapper:
    """Could have used another Namespace instance instead, or a dictionary -
    doesn't matter. At least here we can do a nice repr for diagnostics.
    """
    objects: Namespace
    relations: List


objects = Namespace()  # create a namespace for the variables
objects.id1 = Entity(strength=1, wise=True, experience=80)
objects.id2 = Entity(strength=2, wise=False, experience=20)
objects.id3 = Entity(strength=3, wise=True, experience=100)
rm = RelationshipManager()
rm.add_rel(objects.id1, objects.id2)
rm.add_rel(objects.id1, objects.id3)


def checkRelationships(rm, objects):
    assert rm.FindObjectPointedToByMe(objects.id1) == objects.id2
    assert rm.FindObjects(objects.id1) == [objects.id2, objects.id3]
    assert rm.FindObjectPointingToMe(
        objects.id2) == objects.id1  # back pointer
    assert rm.FindObjectPointingToMe(
        objects.id3) == objects.id1  # back pointer

    # Extra check, ensure new objects have not been created in the rm which simply
    # refers to existing instances which have been resurrected. Use 'is' to check.
    id1 = objects.id1
    id2 = objects.id2
    id3 = objects.id3
    assert rm.FindObjectPointedToByMe(id1) is id2
    assert rm.FindObjectPointingToMe(id3) is id1  # back pointer
    # double check again that references not copies are being created, by changing an attribute
    oldStringth = id2.strength
    id2.strength = 1000
    assert rm.FindObjectPointedToByMe(id1).strength == 1000
    id2.strength = oldStringth


checkRelationships(rm, objects)

# prepare for persistence - wrap the objects and relationships in an outer object
# to create a namespace for persisting - could use a dict, it doesn't matter.
data = PersistenceWrapper(objects=objects, relations=rm.Relationships)
pprint.pprint(data, indent=4, width=1)  # doesn't seem to indent?

# persist
asbytes = pickle.dumps(data)
# asbytes = pickle.dumps(rm.Relationships)  # yes this works but don't get objects id1, id2 etc easily accessible

# resurrect from a asbytes
data2 = pickle.loads(asbytes)
pprint.pprint(data2, indent=4, width=1)  # doesn't seem to indent?
rm2 = RelationshipManager()
objects2 = data2.objects
rm2.Relationships = data2.relations
# rm2.Relationships = pickle.loads(asbytes)  # yes this works but don't get objects id1, id2 etc easily accessible

# check resurrected version is the same as the original
assert isinstance(data2, PersistenceWrapper)
assert isinstance(data2.objects.id1, Entity)
assert isinstance(objects, Namespace)
assert isinstance(objects2, Namespace)

# cannot be true cos instances are different unless supply __eq__ and __hash__ (use dataclass to do this for us)
assert objects == objects2

assert objects.id1.wise == objects2.id1.wise
checkRelationships(rm2, objects2)

print('done, all OK')
