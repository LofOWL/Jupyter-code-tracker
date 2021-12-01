from configs import DELETED,INSERTED,MODIFIED 
from floc_simhash import SimHash
from scipy.spatial.distance import hamming
import textdistance


def collect_mapping(lines,old_len,new_len):
	
	old_map = {i:[] for i in range(old_len)}

	old_pointer,new_pointer = 0,0
	
	while lines:
		line = lines.pop(0)
		if line[0] != old_pointer:
			lines.insert(0,line)
			old_map[old_pointer] = old_map.get(old_pointer) + [new_pointer]
			old_pointer += 1
			new_pointer += 1
		else:
			if line[1] == INSERTED:
				new_pointer += 1
			elif line[1] == DELETED:
				old_pointer += 1			 
			else:
				old_map[old_pointer] = old_map.get(old_pointer) + [str(new_pointer)+'m']
				old_pointer += 1
				new_pointer += 1
	items = list(old_map.values())
	insert = [str(i) for ele in items for i in ele]
	insert_cell = [ele for ele in range(new_len) if not any(str(ele) in i for i in insert)]

	mapping = list(map(lambda x:[str(x[0]),str(x[1][0])] if len(x[1]) else [str(x[0]),None],list(old_map.items()))) + [[None,str(i)] for i in insert_cell]
	
	return mapping

def extract_lines(pairs,old,new):
	old_indexs,new_indexs = list(),list()
	for pair in pairs:
		if pair[0] != None: old_indexs.append(pair[0])
		if pair[1] != None: new_indexs.append(pair[1])	

	# convert to integer 
	new_indexs = [int(index[:-1]) if type(index) != int else index for index in new_indexs]	
	
	# filter cells
	old_lines = [line for line in old.lines if line.cell_index in old_indexs ]	
	new_lines = [line for line in new.lines if line.cell_index in new_indexs ]
	
	return old_lines, new_lines	

def merge_split(lines_mapping):
	merge,split = dict(),dict()
	for line in lines_mapping:
		merge[line[0][0]] = []
		split[line[1][0]] = []

	for line in lines_mapping:
		if line[1][0] not in merge.get(line[0][0]):
			merge[line[0][0]] = merge.get(line[0][0]) + [line[1][0]]
		if line[0][0] not in split.get(line[1][0]):
			split[line[1][0]] = split.get(line[1][0]) + [line[0][0]]
	
	return list(merge.items()),list(split.items())	

def complete_mapping(lines_mapping,old_len,new_len):
	old_cells, new_cells = list(),list()
	for line_mapping in lines_mapping:
		old_cells.append(line_mapping[0])
		if type(line_mapping[1]) == int:
			new_cells.append(line_mapping[1])
		else:
			new_cells += line_mapping[1]
	
	delete_cells = [cell for cell in range(old_len) if cell not in old_cells]
	add_cells = [cell for cell in range(new_len) if cell not in new_cells]

	delete_mapping = [[cell,None] for cell in delete_cells]
	add_mapping = [[None,cell] for cell in add_cells]
	
	total = lines_mapping[:]

def replace_mapping(mapping,merge):
	tmp_mapping = mapping[:]	
	for mmapping in merge:	
		for i in range(len(tmp_mapping)):
			if tmp_mapping[i][0] == mmapping[0]:
				tmp_mapping[i] = mmapping
				break
	cache_new = set([j for i in tmp_mapping if type(i[1]) == list for j in i[1]])

	# clean
	remove_index = list()
	for i in range(len(tmp_mapping)):
		mapping = tmp_mapping[i]
		if type(mapping[1]) != list:
			if mapping[1] != None and int(mapping[1]) in cache_new:
				remove_index.append(i)
	return [value for index,value in enumerate(tmp_mapping) if index not in remove_index]

def find_move_mapping(mappings,OLD,NEW):
	delete,add = list(),list()
	for mapping in mappings:
		if mapping[1] == None: delete.append(mapping[0])
		if mapping[0] == None: add.append(mapping[1])

	complete = lambda x: '0'*(64-len(x))+x
	hex2bin = lambda x: complete(bin(int(x,16))[2:])
	old = SimHash(n_bits=64).hash('hello my name is')
	new = SimHash(n_bits=64).hash('hello my name is jf')	
	hamming = lambda x,y: sum(i != j for i,j in zip(x,y))
	bin_old,bin_new = hex2bin(old),hex2bin(new)
	
	add_text = [''.join(NEW.cells[i]['source']) for i in add]
	move = list()
	for i in delete:
		old_text = ''.join(OLD.cells[i]['source'])
		similarity = [textdistance.ratcliff_obershelp(old_text,i) for i in add_text]
		max_simi = max(similarity)
		if max_simi >= 0.9:
			index = similarity.index(max_simi)
			move.append([i,add[index]])

	tmp_mapping = mappings[:]
	remove = list()
	for i in move:
		for j in range(len(tmp_mapping)):
			if i[0] == tmp_mapping[j][0]:
				tmp_mapping[j] = [i[0],str(i[1])] 
			if i[1] == tmp_mapping[j][1]:
				remove.append(j)

	return [value for index,value in enumerate(tmp_mapping) if index not in remove]
