import os
import json as js
import pandas as pd

class Map:

    def __init__(self,name):

        self.path = "/Users/apple/Desktop/10118245"
        self.name = name

        self.data = None
        self.missing_index = []
        self.missing_data = []
        self.childFile = NewFile(self.path+"/New/"+name+"#c.txt")
        self.parentFile = NewFile(self.path+"/New/"+name+"#p.txt")

        with open(self.path+"/Map/"+name+".txt",'r') as file:
            self.data = file.read()
            self.data = self.data.split("\n")[:-1]

        exist_list = []
        for i in self.data:
            lin = line(i)
            lin.parent()
            if lin.exist:
                exist_list.append(lin.index)
        self.missing_index = [ i for i in range(1,self.parentFile.totalLength+1) if not(i in exist_list)]

    def parentMaptoChild(self):
        self.missing_data = [ "_,"+self.parentFile.block(i)+",0" for i in self.missing_index]
        self.data = self.data + self.missing_data

    def sortbyParent(self):
        self.data.sort(key=lambda x: line(x).parent())

    def sortbyChild(self):
        self.data.sort(key=lambda x: line(x).child())

    def write(self):
        with open(self.path+"/Map/"+self.name+".txt","w") as file:
            for i in self.data:
                file.write(i+"\n")


class line:

    def __init__(self,word):
        self.word = word
        self.data = None
        self.exist = None
        self.index = None

    def parent(self):
        self.data = self.word.split(",")[1]
        self.exist = True if self.data != '_' else False
        self.index = int(self.data.split(".")[2]) if self.exist else -1
        return self.index

    def child(self):
        self.data = self.word.split(",")[0]
        self.exist = True if self.data != '_' else False
        self.index = int(self.data.split(".")[2]) if self.exist else -1
        return self.index


class NewFile:

    def __init__(self,path):
        self.data = None
        with open(path) as data:
            self.data = js.loads(data.read())
        start = self.data[0]["startIndex"]
        result = []
        for i in self.data:
            result.append([start+1,start+i["linesLength"]])
            start = start+i["linesLength"]

        self.interval=result
        self.totalLength = sum([ i["linesLength"] for i in self.data])

    def block(self,index):
        if index == "_":
            return "_"
        else:
            data = [ (x,j[0]) for x,j in enumerate(self.interval) if j[0] <= int(index) and int(index) <= j[1] ]
            block = data[0][0]+1
            block_index = (int(index) - int(data[0][1]))+1
            return str(block)+"."+str(block_index)+"."+str(index)


if __name__ == "__main__":
    pa = pd.read_csv("/Users/apple/Desktop/10118245/result1.csv")
    pa = pa[pa["status"] == "success"]
    all_list = list(pa["id"])
    for i in all_list:
        print(i)
        a = Map(i)
        a.parentMaptoChild()
        a.sortbyChild()
        a.write()
        print("done")
