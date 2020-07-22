import argparse
import os

parser = argparse.ArgumentParser()
requiredArguments = parser.add_argument_group("required arguments")
requiredArguments.add_argument("-s", "--sourcedir", type=str, required=True, help="Source directory containing the images and annotation")
requiredArguments.add_argument("-sc", "--sourceclasses", type=str, required=True, help="File containing the classes/labels for the source(old) annotations")
requiredArguments.add_argument("-tc", "--targetclasses", type=str, required=True, help="File containing the classes/labels for the target(new) annotations")
args = parser.parse_args()

sourceClasses = []
with open(args.sourceclasses) as cf:
    classes = cf.read().splitlines()
    sourceClasses = [x for x in classes if x.strip()]

targetClasses = []
with open(args.targetclasses) as cf:
    classes = cf.read().splitlines()
    targetClasses = [x for x in classes if x.strip()]
   
imgDir = args.sourcedir
extensions = [".jpg", ".jpeg", ".png"]
for root, directories, filenames in os.walk(args.sourcedir):
    for filename in filenames:
        basename = os.path.basename(filename)
        split = os.path.splitext(basename)
        if(len(split) > 1):
            basenameNoExt = os.path.splitext(basename)[0]
            basenameExt = split[1]
            if basenameExt.lower() in extensions:
                srcImgPath = os.path.join(root, filename)
                srcAnnPath = os.path.join(root, basenameNoExt+".txt")
                if(os.path.isfile(srcAnnPath)):
                    rewrittenContent = []
                    with open(srcAnnPath) as saf:
                        srcLines = saf.read().splitlines()
                        srcLines = [x for x in srcLines if x.strip()]
                        for idx, srcLine in enumerate(srcLines):
                            splitLine = srcLine.split()
                            oldIdx = int(splitLine[0])
                            srcClass = sourceClasses[oldIdx]
                            if(srcClass in targetClasses):
                                newIdx = targetClasses.index(srcClass)
                                splitLine[0] = str(newIdx)
                                rewrittenContent.append(" ".join(splitLine))
                    with open(srcAnnPath, 'w') as saf:
                        saf.write("\n".join(rewrittenContent))                
