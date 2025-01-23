import random
import os
import shutil

path_to_sort = "static/Characters"
path_to_origin = "static/Characters/origin"
onlyfiles = os.listdir(path_to_origin)

random.shuffle(onlyfiles)

i = 1
for e in onlyfiles:
    num = str(i).rjust(3, "0")
    original = f"{path_to_origin}/{e}"
    target = f"{path_to_sort}/{num}.png"
    shutil.copyfile(original, target)
    print(f'"https://fundor333.com/Characters/{num}.png",')
    i += 1
