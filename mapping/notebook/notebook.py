from nline import NotebookLine,convert_lines
import json as js


class Notebook:
	
	def __init__(self,path):
		self.notebook = None
		with open(path,'r') as file:
			self.notebook = js.load(file)				
		
		self.cells = self.notebook['cells']
		index,cell_index = 0,0
		self.lines = list()
		for cell in self.cells:
			lines = cell['source']
			line_index = 0
			for line in lines:
				line = line.replace('\n','')
				nl = NotebookLine(line)
				nl.setCellIndex(cell_index)
				nl.setLineIndex(line_index)	
				nl.setIndex(index)	
				self.lines.append(nl)
				line_index += 1
				index += 1
			cell_index += 1

if __name__ == "__main__":
	print("notebook")
	path = 'notebook.ipynb'
	nt = Notebook(path)
