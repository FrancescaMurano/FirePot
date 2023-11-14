import os
from pathlib import Path
from utils_path import Path as pattino
path1 = os.path.join(__file__,"home")
path2 = os.path.dirname(__file__)

# print(str(Path(path2).parents[0])) # "path/to"
# print(str(Path(path2).parents[1])) # "path"
# print(str(Path(path2).parents[2])) # "."
p = pattino()

# path3 ="C:\Users\fmurano\Documents\GitHub\myhoneypot\app\home\users"
p1 = os.path.dirname(__file__)
print(os.path.basename(p1))
# print("PATH1 ",path1)
# print("PATH2 ",path2)
