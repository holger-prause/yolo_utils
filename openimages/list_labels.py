import argparse
import csv

parser = argparse.ArgumentParser()
requiredArguments = parser.add_argument_group("required arguments")
requiredArguments.add_argument("-a", "--annotationfile", type=str, required=True, help="csv file containing categories and bboxes"
                                                                                        "i.e. validation-annotations-bbox.csv")
requiredArguments.add_argument("-i", "--imageidfile", type=str, required=True,
                    help="File containing image ids in each line for which the labels will be listed")
parser.add_argument("-l", "--labelfile", type=str, required=False, help="csv file the labels with their translations"
                                                                        "i.e. class-descriptions-boxable.csv")
args = parser.parse_args()

translations = dict()
if(args.labelfile):
    with open(args.labelfile, encoding="utf8", newline='') as labelfile:
        csvReader = csv.reader(labelfile, delimiter=',')
        for row in csvReader:
            translations[row[0]] = row[1]

imIds = []
with open(args.imageidfile) as imIdFile:
    imIds = imIdFile.read().splitlines()

stats = dict()
with open(args.annotationfile, encoding="utf8", newline='') as csvfile:
    csvReader = csv.reader(csvfile, delimiter=',')
    for row in csvReader:
        imgId = row[0]
        if imgId in imIds:
            labelName = row[2]
            if labelName in translations:
                labelName = labelName + "  /  " + translations[labelName]

            if labelName not in stats:
                stats[labelName] = [0]
            amount = stats[labelName][0]
            stats[labelName][0] = amount + 1

print(stats)