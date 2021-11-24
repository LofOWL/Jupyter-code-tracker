import set_env
from data import OLD_PATH,NEW_PATH
from data import OLD,NEW

import subprocess
import re

from line_mapping import lcs,line,convert_lines

ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
nbdime = lambda x,y: subprocess.getoutput(f'nbdiff -s {x} {y}')

def convert(output):
	output = ansi_escape.sub('',output)
	sentences = output.split("\n")
	# divide the output into each cell
	changes = list()
	for sentence in sentences:
		if '##' in sentence:
			changes.append([sentence])
		elif re.match(r'^(\+|\-){1}[a-zA-Z ]',sentence):
			tmp = changes.pop(-1)
			tmp.append(sentence.replace(" ",""))
			changes.append(tmp)

	# extract the cell level mapping & type	
	extract_cell_index = lambda x: [int(i) for i in re.findall(r'\d+',x)]
	for change in changes:
		change[0] = extract_cell_index(change[0])

	# nest down into per lines
	lines_split_by_index =lambda x,y: [data[i:j] for data,split in zip(x,y) for i,j in zip([1]+[k+1 for k in split],[k-1 for k in split]+[len(data)]) if data[i:j]] 

	more = [change for change in changes if len(change[0]) >= 2]	
	all_cells = [index for i,j in [mo[0] for mo in more] for index in range(i,j+1)]
	index_split = [[i for i,val in enumerate(mo) if val == '-source:'] for mo in more]
	lines = lines_split_by_index(more,index_split)
	new_cells = [list(i) for i in list(zip(all_cells,lines))]

	# nest down insert 
	insert_double = [change for change in changes if change.count('+source:') >= 2] 
	insert_all_cells = [change[0][0] for change in changes if change.count('+source:') >= 2]
	insert_all_count = [change.count('+source:') for change in changes if change.count('+source:') >= 2]
	zip_cell_count = [i for i,j in zip(insert_all_cells,insert_all_count) for _ in range(j)]
	insert_index_split = [[i for i,val in enumerate(ib) if val == '+source:'] for ib in insert_double]
	insert_lines = lines_split_by_index(insert_double,insert_index_split) 
	new_insert_lines = list(map(list,zip(zip_cell_count,insert_lines)))
	print(new_insert_lines)
		
	# nest down the single index 
	cells = list()
	while changes:
		change = changes.pop(0)
		if len(change[0]) == 1 and change.count('+source:') < 2 :
			new_format = list()
			new_format.append(change[0][0])
			new_format.append(change[1:])
			cells.append(new_format)
	
	# all cells
	cells += new_cells
	cells += new_insert_lines
	cells = sorted(cells,key = lambda x:x[0])

	# clean cells
	ignore = ['-source:','+source:','+codecell:','-codecell:','-markdowncell:','+markdowncell:']
	for cell in cells:
		tmp = [ele for ele in cell[1] if ele not in ignore]
		cell[1] = tmp

	# old and new cell split
	old,new = list(),list()
	for cell in cells:
		old_c,new_c = [cell[0]],[cell[0]]
		for ele in cell[1]:
			if re.match(r'^\-{1}[a-zA-Z]',ele): old_c.append(ele)
			if re.match(r'^\+{1}[a-zA-Z]',ele): new_c.append(ele)
		if len(old_c) >= 2: old.append(old_c)
		if len(new_c) >= 2: new.append(new_c)

	
	return old,new

if __name__ == "__main__":
	old_cell_len = len(OLD.cells)
	new_cell_len = len(NEW.cells)
	print(f'{old_cell_len} {new_cell_len}')
	output = nbdime(OLD_PATH,NEW_PATH)
	extract_old,extract_new = convert(output)	
	old_lines = [line for lines in extract_old for line in lines[1:] ]
	new_lines = [line for lines in extract_new for line in lines[1:] ]
	
	lcs_result = lcs(convert_lines(old_lines),convert_lines(new_lines))
	# for i in lcs_result: print(i)
