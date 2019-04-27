import argparse
import csv

parser = argparse.ArgumentParser()
requiredArguments = parser.add_argument_group("required arguments")
requiredArguments.add_argument("-lf", "--labelfile", type=str, required=True, help="csv file the labels with their translations"
                                                                                   "i.e. class-descriptions-boxable.csv")
requiredArguments.add_argument("-tf", "--translationfile", type=str, required=True, help="text file containing the labels to translate.")
parser.add_argument("-e", "--english2openimage", action="store_true", help="If specified, text from the translation file is translated from english to the open image label."
                                                                           "Default is the other direction, translate from open image label to english")
args = parser.parse_args()

openImage2English = dict()
english2OpenImage = dict()
with open(args.labelfile, encoding="utf8", newline='') as labelfile:
    csvReader = csv.reader(labelfile, delimiter=',')
    for row in csvReader:
        openImage2English[row[0]] = row[1]
        english2OpenImage[row[1]] = row[0]

toTranslate = []
with open(args.translationfile) as tFile:
    toTranslate = tFile.read().splitlines()


translations = []
for l in toTranslate:
    if(args.english2openimage):
        translations.append(english2OpenImage[l])
    else:
        translations.append(openImage2English[l])
print("\n".join(translations))