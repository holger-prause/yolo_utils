import argparse
import os
import src.yoloreport as yr

parser = argparse.ArgumentParser()
requiredArguments = parser.add_argument_group("required arguments")
requiredArguments.add_argument("-s", "--sourcedir", type=str, required=True, help="Directory containing the images and annotations")
requiredArguments.add_argument("-c", "--classesfile", type=str, required=True, help="File containing all classes for the dataset")
parser.add_argument("-f", "--filterclassesfile", type=str, required=False, help="File containing the classes to filter")
parser.add_argument("-i", "--imagepath", action="store_true", help="If specified, the image paths are printed instead of the summary")
args = parser.parse_args()

extensions = [".jpg", ".jpeg", ".png"]
imgDir = args.sourcedir
imgInfos = []
for root, directories, filenames in os.walk(imgDir):
    for filename in filenames:
        basename = os.path.basename(filename)
        split = os.path.splitext(basename)
        if(len(split) > 1):
            basenameNoExt = os.path.splitext(basename)[0]
            basenameExt = split[1]
            if basenameExt.lower() in extensions:
                imgPath = os.path.join(root, filename)
                annPath = os.path.join(root, basenameNoExt+".txt")
                if(os.path.isfile(annPath)):
                    imgInfos.append((imgPath, annPath))
                    
classes = []
with open(args.classesfile) as fc:
    classes = fc.read().splitlines()
    classes = [x for x in classes if x.strip()]

filterClasses = classes
if(args.filterclassesfile):
    with open(args.filterclassesfile) as fc:
        filterClasses = fc.read().splitlines()
        filterClasses = [x for x in filterClasses if x.strip()]

yoloReport = yr.YoloReport(classes, filterClasses)
for imgInfo in imgInfos:
    imgPath = imgInfo[0]
    annPath = imgInfo[1]
    with open(annPath) as annFile:
        for line in annFile:
            if(line.strip()):
                splitLine = line.split()
                classIdx = int(splitLine[0])
                yoloReport.addRow(imgPath, classIdx)
            
yoloReport.printReport(args.imagepath)