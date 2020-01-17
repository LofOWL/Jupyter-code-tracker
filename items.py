from tkinter import *


class vs(Canvas):
    
    def __init__(self, parent,data):
        Canvas.__init__(self, parent)
        self.config(bg="green")
        

        self.parentFile = data.parentFile.data

        self.childFile = data.childFile.data

        self.mapFile = data.formatData()

        self.parentBlock = []
        self.childBlock = []
        
        self._draw_two_notebook_block()

        self._create_line()

        
    def _draw_two_notebook_block(self):

        self.childBlock = []
        h = 0
        for information in self.childFile:
            a = Block(self,information,h,"c")
            self.childBlock.append(a)
            h = a.right


        self.parentBlock = []
        h = 0
        for information in self.parentFile:
            a = Block(self,information,h,"p")
            self.parentBlock.append(a)
            h = a.right

    def _create_line(self):

    	for i in self.mapFile:
    		if i.exist:
    			child = [ j for j in self.childBlock[i.child.block-1].lines if j.index == i.child.line][0]
    			parent =[ j for j in  self.parentBlock[i.parent.block-1].lines if j.index == i.parent.line][0]

    			self.create_line(child.down,child.right-5,parent.top,parent.right-5,fill="black",width=3)





        
class Block:

    def __init__(self,parent,info,ph,type):
        self._width = 100
        self._gap_v = 10
        self._gap_h = 60

        self.block = info["block"] + 1

        self.lines = []

        if type == "c":

            self.height = len(info["lines"])*30 + ph
            self.top = 10
            self.down = self.top + self._width
            self.left = ph+self._gap_v
            self.right = self.height

            parent.create_rectangle(self.top, self.left, self.down, self.right, fill="yellow")

            start_h = ph
            for i in range(len(info["lines"])):
                a = Line(parent,self.top,start_h,i,"c")
                self.lines.append(a)
                start_h = a.right
        else:

            self.height = len(info["lines"])*30 + ph
            self.top = 10+self._width+self._gap_h
            self.down =  self.top + self._width
            self.left = ph+self._gap_v
            self.right = self.height

            parent.create_rectangle(self.top,self.left,self.down, self.right, fill="yellow")

            start_h = ph
            for i in range(len(info["lines"])):
                a = Line(parent,self.top,start_h,i,"p")
                self.lines.append(a)
                start_h = a.right

        parent.pack(fill=BOTH, expand=YES)


class Line:

    def __init__(self,parent,start_w,start_h,index,type):

        self._gap_v = 15
        self._gap_h = 10

        self._height =  10
        self._width = 80

        self.index = index + 1

        self.top = start_w+self._gap_h
        self.down = self.top + self._width
        self.left = start_h+self._gap_v
        self.right = self._gap_v + start_h + self._height

        self.rectangle = parent.create_rectangle(self.top, self.left, self.down, self.right, fill="red")


        parent.pack(fill=BOTH, expand=YES)










