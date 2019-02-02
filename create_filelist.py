import argparse
import os
import glob

parser = argparse.ArgumentParser()
requiredArguments = parser.add_argument_group("required arguments")
requiredArguments.add_argument("-d", "--dir", type=str, required=True, help="Directory containing the annotations/images")
requiredArguments.add_argument("-o", "--outfile", type=str, required=True, help="File containing the absolute path to the images")
args = parser.parse_args()

imgs = []
imgExts = [".jpg", ".jpeg", ".png"]
for root, directories, filenames in os.walk(args.dir):
    for filename in filenames:
        basename = os.path.basename(filename)
        split = os.path.splitext(basename)
        if(len(split) > 1):
            if split[1].lower() in imgExts:
                imgs.append(os.path.abspath(filename))

with open(args.outfile, 'w') as outFile:
    for img in imgs:
        parent = os.path.join(img, os.pardir)
        imgbase = os.path.splitext(os.path.basename(img))[0]
        annFile = os.path.join(parent, imgbase+".txt")
        if(os.path.isfile(annFile)):
            outFile.write(img+"\n")

