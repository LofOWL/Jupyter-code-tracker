import sys
import os

from run import run
import shutil

from connecter import connecter 


def transfer(argv):
	path = sys.argv[1]
	file_name = path.split("/")[-1]
	saveTo = sys.argv[2]
	cn = connecter(folder_from=path,folder_to=saveTo,jar=os.getcwd()+"/lhdiff_2019.jar")
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