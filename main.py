from tkinter import *
from map import Map

import pandas as pd

from items import vs


def data():
	pa = pd.read_csv("/Users/apple/Desktop/10118245/result1.csv")
	#pa = pa[pa["status"] == "success"]
	#all_list = list(pa["id"])

	mp = Map("8e6d37c84f1e373c27dbd1db38d77005d5ab27d4#1")
	return mp



root = Tk()


mp = data()

canvas = vs(root,mp)

screen_height = root.winfo_screenheight()

frame=Frame(root,width=200,height=screen_height)
frame.pack(expand=True, fill=BOTH) #.grid(row=0,column=0)

vbar=Scrollbar(frame,orient=VERTICAL)
vbar.pack(side=RIGHT,fill=Y)
vbar.config(command=canvas.yview)

canvas.configure(scrollregion = canvas.bbox("all"))
canvas.config(yscrollcommand=vbar.set)
canvas.pack(side=LEFT,expand=True,fill=BOTH)

root.geometry("300x"+str(screen_height))


root.mainloop()
