

def cell_mapping(lines_mapping):
	cell_x = {i:[] for i in list(set([i[0] for i in lines_mapping]))}
	for line_map in lines_mapping:
		from_cell = line_map[0]	
		map_cell = line_map[2]
		if map_cell not in cell_x.get(from_cell):
			cell_x[from_cell] = cell_x.get(from_cell) + [map_cell]
	return cell_x	


if __name__ == "__main__":
	print("cell_mapping")
