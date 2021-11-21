import os
import sys
path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.insert(0,path)

from config import *
from line import *
from line_mapping_algorithm import lcs

