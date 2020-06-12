import os
import sys
import argparse
import cv2
import numpy as np
import os
import shutil

DUPLICATES_TEMPLATE = "Duplicate bounding boxes with the same class"
INVALID_DIMENSION_TEMPLATE = "Invalid dimensions [w * h] ({} * {}) - minimum dimension were ({} * {})"
INVALID_COORDINATES_TEMPLATE = "Invalid screen coordinates [x1, y1, x2, y2] - ({}, {} {} {})"

class ProblemUnit:
    def __init__(self, fullImgPath, fullAnnPath, annLines):
        self.fullImgPath = fullImgPath
        self.fullAnnPath = fullAnnPath
        self.annLines = annLines
        
    def __eq__(self, other):
        return (self.fullImgPath == other.fullImgPath 
                and self.fullAnnPath == other.fullAnnPath)

    def __hash__(self):
        return hash((self.fullImgPath, self.fullAnnPath))   

def convertToYoloLine(cls, imW, imH, x1, y1, w, h):
    #voc formar x1,y1,w,h
    dw = 1. / imW
    dh = 1. / imH

    centerX = x1 + w / 2.0
    centerX = centerX * dw

    centerY = y1 + h / 2.0
    centerY = centerY * dh

    rw = w * dw
    rh = h * dh    
    return "{} {} {} {} {}".format(cls, centerX, centerY, rw, rh);


parser = argparse.ArgumentParser()
parser.add_argument("-s", "--sourcedir", type=str, required=True, help="Directory containing the annotations/images")
parser.add_argument("-mw", "--minwidth", type=int, required=False, default=1, help="The minimum width a bounding box must have, default is 1px", )
parser.add_argument("-mh", "--minheight", type=int, required=False, default=1, help="The minimum height a bounding box must have, default is 1px")
parser.add_argument("-sr", "--skipreview", required=False, action="store_true", default=False, help="If flag is specified, the cleanup operation will be applied directly"
                                                                                        " on the source folder - not recommended")

args = parser.parse_args()
mW = args.minwidth
mH = args.minheight



problemUnits = set()
imgExts = [".jpg", ".jpeg", ".png"]
files = os.listdir(args.sourcedir)
for f in files:
    fullImgPath = os.path.join(args.sourcedir, f)
    if(os.path.isfile(fullImgPath)):
        fileSplit = os.path.splitext(f);
        
        
        
        if(len(fileSplit) > 1):
            fileExt = fileSplit[1]
            if fileExt.lower() in imgExts:
                fullAnnPath = os.path.join(args.sourcedir, fileSplit[0]+".txt")    
                if(os.path.isfile(fullAnnPath)):
                    cv2Image = cv2.imread(fullImgPath)
                    imHeight = np.shape(cv2Image)[0]
                    imWidth = np.shape(cv2Image)[1]
                    
                    lines = []
                    hasProblems = False
                    with open(fullAnnPath) as annotationFile:
                        lines = annotationFile.read().splitlines();                        
                        lines = [x1 for x1 in lines if x1.strip()]
                    
                    uniquelines = set(lines)
                    if(len(uniquelines) < len(lines)):
                        print(DUPLICATES_TEMPLATE.format(fullAnnPath))
                        hasProblems = True
                        lines = list(uniquelines)    

                    filteredLines = []
                    logMsgsForFile = []
                    for line in lines:
                        if(line.strip()):
                            lineTokens = line.split(" ")
                            cls = int(lineTokens[0])
                            centerX = int(float(lineTokens[1]) * imWidth)
                            centerY = int(float(lineTokens[2]) * imHeight)
                            w = int(float(lineTokens[3]) * imWidth)
                            h = int(float(lineTokens[4]) * imHeight)
                            x1 = int(centerX - w / 2)
                            x2 = x1 + w;
                            y1 = int(centerY - h / 2)
                            y2 = y1 + h;
                            
                            if(w < mW or h < mH):
                               logMsgsForFile.append(INVALID_DIMENSION_TEMPLATE.format(w, h, mW, mH)) 
                               logMsgsForFile.append("  --Skipping Box") 
                               hasProblems = True
                               continue
                            
                            if(x1 < 0 or x2 > imWidth or y1 < 0 or y2 > imHeight):
                                hasProblems = True
                                logMsgsForFile.append(INVALID_COORDINATES_TEMPLATE.format(x1, y1, x2, y2)) 
                                beyondRepair = (x2 <= 0 or x1 >= imWidth) or (y2 <= 0 or y1 >= imHeight)
                               
                                if(beyondRepair):
                                    logMsgsForFile.append("  --Coordinates completely out of screen - Skipping Box")
                                    continue
                                else:
                                    if(x1 < 0):
                                        x1 = 0
                                    if(x2 > imWidth):
                                        w = imWidth - x1;
                                    if(y1 < 0):
                                        y1 = 0
                                    if(y2 > imHeight):
                                        h = imHeight - y1

                                    if(w < mW or h < mH):
                                        logMsgsForFile.append("  --Invalid Box width after adjusting screen coordinates - Skipping Box") 
                                        continue
                                    else:
                                        logMsgsForFile.append("  --Adjusted Box successfully") 
                                        adjustedLine = convertToYoloLine(cls, imWidth, imHeight, x1, y1, w, h)
                                        line = adjustedLine                                      
                            filteredLines.append(line)   
                            
                    if(hasProblems):                     
                        problemUnits.add(ProblemUnit(fullImgPath, fullAnnPath, filteredLines))  
                        print(fullAnnPath)
                        for msg in logMsgsForFile:
                            print("  " + msg)
                            
                                    
                    
if(len(problemUnits) > 0):
    print("Found {} annotations with at least one error".format(len(problemUnits)))                    
    
    if(not args.skipreview):                  
        reviewDir = os.path.join(args.sourcedir, "review")
        if (not os.path.exists(reviewDir)):
            os.makedirs(reviewDir)
    
    for pU in problemUnits:
        targetAnn = pU.fullAnnPath
        if(not args.skipreview):
            targetImg = os.path.join(reviewDir, os.path.basename(pU.fullImgPath));
            shutil.copy(pU.fullImgPath, targetImg);
            targetAnn = os.path.join(reviewDir, os.path.basename(pU.fullAnnPath));
            
        with open(targetAnn, "w") as ta:
            content = "\n".join(pU.annLines)
            ta.write(content)