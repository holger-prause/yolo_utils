import os
import sys
import argparse
import xml.etree.ElementTree as ET
import shutil
import src.voc_constants as vc


def isValidDir(dir):
    return (os.path.exists(dir) and os.path.isdir(dir))


def isValidFile(file):
    return (os.path.exists(file) and os.path.isfile(file))


def convertBBox(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)


def convertAnnotation(src, target, positives):
    srcFile = open(src)
    targetFile = open(target, 'w')
    tree = ET.parse(srcFile)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in positives or int(difficult) == 1:
            continue
        cls_id = positives.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))
        bb = convertBBox((w, h), b)
        targetFile.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

    srcFile.close()
    targetFile.close()


def createVocDataSet(vocDir, targetDir, vocLabels):
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
            shutil.copyfile(srcImg, targetImg)

            srcAnnotation = (vocInPart + "/Annotations/%s.xml") % (vocDir, year, imgId)
            targetAnnotation = '%s/%s.txt' % (imgOutDir, imgId)
            convertAnnotation(srcAnnotation, targetAnnotation, vocLabels)

            if (image_set == "val"):
                validationListFile.write(os.path.abspath(targetImg) + "\n")
            else:
                trainListFile.write(os.path.abspath(targetImg) + "\n")
            print("processed entry %s of %s." % (idx, len(imgIds)))

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
                        help="The directory that will contain the dataset to create.")
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
