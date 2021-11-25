import os
import sys
path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
notebook_path = os.path.join(path,'..')+"/notebook"
sys.path.insert(0,notebook_path)
path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.insert(1,path)

from notebook import Notebook
OLD_PATH = f'{path}/old_re.ipynb'
NEW_PATH = f'{path}/new_re.ipynb'

OLD = Notebook(OLD_PATH)
NEW = Notebook(NEW_PATH)

OLDLINES = OLD.lines
NEWLINES = NEW.lines

OLDLINESLEN = len(OLDLINES)
NEWLINESLEN = len(NEWLINES)

OLDCELLLEN = len(OLD.cells)
NEWCELLLEN = len(NEW.cells)

OLDLINESSTR = [str(line) for line in OLDLINES]
NEWLINESSTR =  [str(line) for line in NEWLINES]

