The abbreviated Relationship Manager API is typically only used in unit tests and some documentation:

This API is now deprecated.

```python
class RelationshipManager():
    ## Short API

    def ER(self, relId, cardinality, directionality="directional"):
        self.enforce(relId, cardinality, directionality)

    def R(self, source, target, relId=1):
        self.add_rel(source, target, relId)

    def P(self, source, relId=1):
        # rm.find_target(source, rel_id)
        return self.rm._find_object(source, None, relId)

    def B(self, target, relId=1):
        # rm.find_source(taget, rel_id)
        return self.rm._find_object(None, target, relId)

    def PS(self, source, relId=1):
        # rm.find_targets(source, rel_id)
        return self.rm._find_objects(source, None, relId)

    def NR(self, source, target, relId=1):
        self.remove_rel(source, target, relId)

    def CL(self):
        self.clear()
```

## Even older doco on this

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
