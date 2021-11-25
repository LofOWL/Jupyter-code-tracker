
def lcs(x,y):
	m,n = len(x),len(y)
	L = [[0 for x in range(n+1)] for x in range(m+1)]
	
	for i in range(m+1):
		for j in range(n+1):
			if i == 0 or j == 0:
				L[i][j] = 0
			elif x[i-1] == y[j-1]:
				L[i][j] = L[i-1][j-1] + 1
			else:
				L[i][j] = max(L[i-1][j],L[i][j-1])
				
	index = L[m][n]

	lcs  = [""] * (index+1)
	lcs[index] = ""
	
	i,j = m,n
	while i > 0 and j > 0:
		if x[i-1] == y[j-1]:
			# lcs[index-1] = [x[i-1].cell_index,x[i-1].line_index,y[j-1].cell_index,y[j-1].line_index]
			lcs[index-1] = [x[i-1].id(),y[j-1].id()]
			i -= 1
			j -= 1
			index -= 1
		elif L[i-1][j] > L[i][j-1]:
			i -= 1
		else:
			j -= 1

	return lcs[:-1]	


if __name__ == "__main__":

	from line import Line,convert_lines
	print('line-mapping')
	x = convert_lines(['line 1 iosjf oijsido','line 2jisof sodifjsdfo','line 3jsidosdfioj'])
	y = convert_lines(['line1 iosjf oijsido','line 3jsidosdfioj'])
	lcs(x,y)
		
