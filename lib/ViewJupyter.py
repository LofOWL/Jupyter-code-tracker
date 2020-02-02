
from selenium import webdriver
import os
import appscript
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
    	self.updateC()
    	self.updateP()

    def updateC(self):
    	self.file_path = self.old_path+self.mp.name+"#c"+".ipynb"
    	self.html = self.file_path.replace("#","%23")
    	self.broswer_c.get("http://localhost:9000/tree"+"/Desktop"+self.html.split("Desktop")[1])

    def updateP(self):
    	self.file_path = self.old_path+self.mp.name+"#p"+".ipynb"
    	self.html = self.file_path.replace("#","%23")
    	self.broswer_p.get("http://localhost:9000/tree"+"/Desktop"+self.html.split("Desktop")[1])

    def run(self):
    	commond = "jupyter notebook --allow-root --no-browser --port=9000"
    	terminal = appscript.app('Terminal').do_script(commond)


    	time.sleep(3)


    	diff = subprocess.check_output("jupyter notebook list",shell=True)
    	alist = diff.decode("utf-8").split("\n")
    	#print(alist)
    	address = [i for i in alist if "9000" in i][0].split(" :: ")[0]
    	#print(address)

    	self.address = address

    	self.broswer_c = webdriver.Chrome("chromedriver")
    	self.broswer_c.get(self.address)

    	self.broswer_p = webdriver.Chrome("chromedriver")
    	self.broswer_p.get(self.address)

    	
    	self.updateC()
    	self.updateP()
    	

    def color_block(self,index,type):
        
        def js_set(index):
        	return """var x = document.getElementById("notebook-container").querySelectorAll(".cell");x[%s].style.background='red';"""%(index)
		
        if type == "c":
            self.broswer_c.execute_script(js_set(index-1))
        else:
            self.broswer_p.execute_script(js_set(index-1))
