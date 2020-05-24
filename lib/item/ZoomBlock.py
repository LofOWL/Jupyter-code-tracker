from tkinter import *
import tkinter as tk

from lib.item.Block import Block


class ZoomBlock(Canvas):

    def __init__(self, parent, upperblock):
        Canvas.__init__(self, parent)

        self.config(bg="green")

        a = Block(upperblock.vs,uppterblock.info,upperblock.ph,upperblock.type)
        a.create()

        self.pack()
