"""
Possible revised API
--------------------

def add_rel(self, source, target, rel_id: Union[int,str]=1) -> None: pass
def remove_rel(self, source, target, rel_id=1) -> None: pass
TODO def targets_of(self, source, rel_id) -> List: pass
TODO def sources_to(self, target, rel_id) -> List: pass # Back pointer query
def enforce(self, rel_id, cardinality, directionality="directional"): pass
def clear(self) -> None: pass

# convenience - return the first object 
def target_of(self, source, rel_id) -> object: pass
def source_to(self, target, rel_id) -> object: pass # Back pointer query

# low level
def _find_objects(self, source=None, target=None, rel_id=1) -> Union[List[object], bool]: pass
def _find_object(self, source=None, target=None, rel_id=1) -> object: pass

# persistence related
objects: Namespace
relationships = property(_get_relationships, _set_relationships)  # flat list of rel. tuples
def dumps(self) -> bytes:
def loads(asbytes: bytes) -> RelationshipManager:  # @staticmethod

# potential replacement or extension to persisting objects
objects_dict: Dict  # alternative place for storing objects

# potential extension to persistence objects
add_obj(self, obj, obj_id: str)
get_obj(self, obj_id: str) -> object:
remove_obj(self, obj) -> None:
"""
