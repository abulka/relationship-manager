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
class InterfaceCoreRelationshipManager:
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
