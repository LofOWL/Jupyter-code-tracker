from lib.map import Map
from collections import Counter
import pandas as pd
import os

from lib.state_bar.tool import group

class MapBlock:
    child = "c"
    parent = "p"

    def __init__ (self,mp):
        self.mp = mp
        self.child_info = mp.childFile
        self.parent_info = mp.parentFile

        self.data = self.mp.formatData()

        self.child_block = dict(Counter([ i.child.block for i in self.data if i.child.exist]))
        self.parent_block = dict(Counter([ i.parent.block for i in self.data if i.parent.exist]))

        self.child_block_first_line = [ i for i in self.data if i.child.exist and i.child.line == 1]
        self.parent_block_first_line = [ i for i in self.data if i.parent.exist and i.parent.line == 1]

    def map_block(self,input_block,type):
        if type == "c":
            result = []
            for mp in self.data:
                if mp.child.block == input_block and mp.parent.exist:
                    block = mp.child.block - 1
                    line = mp.child.line - 1
                    word = self.child_info.line(block,line)
                    if word != '\n':
                        result.append(mp)
            return result
        else:
            result = []
            for mp in self.data:
                if mp.parent.block == input_block and mp.child.exist:
                    block = mp.parent.block - 1
                    line = mp.parent.line - 1
                    word = self.parent_info.line(block,line)
                    if word != '\n':
                        result.append(mp)
            return result


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
        parent_exist = [i for i in self.data if i.parent.exist]
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
                if word != '\n':
                    for parent in parent_exist:
                        if mapformat.child.block == parent.child.block and mapformat.child.line == parent.child.line:
                                map_parent.append(int(parent.parent.block))
        if len(set(map_parent)) >= 2:
            split_block.append([current_block_index,set(map_parent)])

        return split_block

    def type_merge(self):
        merge_block = []

        current_block_index = 1
        map_parent = []

        self.mp.sortbyParent()
        self.data = self.mp.formatData()

        child_exist = [i for i in self.data if i.child.exist]
        parent_exist = [i for i in self.data if i.parent.exist]
        for mapformat in parent_exist:
            if current_block_index != mapformat.parent.block:

                if len(set(map_parent)) >= 2:
                    merge_block.append([set(map_parent),current_block_index])

                current_block_index = mapformat.parent.block
                map_parent = []
            else:
                block = mapformat.parent.block - 1
                line = mapformat.parent.line - 1
                word = self.parent_info.line(block,line)

                if word != '\n':
                    for child in child_exist:
                        if mapformat.parent.block == child.parent.block and mapformat.parent.line == child.parent.line:
                                map_parent.append(int(child.child.block))

        if len(set(map_parent)) >= 2:
            merge_block.append([set(map_parent),current_block_index])

        return merge_block


class Block:

    def __init__(self,data):
        self.data = data

    def mapChildParent(self,block):
        filter_list = set([ i.parent.block for i in self.data if i.child.block == block and i.parent.block != -1])
        return filter_list

    def mapParentChild(self,block):
        filter_list = set([ i.child.block for i in self.data if i.parent.block == block and i.child.block != -1])
        return filter_list

def data():
    path = "/home/lofowl/Desktop/Jupyter-code-tracker/10118245/result.csv"
    pa = pd.read_csv(path)
    pa = pa[pa["status"]=="success"]
    all_list = list(pa["id"])
    return all_list

def checkall():
    for i in data():
        print(i)
        mp = Map(i)
        a = MapBlock(mp)
        if len(a.type_merge()) >= 1:
            print(i)


if __name__ == "__main__":

    path = "/home/lofowl/Desktop/Jupyter-code-tracker/10118245/result.csv"
    mp = Map(path)
    a = MapBlock(mp)
    print(a.type_total())
    print(a.type_split())
    print(a.type_merge())
