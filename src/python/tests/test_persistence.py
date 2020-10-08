import unittest
import pprint
import random
from src.persistence import RelationshipManagerPersistent as RelationshipManager
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
        id1 = rm.objects.id1 = Entity(strength=1, wise=True, experience=80)
        id2 = rm.objects.id2 = Entity(strength=2, wise=False, experience=20)
        id3 = rm.objects.id3 = Entity(strength=3, wise=True, experience=100)

        rm.AddRelationship(id1, id2)
        rm.AddRelationship(id1, id3)
        self.assertEqual(rm.FindObjects(id1), [id2, id3])

        # persist
        asbytes = rm.dumps()

        # resurrect
        rm2 = RelationshipManager.loads(asbytes)

        # check things worked
        newid1 = rm2.objects.id1
        newid2 = rm2.objects.id2
        newid3 = rm2.objects.id3
        self.assertEqual(rm2.FindObjects(newid1), [newid2, newid3])
