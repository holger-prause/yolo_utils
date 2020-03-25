import os
import sys
import argparse
import src.voc_constants as vc
import src.voc_util as vu


def isVocAnnotatation(filename):
    basename = os.path.basename(filename)
    split = os.path.splitext(basename)
    if(len(split) > 1):
        if split[1].lower() == ".xml":
            return True
    return False

def stripFileExt(filename):
    basename = os.path.basename(filename)
    split = os.path.splitext(basename)
    return split[0]

def convertVocToYolo(vocDir, targetDir, classes):
    files = os.listdir(vocDir)
    annotationsMap = {}

    for filename in files:
        filePath = os.path.join(vocDir, filename)
        if(isVocAnnotatation(filePath)):
            srcAnnotation = os.path.join(vocDir, filename)
            vocClassInfo = vu.getVocClassInfo(srcAnnotation, classes)
            if(len(vocClassInfo) > 0):
                annotationsMap[stripFileExt(filePath)] = vocClassInfo

    if(len(classes) == 0):
        for vocInfo in annotationsMap.values():
            for ann in vocInfo:
                lbl = ann["label"]
                if(lbl not in classes):
                    classes.append(lbl)

        classesFilePath = os.path.join(targetDir, "classes.txt")
        with open(classesFilePath, "w") as cf:
            for cls in classes:
                cf.write(cls + '\n')

    for annName in annotationsMap:
        annotations = annotationsMap[annName]
        yoloAnnPath = os.path.join(targetDir, annName+".txt")
        with open(yoloAnnPath, "w") as yoloAnnFile:
            for ann in annotations:
                lbl = ann["label"]
                labelIdx = classes.index(lbl)
                bb = ann["bbox"]
                yoloAnnFile.write(str(labelIdx) + " " + " ".join([str(a) for a in bb]) + '\n')
    return

def main():

    #-v data -t exlucded -p car bus truck motorbike licenseplate -i im_ids.txt -e -s
    parser = argparse.ArgumentParser()
    requiredArguments = parser.add_argument_group("required arguments")
    requiredArguments.add_argument("-v", "--vocdir", type=str, required=True, help="Directory containing the voc annotations")
    requiredArguments.add_argument("-t", "--target", type=str, required=True,help="The directory that will contain the yolo annotations")
    parser.add_argument("-c", "--classesfile", type=str,
                        help="File containing the classes to convert."
                             " If not specified - all voc classes will be converted in a new file"
                             " \"classes.txt\" in the target directory")

    args = parser.parse_args()
    targetDir = args.target
    vocDir = args.vocdir
    classesFile = args.classesfile


    if (not os.path.isdir(vocDir)):
        print( "Voc annotation directory \"%s\" does not exists."%(vocDir))
        sys.exit()

    if(os.path.isfile(targetDir)):
        print( "Target directory \"%s\" is a file."%(targetDir))
        sys.exit()

    if(not os.path.isdir(targetDir)):
        os.makedirs(targetDir)

    classes = []
    if(classesFile):
        if(not os.path.isfile(classesFile)):
            print( "Classes file \"%s\" is not a valid file."%(classesFile))
            sys.exit()
        else:
            with open(classesFile) as cf:
                classes = cf.read().splitlines()
                classes = [x for x in classes if x.strip()]

    convertVocToYolo(vocDir, targetDir, classes)

if __name__ == "__main__":
    main()
