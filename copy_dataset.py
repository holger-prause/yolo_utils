import argparse
import os
import shutil

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--imagepathfile", type=str, required=True, help="File containing the image paths")
parser.add_argument("-t", "--targetdir", type=str, required=True, help="Dir where to copy the images and their annotations"
                                                                       "will be created of does not exists")
args = parser.parse_args()

paths = []
with open(args.imagepathfile) as iif:
    paths = iif.read().splitlines()
    paths = [x for x in paths if x.strip()]

if (not os.path.exists(args.targetdir)):
    os.mkdir(args.targetdir)

for p in paths:
    p = os.path.abspath(p)
    imgId = os.path.splitext(p)[0]
    parent = os.path.abspath(os.path.join(p, os.pardir))
    annFile = os.path.join(parent, imgId+".txt")
    if(os.path.isfile(annFile)):
        targetAnnFile = os.path.join(args.targetdir, os.path.basename(annFile))
        shutil.copyfile(annFile, targetAnnFile)
    if(os.path.isfile(p)):
        targetImg = os.path.join(args.targetdir, os.path.basename(p))
        shutil.copyfile(p, targetImg)
