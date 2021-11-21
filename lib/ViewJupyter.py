
from selenium import webdriver
import os
#import appscript
from multiprocessing import Process
import requests
import subprocess
import time


class ViewJupyter:


    def __init__(self,mp):
        self.path = mp.path
        self.old_path = self.path+"/Old/"
        self.mp = mp 
        self.broswer_c = None
        self.broswer_p = None

    def refresh(self,mp):
        self.mp = mp
        if self.broswer_c != None and self.broswer_p != None:
            self.updateC()
            self.updateP()

    def updateC(self):
        # file_path = self.old_path+self.mp.name+"#c"+".ipynb"
        file_path = "example/Old/"+self.mp.name+"#c.ipynb"
        html = file_path.replace("#","%23")
        #self.broswer_c.get("http://localhost:9000/tree"+"/Desktop"+self.html.split("Desktop")[1])
        print(html)
        print("get int c")
        self.broswer_c.get("http://localhost:9000/tree/"+html)

    def updateP(self):
        # file_path = self.old_path+self.mp.name+"#p"+".ipynb"
        file_path = "example/Old/"+self.mp.name+"#p.ipynb"
        html = file_path.replace("#","%23")
        #self.broswer_p.get("http://localhost:9000/tree"+"/Desktop"+self.html.split("Desktop")[1])
        print(html)
        print("get in p")
        self.broswer_p.get("http://localhost:9000/tree/"+html)

    def run(self):

        # terminal = appscript.app('Terminal').do_script(commond)

        #n = os.fork()

        def _init_jupyter():
            commond = "xterm -e jupyter notebook --allow-root --no-browser --port=9000"
            os.system(commond)

        def _init_web():

            isNotInit = True
            while isNotInit:

                diff = subprocess.check_output("jupyter notebook list",shell=True)
                alist = diff.decode("utf-8").split("\n")
                if any(["9000" in i for i in alist]):
                    print(alist)
                    isNotInit = False
                    address = [i for i in alist if "9000" in i][0].split(" :: ")[0]

            self.address = address

            self.broswer_c = webdriver.Chrome('./lib/chromedriver')
            self.broswer_p = webdriver.Chrome('./lib/chromedriver')

            self.broswer_c.get(self.address)
            self.broswer_p.get(self.address)


            self.updateC()
            self.updateP()

        p1 = Process(target=_init_jupyter)

        p1.start()

        _init_web()





    def color_block(self,index,type):

        def js_set(index):
            return """var x = document.getElementById("notebook-container").querySelectorAll(".cell");x[%s].style.background='red';"""%(index)

        if type == "c":
            self.broswer_c.execute_script(js_set(index-1))
        else:
            self.broswer_p.execute_script(js_set(index-1))
