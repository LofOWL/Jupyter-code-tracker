from tkinter import *
import tkinter as tk

from lib.map_block import MapBlock

block_width = 400
block_gap_v = 10
block_gap_h = 60

line_gap_v = 15
line_gap_h = 10
line_height =  20
line_width = 380


text_gap_v = 5
text_gap_h = 5

class vs(Canvas):

    def __init__(self, parent,mp):
        Canvas.__init__(self, parent)
        self.config(bg="green",width=700)

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

        # self._create_line()



    def _draw_two_notebook_block(self):

        self.childBlock = []
        h = 0
        for information in self.childFile:
            a = self.Block(self,information,h,"c")
            a.create()
            self.childBlock.append(a)
            h = a.y2



        self.parentBlock = []
        h = 0
        for information in self.parentFile:
            a = self.Block(self,information,h,"p")
            a.create()
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
            self._main_process(mp)



    class Block:

        def __init__(self,vs,info,ph,type):

            self.vs = vs

            self.block = info["block"] + 1

            self.lines = []

            self.type = type

            self.tags = self.type +","+str(self.block)

            self.ph = ph

            def show(*args):
                print(self.tags)
                for i in info["lines"]:
                    print(i)
                print("-----")

            vs.tag_bind(self.tags,"<Button-1>",show)

            if self.type == "c":
                # self.x1 = 10
                self.x1 = 0
            else:
                # self.x1 = 10+block_width+block_gap_h
                self.x1 = block_width+block_gap_h
            start_h = self.ph
            for i in range(len(info["lines"])):
                a = self.Line(vs,self,info["lines"][i],start_h,i)
                self.lines.append(a)
                start_h = a.y2


            self.end_h = start_h

        def create_coordinate(self):
            self.height = self.end_h + block_gap_v

            self.x2 =  self.x1 + block_width
            self.y1 = self.ph+block_gap_v
            self.y2 = self.height

        def create(self):

            self.create_coordinate()
            self.vs.create_rectangle(self.x1,self.y1,self.x2, self.y2, fill="yellow",tags=self.tags)

            for line in self.lines:
                line.create()

            self.vs.pack(fill=BOTH, expand=YES)


        class Line:

            def __init__(self,vs,block,info,start_h,index):

                def show(*args):
                    print(self.tags)
                    print(info)
                    print("-----")

                self.vs = vs

                self.index = index + 1

                self.x1 = block.x1+line_gap_h
                self.x2 = self.x1 + line_width
                self.y1 = start_h+line_gap_v
                self.y2 = line_gap_v + start_h + line_height
                size_length = 1
                if len(info) >= 1:
                    self.y2 += (len(info) // 50) * line_height



                alist = [block.type,block.block,index]
                self.tags = ",".join([str(i) for i in alist])

                self.info = info

                # self.rectangle = vs.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill="red",tags=self.tags)

                vs.tag_bind(self.tags,"<Button-1>",show)

                # vs.pack(fill=BOTH, expand=YES)

            def create(self):

                self.vs.create_rectangle(self.x1,self.y1,self.x2,self.y2,fill="white",tags=self.tags)


                print(self.info)
                print("*********")
                text = self.vs.create_text(self.x1+text_gap_h,self.y1+text_gap_v,font=("Purisa", 10), anchor='nw',text=self.info,width=line_width-text_gap_h)
                print(text)
                print("$$$$$$$")
