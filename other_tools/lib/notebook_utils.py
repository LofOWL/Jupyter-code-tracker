from re import I
from configs import DELETED,INSERTED,MODIFIED 
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
	
	# find all the identical mapping 
	while old_pointer < old_len:
		old_map[old_pointer] += [new_pointer]
		old_pointer += 1
		new_pointer += 1

	# add insert cell
	items = list(old_map.values())
	insert = [str(i) for ele in items for i in ele]
	insert_cell = [ele for ele in range(new_len) if not any(str(ele) == (i if i[-1] != 'm' else i[:-1]) for i in insert)]

	mapping = list(map(lambda x:[str(x[0]),str(x[1][0])] if len(x[1]) else [str(x[0]),None],list(old_map.items()))) + [[None,str(i)] for i in insert_cell]
	
	return mapping

def collect_not_modified_line(pair,old,new,lcs):
	old_cell = int(pair[0])
	new_cell = int(pair[1][:-1])
	old_lines = [line for line in old.get_cell_lines(old_cell) if line.line.replace(" ","") != ""]
	new_lines = [line for line in new.get_cell_lines(new_cell) if line.line.replace(" ","") != ""]
	mapping_lines = lcs(old_lines,new_lines)
	old_lines_index = [i[0][1] for i in mapping_lines]
	old_not_touch = [line for line in old_lines if line.index not in old_lines_index]

	new_lines_index = [i[1][1] for i in mapping_lines]
	new_not_touch = [line for line in new_lines if line.index not in new_lines_index]

	return old_not_touch,new_not_touch


def collect_not_modified_lines(pairs,old,new,lcs):
	not_touch_lines_old,not_touch_lines_new = list(),list()
	for pair in pairs:
		not_old,not_new = collect_not_modified_line(pair,old,new,lcs)
		not_touch_lines_old += not_old
		not_touch_lines_new += not_new
	return not_touch_lines_old,not_touch_lines_new

def extract_lines(pairs,old,new,lcs):
	old_indexs,new_indexs,modified_pair = list(),list(),list()
	for pair in pairs:
		if "m" in str(pair[1]):
			modified_pair.append(pair)
		else:
			if pair[0] != None: old_indexs.append(pair[0])
			if pair[1] != None: new_indexs.append(pair[1])	

	# not touch in modified cell	
	old_not_touch,new_not_touch = collect_not_modified_lines(modified_pair,old,new,lcs)

	# convert to integer 
	new_indexs = [int(index[:-1]) if type(index) != int else index for index in new_indexs]	
	
	# filter cells
	old_lines = [line for line in old.lines if line.cell_index in old_indexs ]	
	new_lines = [line for line in new.lines if line.cell_index in new_indexs ]

	# remove the empty lines
	old_lines = [line for line in old_lines if line.line.replace(" ","") != ""]
	new_lines = [line for line in new_lines if line.line.replace(" ","") != ""]

	# merge two list
	old_lines += old_not_touch
	old_lines = sorted(old_lines,key= lambda x: x.index,reverse=False)
	new_lines += new_not_touch
	new_lines = sorted(new_lines,key = lambda x: x.index)

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
				# need to change 
				if tmp_mapping[i][1] != None: 
					mcell = int(tmp_mapping[i][1][:-1])
					tmp_mapping[i] = (mmapping[0],list(set(mmapping[1]+[mcell])))
				else:
					tmp_mapping[i] = mmapping
				break
	cache_new = set([j for i in tmp_mapping if type(i[1]) == list for j in i[1]])

	# clean
	remove_index = list()
	for i in range(len(tmp_mapping)):
		mapping = tmp_mapping[i]
		if type(mapping[1]) != list:
			if type(mapping[1]) != int:
				if mapping[1] != None and mapping[1].isnumeric() and int(mapping[1]) in cache_new:
					remove_index.append(i)
			else:
				if mapping[1] in cache_new:
					remove_index.append(i)
	return [value for index,value in enumerate(tmp_mapping) if index not in remove_index]

def find_move_mapping(mappings,OLD,NEW):
	delete,add = list(),list()
	for mapping in mappings:
		if mapping[1] == None: delete.append(mapping[0])
		if mapping[0] == None: add.append(mapping[1])

	complete = lambda x: '0'*(64-len(x))+x
	hex2bin = lambda x: complete(bin(int(x,16))[2:])
	hamming = lambda x,y: sum(i != j for i,j in zip(x,y))
	
	add_text = [''.join(NEW.cells[i]['source'] if 'source' in NEW.cells[i].keys() else NEW.cells[i]['input']) for i in add]
	move = list()
	for i in delete:
		old_text = ''.join(OLD.cells[i]['source'] if 'source' in OLD.cells[i].keys() else OLD.cells[i]['input'])
		similarity = [textdistance.ratcliff_obershelp(old_text,i) for i in add_text]
		if len(similarity) >= 1:
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

def find_split(lines,old,new):
	mapping = dict()
	for line in lines:
		pair = ','.join([str(line[0][0]),str(line[1][0])])
		if pair in mapping.keys():
			mapping[pair] += 1
		else:
			mapping[pair] = 1
	
	correct_mappings = list()
	for key,counts in mapping.items():
		new_cell = int(key.split(",")[1])
		# filter by count
		if counts >= 2:
			correct_mappings.append(key)

		# filter by percentage
		#new_cell_len = len(new.get_cell_lines(new_cell))
		#print(f'{key} {counts} {new_cell_len}')

	format_mapping = dict()
	for correct_mapping in correct_mappings:
		old,new = map(int,correct_mapping.split(","))
		if old in format_mapping.keys():
			format_mapping[old].append(new)
		else:
			format_mapping[old] = [new]

	return list(format_mapping.items())