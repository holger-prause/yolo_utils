import argparse
import os
import glob

parser = argparse.ArgumentParser()
requiredArguments = parser.add_argument_group("required arguments")
requiredArguments.add_argument("-d", "--dir", type=str, required=True, help="Directory containing the annotations/images")
requiredArguments.add_argument("-o", "--outfile", type=str, required=True, help="File containing the absolute path to the images")
args = parser.parse_args()

imgs = []
imgPattern = ["*.jpg", "*.jpeg", "*.png", "*.JPG", "*.JPEG", "*.PNG"]
for imp in imgPattern:
    pattern = args.dir+"/**/"+imp
    for img in glob.glob(pattern, recursive=True):
        imgs.append(os.path.abspath(img))

with open(args.outfile, 'w') as outFile:
    for img in imgs:
        parent = os.path.join(img, os.pardir)
        imgbase = os.path.splitext(os.path.basename(img))[0]
        annFile = os.path.join(parent, imgbase+".txt")
        if(os.path.isfile(annFile)):
            outFile.write(img+"\n")

