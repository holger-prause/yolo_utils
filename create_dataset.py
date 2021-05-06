import os
import sys
import argparse
import random

parser = argparse.ArgumentParser()
requiredArguments = parser.add_argument_group("required arguments")
requiredArguments.add_argument("-s", "--sourcedir", type=str, required=True, help="Directory containing the annotations and images")
requiredArguments.add_argument("-t", "--targetdir", type=str, required=True, help="The direcectory which will contain the yolo dataset")
requiredArguments.add_argument("-l", "--labelsfile", type=str, required=True, help="File containing the label")
parser.add_argument("-v", "--validationdir", type=str, required=False, help="Directory containing the validation annotations and images"                                                                 
                    + " If not specified, 10 percent of the train images will be used.")
args = parser.parse_args()

classes = []
with open(args.labelsfile) as lblFile:
    classes = lblFile.readlines()
    classes = [x.strip() for x in classes if x.strip()]

targetDir = args.targetdir
if (not os.path.exists(targetDir)):
    os.makedirs(targetDir)

imgExts = [".jpg", ".jpeg", ".png"]
def collectAnnotatedImgs(imgDir):
    annotatedImgs = []
    for root, directories, filenames in os.walk(imgDir):
        for filename in filenames:
            basename = os.path.basename(filename)
            split = os.path.splitext(basename)
            if(len(split) > 1):
                basenameNoExt = os.path.splitext(basename)[0]
                basenameExt = split[1]
                if basenameExt.lower() in imgExts:
                    imgPath = os.path.join(root, filename)
                    annPath = os.path.join(root, basenameNoExt+".txt")
                    if(os.path.isfile(annPath)):
                        annotatedImgs.append(os.path.abspath(imgPath))
    return annotatedImgs

trainImgs = collectAnnotatedImgs(args.sourcedir);
trainFile = os.path.join(targetDir, "train.txt");      

valImgs = []
if(args.validationdir):
   valImgs = collectAnnotatedImgs(args.validationdir);
   trainImgs = [x for x in trainImgs if x not in valImgs]
else:
    amounntValImg = int(len(trainImgs) / 10)
    if(amounntValImg) < len(trainImgs):    
        random.shuffle(trainImgs)
        for i in range(amounntValImg):
            valImgs.append(trainImgs.pop(i))
      
with open(trainFile, 'w') as outFile:
    for img in trainImgs:
        outFile.write(img+"\n")
            
valFile = os.path.join(targetDir, "valid.txt");      
with open(valFile, 'w') as outFile:
    for img in valImgs:
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
    dataFile.write("valid = "+os.path.abspath(valFile)  + "\n")
    
print("Picked", len(trainImgs), "training images")
print("Picked", len(valImgs), "validation images")   
    