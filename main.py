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

        #load data
        # pd
        self.pa = None
        self.load_data()

        # create files bar
        self.filesListBox = None
        self.filesData = []
        self.currentFile = None

        # create upper bar
        self.shaListBox = None
        self.shaData = None
        self.currentId = None


        # search Button
        self.search_button = None

        # submit Button
        self.submit_button = None

        # upper bar
        self._init_upper_bar()

        # create vs canvas
        self.canvas = None
        self.vbar = None
        self._init_vs()

    def _init_root(self):
        # self.screen_height = self.root.winfo_screenheight()
        # self.root.geometry("300x"+str(self.screen_height))

        self.root.attributes('-fullscreen', True)

    def load_data(self):
        if self.path != None:
            self.pa = pd.read_csv(self.path+"/result.csv")
        else:
            cwd = os.getcwd()
            self.pa = pd.read_csv(cwd+"/10118245/result.csv")

    def _init_files_box(self):
        current_commit = self.currentId
        pa = self.pa[self.pa["current_commit"] == str(current_commit)]

        all_files = list(pa["filename"])
        self.filesData = all_files
        self.currentFile = self.filesData[0]
        self.filesListBox = ttk.Combobox(self.root,values=self.filesData,width=100)
        self.filesListBox.current(0)

        def callback(eventObject):
            self.currentFile = self.filesListBox.get()

        self.filesListBox.bind("<<ComboboxSelected>>", callback)

    def _init_sha_box(self):
        def alist():
            pa = self.pa[self.pa["status"] == "success"]
            all_list = list(set(list(pa["current_commit"])))
            return all_list
        self.shaData = alist()
        self.currentId = self.shaData[0]
        self.shaList = ttk.Combobox(self.root, values=self.shaData, width=100)
        self.shaList.current(0)

        # change the files box
        def callback(eventObject):
            self.currentId = self.shaList.get()
            current_commit = self.currentId
            pa = self.pa[self.pa["current_commit"] == str(current_commit)]

            all_files = list(pa["filename"])
            self.filesData = all_files
            self.filesListBox['values'] = self.filesData
            self.filesListBox.current(0)

        self.shaList.bind("<<ComboboxSelected>>", callback)


    def _init_search_sha_button(self):
        def reload():
            self.currentId = self.shaList.get()
            current_commit = self.currentId
            pa = self.pa[self.pa["current_commit"] == str(current_commit)]

            all_files = list(pa["filename"])
            self.filesData = all_files
            self.filesListBox['values'] = self.filesData
            self.filesListBox.current(0)
        self.search_button = Button(self.root,text="Search",command=reload)


    def _init_submit_button(self):
        def reload():
            self.currentId = self.shaList.get()
            self.currentFile = self.filesListBox.get()
            mp = Map(self.commit_files_id(),self.path)
            self.canvas.refresh(mp)
            self.vbar.config(command=self.canvas.yview)
            self.canvas.configure(scrollregion = self.canvas.bbox("all"))
            self.canvas.config(yscrollcommand=self.vbar.set)
        self.submit_button = Button(self.root, text="Submit", command=reload)


    def _init_upper_bar(self):
        self._init_sha_box()
        self._init_files_box()
        self._init_search_sha_button()
        self._init_submit_button()

        self.shaList.pack(side=TOP,fill=X,anchor=N, padx=5, pady=5)
        self.search_button.pack(side=TOP)
        self.filesListBox.pack(side=TOP,fill=X,anchor=N,padx=5,pady=5)
        self.submit_button.pack(side=TOP)

    def commit_files_id(self):
        pa = self.pa[self.pa["current_commit"] == str(self.currentId)]
        pa = pa[pa["filename"] == str(self.currentFile)]
        return list(pa["id"])[0]

    def _init_vs(self):

        mp = Map(self.commit_files_id(),self.path)
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
