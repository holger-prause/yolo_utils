import argparse
import os
import src.yoloreport as yr

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dir", type=str, required=True, help="Directory containing the images and annotations")
parser.add_argument("-c", "--classesfile", type=str, required=True, help="File containing all classes for the dataset")
parser.add_argument("-f", "--filterclassesfile", type=str, required=False, help="File containing the classes to filter")
parser.add_argument("-i", "--imagepath", action="store_true", help="If specified, the image paths are printed instead of the summary")
args = parser.parse_args()

imgDir = args.dir
files = os.listdir(imgDir)
extensions = [".jpg", ".jpeg", ".png"]

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
for file in files:
    baseName = os.path.splitext(file)[0]
    extension = os.path.splitext(file)[1]
    if extension.lower() in extensions:
        annPath = os.path.join(imgDir, baseName+".txt")
        if os.path.isfile(annPath):
            with open(annPath) as annFile:
                for line in annFile:
                    if(line.strip()):
                        splitLine = line.split()
                        classIdx = int(splitLine[0])
                        yoloReport.addRow(os.path.join(imgDir, file), classIdx)

yoloReport.printReport(args.imagepath)