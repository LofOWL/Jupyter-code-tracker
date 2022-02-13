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
	
	def show(self):
		index = 0
		for cell in self.cells:
			lines = cell['source'] if 'source' in cell.keys() else cell['input']
			print(f'		{index} {"			".join(lines)}')
			index += 1
	
	def show_with_index(self,index):
		if index == "None":
			self.show()
		else:
			index = int(index)
			lines = self.cells[index]['source'] if 'source' in self.cells[index].keys() else self.cells[index]['input']
			print(f'		{index} {"			".join(lines)}')
			
	def get_cell_lines(self,cell):
		return [line for line in self.lines if line.cell_index == cell]

if __name__ == "__main__":
	print("notebook")
	path = '/media/lofowl/My Passport/CISC834/notebook_cache/645be9dcf5bf311af394a590c5d38fab151aa6d1_docs#Pfam.ipynb'
	nt = Notebook(path)
	print(len(nt.cells))
	nt.show_with_index('None')
