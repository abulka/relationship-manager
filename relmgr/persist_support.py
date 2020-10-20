import copy
import pickle
import pprint
from dataclasses import dataclass
from functools import lru_cache
from typing import Dict, List, Optional, Set, Tuple, Union

# Persistence Helpers

@dataclass
class Namespace:
    """Just want a namespace to store vars/attrs in. Could use a dictionary."""


@dataclass
class PersistenceWrapper:
    """Holds both objects and relationships. Could use a dictionary."""
    objects: Namespace  # Put all your objects involved in relationships as attributes of this object
    relations: List  # Relationship Manager relationship List will go here

