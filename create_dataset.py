import os
import sys
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-s", "--sourcedir", type=str, required=True, help="Directory containing the annotations and images")
parser.add_argument("-t", "--targetdir", type=str, required=True, help="The direcectory which will contain the yolo dataset")
parser.add_argument("-l", "--labelsfile", type=str, required=True, help="File containing the label")
args = parser.parse_args()

classes = []
with open(args.labelsfile) as lblFile:
    classes = lblFile.readlines()
    classes = [x.strip() for x in classes if x.strip()]

targetDir = args.targetdir
if (not os.path.exists(targetDir)):
    os.makedirs(targetDir)

imgs = []
imgExts = [".jpg", ".jpeg", ".png"]
for root, directories, filenames in os.walk(args.sourcedir):
    for filename in filenames:
        basename = os.path.basename(filename)
        split = os.path.splitext(basename)
        if(len(split) > 1):
            if split[1].lower() in imgExts:
                path = os.path.join(root, filename);
                imgs.append(os.path.abspath(path))
                
trainFile = os.path.join(targetDir, "train.txt");      
with open(trainFile, 'w') as outFile:
    for img in imgs:
        parent = os.path.abspath(os.path.join(img, os.pardir))
        imgbase = os.path.splitext(os.path.basename(img))[0]
        annFile = os.path.join(parent, imgbase+".txt")
        if(os.path.isfile(annFile)):
            outFile.write(img+"\n")
            
backupDir = os.path.join(targetDir, "backup");                 
if (not os.path.exists(backupDir)):
    os.makedirs(backupDir)
    
classesFile =  os.path.join(targetDir, "train.names");
if(os.path.abspath(classesFile) != os.path.abspath(args.labelsfile)):
    with open(classesFile, "w") as cF:
        line = "\n".join(classes)
        cF.write(line)
    
with open(os.path.join(targetDir, "train.data"), 'w') as dataFile:
    dataFile.write("classes = "+str(len(classes))+ "\n")        
    dataFile.write("names = "+os.path.abspath(classesFile) + "\n")    
    dataFile.write("backup = "+os.path.abspath(backupDir)  + "\n")
    dataFile.write("train = "+os.path.abspath(trainFile)  + "\n")
    
