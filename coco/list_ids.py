import argparse
import json
import src.coco as co
from operator import itemgetter
from collections import OrderedDict

def addResultCount(coco, result, catIds):
    for catId in catIds:
        resultDictKey = coco.cats[catId]["name"]
        if(not resultDictKey in result):
            result[resultDictKey] = 0
        result[resultDictKey] = result[resultDictKey] + 1

def filterAnn(ann, catIds, filterDims):
    match = ann['category_id'] in catIds
    if match and filterDims:
        minW = int(filterDims[0])
        minH = int(filterDims[1])
        bbox = ann['bbox']
        if bbox[2] < minW or bbox[3] < minH:
            match = False
    return match

parser = argparse.ArgumentParser()
requiredArguments = parser.add_argument_group("required arguments")
requiredArguments.add_argument("-a", "--annotationfile", type=str, required=True, help="Json annotatation file containing categories and bboxes"
                                                                                       "i.e. instances_val2014.json")
requiredArguments.add_argument("-o", "--outfile", type=str, required=True, help="File that will contain the image ids")

requiredArguments.add_argument("-c", "--classesfile", required=True,
                    help="File contain the classes to use."
                         "See coco_info.py for more details to list the available classes.")
parser.add_argument("-e", "--exclusive", action="store_true", default=False,
                    help="If specified - all images not matching the classes or filter dimensions will be excluded.")
parser.add_argument("-f", "--filterdimensions", nargs='+', default=[],
                    help="Space separated width and height filter values."
                         "Bounding boxes bigger than the given dimensions will be filtered out."
                         "If the exclusive flag is specified - the image will be excluded.")


args = parser.parse_args()
classes = []
classesFile = args.classesfile
annotationFile = args.annotationfile
exclusive = args.exclusive
filterDims = args.filterdimensions
outFile = args.outfile

with open(classesFile) as cf:
    classes = cf.read().splitlines()
    classes = [x for x in classes if x.strip()]

coco = co.COCO(annotationFile)
catIds = coco.getCatIds(classes)
imgIds = coco.getImgIds([], catIds)

excludedImgIds = []
includedImgIds = []

includedDict = dict()
excludedDict = dict()

for idx, imgId in enumerate(imgIds):
    img = coco.imgs[imgId]
    imgAnns = coco.imgToAnns[imgId]
    filterAnns = [x for x in imgAnns if filterAnn(x, catIds, filterDims)]

    excludedCatIds = [x['category_id'] for x in imgAnns if x not in filterAnns]
    addResultCount(coco, excludedDict, excludedCatIds)

    if(exclusive and len(imgAnns) != len(filterAnns)):
        excludedImgIds.append(imgId)
    else:
        includedCatIds = [x['category_id'] for x in filterAnns]
        addResultCount(coco, includedDict, includedCatIds)
        includedImgIds.append(imgId)

print("Found", len(imgIds), "image candidates matching the classes")
print("images from class matches included", len(includedImgIds))
print("object stats:")
includedDict = OrderedDict(sorted(includedDict.items(), key=itemgetter(1), reverse=True))
print(json.dumps(includedDict, indent=2))

print("images from class matches excluded", len(excludedImgIds))
print("object stats:")
excludedDict = OrderedDict(sorted(excludedDict.items(), key=itemgetter(1), reverse=True))
print(json.dumps(excludedDict, indent=2))
with open(outFile, 'w') as of:
    for ri in includedImgIds:
        of.write(str(ri)+"\n")