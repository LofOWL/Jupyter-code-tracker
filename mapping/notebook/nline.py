import os
import sys
path = os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))+"/cell_mapping"
sys.path.insert(0,path)

from line_mapping import Line,convert_lines


class NotebookLine(Line):
	
	def __init__(self,line):
		super().__init__(line)
		self.cell_index = None
		self.line_index = None	
		self.index = None

	def id(self):
		return [self.cell_index,self.index]

	def setCellIndex(self,index):
		self.cell_index = index

	def setLineIndex(self,index):
		self.line_index = index

	def setIndex(self,index):
		self.index = index
	
	def format(self,*kwg):
		return f'{self.cell_index},{self.line_index},{self.line_index}'	

if __name__ == "__main__":
	print("notebook line")
	nl = NotebookLine('sjdiofjsidof')
	nn = NotebookLine('jsidofjsiodfjsoidfjsdiof')
	print(nl.similarity(nn))
	print(nl.format())
