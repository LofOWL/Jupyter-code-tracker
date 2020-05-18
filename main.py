from tkinter import *
from tkinter import ttk

import os
import sys
import pandas as pd

from lib.map import Map
from lib.items import vs


class Tool:

    def __init__(self,path=None):
        self.root = Tk()
        self.screen_height = None

        self.path = path

        self._init_root()
        self.shaListBox = None
        self.data = None
        self.currentId = None
        self._init_box()
        self._init_button()
        self.canvas = None
        self.vbar = None
        self._init_vs()

    def _init_root(self):
        # self.screen_height = self.root.winfo_screenheight()
        # self.root.geometry("300x"+str(self.screen_height))

        self.root.attributes('-zoomed', True)

    def _init_box(self):
        def alist():
            if self.path != None:
                pa = pd.read_csv(self.path+"/result.csv")
            else:
                cwd = os.getcwd()
                pa = pd.read_csv(cwd+"/10118245/result.csv")
            pa = pa[pa["status"] == "success"]
            all_list = list(pa["id"])
            return all_list
        self.data = alist()
        self.currentId = self.data[0]
        self.shaList = ttk.Combobox(self.root, values=self.data, width=100)
        self.shaList.current(1)
        self.shaList.pack()

    def _init_button(self):
        def reload():
            self.currentId = self.data[self.shaList.current()]
            mp = Map(self.currentId,self.path)
            self.canvas.refresh(mp)
            self.vbar.config(command=self.canvas.yview)
            self.canvas.configure(scrollregion = self.canvas.bbox("all"))
            self.canvas.config(yscrollcommand=self.vbar.set)
        change = Button(self.root, text="change", command=reload)
        change.pack()

    def _init_vs(self):

        mp = Map(self.currentId,self.path)
        self.canvas = vs(self.root,mp)

        self.vbar=Scrollbar(self.root,orient=VERTICAL)
        self.vbar.pack(side=RIGHT,fill=Y)
        self.vbar.config(command=self.canvas.yview)

        self.canvas.configure(scrollregion = self.canvas.bbox("all"))
        self.canvas.config(yscrollcommand=self.vbar.set)

        self.canvas.pack(side=LEFT,expand=True,fill=BOTH)
        # self.canvas.pack(side=LEFT,expand=False)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":

    alist = sys.argv
    if len(alist) == 1:
        tool = Tool()
        tool.run()
    else:
        tool = Tool(path=sys.argv[1])
        tool.run()
