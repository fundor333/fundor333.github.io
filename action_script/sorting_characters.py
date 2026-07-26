import random
import shutil
from pathlib import Path

path_to_sort = Path("static/Characters")
path_to_origin = Path("static/Characters/origin")

# collect only files from origin directory
onlyfiles = [p for p in path_to_origin.iterdir() if p.is_file()]

random.shuffle(onlyfiles)

i = 1
for p in onlyfiles:
    num = str(i).rjust(3, "0")
    original = p
    target = path_to_sort / f"{num}.png"
    shutil.copyfile(str(original), str(target))
    print(f'"https://fundor333.com/Characters/{num}.png",')
    i += 1
