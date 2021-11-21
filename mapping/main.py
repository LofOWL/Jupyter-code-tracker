from cell_mapping.line_mapping import lcs
from cell_mapping.cell_mapping import cell_mapping
from notebook.notebook import Notebook

old = Notebook('old.ipynb')
new = Notebook('new.ipynb')

lcs_result = lcs(old.lines,new.lines)
print(lcs_result)
map_cell = cell_mapping(lcs_result) 
print(map_cell)
 
 
 
