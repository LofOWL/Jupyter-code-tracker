from map import Map
from collections import Counter


class MapBlock:

	def __init__ (self,mp):
		self.lines = mp
		self.data = self.lines.formatData()

		self.child_block = dict(Counter([ i.child.block for i in self.data if i.child.exist]))
		self.parent_block = dict(Counter([ i.parent.block for i in self.data if i.parent.exist]))

		self.child_block_first_line = [ i for i in self.data if i.child.exist and i.child.line == 1]

	def type_total(self):
		

		blockmap = Block(self.data)
		
		map_block = []
		for i in self.child_block_first_line:
			if i.child.exist and i.parent.exist:
				c_block = i.child.block
				p_block = i.parent.block
				len_child_block = self.child_block[c_block]
				len_parent_block = self.parent_block[p_block]
				if len_child_block == len_parent_block:
					bp = blockmap.mapChildParent(c_block)
					if len(bp) == 1:
						map_block.append([c_block,p_block])

		return map_block

	def type_split(self):

		blockmap = Block(self.data)
		
		split_block = []
		for i in self.child_block_first_line:
			c_block = i.child.block
			bp = blockmap.mapChildParent(c_block)
			if len(bp) != 1:
				split_block.append([c_block,bp])

		return split_block


class Block:

	def __init__(self,data):
		self.data = data

	def mapChildParent(self,block):
		filter_list = set([ i.parent.block for i in self.data if i.child.block == block])
		return filter_list

if __name__ == "__main__":
	mp = Map("4696d4bbcb4aff65c43cbed94ad060518dedc346#0")
	a = MapBlock(mp)
	total = a.type_total()
	print(total)
	print(a.type_split())
