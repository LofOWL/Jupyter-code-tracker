from tkinter import *
from tkinter import ttk
from map import Map

import pandas as pd

from items import vs
import os

class Tool:

	def __init__(self):
		self.root = Tk()
		self.screen_height = None

		self._init_root()
		self.shaListBox = None
		self.data = None
		self.currentId = None
		self._init_box()
		self._init_button()
		self.canvas = None
		self._init_vs()

	def _init_root(self):
		self.screen_height = self.root.winfo_screenheight()
		self.root.geometry("300x"+str(self.screen_height))

	def _init_box(self):
		def alist():
			cwd = os.getcwd()
			pa = pd.read_csv(cwd+"/10118245/result1.csv")
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
			mp = Map(self.currentId)
			self.canvas.refresh(mp)
		change = Button(self.root, text="change", command=reload)
		change.pack()


	def _init_vs(self):

		mp = Map(self.currentId)
		self.canvas = vs(self.root,mp)

		frame=Frame(self.root,width=200,height=self.screen_height)
		frame.pack(expand=True, fill=BOTH) #.grid(row=0,column=0)

		vbar=Scrollbar(frame,orient=VERTICAL)
		vbar.pack(side=RIGHT,fill=Y)
		vbar.config(command=self.canvas.yview)

		self.canvas.configure(scrollregion = self.canvas.bbox("all"))
		self.canvas.config(yscrollcommand=vbar.set)
		self.canvas.pack(side=LEFT,expand=True,fill=BOTH)



	def run(self):
		self.root.mainloop()


if __name__ == "__main__":
	tool = Tool()
	tool.run()
