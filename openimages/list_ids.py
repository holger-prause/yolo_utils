import argparse
import os
import sys
import csv

parser = argparse.ArgumentParser()
requiredArguments = parser.add_argument_group("required arguments")
requiredArguments.add_argument("-a", "--annotationfile", type=str, required=True, help="csv annotatation file containing classes and bboxes"
                                                                                       "i.e. validation-annotations-bbox.csv")
requiredArguments.add_argument("-o", "--outfile", type=str, required=True, help="File that will contain the image ids")
parser.add_argument("-c", "--classes", nargs='+', default=[],
                    help="List of space separated classes to use.")

args = parser.parse_args()
annotationFile = args.annotationfile
outFilePath = args.outfile
classes = args.classes

if (not os.path.exists(annotationFile)):
    print("Annotation file \"%s\" does not exists.." % (annotationFile))
    sys.exit()

imgIds = set()
with open(annotationFile, encoding="utf8", newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        labelName = row[2]
        imgId = row[0]
        if labelName in classes:
            imgIds.add(imgId)

with open(outFilePath, 'w') as outFile:
    for imgId in imgIds:
        outFile.write(imgId+"\n")