import sys
import os

EXPECTED_DEPENDENCIES_PATH = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
if EXPECTED_DEPENDENCIES_PATH not in sys.path: 
	sys.path.append(EXPECTED_DEPENDENCIES_PATH)

from time import time
from collections import OrderedDict
import json
import hashlib

DEBUG_ENABLE = False