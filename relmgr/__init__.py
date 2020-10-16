# __init__.py

from relmgr.relationship_manager import RelationshipManager
from relmgr.relationship_manager import RelationshipManager as RelMgr  # shorter name

# Version of relationship-manager package
__version__ = "1.4.2"

__all__ = ["RelationshipManager", "RelMgr"]  # for "from relmgr import *"" syntax
