# Old Python versions of Relationship Manager 

These only cover the core functionality and core data structures. 

There are more layers added via inheritence, to make the modern Relationship Manager, like the 'relationships' property, constraints and persistence, which are not covered by these.

- `RelationshipManagerOriginal` - original, as published in Andy Bulka's original design pattern.
- `RelationshipManagerOriginalBetterFindObjects` - original with more options to the find method.
- `EfficientRelationshipManagerBuggy` - keeps track of reverse relationships but only allows one relationship id between source and target. It really needed to hold a list of relationships ids per source and target, which the next version did.
- `EfficientRelationshipManager` - latest.

## Tests against these old versions

Just as a curiosity, running these core implementations against current latest 2020 tests yields the following results:

| import | test results |
|--------|--------------|
| from `relmgr.old.v0_rel_mgr_original` import RelationshipManagerOriginal as RMCoreImplementation | 8 test failures |
| from `relmgr.old.v1_rel_mgr_original_better_findobjects` import RelationshipManagerOriginalBetterFindObjects as RMCoreImplementation | 2 test failures |
| from `relmgr.old.v2_rel_mgr_efficient_buggy` import EfficientRelationshipManagerBuggy as RMCoreImplementation | 12 test failures |
| from `relmgr.old.v3_rel_mgr_efficient` import EfficientRelationshipManager as RMCoreImplementation | 0 test failures |

### Comments on the tests

The reason the later `v2_rel_mgr_efficient_buggy` does worse in the tests than the earlier versions (even the original implementation does better) is because the original implementations used a flat list to hold all relationships e.g.
```python
[('a', 'b', 1), ('a', 'b', 2)]
```
so multiple relationships ids per source and target were possible, even then. Whilst accurate, it wasn't that great, efficiency wise, compared to the modern dictionary based approach viz.
```python
{'a': {'b': [1, 2]}}
```

## The Relationship Manager data structure

The original implementations v0, v1 used a flat list of relationship tuples. The later implementations v2, v3 used a dictionary of dictionaries - thus lookup becomes much faster.

Assuming we create some relationships like this:

```python
import pprint

rm = RelationshipManager()
rm.AddRelationship('a', 'b', 1)
rm.AddRelationship('a', 'b', 2)
rm.AddRelationship('a', 'x', 1)
rm.AddRelationship('fred', 'mary', 1)
pprint.pprint(rm.Relations)
```

### original

```python
[
    ('a', 'b', 1), 
    ('a', 'b', 2), 
    ('a', 'x', 1), 
    ('fred', 'mary', 1)
]
```

### modern

```python
{
    'a': {
        'b': [1, 2], 
        'x': [1]
    }, 
    'fred': {'mary': [1]}
}
```

Note also that the dictionary based Python implementation also simultaneously model the reverse relationships in a mirror backward relationship dictionary - so that backward pointer lookups are just as fast as forward relationships. So for the above example:

```python
{
    'b': {
        'a': [1, 2]
    }, 
    'mary': {
        'fred': [1]
    }, 
    'x': {
        'a': [1]
    }
}
```

Ironically, the modern `.Relationships` property returns a flat list of relationship tuples, just like the original implementation. The setter for the `.Relationships` property accepts a flat list of relationship tuples and builds the more optimised data structure. The reason for this is unclear - probably for simpler persistence or testing? Whilst pickle is unlikely to be thrown by saving a Relationship Manager with dictionaries possibly other persistence methods might prefer such a flat list.