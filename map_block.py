from map import Map
from collections import Counter


class MapBlock:

	def __init__ (self,mp):
		self.lines = mp
		self.data = self.lines.formatData()
		

	def type_total(self):
		child_block = dict(Counter([ i.child.block for i in self.data if i.child.exist]))
		parent_block = dict(Counter([ i.parent.block for i in self.data if i.parent.exist]))
		
		child_block_first_line = [ i for i in self.data if i.child.exist and i.child.line == 1]
		
		map_block = []
		for i in child_block_first_line:
			if i.child.exist and i.parent.exist:
				c_block = i.child.block
				p_block = i.parent.block
				len_child_block = child_block[c_block]
				len_parent_block = parent_block[p_block]
				if len_child_block == len_parent_block:
					map_block.append([c_block,p_block])

		return map_block


if __name__ == "__main__":
	a = MapBlock("09c24d5ec7682c2e1cf55751bd1761df31a2746b#1")
	a.type_total()
