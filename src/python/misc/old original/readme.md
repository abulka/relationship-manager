# Old versions

Core Implementations of Relationship Manager - various:

- RelationshipManagerOriginal
- RelationshipManagerOriginal2
- BigRelationshipManager1
- EfficientRelationshipManager1 (latest)

## Tests against these old versions

| import | test results |
|--------|--------------|
| from `src.core.v0_rel_mgr_original` import RelationshipManagerOriginal as RMCoreImplementation | 8 test failures |
| from `src.core.v1_rel_mgr_original_better_findobjects` import RelationshipManagerOriginalBetterFindObjects as RMCoreImplementation | 2 test failures |
| from `src.core.v2_rel_mgr_efficient_buggy` import EfficientRelationshipManagerBuggy as RMCoreImplementation | 12 test failures |
| from `src.core.v3_rel_mgr_efficient` import EfficientRelationshipManager as RMCoreImplementation | 0 test failures |

### Old import statements

```python
from src.core.v0_rel_mgr_original import RelationshipManagerOriginal as RMCoreImplementation
from src.core.v1_rel_mgr_original_better_findobjects import RelationshipManagerOriginalBetterFindObjects as RMCoreImplementation
from src.core.v2_rel_mgr_efficient_buggy import EfficientRelationshipManagerBuggy as RMCoreImplementation
from src.core.v3_rel_mgr_efficient import EfficientRelationshipManager as RMCoreImplementation
```
