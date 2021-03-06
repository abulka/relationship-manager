import pprint
import random
from dataclasses import dataclass  # requires 3.7
import copy
from typing import List, Set, Dict, Tuple, Optional
from relmgr import RelationshipManager

"""
Persist a dictionary of objects Dict[str, Entity] using repr into a string and
use eval() to convert the string back to an dictionary of objects again. Keys of
the 'objects' dictionary are string ids. 

Relationships between objects are maintained by Relationship Manager, via their
string ids not by object refs - slightly unique!  But this is the way we get
repr to represent object references, which are normally impossible to persist in
repr. Sure you can create new nested objects using repr but how to have multiple
references to the same object? This is the workaround.

{   'objects': {   'id-1': Entity(strength=58, wise=True, experience=80),
                   'id-2': Entity(strength=77, wise=False, experience=20),
                   'id-3': Entity(strength=100, wise=True, experience=100)},

    'relations': [('id-1', 'id-2', 1), ('id-1', 'id-3', 1)]
}
"""

@dataclass
class Entity:
    strength: int = 0
    wise: bool = False
    experience: int = 0
    
objects: Dict[str, Entity] = {
    'id-1': Entity(strength=58, wise=True, experience=80),
    'id-2': Entity(strength=77, wise=False, experience=20),
    'id-3': Entity(strength=100, wise=True, experience=100),
}
rm = RelationshipManager()
rm.add_rel('id-1', 'id-2')
rm.add_rel('id-1', 'id-3')
def checkRelationships(rm):
    assert rm.find_target('id-1') == 'id-2'
    assert rm.find_targets('id-1') == ['id-2', 'id-3']
    assert rm.find_source('id-2') == 'id-1'  # back pointer
    assert rm.find_source('id-3') == 'id-1'  # back pointer
checkRelationships(rm)

# persist
mydict = {
    'objects': objects,
    'relations': rm.relationships
}
pprint.pprint(mydict, indent=4)
s = repr(mydict)
print()
print(f"PERSISTED STRING IS: {s}")
print()

# resurrect from a string
mydict2 = eval(s)
pprint.pprint(mydict2, indent=4)
rm2 = RelationshipManager()
objects2 = mydict2['objects']
rm2.relationships = mydict2['relations']

# check resurrected version is the same as the original
assert isinstance(mydict2, dict)
assert isinstance(mydict2['objects']['id-1'], Entity)
assert isinstance(objects, dict)
assert isinstance(objects2, dict)
assert objects == objects2
assert objects['id-1'].wise == objects2['id-1'].wise
checkRelationships(rm2)

print('done, all OK')
