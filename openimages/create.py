import os
import sys
import argparse
import shutil
import csv
from PIL import Image

parser = argparse.ArgumentParser()
requiredArguments = parser.add_argument_group("required arguments")
requiredArguments.add_argument("-a", "--annotationfile", type=str, required=True, help="csv file containing categories and bboxes"
                                                                                       "i.e. validation-annotations-bbox.csv")
requiredArguments.add_argument("-t", "--targetdir", type=str, required=True,
                               help="Directory that will contain the yolo dataset.")
requiredArguments.add_argument("-s", "--sourcedir", type=str, required=True, help="Source open images directory containing the images")
parser.add_argument("-c", "--classes", nargs='+', default=[],
                    help="List of space separated classes to use.")
parser.add_argument("-n", "--negatives", action="store_true",
                    help="If specified, images not containing the classes will be used as negatives.")
args = parser.parse_args()

annotationFile = args.annotationfile
if (not os.path.exists(annotationFile)):
    print("Could not find annotation file \"%s\" make sure the file exists.." % (annotationFile))
    sys.exit()

classes = args.classes
sourceDir = args.sourcedir
if (not os.path.exists(sourceDir)):
    print("Image directory \"%s\" does not exists.." % (sourceDir))
    sys.exit()

targetDir = args.targetdir
targetImgDir = os.path.join(targetDir, 'img')
targetPosImgDir = os.path.join(targetImgDir, 'positives')
targetNegImgDir = os.path.join(targetImgDir, 'negatives')

if (not os.path.exists(targetDir)):
    os.makedirs(targetDir)
if (not os.path.exists(targetImgDir)):
    os.mkdir(targetImgDir)
if (not os.path.exists(targetPosImgDir)):
    os.mkdir(targetPosImgDir)
if (not os.path.exists(targetNegImgDir)):
    os.mkdir(targetNegImgDir)


def writeYoloBoxes(yoloFilePath, boxes):
    with open(yoloFilePath, "w") as yoloFile:
        #XMin,XMax,YMin,YMax,label in that order
        #positions are already relative to im dimensions - good job guys :-)
        for box in boxes:
            clsIdx = classes.index(box[4])
            x = box[0]
            y = box[2]
            w = box[1] - x
            h = box[3] - y
            yoloX = x + w / 2.0
            yoloY = y + h / 2.0
            yoloLine = "{0} {1} {2} {3} {4}".format(clsIdx, yoloX, yoloY, w, h)
            yoloFile.write(yoloLine+"\n")

imBboxes = dict()
with open(annotationFile, encoding="utf8", newline='') as csvfile:
    csvReader = csv.reader(csvfile, delimiter=',')
    for row in csvReader:
        labelName = row[2]
        imgId = row[0]
        if labelName in classes:
            if imgId not in imBboxes:
                imBboxes[imgId] = []
            boxes = imBboxes[imgId]
            #XMin,XMax,YMin,YMax
            boxes.append((float(row[4]),float(row[5]),float(row[6]),float(row[7]), labelName))

for idx, imgId in enumerate(imBboxes):
    print("processing {0} out of {1} images".format(idx, len(imBboxes)))

    boxes = imBboxes[imgId]
    imName = imgId+".jpg"
    srcImPath = os.path.join(sourceDir, imName)

    if not os.path.exists(srcImPath):
        print("source image {0} does not exists - skipping".format(srcImPath))
        continue

    yoloFilePath = None;
    if boxes:
        targetImPath = os.path.join(targetPosImgDir, imName)
        yoloFilePath = os.path.join(targetPosImgDir, imgId+".txt")
    else:
        targetImPath = os.path.join(targetNegImgDir, imName)
        yoloFilePath = os.path.join(targetNegImgDir, imgId+".txt")
    shutil.copy(srcImPath, targetImPath)
    writeYoloBoxes(yoloFilePath, boxes)



