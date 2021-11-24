from configs import DELETED,INSERTED,MODIFIED 

def cell_mapping(lines,old_len,new_len):
	
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

	
