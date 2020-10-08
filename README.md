# Relationship Manager Pattern

A central mediating class which records all the one-to-one, one-to-many and many-to-many relationships between a group of selected classes. 

Official [Relationship Manager Pattern](https://abulka.github.io/blog/2001/08/04/relationship-manager-design-pattern/) page incl. academic paper by Andy Bulka.

## Brief Discussion

In a sense, an [Object Database](https://en.wikipedia.org/wiki/Object_database) is an implementation of the RM pattern. 
The *intent* of the RM pattern is lighter weight, to replace the wirings between objects
rather than acting as a huge central database.

Classes that use a Relationship Manager to implement their relationship properties and methods have a consistent metaphor and trivial implementation code (one line calls). In contrast - traditional "pointer" and "arraylist" techniques of implementing relationships are fully flexible but often require a reasonable amount of non-trivial code which can be tricky to get working correctly and are almost always a pain to maintain due to the detailed coding and coupling between classes involved.

Using a `Relationship Manager` object to manage the relationships can mitigate these problems and make managing relationships straightforward.

# Implementations

Here are various implementations of the Relationship Manager Pattern:

- Python: Uses Python 3, there are no dependencies.
- Java
- C#: Visual Studio 2005 project with unit test. Very fast implementation used in at least one commercial product.

## Python

For general use import like this

```python
from src.relationship_manager import EnforcingRelationshipManager as RelationshipManager
```

Then to use e.g.

```python
rm = RelationshipManager()
rm.EnforceRelationship("xtoy", "onetoone", "directional")
x = object()
y = object()
rm.AddRelationship(x, y, "xtoy")
self.assertEqual(rm.FindObjectPointedToByMe(x, "xtoy"), y)
```

Read the unit test to see all functionality being exercised, incl. backpointer queries.

### Python API

The API is:

```python
def AddRelationship(self, From, To, RelId: Union[int,str]=1) -> None: pass
def RemoveRelationships(self, From, To, RelId=1) -> None: pass
def FindObjects(self, From=None, To=None, RelId=1) -> Union[List[object], bool]: pass
def FindObject(self, From=None, To=None, RelId=1) -> object: pass
def Clear(self) -> None: pass
def FindObjectPointedToByMe(self, fromObj, relId) -> object: pass
def FindObjectPointingToMe(self, toObj, relId) -> object: pass # Back pointer query
def GetRelations(self) -> List[Tuple[object, object, Union[int, str]]]: pass
def SetRelations(self, listofrelationshiptuples: List[Tuple[object, object, Union[int, str]]]) -> None: pass
Relationships = property(GetRelations, SetRelations)
def EnforceRelationship(self, relId, cardinality, directionality="directional"): pass
```

If you don't need the `EnforceRelationship` method then simply
```python
from src.relationship_manager import RelationshipManager
```

### Hiding the use of Relationship Manager

Its probably best to hide the use of Relationship Manager and simply use it as
an implementation underneath traditional wiring methods like `.add()` and
`setY()` or properties like `.subject` etc. 

For example, to implement:
```
         ______________        ______________
        |       X      |      |       Y      |
        |______________|      |______________|
        |              |      |              |
        |void  setY(y) |1    1|              |
        |Y     getY()  |----->|              |
        |void  clearY()|      |              |
        |______________|      |______________|
```

write the Python code like this:
```python
class X:
    def __init__(self):        RM.ER("xtoy", "onetoone", "directional")
    def setY(self, y):         RM.R(self, y, "xtoy")
    def getY(self):     return RM.P(self, "xtoy")
    def clearY(self):          RM.NR(self, self.getY(), "xtoy")

class Y:
    pass
```

Note the use of the abbreviated Relationship Manager API `EnforcingRelationshipManagerShortMethodNames` found in 
python/src/relationship_manager.py

All possible permutations of this approach can be found in 
python/tests/test_enforcing_relationship_manager.py

### Persistence

Persistence can be a bit tricky because you need to persist both objects and relationships between those objects.

Other libraries that implement models, schemas, serializers/deserializers,
ODM's/ORM's, Active Records or similar patterns will require you to define your
classes in a particular way. Relationship Manager works with any Python objects
like dataclass objects etc. without any special decoration or structure
required.

Whilst it is possible to simply pickle a Relationship Manager instance and
restore it, you won't have easy access to the objects involved. Sure,
Relationship Manager will return objects which have been resurrected from
persistence correctly but how, in such a unpickled situation, will you pass
object instances to the Relationship Manager API? Thus its better to prepare
your persitence properly and store all your objects in a dictionary or object
and pickle that together with the Relationship Manager.  E.g.

```python
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
rm.AddRelationship(objects.id1, objects.id2)
rm.AddRelationship(objects.id1, objects.id3)
assert rm.FindObjects(objects.id1) == [objects.id2, objects.id3]

# persist
asbytes = pickle.dumps(PersistenceWrapper(objects=objects, relations=rm.Relationships))

# resurrect
data: PersistenceWrapper = pickle.loads(asbytes)
rm2 = RelationshipManager()
objects2 = data.objects
rm2.Relationships = data.relations

# check things worked
assert rm2.FindObjects(objects2.id1) == [objects2.id2, objects2.id3]
```

For a more detailed example, see 
python/src/examples/persistence/persist_pickle.py
as well as other persistence approached in that directory.

### Easiest persistence technique

Alternatively, the easiest approach to persistence is to use the built in
`RelationshipManagerPersistent`. It provides an attribute
object called `.objects` where you should keep all the objects involved in
relationships e.g.

```python
rm.objects.obj1 = Entity(strength=1, wise=True, experience=80)
```

Then when you persist the Relationship Manager both the objects and
relations are pickled and later restored. This means your objects are
accessible by attribute name e.g. `rm.objects.obj1` at all times. You can
assign these references to local variables for convenience e.g. `obj1 = rm.objects.obj1`.
    
Here is complete example of creating three entitys, wiring them up, 
persisting them then restoring them:

```python
import pprint
import random
from src.relationship_manager import RelationshipManagerPersistent as RelationshipManager
from dataclasses import dataclass  # requires 3.7

"""
Simplest RelationshipManager with built in persistence.

See tests/test_persistence.py for corresponding unit test.
See src/relationship_manager.py for doco.
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


rm = RelationshipManager()
obj1 = rm.objects.obj1 = Entity(strength=1, wise=True, experience=80)
obj2 = rm.objects.obj2 = Entity(strength=2, wise=False, experience=20)
obj3 = rm.objects.obj3 = Entity(strength=3, wise=True, experience=100)

rm.AddRelationship(obj1, obj2)
rm.AddRelationship(obj1, obj3)
assert rm.FindObjects(obj1) == [obj2, obj3]

# persist
asbytes = rm.dumps()

# resurrect
rm2 = RelationshipManager.loads(asbytes)

# check things worked
newobj1 = rm2.objects.obj1
newobj2 = rm2.objects.obj2
newobj3 = rm2.objects.obj3
assert rm2.FindObjects(newobj1) == [newobj2, newobj3]
assert rm2.FindObjectPointedToByMe(newobj1) is newobj2

print('done, all OK')
```

The API of `RelationshipManagerPersistent` adds:

```python
objects: Namespace  # create attributes on this, pointing to those objects involved in relationships

def dumps(self) -> bytes:

@staticmethod
def loads(asbytes: bytes) -> RelationshipManagerPersistent:
```

There are currently no `dump()` or `load()` methods implemented, which would pickle
to and from a file. These can easily be added in a subclass or just write and
read the results of the existing `dumps()` and `loads()` methods to a file
yourself, as bytes.

### Running the tests

Open the `src/python` directory in vscode or your favourite IDE and run tests etc. from there.

```shell
python -m unittest discover -p 'test*' -v tests
```

output

```
bash-3.2$ testall 
Python 2.7.17
/Users/Andy/Devel/relationship-manager/src/python
test_OneToOne_XNoApi_YSingularApi (test_rm.TestCase01_OneToOne) ... ok
test_OneToOne_XSingularApi_YNoApi (test_rm.TestCase01_OneToOne) ... ok
test_OneToOne_XSingularApi_YSingularApi (test_rm.TestCase01_OneToOne) ... ok
test_OneToOne_XSingularApi_YSingularApi_Alt (test_rm.TestCase01_OneToOne) ... ok
test_OneToMany_XPluralApi_YNoApi (test_rm.TestCase02_OneToMany) ... ok
test_OneToMany_XPluralApi_YSingularApi (test_rm.TestCase02_OneToMany) ... ok
test_OneToMany_XPluralApi_YSingularApi_Alt (test_rm.TestCase02_OneToMany) ... ok
test_example (test_core.TestCase00) ... ok
test_Basic00 (test_core.TestCase01) ... ok
test_Basic01Singular (test_core.TestCase01) ... ok
test_FindRelationshipIds_NewFeatureFeb2005_01 (test_core.TestCase02) ... ok
test_FindRelationshipIds_NewFeatureFeb2005_02 (test_core.TestCase02) ... ok
test_IfRelIdIsWorking01 (test_core.TestCase02) ... ok
test_MultipleReturns01 (test_core.TestCase02) ... ok
test_NonExistent01 (test_core.TestCase02) ... ok
test_Removal_01 (test_core.TestCase02) ... ok
test_Removal_02 (test_core.TestCase02) ... ok
test_Removal_03 (test_core.TestCase02) ... ok
test_Removal_04 (test_core.TestCase02) ... ok
test_Speed01 (test_core.TestCase03) ... ok
test_Duplicates01 (test_core.TestCase04) ... ok
test_Get01 (test_core.TestCase05) ... ok
test_Set01 (test_core.TestCase05) ... ok

----------------------------------------------------------------------
Ran 23 tests in 0.012s
```

## C#

Very fast implementation - the Visual Studio 2005 projects/solutions need updating to a more recent version of Visual Studio.

## Boo

The [boo language](http://boo-language.github.io/) for .NET is now dead, however this implementation created a .dll that was usable by other .NET languages.

## Java

A java implementation.

## Javascript

To be completed.

# Final Thoughts

## Persistence

Persistence is an issue. Often you want to persist all objects and the relationships between them. This has been solved in Relationship Manager a few times but I have to find the code.

## References and memory

Be careful - the Relationship Manager will have references to your objects so garbage collection may not be able to kick in. If you remove all relationships for an object it should be removed from the Relationship Manager, but this needs to be verified in these implementations.

## Performance

Be mindful that normal object to object wiring using references and lists of references is going to be much faster than a Relationship Manager.

You can have multiple relationship manager instances to manage different areas of your programming domain, which increases efficiency and comprehensibility.

## Other implementations

You may want to google for other more professional [Object Databases](https://en.wikipedia.org/wiki/Object_database). For example, in the Python space we have:

- https://github.com/grundic/awesome-python-models - A curated list of awesome Python libraries, which implement models, schemas, serializers/deserializers, ODM's/ORM's, Active Records or similar patterns.
- https://www.opensourceforu.com/2017/05/three-python-databases-pickledb-tinydb-zodb/ - A peek at three Python databases: PickleDB, TinyDB and ZODB
- https://tinydb.readthedocs.io/en/stable/usage.html#queries - Welcome to TinyDB, your tiny, document oriented database optimized for your happiness
- https://divmod.readthedocs.io/en/latest/products/axiom/index.html - Axiom is an object database whose primary goal is to provide an object-oriented layer to an SQL database
- http://www.newtdb.org/en/latest/getting-started.html - Newt DB - You’ll need a Postgres Database server.
- http://www.zodb.org/en/latest/tutorial.html#tutorial-label - This tutorial is intended to guide developers with a step-by-step introduction of how to develop an application which stores its data in the ZODB.

However most of these need a backing SQL database - Relationship Manager does not. Then again, Relationship Manager doesn't have built in persistence.
