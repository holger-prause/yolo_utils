import os
import argparse
import lib.coco as co
import lib.coco_util as cu

parser = argparse.ArgumentParser()
requiredArguments = parser.add_argument_group("required arguments")
requiredArguments.add_argument("-a", "--annotationfile", type=str, required=True, help="Json annotatation file containing categories and bboxes"
                                                                                       "i.e. instances_val2014.json")
requiredArguments.add_argument("-d", "--dataset", type=str, required=True,
                               help="Directory that contains the yolo dataset to modiy.")
requiredArguments.add_argument("-c", "--classes", nargs='+', default=[], required=True,
                              help="List of space separated classes to add.")
requiredArguments.add_argument("-i", "--index", required=True,
                               help="The index on which the classes will be inserted. Existing classes will be shifted if required.")
args = parser.parse_args()
classes = args.classes
datasetDir = args.dataset
annotationFile = args.annotationfile
index = int(args.index)

coco = co.COCO(annotationFile)
catIdsToAdd = coco.getCatIds(classes)
print("found", len(catIdsToAdd), "coco classes for the given classes")

files = os.listdir(datasetDir)
imgIds = []
for file in files:
    baseName = os.path.splitext(file)[0]
    extension = os.path.splitext(file)[1].lower()
    if extension == ".jpg" or extension == ".jpeg":
        imgId = int(baseName.split("_")[2])

        yoloSrcAnnPath = baseName + ".txt"
        yoloSrcAnnPath = os.path.join(datasetDir, yoloSrcAnnPath)
        yoloSrcAnnPathBak = baseName + "_bak.txt"
        yoloSrcAnnPathBak = os.path.join(datasetDir, yoloSrcAnnPathBak)
        with open(yoloSrcAnnPath) as ya:
            lines = ya.read().splitlines()
            lines = [x for x in lines if x.strip()]

            with open(yoloSrcAnnPathBak, 'w') as yab:
                for line in lines:
                    splitLine = line.split()
                    oldIdx = int(splitLine[0])
                    if(oldIdx >= index):
                        splitLine[0] = str(oldIdx + len(classes))
                    yab.write(" ".join(splitLine) + '\n')

                    #write new entries
                    img = coco.imgs[imgId]
                    anns = coco.imgToAnns[imgId]
                    posAnns = [ann for ann in anns if ann['category_id'] in catIdsToAdd]

                for ann in posAnns:
                    catId = ann['category_id']
                    catName = coco.cats[catId]['name']
                    clIdx = classes.index(catName)

                    newIdx = index + clIdx
                    yoloBox = cu.convertBBox(img, ann['bbox'])
                    yab.write(str(newIdx) + " " + " ".join([str(a) for a in yoloBox]) + '\n')
        os.remove(yoloSrcAnnPath)
        os.rename(yoloSrcAnnPathBak, yoloSrcAnnPath)