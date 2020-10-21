# Future API ideas

## import a shorter name

```python
from relmgr import RelMgr
```

# persistence api enhancement

Maybe

```python
# potential replacement or extension to persisting objects
objects_dict: Dict  # alternative place for storing objects

# potential extension to persistence objects
add_obj(self, obj, obj_id: str)
get_obj(self, obj_id: str) -> object:
remove_obj(self, obj) -> None:
```
