import pprint
import random
from dataclasses import dataclass  # requires 3.7
import copy
import pickle
from typing import List, Set, Dict, Tuple, Optional
from src.relationship_manager import RelationshipManager

"""
Persist a bunch of objects and proper "object to object" Relationship Manager
based relationships using pickle. No dictionary workarounds needed.

{   'objects': {   'id-1': Entity(strength=58, wise=True, experience=80),
                   'id-2': Entity(strength=77, wise=False, experience=20),
                   'id-3': Entity(strength=100, wise=True, experience=100)},
    'relations': [   (   Entity(strength=58, wise=True, experience=80),
                         Entity(strength=77, wise=False, experience=20),
                         1),
                     (   Entity(strength=58, wise=True, experience=80),
                         Entity(strength=100, wise=True, experience=100),
                         1)]}

Note: the dataclass version, the relationships seem to be reporting the creation of new entities,
but my tests below indicate this is simply an artifact of having the automatic repr method that
dataclasses create for us. 
The standard, non-dataclass version reports the refereces to existing objects:

{   'objects': {   'id-1': <__main__.Entity object at 0x1012366d0>,
                   'id-2': <__main__.Entity object at 0x101236670>,
                   'id-3': <__main__.Entity object at 0x1011c9ca0>},
    'relations': [   (   <__main__.Entity object at 0x1012366d0>,
                         <__main__.Entity object at 0x101236670>,
                         1),
                     (   <__main__.Entity object at 0x1012366d0>,
                         <__main__.Entity object at 0x1011c9ca0>,
                         1)]}
"""


@dataclass
class Entity:  # this works
    strength: int = 0
    wise: bool = False
    experience: int = 0

    def __hash__(self):  # even though __eq__ is built for us by dataclass, it seems __hash__ is not!
        hash_value = hash(self.strength) ^ hash(
            self.wise) ^ hash(self.experience)
        return hash_value


class XXEntity:  # this works as well
    def __init__(self, strength, wise, experience) -> None:
        self.strength: int = strength
        self.wise: bool = wise
        self.experience: int = experience

    def __eq__(self, other):
        return (isinstance(other, Entity) and
                self.strength == other.strength and
                self.wise == other.wise and
                self.experience == other.experience)

    def __hash__(self):
        hash_value = hash(self.strength) ^ hash(
            self.wise) ^ hash(self.experience)
        return hash_value


objects: Dict[str, Entity] = {
    'id-1': Entity(strength=1, wise=True, experience=80),
    'id-2': Entity(strength=2, wise=False, experience=20),
    'id-3': Entity(strength=3, wise=True, experience=100),
}
rm = RelationshipManager()
rm.AddRelationship(objects['id-1'], objects['id-2'])
rm.AddRelationship(objects['id-1'], objects['id-3'])


def checkRelationships(rm, objects):
    assert rm.FindObjectPointedToByMe(objects['id-1']) == objects['id-2']
    assert rm.FindObjects(
        objects['id-1']) == [objects['id-2'], objects['id-3']]
    assert rm.FindObjectPointingToMe(
        objects['id-2']) == objects['id-1']  # back pointer
    assert rm.FindObjectPointingToMe(
        objects['id-3']) == objects['id-1']  # back pointer

    # Extra check, ensure new objects have not been created in the rm which simply
    # refers to existing instances which have been resurrected. Use 'is' to check.
    id1 = objects['id-1']
    id2 = objects['id-2']
    id3 = objects['id-3']
    assert rm.FindObjectPointedToByMe(id1) is id2
    assert rm.FindObjectPointingToMe(id3) is id1  # back pointer
    # double check again that references not copies are being created, by changing an attribute
    oldStringth = id2.strength
    id2.strength = 1000
    assert rm.FindObjectPointedToByMe(id1).strength == 1000
    id2.strength = oldStringth


checkRelationships(rm, objects)

# persist
mydict = {
    'objects': objects,
    'relations': rm.Relationships
}
pprint.pprint(mydict, indent=4)
asbytes = pickle.dumps(mydict)

# resurrect from a asbytes
mydict2 = pickle.loads(asbytes)
pprint.pprint(mydict2, indent=4)
rm2 = RelationshipManager()
objects2 = mydict2['objects']
rm2.Relationships = mydict2['relations']

# check resurrected version is the same as the original
assert isinstance(mydict2, dict)
assert isinstance(mydict2['objects']['id-1'], Entity)
assert isinstance(objects, dict)
assert isinstance(objects2, dict)
# cannot be true cos instances are different unless supply __eq__ and __hash__
assert objects == objects2
assert objects['id-1'].wise == objects2['id-1'].wise
checkRelationships(rm2, objects2)

print('done, all OK')
