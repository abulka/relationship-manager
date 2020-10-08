import pprint
import random
from dataclasses import dataclass  # requires 3.7
import copy
from typing import List, Set, Dict, Tuple, Optional

"""
Demonstrates how to persist an object using repr to convert to a string and eval
to convert back to an object again.

Yes you can represent complex Python objects as strings using syntax like:
 { 'x': Entity(strength=78, wise=True, experience=28),
   'y': Entity(strength=66, wise=False, experience=13)}
which is a dictionary with two objects inside.

More options and ideas:
https://stackoverflow.com/questions/1047318/easiest-way-to-persist-a-data-structure-to-a-file-in-python
https://stackoverflow.com/questions/4529815/saving-an-object-data-persistence/4529901
"""

@dataclass
class Entity:
    """
    Being a dataclass we automatically get
        def __init__(self, name: int=0, wise: bool=False, experience: int=0):
    which means the eval() of a string which looks like
        "Entity(strength=56, wise=False, experience=12)"
    will create the Entity object nicely with the correct values.

    We also get repr and eq methods etc.
    """
    strength: int = 0
    wise: bool = False
    experience: int = 0
    
    """
    Don't define a post init which sets values otherwise
    when you resurrect an object, its values will be filled in
    then the __post_init__ will be called and those values
    obliterated.
    """
    def X__post_init__(self):
        self.strength = random.randint(50, 100)
        self.wise = random.choice([True, False])
        self.experience = random.randint(10, 100)

    def randomise(self):
        # only call this when creating new objects - not when resurrecting
        self.strength = random.randint(50, 100)
        self.wise = random.choice([True, False])
        self.experience = random.randint(10, 100)

    """
    The default repr by dataclass is GOOD and gives the string
        "Entity(strength=56, wise=False, experience=12)"
    which is what we want, so that we get Entity objects back 
    when we eval().

    If on the other hand, we define a repr that is just a mere dict
        "{'strength': 58, 'wise': True, 'experience': 80}"
    then we only get back a dict, not a proper Entity when we eval().
    """
    def X__repr__(self):
        data = {
            'strength': self.strength,
            'wise': self.wise,
            'experience': self.experience,
        }
        return repr(data)

x = Entity()
y = Entity()
x.randomise()
y.randomise()
mydict: Dict[str, Entity] = {
    'x': x,
    'y': y,
}
pprint.pprint(mydict, indent=4)

# persist the dict containing Entity objects
s = repr(mydict)
print(f"PERSISTED STRING IS: {s}")

# resurrect from a string
mydict2 = eval(s)
pprint.pprint(mydict2, indent=4)

# check resurrected version is the same as the original
assert isinstance(mydict2, dict)
assert isinstance(mydict2['x'], Entity)
assert mydict['x'].wise == mydict2['x'].wise
assert mydict['y'].wise == mydict2['y'].wise
assert mydict['x'].strength == mydict2['x'].strength
assert mydict['y'].strength == mydict2['y'].strength
assert mydict['x'].experience == mydict2['x'].experience
assert mydict['y'].experience == mydict2['y'].experience

print('done, all OK')
