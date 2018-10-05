import os
import sys
import argparse
import src.voc_constants as vc


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--vocdir", type=str, required=True, help="Directory containing the 'VOCdevkit' folder")
    parser.add_argument("-l", "--listvoc", action='store_true',
                        help="Lists all available labels from the voc dataset.")
    parser.add_argument("-i", "--images", nargs='+', help="Lists the images for the given label(s)."
                                                         "Can be either single label or space separated list of labels")

    args = parser.parse_args()
    vocDir = args.vocdir
    imageLabels = args.images

    if (args.listvoc):
        for label in vc.vocLabels:
            print(label)
        sys.exit()

    if (imageLabels):
        invalidLabels = set(imageLabels) - set(vc.vocLabels)
        if (len(invalidLabels) > 0):
            print("Invalid labels found: ", invalidLabels)
            sys.exit(-1)

        imagePaths = []
        for label in imageLabels:
            for year, image_set in vc.vocDataSets:
                statsFilePath = ("%s/VOCdevkit/VOC%s/ImageSets/Main/%s_%s.txt") % (vocDir, year, label, image_set)
                if (os.path.isfile(statsFilePath)):
                    with open(statsFilePath) as statsFile:
                        lines = statsFile.readlines();
                        for line in lines:
                            splittedLine = line.split()
                            if (splittedLine[1] == "1"):
                                imageId = splittedLine[0]
                                imagePath = ("%s/VOCdevkit/VOC%s/JPEGImages/%s.jpg") % (vocDir, year, imageId)
                                imagePaths.append(imagePath)

        for imagePath in imagePaths:
            print(imagePath)

    sys.exit()

if __name__ == "__main__":
    main()
