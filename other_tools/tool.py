import set_env
from main import convert_nbdime,nbdime
from notebook_utils import collect_mapping, extract_lines,merge_split,replace_mapping, find_move_mapping
from sort import cell_sorted
from utils import filter_cell
from line_mapping_algorithm import lcs

from notebook import Notebook

def CellMapping(old,new):
	# convert nbdime
	output = nbdime(old.path,new.path)
	output = convert_nbdime(output)
	output = collect_mapping(output,len(old.cells),len(new.cells))
	identical = [[int(mapping[0]),int(mapping[1])] for mapping in output if mapping[1] and mapping[1][-1] != 'm' and mapping[0]]
	output = cell_sorted(output)
	mapping = output[:]
	# print("---")

	# find merge & split
	output = filter_cell(output)
	old_lines,new_lines = extract_lines(output,old,new)
	output = lcs(old_lines,new_lines)
	merge,split = merge_split(output)

	# new mapping
	output = replace_mapping(mapping,merge)	
	# for i in output:
	# 	if i[1] == None:
	# 		print(f'C{i[0]} --- ')
	# 	elif i[0] == None:
	# 		print(f'--- C{i[1]}')
	# 	elif type(i[1]) == str:
	# 		print(f'C{i[0]} --- C{i[1]}')
	# 	else:
	# 		add = ','.join([f'C{i}m' for i in i[1]])
	# 		print(f'C{i[0]} --- {add}')

	# print("---")	
	# move mapping
	output = find_move_mapping(output,old,new)
	# for i in output:
	# 	if i[1] == None:
	# 		print(f'C{i[0]} --- ')
	# 	elif i[0] == None:
	# 		print(f'--- C{i[1]}')
	# 	elif type(i[1]) == str:
	# 		print(f'C{i[0]} --- C{i[1]}')
	# 	else:
	# 		add = ','.join([f'C{i}m' for i in i[1]])
	# 		print(f'C{i[0]} --- {add}')
	return output

if __name__ == "__main__":
	#old_path = '/home/lofowl/Desktop/CISC834/project/Jupyter-cell-evoluation/lib/cache/376b094aa6a3f4572774e15e7659af9eb82981b3_graphics#graphics.ipynb'
	#new_path = '/home/lofowl/Desktop/CISC834/project/Jupyter-cell-evoluation/lib/cache/8336e016614e784c0ca8820574798ab3e8606732_graphics#graphics.ipynb'
	old_path = "/media/lofowl/My Passport/CISC834/notebook_cache/e4b53b93bf0f2a5d4803457d6b6cb57cc4517019_galleryTestFunctions.ipynb"
	new_path = "/media/lofowl/My Passport/CISC834/notebook_cache/15e288a9605c778bd8976bdcb93f4e19009ace23_galleryTestFunctions.ipynb"
	#old_path = '/home/lofowl/Desktop/old1.ipynb'
	#new_path = '/home/lofowl/Desktop/new1.ipynb'
	old,new = Notebook(old_path),Notebook(new_path)		
	output = CellMapping(old,new)
	print(output)
