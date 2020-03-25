import os
import sys
import argparse
import shutil
import src.voc_constants as vc
import src.voc_util as vu

def createVocDataSet(vocDir, targetDir, vocLabels,  filterImIds, excludeIms, skipNegatives):
    os.mkdir(targetDir)
    os.mkdir("%s/backup" % (targetDir))

    vocInPart = "%s/VOCdevkit/VOC%s"
    trainListFile = open("%s/train.txt" % (targetDir), "w")
    validationListFile = open("%s/valid.txt" % (targetDir), "w")

    with open("%s/obj.names" % (targetDir), "w") as configFile:
        configFile.write("\n".join(vocLabels))

    cfg = {
        "classes": len(vocLabels),
        "train": os.path.abspath(trainListFile.name),
        "valid": os.path.abspath(validationListFile.name),
        "names": os.path.abspath("%s/obj.names" % (targetDir)),
        "backup": os.path.abspath("%s/backup" % (targetDir))
    }

    with open("%s/obj.data" % (targetDir), "w") as configFile:
        for key in cfg:
            line = "%s=%s \n" % (key, cfg[key])
            configFile.write(line)

    # iterate the sub datasets
    for year, image_set in vc.vocDataSets:
        imgInDir = (vocInPart + "/JPEGImages") % (vocDir, year)
        imgOutDir = (vocInPart + "/img") % (targetDir, year)

        if(not os.path.exists(vocInPart % (vocDir, year))):
            print("dataset", vocInPart % (vocDir, year), "does not exists - skipping")
            continue
        elif(not os.path.exists(imgOutDir)):
            os.makedirs(imgOutDir)

        # convert the xml annotations to txt(yolo format)
        imgIds = open((vocInPart + "/ImageSets/Main/%s.txt") % (vocDir, year, image_set)).read().strip().split()
        if (excludeIms):
            imgIds = [x for x in imgIds if x not in filterImIds]
        elif filterImIds:
            imgIds = filterImIds

        for idx, imgId in enumerate(imgIds):
            print("processing entry %s of %s for dataset %s_%s" % (idx+1, len(imgIds), year, image_set))
            srcImg = ("%s/%s.jpg") % (imgInDir, imgId)
            targetImg = ("%s/%s.jpg") % (imgOutDir, imgId)
            srcAnnotation = (vocInPart + "/Annotations/%s.xml") % (vocDir, year, imgId)
            targetAnnotation = '%s/%s.txt' % (imgOutDir, imgId)

            #get the matching bounding boxes for the specified classes/labels
            yoloClassInfos = vu.getVocClassInfo(srcAnnotation, vocLabels)
            if(not skipNegatives or len(yoloClassInfos) > 0):
                with open(targetAnnotation, "w") as targetAnnotationFile:
                    for yci in yoloClassInfos:
                        labelIdx = vocLabels.index(yci["label"])
                        bb = yci["bbox"]
                        targetAnnotationFile.write(str(labelIdx) + " " + " ".join([str(a) for a in bb]) + '\n')
                shutil.copyfile(srcImg, targetImg)
                if (image_set == "val"):
                    validationListFile.write(os.path.abspath(targetImg) + "\n")
                else:
                    trainListFile.write(os.path.abspath(targetImg) + "\n")

    trainListFile.close()
    validationListFile.close()
    return

def main():

    #-v data -t exlucded -p car bus truck motorbike licenseplate -i im_ids.txt -e -s
    parser = argparse.ArgumentParser()
    requiredArguments = parser.add_argument_group("required arguments")
    requiredArguments.add_argument("-v", "--vocdir", type=str, required=True, help="Directory containing the 'VOCdevkit' folder")
    requiredArguments.add_argument("-t", "--target", type=str, required=True,
                        help="The directory that will contain the dataset to create."
                             "This folder must not exists and wil be created by this script. ")

    parser.add_argument("-p", "--positives", nargs='+', default=vc.vocLabels,
                        help="List of space separated voc labels to use as positives."
                             "See voc_info.py for more details to list the available labels.")
    parser.add_argument("-i", "--imageidfile", type=str,
                        help="File containing image ids in each line.These images will be included or excluded."
                             "Per default images will be included, using the -e option excludes them.")
    parser.add_argument("-e", "--exclude", action="store_true",
                        help="If specified, images listed in the image id file will be excluded instead of included.")
    parser.add_argument("-s", "--skipnegatives", action="store_true", default=False,
                        help="Flag determining if negatives should be included or not."
                             "If specified - negatives will not be created."
                             "Default value is False.")

    args = parser.parse_args()
    targetDir = args.target
    excludeIms = args.exclude
    vocDir = args.vocdir
    filterImIdPath = args.imageidfile
    skipNegatives = args.skipnegatives
    filterImIds = []

    if (filterImIdPath != None):
        if (not os.path.exists(filterImIdPath)):
            print( "Could not find ignore file \"%s\" make sure the file exists.."%(filterImIdPath))
            sys.exit()
        else:
            with open(filterImIdPath) as imIdFile:
                filterImIds = imIdFile.read().splitlines()
                filterImIds = [x for x in filterImIds if x.split()]

    if (os.path.exists(targetDir)):
        print( "File or directory \"%s\" already exists - make sure the target directory does not exists and can be created."%(targetDir))
        sys.exit()
    createVocDataSet(vocDir, targetDir, args.positives, filterImIds, excludeIms, skipNegatives)

if __name__ == "__main__":
    main()
