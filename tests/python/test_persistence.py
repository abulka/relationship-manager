import unittest
import pprint
import random
from dataclasses import dataclass  # requires 3.7
from relmgr import RelationshipManager
from tests.python.settings import USE_RM_CACHE


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
        rm = RelationshipManager(caching=USE_RM_CACHE)
        obj1 = rm.objects.obj1 = Entity(strength=1, wise=True, experience=80)
        obj2 = rm.objects.obj2 = Entity(strength=2, wise=False, experience=20)
        obj3 = rm.objects.obj3 = Entity(strength=3, wise=True, experience=100)

        rm.add_rel(obj1, obj2)
        rm.add_rel(obj1, obj3)
        self.assertEqual(rm.find_targets(obj1), [obj2, obj3])

        # persist
        asbytes = rm.dumps()

        # resurrect
        rm2 = RelationshipManager.loads(asbytes)

        # check things worked
        newobj1 = rm2.objects.obj1
        newobj2 = rm2.objects.obj2
        newobj3 = rm2.objects.obj3
        self.assertEqual(rm2.find_targets(newobj1), [newobj2, newobj3])
        self.assertIs(rm2.find_target(newobj1), newobj2, "getting copies not references?")