import unittest
import pprint
import random
from rm_python.relationship_manager import RelationshipManagerPersistent as RelationshipManager
from dataclasses import dataclass  # requires 3.7


@dataclass
class Entity:
    strength: int = 0
    wise: bool = False
    experience: int = 0

    def __hash__(self):
        hash_value = hash(self.strength) ^ hash(
            self.wise) ^ hash(self.experience)
        return hash_value


class TestPersistence(unittest.TestCase):

    def test_persistence(self):
        rm = RelationshipManager()
        obj1 = rm.objects.obj1 = Entity(strength=1, wise=True, experience=80)
        obj2 = rm.objects.obj2 = Entity(strength=2, wise=False, experience=20)
        obj3 = rm.objects.obj3 = Entity(strength=3, wise=True, experience=100)

        rm.AddRelationship(obj1, obj2)
        rm.AddRelationship(obj1, obj3)
        self.assertEqual(rm.FindObjects(obj1), [obj2, obj3])

        # persist
        asbytes = rm.dumps()

        # resurrect
        rm2 = RelationshipManager.loads(asbytes)

        # check things worked
        newobj1 = rm2.objects.obj1
        newobj2 = rm2.objects.obj2
        newobj3 = rm2.objects.obj3
        self.assertEqual(rm2.FindObjects(newobj1), [newobj2, newobj3])
        self.assertIs(rm2.FindObjectPointedToByMe(newobj1), newobj2, "getting copies not references?")