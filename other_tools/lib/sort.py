

def cell_sorted(lines):
	normal,inserted = list(),list()
	for line in lines:
		if not line[0]:
			line[1] = int(line[1])
			inserted.append(line)
		else:
			line[0] = int(line[0])
			normal.append(line)
	normal = sorted(normal,key = lambda x:x[0])
	
	convert_int = lambda x: int(''.join(filter(str.isdigit,x))) if type(x) != int else x
	for line in inserted:
		add_index = len(normal) 
		for i,j in zip(list(range(len(normal)-1)),list(range(1,len(normal)))):
			if normal[i][1] and normal[j][1]:
				if convert_int(normal[i][1]) <= line[1] <= convert_int(normal[j][1]):
					add_index = j
		normal.insert(add_index,line)	
	return normal
if __name__ == "__main__":
	print("sort")
