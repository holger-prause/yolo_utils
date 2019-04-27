import argparse
import os
import glob
import shutil

parser = argparse.ArgumentParser()
requiredArguments = parser.add_argument_group("required arguments")
requiredArguments.add_argument("-s", "--sourcedir", type=str, required=True, help="Directory containing the source annotations/images")
requiredArguments.add_argument("-t", "--targetdir", type=str, required=True, help="Directory containing the target annotations/images")
requiredArguments.add_argument("-sc", "--sourceclasses", type=str, required=True, help="File containing the classes/labels for the source annotations")
requiredArguments.add_argument("-tc", "--targetclasses", type=str, required=True, help="File containing the classes/labels for the target annotations")
args = parser.parse_args()

annSourceDir = args.sourcedir
annTargetDir = args.targetdir

sourceClasses = []
with open(args.sourceclasses) as cf:
    classes = cf.read().splitlines()
    sourceClasses = [x for x in classes if x.strip()]

targetClasses = []
with open(args.targetclasses) as cf:
    classes = cf.read().splitlines()
    targetClasses = [x for x in classes if x.strip()]

#keep old idx and append unknown classes
srcClsDiff = [x for x in sourceClasses if x not in targetClasses]
mergedClasses = []
mergedClasses.extend(targetClasses)
mergedClasses.extend(srcClsDiff)

targetAnns = glob.iglob(annTargetDir + '/*.txt')
targetAnns = [os.path.basename(x) for x in targetAnns]

srcImgs = dict()
imgPattern = ["*.jpg", "*.jpeg", "*.png", "*.JPG", "*.JPEG", "*.PNG"]
for imp in imgPattern:
    pattern = annSourceDir+"/"+imp

    for img in glob.iglob(pattern):
        imgId = os.path.basename(img)
        imgId = os.path.splitext(imgId)[0]
        srcImgs[imgId] = os.path.basename(img)

#take care of line ending stuff
def appendToFile(path, content):
    newContent = []
    if(os.path.isfile(path)):
        with open(path) as f:
            oldLines = f.read().splitlines()
            oldLines = [x for x in oldLines if x.strip()]
            newContent.extend(oldLines)
    newContent.extend(content)
    with open(path, 'w') as f:
        if newContent:
            f.write("\n".join(newContent))

def writeAnnotation(srcAnn, targetAnn):
    with open(srcAnn) as saf:
        srcLines = saf.read().splitlines()
        srcLines = [x for x in srcLines if x.strip()]

        #rewrite old idx to new idx
        for idx, srcLine in enumerate(srcLines):
            splitLine = srcLine.split()
            oldIdx = int(splitLine[0])
            srcClass = sourceClasses[oldIdx]
            newIdx = mergedClasses.index(srcClass)
            splitLine[0] = str(newIdx)
            srcLines[idx] = " ".join(splitLine)
        appendToFile(targetAnn, srcLines);

for srcAnn in glob.iglob(annSourceDir+'/*.txt'):
    print("processing %s" % (srcAnn))
    srcAnnFileName = os.path.basename(srcAnn)
    srcAnnId = os.path.splitext(srcAnnFileName)[0]
    targetAnn = os.path.join(annTargetDir, srcAnnFileName)

    if(srcAnnFileName in targetAnns):
        writeAnnotation(srcAnn, targetAnn)

    #unknown annotation but with corresponding image - merge it
    elif(srcAnnId in srcImgs):
        srcImg = os.path.join(annSourceDir, srcImgs[srcAnnId])
        targetImg = os.path.join(annTargetDir, srcImgs[srcAnnId])
        shutil.copyfile(srcImg, targetImg)
        writeAnnotation(srcAnn, targetAnn)
    else:
        print("No matching src image or target annotation found for %s - skipping." % (srcAnnFileName))

with open(os.path.join(annTargetDir, "classes_merged.txt"), "w") as cmf:
    cmf.write("\n".join(mergedClasses))

appendToFile(args.targetclasses,srcClsDiff)
