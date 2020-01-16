from tkinter import *


class vs(Canvas):
    
    def __init__(self, parent,data):
        Canvas.__init__(self, parent)
        self.config(bg="green")
        

        self.parentFile = data.parentFile.data;

        self.childFile = data.childFile.data;
        
        self._draw_two_notebook_block()

        
    def _draw_two_notebook_block(self):

        h = 0
        for information in self.childFile:
            a = Block(self,information,h,"c")
            h = a.height

        h = 0
        for information in self.parentFile:
            a = Block(self,information,h,"p")
            h = a.height


        
class Block:

    def __init__(self,parent,info,ph,type):
        self._width = 100
        self._gap_v = 10
        self._gap_h = 60

        self.height = len(info["lines"])*30 + ph
        if type == "c":
            start = 10
            end = start + self._width
            parent.create_rectangle(start, ph+self._gap_v, end, self.height, fill="yellow")
            start_h = ph
            for i in info["lines"]:
                a = Line(parent,start,start_h,"c")
                start_h = a.height
        else:
            start = 10+self._width+self._gap_h
            end = start + self._width
            parent.create_rectangle(start,ph+self._gap_v,end, self.height, fill="yellow")
            start_h = ph
            for i in info["lines"]:
                a = Line(parent,start,start_h,"p")
                start_h = a.height

        parent.pack(fill=BOTH, expand=YES)


class Line:

    def __init__(self,parent,start_w,start_h,type):

        self._gap_v = 15
        self._gap_h = 10

        self.height =  self._gap_v + start_h + 10
        self._width = 80

        start = start_w+self._gap_h
        end = start + self._width
        parent.create_rectangle(start, start_h+self._gap_v, end, self.height, fill="red")


        parent.pack(fill=BOTH, expand=YES)








