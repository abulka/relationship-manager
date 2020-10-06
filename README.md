# Relationship Manager Pattern

A central mediating class which records all the one-to-one, one-to-many and many-to-many relationships between a group of selected classes. 

Official [Relationship Manager Pattern](https://abulka.github.io/blog/2001/08/04/relationship-manager-design-pattern/) page incl. academic paper by Andy Bulka.

## Brief Discussion

In a sense, an [Object Database](https://en.wikipedia.org/wiki/Object_database) is an implementation of the RM pattern. 
The *intent* of the RM pattern is lighter weight, to replace the wirings between objects
rather than acting as a huge central database.

Classes that use a Relationship Manager to implement their relationship properties and methods have a consistent metaphor and trivial implementation code (one line calls). In contrast - traditional "pointer" and "arraylist" techniques of implementing relationships are fully flexible but often require a reasonable amount of non-trivial code which can be tricky to get working correctly and are almost always a pain to maintain due to the detailed coding and coupling between classes involved.




# Implementations

Andy's Relationship Manager Pattern incl. various implementations

## Python

Uses Python 2 (this code was implemented before Python 3 even existed).

Run the tests

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

A java implementation

## Javascript

To be completed.

