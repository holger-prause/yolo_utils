import os
import sys
import argparse
import json
import lib.coco as co


parser = argparse.ArgumentParser()
requiredArguments = parser.add_argument_group("required arguments")
requiredArguments.add_argument("-a", "--annotationfile", type=str, required=True, help="Json annotatation file containing categories and bboxes"
                                                                            "i.e. instances_val2014.json")
parser.add_argument("-l", "--listclasses", action="store_true", default=False,
                    help="If specified, the coco classes will be printed")
parser.add_argument("-r", "--relatedclassses", action="store_true", default=False,
                    help="If specified, stats about re")

args = parser.parse_args()
annotationFile = args.annotationfile

if (not os.path.exists(annotationFile)):
    print("Could not find annotation file \"%s\" make sure the file exists.." % (annotationFile))
    sys.exit()

coco = co.COCO(annotationFile)
if(args.listclasses):
    print("\n".join(coco.getCatNames()))
    sys.exit()

stats = coco.getStats()
print(json.dumps(stats, indent=2))

