from tkinter import *

from lib.map_block import MapBlock
from lib.ViewJupyter import ViewJupyter


class vs(Canvas):

    def __init__(self, parent,mp):
        Canvas.__init__(self, parent)
        self.config(bg="green")

        self.ViewJ = ViewJupyter(mp)
        self.ViewJ.run()
        self._main_process(mp)




    def _main_process(self,mp):

        self.mp = mp

        self.parentFile = mp.parentFile.data

        self.childFile = mp.childFile.data

        self.mapFile = mp.formatData()

        self.parentBlock = []
        self.childBlock = []

        self.line_widget = []
        self.block_widget = []

        self._draw_two_notebook_block()

        self._create_block()

        self._create_split_type_block()

        self._create_merge_type_block()

        self._create_line()



    def _draw_two_notebook_block(self):

        self.childBlock = []
        h = 0
        for information in self.childFile:
            a = Block(self,information,h,"c")
            self.childBlock.append(a)
            h = a.y2


        self.parentBlock = []
        h = 0
        for information in self.parentFile:
            a = Block(self,information,h,"p")
            self.parentBlock.append(a)
            h = a.y2

    def _create_line(self):

        for i in self.mapFile:
            if i.exist:

                #child = self.childBlock[i.child.block-1].lines[i.child.line-1]
                child = [ j for j in self.childBlock[i.child.block-1].lines if j.index == i.child.line][0]
                #parent = self.parentBlock[i.parent.block-1].lines[i.parent.line-1]
                parent =[ j for j in  self.parentBlock[i.parent.block-1].lines if j.index == i.parent.line][0]

                self.line_widget.append(self.create_line(child.x2,child.y2-5,parent.x1,parent.y2-5,fill="black",width=3))


    def _create_block(self):

        a = MapBlock(self.mp)
        for i in a.type_total():
            child = self.childBlock[i[0]-1]
            parent = self.parentBlock[i[1]-1]
            self.create_polygon(child.x2,child.y1,parent.x1,parent.y1,parent.x1,parent.y2,child.x2,child.y2,fill='#808080')

    def _create_split_type_block(self):
        a = MapBlock(self.mp)

        for i in a.type_split():
            child = self.childBlock[i[0]-1]
            for j in i[1]:
                parent = self.parentBlock[j-1]
                self.create_polygon(child.x2,child.y1,parent.x1,parent.y1,parent.x1,parent.y2,child.x2,child.y2,fill='blue')

    def _create_merge_type_block(self):
        a = MapBlock(self.mp)

        for i in a.type_merge():
            parent = self.parentBlock[i[1]-1]
            for j in i[0]:
                child = self.childBlock[j-1]
                self.create_polygon(child.x2,child.y1,parent.x1,parent.y1,parent.x1,parent.y2,child.x2,child.y2,fill='red')

    def refresh(self,mp):
        self.delete("all")
        print("get in **** ")
        print(self.mp)
        for _ in range(3):
            self.ViewJ.refresh(self.mp)
            self._main_process(mp)



class Block:

    def __init__(self,vs,info,ph,type):
        self._width = 100
        self._gap_v = 10
        self._gap_h = 60

        self.block = info["block"] + 1

        self.lines = []

        self.type = type

        self.height = len(info["lines"])*10 + (len(info["lines"]) -1)*15+ 2*10 +ph

        if self.type == "c":

            #self.height = len(info["lines"])*10 + (len(info["lines"]) -1)*15+ 2*10 +ph
            self.x1 = 10
            self.x2 = self.x1 + self._width
            self.y1 = ph+self._gap_v
            self.y2 = self.height
            self.tags = self.type +","+str(self.block)

        else:

            #self.height = len(info["lines"])*30 + ph
            self.x1 = 10+self._width+self._gap_h
            self.x2 =  self.x1 + self._width
            self.y1 = ph+self._gap_v
            self.y2 = self.height
            self.tags = self.type +","+str(self.block)

        vs.create_rectangle(self.x1,self.y1,self.x2, self.y2, fill="yellow",tags=self.tags)

        def show(*args):
            print(self.tags)
            for i in info["lines"]:
                print(i)
            print("-----")
            vs.ViewJ.color_block(self.block,self.type)


        vs.tag_bind(self.tags,"<Button-1>",show)

        start_h = ph
        for i in range(len(info["lines"])):
            a = Line(vs,self,info["lines"][i],start_h,i)
            self.lines.append(a)
            start_h = a.y2

        vs.pack(fill=BOTH, expand=YES)


class Line:

    def __init__(self,vs,block,info,start_h,index):

        def show(*args):
            print(self.tags)
            print(info)
            print("-----")

        self._gap_v = 15
        self._gap_h = 10

        self._height =  10
        self._width = 80

        self.index = index + 1

        self.x1 = block.x1+self._gap_h
        self.x2 = self.x1 + self._width
        self.y1 = start_h+self._gap_v
        self.y2 = self._gap_v + start_h + self._height

        alist = [block.type,block.block,index]
        self.tags = ",".join([str(i) for i in alist])

        self.rectangle = vs.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill="red",tags=self.tags)

        vs.tag_bind(self.tags,"<Button-1>",show)


        vs.pack(fill=BOTH, expand=YES)
