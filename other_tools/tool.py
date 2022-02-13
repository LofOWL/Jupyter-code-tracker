import set_env
from nbdime2format import convert_nbdime,nbdime
from notebook_utils import collect_mapping, extract_lines,merge_split,replace_mapping, find_move_mapping,find_split
from sort import cell_sorted
from utils import filter_cell
from line_mapping_algorithm import lcs

from notebook import Notebook

def show(output):
	for i in output:
		if i[1] == None:
			print(f'C{i[0]} --- ')
		elif i[0] == None:
			print(f'--- C{i[1]}')
		elif type(i[1]) == str:
			print(f'C{i[0]} --- C{i[1]}')
		else:
			add = ','.join([f'C{i}m' for i in i[1]])
			print(f'C{i[0]} --- {add}')

def CellMapping(old,new):
	# convert nbdime
	output = nbdime(old.path,new.path)
	output = convert_nbdime(output)
	output = collect_mapping(output,len(old.cells),len(new.cells))

	output = cell_sorted(output)
	#show(output)
	mapping = output[:]
	#print("---")

	# find all the lines from old version and new version
	output = filter_cell(output)
	old_lines,new_lines = extract_lines(output,old,new)

	# get the lines mapping
	output = lcs(old_lines,new_lines)

	# get the split
	split = find_split(output,old,new)

	# get the merge and split
	#merge,split = merge_split(output)
	#print(merge)

	# new mapping
	output = replace_mapping(mapping,split)	
	#show(output)

	#print("---")	
	# move mapping
	output = find_move_mapping(output,old,new)
	#show(output)

	return output

if __name__ == "__main__":
	#old_path = '/home/lofowl/Desktop/CISC834/project/Jupyter-cell-evoluation/lib/cache/376b094aa6a3f4572774e15e7659af9eb82981b3_graphics#graphics.ipynb'
	#new_path = '/home/lofowl/Desktop/CISC834/project/Jupyter-cell-evoluation/lib/cache/8336e016614e784c0ca8820574798ab3e8606732_graphics#graphics.ipynb'
	#old_path = '/home/lofowl/Desktop/old1.ipynb'
	#new_path = '/home/lofowl/Desktop/new1.ipynb'
	#old_path = "/media/lofowl/My Passport/CISC834/notebook_cache/f6cb8be5c0439546057ec8ae1557fa918f7ec746_lab_sessions#lab3#Lab3-Assignment.ipynb"
	#new_path = "/media/lofowl/My Passport/CISC834/notebook_cache/5bd61e0b276b4eb3ee30d67497795f4ad52f02e0_lab_sessions#lab3#Lab3-Assignment.ipynb"
	old_path = "/media/lofowl/My Passport/CISC834/notebook_cache/113bcfb40d219ab484461375b30439039ac95d7a_bin#plot_profile.ipynb"
	new_path = "/media/lofowl/My Passport/CISC834/notebook_cache/44e77fb47c3dac018079c26643bc1a7634c5c24d_bin#plot_profile.ipynb"
	old,new = Notebook(old_path),Notebook(new_path)		
	output = CellMapping(old,new)
	print(output)
