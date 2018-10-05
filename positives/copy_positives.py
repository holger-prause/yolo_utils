import shutil as sh

with open("pos.txt") as pFile:
    lines = pFile.readlines()
    for line in lines:
        sh.copy(line.strip(), ".")
