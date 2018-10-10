import os
import sys
import argparse
import src.voc_constants as vc
import src.voc_util as vu

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--vocdir", type=str, required=True, help="Directory containing the 'VOCdevkit' folder")
    parser.add_argument("-l", "--listvoc", action='store_true',
                        help="Lists all available labels from the voc dataset.")
    parser.add_argument("-i", "--images", nargs='+', help="Lists the image ids for the given label(s)."
                                                         "Can be either single label or space separated list of labels")

    args = parser.parse_args()
    vocDir = args.vocdir
    imageLabels = args.images

    if (args.listvoc):
        for label in vc.vocLabels:
            print(label)
        sys.exit()

    imageIds = []
    if (imageLabels):
        invalidLabels = set(imageLabels) - set(vc.vocLabels)
        if (len(invalidLabels) > 0):
            print("Invalid labels found: ", invalidLabels)
            sys.exit(-1)

        vocInPart = "%s/VOCdevkit/VOC%s"
        for year, image_set in vc.vocDataSets:
            if(not os.path.exists(vocInPart % (vocDir, year))):
                continue

            statsFilePath = (vocInPart + "/ImageSets/Main/%s.txt") % (vocDir, year, image_set)
            with open(statsFilePath) as statsFile:
                imgIds = statsFile.read().strip().split()
                for imgId in imgIds:
                    annotationFilePath = (vocInPart + "/Annotations/%s.xml") % (vocDir, year, imgId)
                    classInfo = vu.getYoloClassInfo(annotationFilePath, imageLabels)
                    if(len(classInfo) > 0):
                        imageIds.append(imgId)
        print("\n".join(imageIds))
    sys.exit()


if __name__ == "__main__":
    main()
