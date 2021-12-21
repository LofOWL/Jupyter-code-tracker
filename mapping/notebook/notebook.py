from nline import NotebookLine,convert_lines
import json as js


class Notebook:
	
	def __init__(self,path):
		self.path = path
		self.notebook = None
		with open(path,'r') as file:
			self.notebook = js.load(file)				
		self.cells = self.notebook['cells'] if 'worksheets' not in self.notebook.keys() else self.notebook['worksheets'][0]['cells']
		self.is_old = 'worksheets' in self.notebook.keys()
		index,cell_index = 0,0
		self.lines = list()
		for cell in self.cells:
			lines = cell['source'] if 'source' in cell.keys() else cell['input']
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
	path = '/media/lofowl/My Passport/CISC834/notebook_cache/881994c6fcbba6ad8a41829410e5b568ff28d00d_notebooks#Riemann Constant Vector Paper.ipynb'
	nt = Notebook(path)
