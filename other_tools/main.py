import set_env
from data import OLD_PATH,NEW_PATH,OLDCELLLEN,NEWCELLLEN,OLD,NEW

import subprocess
import re

from configs import DELETED,INSERTED,MODIFIED
from csection import csection
from notebook_utils import collect_mapping,extract_lines,merge_split,replace_mapping, find_move_mapping
from sort import cell_sorted,cell_sorted_merge_identical
from utils import filter_cell
from line_mapping_algorithm import lcs

ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
nbdime = lambda x,y: subprocess.getoutput(f'nbdiff -s {x} {y}')

	
def convert_nbdime(output):
	output = ansi_escape.sub('',output)
	sentences = output.split("\n")
	# divide the output into each cell
	changes = list()
	for sentence in sentences:
		if re.match(f'^## ',sentence):
			changes.append([sentence])
		elif re.match(r'^(\+|\-){1}[a-zA-Z ]',sentence):
			tmp = changes.pop(-1)
			tmp.append(sentence.replace(" ",""))
			changes.append(tmp)

	csections = [csection(i) for i in changes] 
	
	lines,inserts = list(),list()	
	for cs in csections:
		output = cs.format()
		if cs.type == MODIFIED:
			lines.append(output)
		else:
			lines += output

	return lines
		
if __name__ == "__main__":
	# convert nbdime
	output = nbdime(OLD_PATH,NEW_PATH)
	output = convert_nbdime(output)
	output = collect_mapping(output,OLDCELLLEN,NEWCELLLEN)
	identical = [[int(mapping[0]),int(mapping[1])] for mapping in output if mapping[1] and mapping[1][-1] != 'm' and mapping[0]]
	output = cell_sorted(output)
	mapping = output[:]
	print("---")

	# find merge & split
	output = filter_cell(output)
	old_lines,new_lines = extract_lines(output,OLD,NEW)
	output = lcs(old_lines,new_lines)
	merge,split = merge_split(output)

	# new mapping
	output = replace_mapping(mapping,merge)	
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

	print("---")	
	# move mapping
	output = find_move_mapping(output,OLD,NEW)
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
