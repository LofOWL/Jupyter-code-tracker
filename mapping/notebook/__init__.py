import os
import sys
path = os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))+'/cell_mapping'
#print(f'__init__.notebook {path}')
sys.path.insert(0,path)
current_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
#print(f'__init__.notebook {current_path}')
sys.path.insert(1,current_path)

