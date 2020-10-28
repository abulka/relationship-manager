# Relationship Manager - a lightweight Object Database class

A central mediating class which records all the one-to-one, one-to-many and many-to-many relationships between a group of classes. 

## What is it?

Classes that use a Relationship Manager to implement their relationship properties and methods have a consistent metaphor and trivial implementation code (one line calls). In contrast - traditional "pointer" and "arraylist" techniques of implementing relationships are fully flexible but often require a reasonable amount of non-trivial code which can be tricky to get working correctly and are almost always a pain to maintain due to the detailed coding and coupling between classes involved, especially when back-pointers are involved.

Using a `Relationship Manager` object to manage the relationships can mitigate these problems and make managing relationships straightforward. It also opens up the possibility of powerful querying of relationships, a very simple version of something like [LINQ](https://docs.microsoft.com/en-us/dotnet/csharp/programming-guide/concepts/linq/).

In a sense, an [Object Database](https://en.wikipedia.org/wiki/Object_database)
is an elaborate implementation of the Relationship Manager pattern. However the
*intent* of the Relationship Manager pattern is lighter weight, to replace the
wirings between objects rather than acting as a huge central database on disk -
though persistence is built into Relationship Manager too.

Here are various implementations of the Relationship Manager Pattern in this GitHub repository:

- Python: Uses Python 3, there are no dependencies.
- C#: Used in at least one major commercial product. Implementations for .NET4 and .NET Core 3.1 (the latter project is cross platform and has been verified to run on Mac using [Visual Code for Mac](https://visualstudio.microsoft.com/vs/mac/)).
- Java

# Python

## Installation

```shell
pip install relationship-manager
```

## Usage

```python
from relmgr import RelationshipManager
  
rm = RelationshipManager()
rm.enforce("xtoy", "onetoone", "directional")
x = object()
y = object()
rm.add_rel(x, y, "xtoy")
assert rm.find_target(x, "xtoy") == y
```

- Read the unit tests to see all functionality being exercised, incl. backpointer queries. 
- See the examples below and in the `relmgr/examples/` directory of this repository.
- See full [API documentation](https://abulka.github.io/relationship-manager/relmgr/index.html).
- See the Relationship Manager pattern referred to above for lots more documentation.

## Python API

Quick summary of the v2 API:

```python
def add_rel(self, source, target, rel_id: Union[int,str]=1) -> None:
def remove_rel(self, source, target, rel_id=1) -> None:
def enforce(self, rel_id, cardinality, directionality="directional"):
def clear(self) -> None:

# query API
def find_targets(self, source, rel_id) -> List:
def find_target(self, source, rel_id) -> object:
def find_sources(self, target, rel_id) -> List: # Back pointer query
def find_source(self, target, rel_id) -> object: # Back pointer query
def find_rels(self, source, target) -> List:
def is_rel(self, source, target, rel_id=1) -> bool:

# persistence related
objects: Namespace
relationships = property(_get_relationships, _set_relationships)  # flat list of rel. tuples
def dumps(self) -> bytes:
def loads(asbytes: bytes) -> RelationshipManager:  # @staticmethod
```

See full [API documentation](https://abulka.github.io/relationship-manager/relmgr/index.html).

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
    def __init__(self):        rm.enforce("xtoy", "onetoone", "directional")
    def setY(self, y):         rm.add_rel(self, y, "xtoy")
    def getY(self):     return rm.find_target(source=self, rel_id="xtoy")
    def clearY(self):          rm.remove_rel(self, self.getY(), "xtoy")

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
        return rm.find_target(self)

    @subject.setter
    def subject(self, _subject):
        rm.add_rel(self, _subject)

    def notify(self, subject, notification_type):
        pass  # implementations override this and do something


class Subject:

    def notify_all(self, notification_type: str):
        observers = rm.find_sources(self)  # all things pointing at me
        for o in observers:
            o.Notify(self, notification_type)

    def add_observer(self, observer):
        rm.add_rel(observer, self)

    def remove_observer(self, observer):
        rm.remove_rel(source=observer, target=self)

```

When using the Subject and Observer, you use their methods without realising their functionality has been implemented using rm.  See `tests/python/examples/test_observer.py` in the GitHub project for the unit tests for this code.

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
from dataclasses import dataclass
from relmgr import RelationshipManager

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

rm.add_rel(obj1, obj2)
rm.add_rel(obj1, obj3)
assert rm.find_targets(obj1) == [obj2, obj3]

# persist
asbytes = rm.dumps()

# resurrect
rm2 = RelationshipManager.loads(asbytes)

# check things worked
newobj1 = rm2.objects.obj1
newobj2 = rm2.objects.obj2
newobj3 = rm2.objects.obj3
assert rm2.find_targets(newobj1) == [newobj2, newobj3]
assert rm2.find_target(newobj1) is newobj2

print('done, all OK')
```

### Persistence API

As a reminder, the persistence API of `RelationshipManager` is:

```python
objects: Namespace  

def dumps(self) -> bytes:

@staticmethod
def loads(asbytes: bytes) -> RelationshipManager:
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

For code examples of custom persistence, see 
`research/python persistence research/persist_pickle_simple.py`
as well as other persistence approaches in that directory, including an approach which 
stores objects in dictionaries with ids and uses the Relationship Manager to store relationships between those ids, rather than relationships between object references.

## Running the tests

### Python tests

Check our this project from GitHub, open the project directory in vscode and there is a local `settings.json` and `launch.json` already populated which means you can choose the launch profile `Run all tests: using -m unittest` or use the vscode built in GUI test runner (hit the `Discover Tests` button then the `Run all tests` button).

Or simply:

```shell
python -m unittest discover -p 'test*' -v tests
```

### C# and Java tests

Open the projects and run the tests from your IDE.

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

- A [curated list](https://github.com/grundic/awesome-python-models) of awesome Python libraries, which implement models, schemas, serializers/deserializers, ODM's/ORM's, Active Records or similar patterns.
- A peek at [three Python databases](https://www.opensourceforu.com/2017/05/three-python-databases-pickledb-tinydb-zodb/): PickleDB, TinyDB and ZODB. Also see the [welcome to TinyDB](https://tinydb.readthedocs.io/en/stable/usage.html#queries), your tiny, document oriented database optimized for your happiness, and a [tutorial on ZODB](http://www.zodb.org/en/latest/tutorial.html#tutorial-label).
- [Axiom](https://divmod.readthedocs.io/en/latest/products/axiom/index.html) is an object database whose primary goal is to provide an object-oriented layer to an SQL database.
- [Newt DB](http://www.newtdb.org/en/latest/getting-started.html) - You’ll need a Postgres Database server.

However most of these need a backing SQL database - Relationship Manager does not, which may be a benefit - no databases to set up - just get on with coding!

# C# and Java implementations of Relationship Manager 

In this Github repository there are several other implementations of Relationship Manager. Currently only the Python implementation uses the newer v2 API and implementation. The C# and Java implementations use the v1 API.

The C# and Java implementations have a strict, typed API interface `IRelationshipManager` to talk to.

## C#

A fast implementation for .NET - has been used in a major commercial project.
- `csharp-net4` uses the .NET 4 framework.
- `csharp-netcore` is the same code, using the new .NET Core 3.1 framework. This solution also loads and runs OK in [Visual Code for Mac](https://visualstudio.microsoft.com/vs/mac/).
 
## Java

A Java implementation.  Needs a bit of dusting off, but should run.

## C# and Java API

> Note: C# and Java implementations use the original older v1 API, not the new v2 API implemented in Python, above.

```java
public enum Cardinality  
{  
    OneToOne,  
    OneToMany,  
    ManyToOne,  
    ManyToMany  
}

public enum Directionality  
{  
    UniDirectional,  
    DirectionalWithBackPointer,  
    DoubleDirectional  
}

interface IRelationshipManager {
  void AddRelationship(object fromObj, object toObj, string relId);  
  void AddRelationship(object fromObj, object toObj);  // overloaded, uses a default relId
  void EnforceRelationship(string relId, Cardinality cardinality);    // overloaded, uses a default directionality
  void EnforceRelationship(string relId, Cardinality cardinality, Directionality directionality);  
  IList FindObjectsPointedToByMe(object fromObj, string relId);  
  object FindObjectPointedToByMe(object fromObj, string relId);  
   IList FindObjectsPointingToMe(object toObj, string relId);  
  object FindObjectPointingToMe(object toObj, string relId);  
  void RemoveRelationship(object fromObj, object toObj, string relId);  
  void RemoveAllRelationshipsInvolving(object obj, string relId);  
  int Count();  
  int CountRelationships(string relId);  
  void Clear();  
  bool DoesRelIdExistBetween(object fromObj, object toObj, string relId);  
  IList FindRelIdsBetween(object fromObj, object toObj);
}
```

Both `from` and `to` (aka. `source` and `target`) are *your* object instances that you want to record a relationship between.
After a Find... call you may need to `cast` to a type, as I think every object is stored as a `object` type. Relationship Manager really needs to use generics to avoid this. The Python implementation doesn't need to deal with this issue because it is dynamically typed.

### C# and Java abbreviated API

The abbreviated API is more succinct, but is only recommended for unit tests. In the abbreviated API:
- `f` means `from` (or the more modern v2. API name of `source`).
- `t` means `to` (or the more modern v2. API name of `target`). It is one of *your* object instances.

```csharp
public interface IRM
{
    object B(object toObj, string relId);
    System.Collections.IList BS(object toObj, string relId);
    void ER(string relId, Cardinality cardinality);
    void ER(string relId, Cardinality cardinality, Directionality directionality);
    void NR(object fromObj, object toObj, string relId);
    void NRS(object obj, string relId);
    object P(object fromObj, string relId);
    System.Collections.IList PS(object fromObj, string relId);
    void R(object fromObj, object toObj, string relId);
    bool QR(object fromObj, object toObj, string relId);
    int Count();
    int CountRelationships(string relId);
    void Clear();
}
```

### API v1 and v2 equivalence table

This table also shows the equivalent modern Python v2 API call for each method in the C#/Java v1 API.

| Return Type            | C#/Java Method (v1 API) | Abbreviated (v1) | Python (v2 API)            |
|------------------------|-------------------------|------------------|----------------------------|
| void   | `AddRelationship`(from, to, id)       | `R`(f, t, id)        | `add_rel`(source, target, rel_id=1) -> None |
| void   | `RemoveRelationship`(from, to, id)    | `NR`(f, t, id)       | `remove_rel`(source, target, rel_id=1) -> None |
| void   | `RemoveAllRelationshipsInvolving`(object, id) | `NRS`(o, id) | `remove_rel`(source, target, rel_id=1) -> None |
| List   | `FindObjectsPointedToByMe`(from, id)  | `PS`(f, id)          | `find_targets`(source, rel_id=1) -> List |
| object | `FindObjectPointedToByMe`(from, id)   | `P`(f, id)           | `find_target`(source, rel_id=1) -> object |
| List   | `FindObjectsPointingToMe`(to, id)     | `BS`(t, id)          | `find_sources`(target, rel_id=1) -> List |
| object | `FindObjectPointingToMe`(to, id)      | `B`(t, id)           | `find_source`(target, rel_id=1) -> object |
| void   | `EnforceRelationship`(id, cardinality, bidirectionality) | `ER`(id, c, bi) | `enforce`(rel_id, cardinality, directionality="directional") |
| bool   | `DoesRelIdExistBetween`(from, to, id) | `QR`(f, t, id)       | `is_rel`(source, target, rel_id=1) -> bool |
| IList  | `FindRelIdsBetween`(from, to)         | -                    | `find_rels`(self, source, target) -> List |
| void   | `Clear`()                             | `Clear`()            | `clear`(self) -> None |
| void   | `Count`()                             | `Count`()            | - |
| void   | `CountRelationships`(id)              | `CountRelationships`(id) | - |
|        | -                                     | -                    | `relationships` *property* |
|        | -                                     | -                    | `dumps`() -> bytes |
|        | -                                     | -                    | `loads`(asbytes: bytes): -> RelationshipManager |

### C# and Java - Finding just one object

The pair of find methods `FindObjectPointedToByMe()` and `FindObjectPointedToByMe()` only find _one_ object (even though there may be more).  This is a commonly used convenience method - the more painful way would be to use `FindObjectsPointingToMe()` and just grab the first object from the returned list.
Exactly which object is found is undefined, but would typically be the first one added.

### C# and Java - Relationship Id

What to use as the Relationship Id?

This is traditionally either an `integer` or a `string` in the Python implementation.  I have chosen to only use a `string` type in the C# and Java implementations, since you can describe relationships easily in this way rather than having to map from an integer back to some meaningful description.

```csharp
rm.AddRelationship(fromObject, toObject, relationshipId)
```

will raise an exception if relationshipId is an empty string.  TODO: Presumably an empty relationship id should be treated like in Python, as the default relationship.

TODO: The use of "\*" as relationship id which matches any relationship needs to be verified in the C# and Java implementations, (not sure its implemented or needed) so please disregard the following comment for now: ~~All other functions (except for `AddRelationship`) can pass either an empty string or "\*" as the `relationshipId`, which means you are searching for any relationship at all.  You would usually only want to do this if there is only _one_ relationship between class X and class Y, then your `P` and `NR` calls can specify "\*" as the `relationshipId` in order to match any relationship between these two objects.  Alternatively, you can use relationship manager's overloaded versions of all its routines (except for `AddRelationship`) which don't take a `relationshipId` where `relationshipId` defaults to "\*".~~

### C# Usage

In your project, add references to

![Adding refs](http://www.andypatterns.com/files/85941233059578rmdotnetRefs1.png)

and in your code add the using clauses:

```csharp
using RelationshipManager.Interfaces;
using RelationshipManager.Turbo;
```

There are a number of directories in the project, but you really only need to reference the two dll's 

```
Relationship Manager Interfaces.dll
Relationship Manager Turbo.dll
```

to use Relationship Manager.

#### Example 1

```csharp
private IRelationshipManager rm;
rm = new RelationshipMgrTurbo();
rm.AddRelationship('a', 'b', "rel1");
IList list = rm.FindObjectsPointedToByMe('a', "rel1");
Assert.AreEqual(list[0], 'b');
```

#### Example 2

```csharp
private IRelationshipManager rm;
rm = new RelationshipMgrTurbo();
rm.AddRelationship('a', 'b', "rel1");
rm.AddRelationship('a', 'c', "rel1");
rm.AddRelationship('a', 'z', "rel2");
IList list;
list = rm.FindObjectsPointedToByMe('a', "rel1");
char[] expected = {'b', 'c'};
Assert.AreEqual(list.ToString(), new ArrayList(expected).ToString());
list = rm.FindObjectsPointedToByMe('a', "rel2");
Assert.AreEqual(list[0], 'z');
```

#### Example Person Order

This example project is available the .net core version of the Relationship Manager C# implementation. Note that the use of Relationship Manager is hidden, and is a mere implementation detail.

```csharp
using System;
using System.Collections;
using System.Collections.Generic;
using RelationshipManager.Interfaces;
using RelationshipManager.Turbo;

namespace Example_Person_Order_Console_App
{
    class Program
    {
        static void Main(string[] args)
        {
            var jane = new Person("Jane");
            var order1 = new Order("Boots");
            var order2 = new Order("Clothes");
            jane.AddOrder(order1);
            jane.AddOrder(order2);

            // test forward pointer wiring
            Console.WriteLine(jane + " has " + jane.GetOrders().Count + " orders");

            // test the backpointer wiring
            foreach (var order in jane.GetOrders())
            {
                Console.WriteLine("The person who ordered " + order + " is " + order.GetPerson());
            }

            Console.WriteLine("Done!");

        }

        ///   
        /// BO is the base Business Object class which holds a single static reference  
        /// to a relationship manager. This one relationship manager is  
        /// used for managing all the relationships between Business Objects
        /// like Person and Order.  
        ///   
        public class BO // Base business object  
        {
            static protected RelationshipMgrTurbo rm = new RelationshipMgrTurbo();
        }


        ///   
        /// Person class points to one or more orders.  
        /// Implemented using a relationship manager rather   
        /// than via pointers and arraylists etc.  
        ///   
        public class Person : BO
        {
            public string name;

            static Person()
            {
                rm.EnforceRelationship("p->o", Cardinality.OneToMany, Directionality.DirectionalWithBackPointer);
            }

            public Person(string name)
            {
                this.name = name;
            }

            public override string ToString()
            {
                return "Person: " + this.name;
            }

            public void AddOrder(Order o)
            {
                rm.AddRelationship(this, o, "p->o");
            }

            public void RemoveOrder(Order o)
            {
                rm.RemoveRelationship(this, o, "p->o");
            }

            public List<Order> GetOrders()
            {
                IList list = rm.FindObjectsPointedToByMe(this, "p->o");

                // cast from list of 'object' to list of 'Person'
                var result = new List<Order>();
                foreach (var order in list)
                    result.Add((Order)order);

                // attempts at other simpler ways to cast a whole list
                //result = list as List<Order>;  // crash
                //result = new List<Order>(list); // syntax error?

                return result;
            }
        }

        ///   
        /// Order class points back to the person holding the order.  
        /// Implemented using a relationship manager rather
        /// than via pointers and arraylists etc.  
        ///  
        public class Order : BO
        {
            public string description;

            public Order(string description)
            {
                this.description = description;
            }

            public override string ToString()
            {
                return "Order Description: " + this.description;
            }

            public void SetPerson(Person p)
            {
                // though mapping is bidirectional, there is still a primary relationship direction!
                rm.AddRelationship(p, this, "p->o");

            }

            public Person GetPerson()
            {
                // cast from 'object' to 'Person'
                return (Person)rm.FindObjectPointingToMe(this, "p->o");
            }

            public void ClearPerson()
            {
                rm.RemoveRelationship(this, this.GetPerson(), "p->o");
            }
        }

    }

}
```

Output:

```
Person: Jane has 2 orders
The person who ordered Order Description: Clothes is Person: Jane
The person who ordered Order Description: Boots is Person: Jane
Done!
```

A generics version of relationship manager would be cool - that way no casting would be required. Presently all calls to relationship manager return objects or lists of objects - which you have to cast to the specific type you actually have stored. You can see this casting in the above example.

#### Other C# examples

Study the unit tests to see how to drive this library even further.

### UML for the C# implementation of Relationship Manager

![UML class diagram](http://www.andypatterns.com/files/60481233059254rmdotnetuml1.png)
UML for the C# version of Relationship Manager.

# Resources

- Full [API documentation](https://abulka.github.io/relationship-manager/relmgr/index.html).

- Official [Relationship Manager Pattern](https://abulka.github.io/projects/patterns/relationship-manager/) page incl. academic paper by Andy Bulka.

- Python Implementation [README](https://github.com/abulka/relationship-manager) (this page) and [GitHub project](https://github.com/abulka/relationship-manager).
