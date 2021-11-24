import os
import sys
path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
# import notebook
notebook_path = os.path.abspath(os.path.join(path,'..'))+"/mapping/notebook"
sys.path.insert(0,notebook_path)
# import data
data_path = os.path.abspath(os.path.join(path,'..'))+"/mapping/data_notebook"
sys.path.insert(0,data_path)
# import lcs and line
lcs_path = os.path.abspath(os.path.join(path,'..'))+'/mapping/cell_mapping/line_mapping'
sys.path.insert(0,lcs_path)
# import lib
lib_path = os.path.abspath(os.path.join(path))+'/lib'
sys.path.insert(0,lib_path)

