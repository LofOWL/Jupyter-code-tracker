import textdistance
from config import THRESHOLD

class Line:
	
	def __init__(self,line=None):
		self.line = line	
	
	def __str__(self):
		return self.line

	def __eq__(self,others):
		return self.similarity(others) >= THRESHOLD	
	
	def id(self):
		return self.line

	def simi_function(self,x,y):
		return textdistance.ratcliff_obershelp(x,y)
	
	def similarities(self,others):
		return [self.similarity(line) for line in others]	

	def similarity(self,others):
		return self.simi_function(self.line,others.line)

convert_line = lambda x: Line(x)

def convert_lines(x):
	return [convert_line(i) for i in x]	

if __name__ == "__main__":
	print('line-mapping')
	old = 'a = '
	new = 'a = pd.read_csv("test.csv")'
	print(textdistance.ratcliff_obershelp(old,new))

	line_old = Line('a = ')
	line_new = Line('a = pd.read_csv("test.csv")')
	print(line_old.similarity(line_new))

	print(line_old == line_new)

