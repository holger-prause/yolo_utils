import os
import sys
import argparse
import cv2
import numpy as np

def getPath(path, configRoot):
    if(os.path.isabs(path)):
        return path
    return os.path.join(configRoot, path)

def verifyImage(imgPath, showBbox, labels, logs):
    if(not os.path.isfile(imgPath)):
        logs.append("Missing cv2Image {}".format(os.path.abspath(imgPath)))
        return

    parentDir = os.path.abspath(os.path.join(imgPath, os.pardir))
    imgId = os.path.splitext(os.path.basename(imgPath))[0]
    annotationFilePath = os.path.join(parentDir, imgId+".txt")

    if(not os.path.isfile(annotationFilePath)):
        logs.append("Missing annotation file {}".format(os.path.abspath(annotationFilePath)))
        return

    with open(annotationFilePath) as annotationFile:
        lines = annotationFile.read().splitlines()

        #regardless if bboxes will be shown or not - try to read in the image to see if its corrupt
        cv2Image = cv2.imread(imgPath)
        if (np.shape(cv2Image) == ()):
            logs.append("Can not read cv2Image {}".format(imgPath))
            return

        for line in lines:
            line = line.split(" ")
            labelIdx = int(line[0])
            labelText = labels[labelIdx]
            imHeight = np.shape(cv2Image)[0]
            imWidth = np.shape(cv2Image)[1]
            centerX = int(float(line[1]) * imWidth)
            centerY = int(float(line[2]) * imHeight)
            w = int(float(line[3]) * imWidth)
            h = int(float(line[4]) * imHeight)
            x = int(centerX - w / 2)
            y = int(centerY - h / 2)

            try:
                bboxImage = cv2Image[y:y+h, x:x+w]
                if(bboxImage.shape == (0,0,3)):
                    raise ValueError("Invalid bounding box")
                if showBbox:
                    cv2.putText(cv2Image, labelText, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,0,255), lineType=cv2.LINE_AA)
                    cv2.rectangle(cv2Image,(x,y),(x+w,y+h),(0,255,0),1)

            except:
                logs.append("Invalid bounding box: {} {} {} {} in file {}".format(x,y,w,h, annotationFilePath))

        if(showBbox):
            title = os.path.basename(imgPath) + "  from  " + os.path.basename(annotationFilePath)
            cv2.imshow(title, cv2Image)
            cv2.waitKeyEx()
            cv2.destroyWindow(title)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--outfile", type=str, default=None,
                        help="Path to a file that will contain the error messages. None is the default value."
                             "In that case errors will be print to console.")
    parser.add_argument("-s", "--showbbox", action="store_true",
                        help="Flag. If specified, the bounding boxes within the original image will be shown."
                             "False is the default value.")
    parser.add_argument("-c", "--config", type=str, default="obj.data",
                        help="Yolo training config file. Will contain the references to the label and train/val files."
                             "obj.data is the default value")
    args = parser.parse_args()


    logs = []
    logFile = args.outfile
    if(logFile != None and not os.path.isfile(logFile)):
        print("Log file", os.path.abspath(logFile), "does not exits or is no file.")
        sys.exit(2)

    configFilePath = args.config
    if(not os.path.isfile(configFilePath)):
        print("config file", os.path.abspath(configFilePath), "does not exits or is no file.")
        sys.exit(2)
    configFileRootPath = os.path.abspath(os.path.join(configFilePath, os.pardir))

    showBbox = args.showbbox
    config = {}

    with open(configFilePath) as configFile:
        configLines = configFile.readlines()
        for line in configLines:
            splittedLine = line.split(":", 1)
            key = splittedLine[0].strip()
            value = splittedLine[1].strip()
            config[key] = value

    labels = []
    with open(getPath(config["names"], configFileRootPath)) as labelFile:
        labels = labelFile.read().splitlines()

    trainImages = []
    with open(getPath(config["train"], configFileRootPath)) as trainFile:
        trainImages = trainFile.read().splitlines()

    validationImages = []
    with open(getPath(config["valid"], configFileRootPath)) as validationFile:
        validationImages = validationFile.read().splitlines()

    for img in trainImages:
        verifyImage(getPath(img, configFileRootPath), showBbox, labels, logs)

    for img in validationImages:
        verifyImage(getPath(img, configFileRootPath), showBbox, labels, logs)

    logs = "\n".join(logs)
    if(logFile != None):
        with open(logFile, "w") as f:
            f.write(logs)
    else:
        print(logs)

if __name__ == "__main__":
    main()