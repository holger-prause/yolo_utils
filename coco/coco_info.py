import os
import sys
import argparse
import json
import src.coco as co


parser = argparse.ArgumentParser()
requiredArguments = parser.add_argument_group("required arguments")
requiredArguments.add_argument("-a", "--annotationfile", type=str, required=True, help="Json annotatation file containing categories and bboxes"
                                                                            "i.e. instances_val2014.json")
parser.add_argument("-c", "--classes", nargs='+', default=[],
                    help="List of space separated classes to use. If not specified - all classes in the dataset will be used."
                         "See coco_info.py for more details to list the available classes.")
args = parser.parse_args()
classes = args.classes
annotationFile = args.annotationfile

if (not os.path.exists(annotationFile)):
    print("Could not find annotation file \"%s\" make sure the file exists.." % (annotationFile))
    sys.exit()

coco = co.COCO(annotationFile)
stats = coco.getStats(classes)
print(json.dumps(stats, indent=2))

