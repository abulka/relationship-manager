import sys

"""
If running this script from root of project e.g.

python relmgr/examples/import_eg.py

then do one of the following

1. 
# ensure root of project is in path so modules are found
export PYTHONPATH="$PWD"
python relmgr/examples/persistence/persist_pickle_dict.py

2.
sys.path.append('/Users/Andy/Devel/relationship-manager/')

2A. (better way then 2. - avoids absolute dir reference)
from os.path import dirname, abspath, join
import sys

# Find code directory relative to our directory
THIS_DIR = dirname(__file__)
CODE_DIR = abspath(join(THIS_DIR, '..', 'code'))
sys.path.append(CODE_DIR)
"""

for path in sys.path:
    print(path)

from relmgr import RelationshipManager
print("ok")

