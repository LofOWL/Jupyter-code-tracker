import re
from configs import DELETED,INSERTED,MODIFIED
from utils import convert

class csection:


	def __init__(self,data):
		self.data = data
		self.head = data[0]
		self.body = data[1:]
		self.type = self.head.split(" ")[1]
		self.cells = list(map(int,re.findall(r'\d+',self.head)))
		if self.type == 'deleted':
			self.cells = [index for index in range(self.cells[0],self.cells[-1]+1)]

	def __str__(self):
		return "hello"

	def format(self):
		if self.type == DELETED:
			return 	[[c.index,self.type,c.lines] for c in convert(self,'-source:')]
		elif self.type == INSERTED:
			return 	[[c.index,self.type,c.lines] for c in convert(self,'+source:')]
		elif self.type == MODIFIED:
			return [self.cells[0],self.type,self.body]


if __name__ == "__main__":
	print("change section")
