import set_env
from data import OLD_PATH,NEW_PATH
from data import OLDCELLLEN,NEWCELLLEN

import subprocess
import re

from csection import csection
from configs import DELETED,INSERTED,MODIFIED
from convert_lines import cell_mapping
from sort import cell_sorted

ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
nbdime = lambda x,y: subprocess.getoutput(f'nbdiff -s {x} {y}')

	
def convert(output):
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
	output = nbdime(OLD_PATH,NEW_PATH)
	output = convert(output)
	output = cell_mapping(output,OLDCELLLEN,NEWCELLLEN)
	output = cell_sorted(output)
	for out in output:
		if out[0] == None:
			print(f' --- C{out[1]}')
		elif out[1] == None:
			print(f'C{out[0]} --- ')
		else:
			print(f'C{out[0]} --- C{out[1]}')


