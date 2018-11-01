import os
import sys
import argparse
import src.coco as co
import shutil


def convertBBox(img, cocoBbox):
    # turn bbox into yolo format- bbox center relative to img width and height
    dw = 1. / img['width']
    dh = 1. / img['height']

    centerX = cocoBbox[0] + cocoBbox[2] / 2.0
    centerX = centerX * dw

    centerY = cocoBbox[1] + cocoBbox[3] / 2.0
    centerY = centerY * dh

    rw = cocoBbox[2] * dw
    rh = cocoBbox[3] * dh
    return (centerX, centerY, rw, rh)


parser = argparse.ArgumentParser()
parser = argparse.ArgumentParser()
requiredArguments = parser.add_argument_group("required arguments")
requiredArguments.add_argument("-a", "--annotationfile", type=str, required=True, help="Json annotatation file containing categories and bboxes"
                                                                                       "i.e. instances_val2014.json")
requiredArguments.add_argument("-t", "--targetdir", type=str, required=True,
                    help="Directory that will contain the yolo dataset."
                         "The directory must not exist and will be created.")

parser.add_argument("-c", "--classes", nargs='+', default=[],
                    help="List of space separated classes to use. If not specified - all classes in the dataset will be used."
                         "See coco_info.py for more details to list the available classes.")
parser.add_argument("-s", "--sourcedir", type=str, required=True, help="Source coco directory containing the images")
parser.add_argument("-i", "--imageidfile", type=str, required=False,
                    help="File containing image ids in each line.These images will be included or excluded."
                         "Per default images will be included, using the -e option excludes them.")
parser.add_argument("-e", "--exclude", action="store_true",
                    help="If specified, images listed in the image id file will be excluded instead of included.")

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
    os.mkdir(targetDir)
if (not os.path.exists(targetImgDir)):
    os.mkdir(targetImgDir)
if (not os.path.exists(targetPosImgDir)):
    os.mkdir(targetPosImgDir)
if (not os.path.exists(targetNegImgDir)):
    os.mkdir(targetNegImgDir)

imIdPath = args.imageidfile
filterIds = []
if (imIdPath):
    if not os.path.isfile(imIdPath):
        print("Image ids file \"%s\" does not exists.." % (imIdPath))
        sys.exit()
    with open(imIdPath) as imIdFile:
        lines = imIdFile.readlines()
        filterIds = [int(x) for x in lines if x.strip().isdigit()]

excludeIms = args.exclude
coco = co.COCO(annotationFile)
if (not classes):
    classes = coco.getCatNames()

catIds = coco.getCatIds(classes)
imgIds = coco.getImgIds()

if (excludeIms):
    imgIds = [x for x in imgIds if x not in filterIds]
elif filterIds:
    imgIds = filterIds

#only create negatives from categories which occur togther with the positives
negCatIds = set()
for imgId in imgIds:
    anns = coco.imgToAnns[imgId]
    posAnns = [ann for ann in anns if ann['category_id'] in catIds]
    negAnns = [ann for ann in anns if ann['category_id'] not in catIds]
    if posAnns and negAnns:
        for negAnn in negAnns:
            negCatIds.add(negAnn['category_id'])

yoloClassesPath = os.path.join(targetDir, "classes.txt")
with open(yoloClassesPath, 'w') as yoloClassesFile:
    yoloClassesFile.write("\n".join(classes))

print("processing %s images" % (len(imgIds)))
for idx, imgId in enumerate(imgIds):
    print("processing %s out of %s images" %(idx+1, len(imgIds)) )
    img = coco.imgs[imgId]
    anns = coco.imgToAnns[imgId]

    posAnns = [ann for ann in anns if ann['category_id'] in catIds]
    negAnns = [ann for ann in anns if ann['category_id'] not in catIds and ann['category_id'] in negCatIds]
    include = len(posAnns) > 0 or len(negAnns) > 0

    if(include):
        srcImg = os.path.join(sourceDir, img['file_name'])
        imBase = os.path.splitext(img['file_name'])[0]
        #determine if positive or negative
        yoloAnnPath = ""
        if posAnns:
            yoloAnnPath = os.path.join(targetPosImgDir, imBase + ".txt")
            targetImg = os.path.join(targetPosImgDir, img['file_name'])
        else:
            yoloAnnPath = os.path.join(targetNegImgDir, imBase + ".txt")
            targetImg = os.path.join(targetNegImgDir, img['file_name'])
        shutil.copyfile(srcImg, targetImg)

        with open(yoloAnnPath, "w") as yoloAnnFile:
            for ann in posAnns:
                catId = ann['category_id']
                catName = coco.cats[catId]['name']
                clIdx = classes.index(catName)
                yoloBox = convertBBox(img, ann['bbox'])
                yoloAnnFile.write(str(clIdx) + " " + " ".join([str(a) for a in yoloBox]) + '\n')