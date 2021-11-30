import os
import sys
path = os.path.abspath(os.path.join(os.path.dirname(__file__)))+'/mapping/data'
print(path)
sys.path.insert(0,path)

from data import OLD,NEW

