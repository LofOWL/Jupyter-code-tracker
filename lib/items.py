from tkinter import *
import tkinter as tk

from lib.map_block import MapBlock

from lib.state_bar.state_bar import StateBar
from lib.item.Block import Block


class vs(Canvas):

    def __init__(self, parent,mp):
        Canvas.__init__(self, parent)
        self.config(bg="white",width=700)

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

        # create mppaing block type information
        self._block_type_information()

        # create left children block and right parent block
        self._draw_two_notebook_block()

        # create state StateBar
        self._draw_state_bar()

        # show the total mapping
        self._mapping_total_100_block()

        # show the total 90 mapping
        self._mapping_total_90_block()

        # show the split mapping
        self._mapping_split_type_block()

        # show the merge mapping
        self._mapping_merge_type_block()

        # create line from line to line
        # self._create_line()/



    def _block_type_information(self):

        get = MapBlock(self.mp)

        self.type_total,self.type_total_100,self.type_total_90 = get.type_total()

        self.type_split = get.type_split()

        self.type_merge = get.type_merge()


    def _draw_two_notebook_block(self):

        self.childBlock = []
        h = 0
        for information in self.childFile:
            a = Block(self,information,h,"c")
            a.create()
            self.childBlock.append(a)
            h = a.y2



        self.parentBlock = []
        h = 0
        for information in self.parentFile:
            a = Block(self,information,h,"p")
            a.create()
            self.parentBlock.append(a)
            h = a.y2

    def _draw_state_bar(self):
        x1 = Block.block_width+Block.block_gap_h+Block.block_width+10
        a = MapBlock(self.mp)
        self.StateBar = StateBar(x1 = x1,vs = self, mapblock=a)



    def _create_line(self):

        for i in self.mapFile:
            if i.exist:

                #child = self.childBlock[i.child.block-1].lines[i.child.line-1]
                child = [ j for j in self.childBlock[i.child.block-1].lines if j.line_index == i.child.line][0]
                #parent = self.parentBlock[i.parent.block-1].lines[i.parent.line-1]
                parent =[ j for j in  self.parentBlock[i.parent.block-1].lines if j.line_index == i.parent.line][0]

                if child.info != '\n':
                    self.line_widget.append(self.create_line(child.x2,child.y2-5,parent.x1,parent.y2-5,fill="black",width=3))


    def _mapping_total_100_block(self):

        for i in self.type_total_100:
            child = self.childBlock[i[0]-1]
            parent = self.parentBlock[i[1]-1]

            child_mid = (child.y1+child.y2) // 2
            parent_mid = (parent.y1 + parent.y2) // 2

            self.create_line(child.x2,child_mid,parent.x1,parent_mid,fill='#808080')

    def _mapping_total_90_block(self):
        for i in self.type_total_90:
            child = self.childBlock[i[0]-1]
            parent = self.parentBlock[i[1]-1]

            child_mid = (child.y1+child.y2) // 2
            parent_mid = (parent.y1 + parent.y2) // 2

            self.create_line(child.x2,child_mid,parent.x1,parent_mid,fill='#808080')

    def _mapping_split_type_block(self):

        for i in self.type_split:
            child = self.childBlock[i[0]-1]
            child_mid = (child.y1 +child.y2) // 2
            for j in i[1]:
                parent = self.parentBlock[j-1]
                parent_mid = (parent.y1 + parent.y2) //2
                self.create_line(child.x2,child_mid,parent.x1,parent_mid,fill='blue')

    def _mapping_merge_type_block(self):

        print(self.type_merge)
        for i in self.type_merge:
            parent = self.parentBlock[i[1]-1]
            parent_mid = (parent.y1 + parent.y2) // 2
            for j in i[0]:
                child = self.childBlock[j-1]
                child_mid = (child.y1 +child.y2) // 2
                self.create_line(child.x2,child_mid,parent.x1,parent_mid,fill='red')

    def refresh(self,mp):
        self.delete("all")
        print("get in **** ")
        print(self.mp)
        self._main_process(mp)
