from cell import Cell
from configs import INSERTED,DELETED

def convert(self,key):
        index_split = [i for i,val in enumerate(self.body) if val == key]        
        sub_cells = [self.body[i:j] for i,j in zip([1]+[k+1 for k in index_split],[k-1     for k in index_split]+[len(self.body)]) if self.body[i:j]] 
        # get empty 
        if len(sub_cells) == 0:
            sub_cells = [['']]
        cells_type = [line for line in self.body if any(key in line for key in ['markdowncell','codecell'])]
        lines = list(map(list,zip(cells_type,sub_cells)))
        cells_index = [self.cells[0] for _ in range(len(lines))] if self.type == INSERTED else self.cells
        index_type_lines = list(map(list,zip(cells_index,lines)))
        def fmap(x):
                c = Cell()
                c.index = x[0]
                c.type = x[1][0]
                c.lines = x[1][1]
                return c
        cells = list(map(fmap,index_type_lines))
        return cells

def filter_cell(mapping):
	pairs = list()
	for pair in mapping:
		if pair[1] == None:
			pairs.append(pair)
		elif pair[0] == None:
			pairs.append(pair)
		elif pair[1][-1] == 'm':
			pairs.append(pair)
	return pairs

if __name__ == "__main__":
	print(Cell)
