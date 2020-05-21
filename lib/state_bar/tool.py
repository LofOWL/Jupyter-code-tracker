import os

class group:

    def __init__(self,value):
        self.value = value


    def group(self,block):
        result = []
        pro_count = 0
        for i in self.value:
            if i.child.block == block:
                pro_count += float(i.pro)

        return pro_count
