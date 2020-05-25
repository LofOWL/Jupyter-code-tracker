from tkinter import *
import tkinter as tk
from lib.map_block import MapBlock

block_width = 420
block_gap_v = 10
block_gap_h = 60

text_gap_v = 5
text_gap_h = 5

line_gap_v = 15
line_gap_h = 10
line_height = 25
line_width = 380

line_index_block_length = 15
line_index_block_width = 15
line_index_block_height = 15

class Block:

    block_width = block_width
    block_gap_v = block_gap_v
    block_gap_h = block_gap_h

    def __init__(self,parent,info,ph,type):

        self.parent = parent

        self.block_index = info["block"] + 1

        self.lines = []

        self.type = type

        self.tags = self.type +","+str(self.block_index)

        self.ph = ph

        self.info = info

        def show(*args):
            print(self.tags)
            for i in self.info["lines"]:
                print(i)
            print("-----")
            win = tk.Toplevel()
            win.config(width=400,height= 400)
            zoom_block = ZoomBlock(win,self)

        self.parent.tag_bind(self.tags,"<Button-1>",show)

        if self.type == "c":
            # self.x1 = 10
            self.x1 = 0
        else:
            # self.x1 = 10+block_width+block_gap_h
            self.x1 = block_width+block_gap_h
        start_h = self.ph

        for i in range(len(info["lines"])):
            a = self.Line(self.parent,self,info["lines"][i],start_h,i)
            self.lines.append(a)
            start_h = a.y2

        if len(info["lines"]) != 0:
            self.end_h = start_h
        else:
            self.end_h = self.ph + block_gap_h

    def check_type(self):
        self.type_total_100 = self.parent.type_total_100
        self.type_total_90 = self.parent.type_total_90
        self.type_split = self.parent.type_split
        self.type_merge = self.parent.type_merge

        index = 0 if self.type == "c" else 1
        for i in self.type_total_100:
            if type(i[index]) == int:
                if self.block_index == i[index]:
                    return "total_100","grey"
            else:
                for j in i[index]:
                    if self.block_index == j:
                        return "total_100","grey"

        print("not pass")

        for i in self.type_total_90:
            if type(i[index]) == int:
                if self.block_index == i[index]:
                    return "total_90","blue"
            else:
                for j in i[index]:
                    if self.block_index == j:
                        return "total_90","blue"

        for i in self.type_split:
            if type(i[index]) == int:
                if self.block_index == i[index]:
                    return "split","blue"
            else:
                for j in i[index]:
                    if self.block_index == j:
                        return "split","blue"

        for i in self.type_merge:
            if type(i[index]) == int:
                if self.block_index == i[index]:
                    return "merge","blue"
            else:
                for j in i[index]:
                    if self.block_index == j:
                        return "merge","blue"


        if self.type == "c":
            return "delete","red"
        else:
            return "add","green"


    def create_coordinate(self):
        self.height = self.end_h + block_gap_v

        self.x2 =  self.x1 + block_width
        self.y1 =  self.ph+block_gap_v
        self.y2 = self.height

    def create(self):
        # check block type
        block_type,block_color = self.check_type()
        print(f"block_index: {self.block_index} block_type {block_type}")

        # create rectangle
        self.create_coordinate()
        if block_color == "blue":
            self.parent.create_rectangle(self.x1,self.y1,self.x2,self.y2,fill=block_color,tags=self.tags)
        else:
            self.parent.create_rectangle(self.x1,self.y1,self.x2,self.y2,fill=block_color)

        # create index block rectangle
        index_x1 = self.x1 + text_gap_h
        index_y1 = self.y1 + text_gap_v
        index_x2 = index_x1 + line_index_block_width
        index_y2 = index_y1 + line_index_block_height
        self.parent.create_rectangle(index_x1,index_y1,index_x2,index_y2,fill="white")

        # create index block
        index_text_x = index_x1 + line_index_block_width // 2
        index_text_y = index_y1 + line_index_block_height // 2
        self.parent.create_text(index_text_x,index_text_y,font=("Purisa",10),anchor='c',text=self.block_index)

        # create block and makdown type
        type_x1 = index_x1
        type_y1 = index_y2
        type_x2 = type_x1 + line_index_block_width
        type_y2 = type_y1 + line_index_block_height
        type_color = "red" if self.info["type"] == "code" else "blue"
        self.parent.create_rectangle(type_x1,type_y1,type_x2,type_y2,fill=type_color)

        # create type text
        type_text_x = type_x1 + line_index_block_width // 2
        type_text_y = type_y1 + line_index_block_height // 2
        block_type = "c" if self.info["type"] == "code" else "m"
        self.parent.create_text(type_text_x,type_text_y,fill="white",font=("Purisa",10),anchor='c',text=block_type)

        for line in self.lines:
            line.create()

        self.parent.pack(fill=BOTH, expand=YES)


    class Line:

        def __init__(self,parent,block,info,start_h,index):


            def show(*args):
                print(self.tags)
                print(info)
                print("-----")

            self.parent = parent

            self.block = block

            self.line_index = index + 1

            self.x1 = block.x1+line_index_block_width+line_gap_h
            self.x2 = self.x1 + line_width
            self.y1 = start_h+line_gap_v
            self.y2 = self.y1 + line_height
            size_length = 1
            if len(info) >= 1:
                self.y2 += (len(info) // 50) * line_height



            alist = [block.type,block.block_index,index]
            self.tags = ",".join([str(i) for i in alist])

            self.info = info

            # self.rectangle = vs.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill="red",tags=self.tags)

            self.parent.tag_bind(self.tags,"<Button-1>",show)

            # vs.pack(fill=BOTH, expand=YES)

        def create(self):

            mf = self.parent.mapFile

            # create text line rectangle
            pro = 0
            for i in mf:
                if self.block.type == "c":
                    if i.child.block == self.block.block_index and i.child.line == self.line_index:
                        pro = i.pro
                        break
                else:
                    if i.child.block == self.block.block_index and i.child.line == self.line_index:
                        pro = i.pro
                        break
            line_color = "grey30" if float(pro) == 1.0 else "grey80"
            print(f"pro {pro} line_color {line_color}")
            self.parent.create_rectangle(self.x1,self.y1,self.x2,self.y2,fill=line_color,tags=self.tags)

            # create index rectangle
            index_x1 = self.x1+text_gap_h
            index_y1 = self.y1+text_gap_v
            index_x2 = index_x1 + line_index_block_width
            index_y2 = index_y1 + line_index_block_height
            self.parent.create_rectangle(index_x1,index_y1,index_x2,index_y2,fill="white")

            # create index text
            index_text_x = index_x1 + line_index_block_width // 2
            index_text_y = index_y1 + line_index_block_height // 2
            self.parent.create_text(index_text_x,index_text_y,font=("Purisa",10),anchor='c',text=self.line_index)

            # create text
            text_x = index_x2 + text_gap_h
            text_y = self.y1 + text_gap_v
            text_width = line_width - text_gap_h - line_index_block_width - text_gap_h
            text = self.parent.create_text(text_x,text_y,font=("Purisa", 10), anchor='nw',text=self.info,width=text_width)


class ZoomBlock(Canvas):

    def __init__(self, parent, upperblock):
        Canvas.__init__(self, parent)
        screen_width = parent.winfo_screenwidth()
        self.config(bg="green",width = screen_width)

        self.clickedblock = upperblock

        self.type_total_100 = self.clickedblock.parent.type_total_100
        self.type_total_90 = self.clickedblock.parent.type_total_90
        self.type_split = self.clickedblock.parent.type_split
        self.type_merge = self.clickedblock.parent.type_merge

        self.mapFile = self.clickedblock.parent.mapFile

        self.currentblock = None

        # create the init current block
        self.__init_current_block()

        # create the init link block
        self.__create_link_block()

        self.pack()

    def __init_current_block(self):

        self.currentblock = Block(self,self.clickedblock.info,0,self.clickedblock.type)
        self.currentblock.create()

    def __create_link_block(self):
        data = self.clickedblock.parent.mp
        map = MapBlock(data)

        output = map.map_block(self.currentblock.block_index,self.clickedblock.type)

        if self.clickedblock.type == "c":
            mapped_block = set([i.parent.block for i in output])

            block_list = []
            h = 0
            for i in mapped_block:
                block = Block(self,self.clickedblock.parent.parentFile[i-1],h,"p")
                block.create()
                block_list.append(block)
                h = block.end_h + text_gap_h

            #create lines
            for mp in output:
                child = [i for i in self.currentblock.lines if i.line_index == mp.child.line][0]
                parent = None
                for block in block_list:
                    if block.block_index == mp.parent.block:
                        parent = [i for i in block.lines if i.line_index == mp.parent.line][0]
                if parent != None:
                    child_mid = (child.y1+child.y2) // 2
                    parent_mid = (parent.y1+parent.y2) // 2
                    self.create_line(child.x2,child_mid,parent.x1,parent_mid,fill="black",width=3)
        else:
            mapped_block = set([i.child.block for i in output])
            h = 0

            block_list = []
            for i in mapped_block:
                block = Block(self,self.clickedblock.parent.childFile[i-1],h,"c")
                block.create()
                block_list.append(block)
                h = block.end_h + text_gap_h


            #create lines
            for mp in output:
                child = [i for i in self.currentblock.lines if i.line_index == mp.parent.line][0]
                parent = None
                for block in block_list:
                    if block.block_index == mp.child.block:
                        parent = [i for i in block.lines if i.line_index == mp.child.line][0]
                if parent != None:
                    child_mid = (child.y1+child.y2) // 2
                    parent_mid = (parent.y1+parent.y2) // 2
                    self.create_line(parent.x2,parent_mid,child.x1,child_mid,fill="black",width=3)
