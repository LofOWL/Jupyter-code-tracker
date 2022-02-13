import subprocess
import re

from configs import DELETED,INSERTED,MODIFIED
from csection import csection
from notebook_utils import collect_mapping,extract_lines,merge_split,replace_mapping, find_move_mapping
from sort import cell_sorted,cell_sorted_merge_identical
from utils import filter_cell

ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
nbdime = lambda x,y: subprocess.getoutput(f'nbdiff -s "{x}" "{y}"')

	
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
		