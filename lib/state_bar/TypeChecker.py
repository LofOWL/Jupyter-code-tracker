import os
from collections import Counter
import pandas as pd

from lib.state_bar.tool import group

class MapBlock:

    def __init__ (self,files):
        self.data = files

        self.child_block = dict(Counter([ i.child.block for i in self.data if i.child.exist]))
        self.parent_block = dict(Counter([ i.parent.block for i in self.data if i.parent.exist]))

        self.child_block_first_line = [ i for i in self.data if i.child.exist and i.child.line == 1]
        self.parent_block_first_line = [ i for i in self.data if i.parent.exist and i.parent.line == 1]

    def type_total(self):

        blockmap = Block(self.data)
        tool = group(self.data)

        map_block = []
        map_block_100 = []
        map_block_90 = []
        for i in self.child_block_first_line:
            if i.child.exist and i.parent.exist:
                c_block = i.child.block
                p_block = i.parent.block
                len_child_block = self.child_block[c_block]
                len_parent_block = self.parent_block[p_block]
                if len_child_block == len_parent_block:
                    bp = blockmap.mapChildParent(c_block)
                    print(f"bp: {bp}")
                    if len(bp) == 1:
                        map_block.append([c_block,p_block])
                        count_pro = tool.group(i.child.block)
                        if count_pro == len_child_block:
                            map_block_100.append([c_block,p_block])
                        else:
                            map_block_90.append([c_block,p_block])
        return map_block,map_block_100,map_block_90

    def type_split(self):
        split_block = []

        current_block_index = 1
        map_parent = []

        child_exist = [i for i in self.data if i.child.exist]
        for mapformat in child_exist:
            if current_block_index != mapformat.child.block:

                if len(set(map_parent)) >= 2:
                    split_block.append([current_block_index,set(map_parent)])

                current_block_index = mapformat.child.block
                map_parent = []
            else:
                block = mapformat.child.block - 1
                line = mapformat.child.line - 1
                word = self.child_info.line(block,line)
                print(mapformat.data)
                print(set(word))
                if word != '\n':
                    map_parent.append(int(mapformat.parent.block))
        if len(set(map_parent)) >= 2:
            split_block.append([current_block_index,set(map_parent)])
        print("new")
        print(split_block)

        return split_block

    def type_merge(self):
        blockmap = Block(self.data)

        split_block = []
        for i in self.parent_block_first_line:
            p_block = i.parent.block
            bp = blockmap.mapParentChild(p_block)
            if len(bp) > 1:
                split_block.append([bp,p_block])

        return split_block

    def parent_delete(self):
        return len([ i for i in self.data if not(i.parent.exist)])

    def parent_create(self):
        return len([ i for i in self.data if not(i.child.exist)])

class Block:

    def __init__(self,data):
        self.data = data

    def mapChildParent(self,block):
        filter_list = set([ i.parent.block for i in self.data if i.child.block == block and i.parent.block != -1])
        return filter_list

    def mapParentChild(self,block):
        filter_list = set([ i.child.block for i in self.data if i.parent.block == block and i.child.block != -1])
        return filter_list
