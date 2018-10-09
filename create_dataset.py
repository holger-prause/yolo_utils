import os
import sys
import argparse
import shutil
import src.voc_constants as vc
import src.voc_util as vu


def createVocDataSet(vocDir, targetDir, vocLabels,  includeNegatives=True):
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
            line = "%s : %s \n" % (key, cfg[key])
            configFile.write(line)

    # iterate the sub datasets
    for year, image_set in vc.vocDataSets:
        imgInDir = (vocInPart + "/JPEGImages") % (vocDir, year)
        imgOutDir = (vocInPart + "/JPEGImages") % (targetDir, year)

        if(not os.path.exists(vocInPart % (vocDir, year))):
            print("dataset", vocInPart % (vocDir, year), "does not exists - skipping")
            continue
        elif(not os.path.exists(imgOutDir)):
            os.makedirs(imgOutDir)
        print("processing %s_%s" % (year, image_set))

        # convert the xml annotations to txt(yolo format)
        imgIds = open((vocInPart + "/ImageSets/Main/%s.txt") % (vocDir, year, image_set)).read().strip().split()
        for idx, imgId in enumerate(imgIds):
            srcImg = ("%s/%s.jpg") % (imgInDir, imgId)
            targetImg = ("%s/%s.jpg") % (imgOutDir, imgId)
            srcAnnotation = (vocInPart + "/Annotations/%s.xml") % (vocDir, year, imgId)
            targetAnnotation = '%s/%s.txt' % (imgOutDir, imgId)

            #get the matching bounding boxes for the specified classes/labels
            yoloClassInfos = vu.getYoloClassInfo(srcAnnotation, vocLabels)
            if(includeNegatives or len(yoloClassInfos) > 0):
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
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--vocdir", type=str, required=True, help="Directory containing the 'VOCdevkit' folder")
    parser.add_argument("-d", "--datasetdir", type=str, default=os.curdir,
                        help="Directory containing the custom images with annotations."
                             "Working dir is default.")
    parser.add_argument("-t", "--target", type=str, required=True,
                        help="The directory that will contain the dataset to create."
                             "This folder must not exists and wil be created by this script. ")
    parser.add_argument("-p", "--positives", nargs='+', default=vc.vocLabels,
                        help="List of space separated voc labels to use as positives."
                             "See voc_info.py for more details to list the available labels.")

    args = parser.parse_args()
    targetDir = args.target
    vocDir = args.vocdir

    if (os.path.exists(targetDir)):
        print( "File or directory \"%s\" already exists - make sure the target directory does not exists and can be created."%(targetDir))
        sys.exit()
    createVocDataSet(vocDir, targetDir, args.positives)

if __name__ == "__main__":
    main()
