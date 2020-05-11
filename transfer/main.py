import sys
import os
import shutil
import pandas as pd

from lib.connecter import connecter
from lib.run import run
from lib.Map import Map

def transfer(argv):
    path = sys.argv[1]
    file_name = path.split("/")[-1]
    saveTo = sys.argv[2]
    cn = connecter(folder_from=path,folder_to=saveTo,jar=os.getcwd()+"/Tool/lhdiff_2019.jar")
    cn.copy2(file_name)
    return cn.folder_to,file_name



if __name__ == "__main__":
    a_path,file_name = transfer(sys.argv)

    path = "/".join([a_path,file_name,file_name])
    saveTo="/".join([a_path,file_name])

    repo = run(path,saveTo)
    repo.collectIpynb()

    saveTo="/".join([a_path,file_name])

    repo = run(saveTo,saveTo)
    repo.processIpynb()

    pa = pd.read_csv(saveTo+"/result1.csv")
    pa = pa[pa["status"] == "success"]
    all_list = list(pa["id"])
    for i in all_list:
        a = Map(i,saveTo)
        a.parentMaptoChild()
        a.sortbyChild()
        a.write()
