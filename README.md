# Relationship Manager - Lightweight Object Database

A central mediating class which records all the one-to-one, one-to-many and many-to-many relationships between a group of selected classes. 

Official [Relationship Manager Pattern](https://abulka.github.io/projects/patterns/relationship-manager/) page incl. academic paper by Andy Bulka.

## What is it?

In a sense, an [Object Database](https://en.wikipedia.org/wiki/Object_database) is an elaborate implementation of the RM pattern. 
The *intent* of the RM pattern is lighter weight, to replace the wirings between objects
rather than acting as a huge central database.

Classes that use a Relationship Manager to implement their relationship properties and methods have a consistent metaphor and trivial implementation code (one line calls). In contrast - traditional "pointer" and "arraylist" techniques of implementing relationships are fully flexible but often require a reasonable amount of non-trivial code which can be tricky to get working correctly and are almost always a pain to maintain due to the detailed coding and coupling between classes involved.

Using a `Relationship Manager` object to manage the relationships can mitigate these problems and make managing relationships straightforward.

Here are various implementations of the Relationship Manager Pattern in this GitHub repository:

- Python: Uses Python 3, there are no dependencies.
- Java
- C#: Visual Studio 2005 project with unit test. Very fast implementation used in at least one commercial product.

# Python

## Installation

```shell
pip install -i relationship-manager
```

You can also simply copy the single file `relationship_manager.py` into your project and import the `RelationshipManager` class from that single file. However `pip` is the preferred way and the following examples will assume you are importing from the `relmgr` package installed by `pip`.

## Usage

```python
from relmgr import RelationshipManager
  
rm = RelationshipManager()
rm.EnforceRelationship("xtoy", "onetoone", "directional")
x = object()
y = object()
rm.AddRelationship(x, y, "xtoy")
assert rm.FindObjectPointedToByMe(x, "xtoy") == y
```

- Read the unit tests to see all functionality being exercised, incl. backpointer queries. 
- See the examples below and in the `relmgr/examples/` directory of this repository.
- See API below. 
- See the Relationship Manager pattern referred to above for lots more documentation.

## Python API

The API is:

```python
def AddRelationship(self, From, To, RelId: Union[int,str]=1) -> None: pass
def RemoveRelationships(self, From, To, RelId=1) -> None: pass
def FindObjects(self, From=None, To=None, RelId=1) -> Union[List[object], bool]: pass
def FindObject(self, From=None, To=None, RelId=1) -> object: pass
def Clear(self) -> None: pass
def FindObjectPointedToByMe(self, fromObj, relId) -> object: pass
def FindObjectPointingToMe(self, toObj, relId) -> object: pass # Back pointer query
Relationships = property(GetRelations, SetRelations)
def EnforceRelationship(self, relId, cardinality, directionality="directional"): pass

# persistence related
objects: Namespace
def dumps(self) -> bytes:
def loads(asbytes: bytes) -> RelationshipManagerPersistent: # @staticmethod
```

The abbreviated Relationship Manager API is typically only used in unit tests and some documentation:

```python
def ER(self, relId, cardinality, directionality="directional"): # EnforceRelationship
def R(self, fromObj, toObj, relId=1):  # AddRelationship
def P(self, fromObj, relId=1):  # findObjectPointedToByMe
def PS(self, fromObj, relId=1):  # findObjectsPointedToByMe
def B(self, toObj, relId=1):  # findObjectPointingToMe
def NR(self, fromObj, toObj, relId=1):  # RemoveRelationships
def CL(self):  # Clear

# No abbreviated API for the following:
def FindObjects(self, From=None, To=None, RelId=1) -> Union[List[object], bool]: pass
def FindObject(self, From=None, To=None, RelId=1) -> object: pass
Relationships = property(GetRelations, SetRelations)
# No abbreviated API for the persistence API:
objects: Namespace
def dumps(self) -> bytes:  # pickle persistence related
def loads(asbytes: bytes) -> RelationshipManagerPersistent:
```

All possible permutations of using this abbreviate API approach can be found in 
`tests/python/test_enforcing_relationship_manager.py`. Using these shorter names in unit tests was helpful in testing Relationship Manager itself, however you should probably use the proper long method names in your own code.

Finally, you can import the shorter relationship manager class `RM` - which is equivalent to the usual `RelationshipManager` class.

```python
from relmgr import RelMgr
```

## Hiding the use of Relationship Manager

Its probably best practice to hide the use of Relationship Manager and simply use it as
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
from relmgr import RelMgr

RM = RelMgr()

class X:
    def __init__(self):        RM.ER("xtoy", "onetoone", "directional")
    def setY(self, y):         RM.R(self, y, "xtoy")
    def getY(self):     return RM.P(self, "xtoy")
    def clearY(self):          RM.NR(self, self.getY(), "xtoy")

class Y:
    pass
```

Note the use of the abbreviated Relationship Manager API in this example.

### Another example

Here is another example of hiding the use of Relationship Manager, 
found in the examples folder as `relmgr/examples/observer.py` - the
classic Subject/Observer pattern:

```python
from relmgr import RelationshipManager


rm = RelationshipManager()


class Observer:
   
    @property
    def subject(self):
        return rm.FindObjectPointedToByMe(self)

    @subject.setter
    def subject(self, _subject):
        rm.AddRelationship(self, _subject)

    def Notify(self, subject, notificationEventType):
        pass  # implementations override this and do something


class Subject:

    def NotifyAll(self, notificationEventType):
        observers = rm.FindObjects(None, self)  # all things pointing at me
        for o in observers:
            o.Notify(self, notificationEventType)

    def AddObserver(self, observer):
        rm.AddRelationship(observer, self)

    def RemoveObserver(self, observer):
        rm.RemoveRelationships(From=observer, To=self)
```

## Persistence

The easiest approach to persistence is to use the built in `dumps` and `loads`
methods of `RelationshipManager`. Relationship Manager also provides an attribute
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
from relmgr import RelationshipManager
from dataclasses import dataclass

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

### Persistence API

As a reminder, the persistence API of `RelationshipManager` is:

```python
objects: Namespace  

def dumps(self) -> bytes:

@staticmethod
def loads(asbytes: bytes) -> RelationshipManagerPersistent:
```

Please create attributes on the `objects` property of the relationship manager, pointing to those objects involved in relationships. It is however optional, and only provides a guaranteed way of pickling and persisting the objects involved in the relationships along with the relationships themselves, when persisting the relationship manager.  

You could attach your other application state to this `objects` property of the relationship manager and thus save your entire application state into the same file.  Alternively save the pickeled bytes into your own persistence file solution.

There are currently no `dump()` or `load()` methods implemented, which would pickle
to and from a *file*. These can easily be added in a subclass or just write and
read the results of the existing `dumps()` and `loads()` methods to a file
yourself, as bytes.

### Manual Control of Persistence

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
`relmgr/examples/persistence/persist_pickle.py`
as well as other persistence approaches in that directory, including an approach which 
stores objects in dictionaries with ids and uses the Relationship Manager to store relationships between those ids, rather than relationships between object references.

## Running the tests

Check our this project from GitHub, open the project directory in vscode and there is a local `settings.json` and `launch.json` already populated which means you can choose the launch profile `Run all tests: using -m unittest` or use the vscode built in GUI test runner (hit the `Discover Tests` button then the `Run all tests` button).

Or simply:

```shell
python -m unittest discover -p 'test*' -v tests
```

## Appendix: Installing into a new virtual environment

Either use `pipenv` to manage a new virtual environment or use Python's built in `venv`:

```shell
mkdir proj1
cd proj1
python -m venv env

env/bin/pip install relationship-manager
env/bin/python
> from relmgr import RelationshipManager
```

You can activate the virtual environment after you create it, which makes running `pip` and `python` etc. easier

```
mkdir proj1
cd proj1
python -m venv env

source env/bin/activate
pip install relationship-manager
python
> from relmgr import RelationshipManager
```

# Final Thoughts on the Python Implementation

## References and memory

Be careful - the Relationship Manager will have references to your objects so garbage collection may not be able to kick in. If you remove all relationships for an object it should be removed from the Relationship Manager, but this needs to be verified in these implementations.

## Performance

Be mindful that normal object to object wiring using references and lists of references is going to be much faster than a Relationship Manager.

You can have multiple relationship manager instances to manage different areas of your programming domain, which increases efficiency and comprehensibility.

You may want to google for other more professional [Object Databases](https://en.wikipedia.org/wiki/Object_database). For example, in the Python space we have:

- https://github.com/grundic/awesome-python-models - A curated list of awesome Python libraries, which implement models, schemas, serializers/deserializers, ODM's/ORM's, Active Records or similar patterns.
- https://www.opensourceforu.com/2017/05/three-python-databases-pickledb-tinydb-zodb/ - A peek at three Python databases: PickleDB, TinyDB and ZODB
- https://tinydb.readthedocs.io/en/stable/usage.html#queries - Welcome to TinyDB, your tiny, document oriented database optimized for your happiness
- https://divmod.readthedocs.io/en/latest/products/axiom/index.html - Axiom is an object database whose primary goal is to provide an object-oriented layer to an SQL database
- http://www.newtdb.org/en/latest/getting-started.html - Newt DB - You’ll need a Postgres Database server.
- http://www.zodb.org/en/latest/tutorial.html#tutorial-label - This tutorial is intended to guide developers with a step-by-step introduction of how to develop an application which stores its data in the ZODB.

However most of these need a backing SQL database - Relationship Manager does not, which may be a benefit - no databases to set up - just get on with coding.

# Other implementations of Relationship Manager 

In this Github repository there are several other implementations of Relationship Manager 

## C#

Very fast implementation for .NET - has been used in a commercial project. Note that the Visual Studio 2005 projects/solutions need updating to a more recent version of Visual Studio.

## Boo

The [boo language](http://boo-language.github.io/) for .NET is now dead, however this implementation created a .net `.dll` that was usable by other .NET languages.  This dll is still in the project and perfectly usable, however the C# implementation is much faster.

## Java

A java implementation.

## Javascript

To be completed.

