import os
import sys, getopt
import cv2
import numpy as np

dataSetDir = os.curdir

def isImage(path):
    if(os.path.isfile(os.path.join(dataSetDir, path)) and path.lower().endswith((".jpg", ".jpeg"))):
        return True
    return False

def isAnnotationFile(path):
    if(os.path.isfile(os.path.join(dataSetDir, path)) and path.lower().endswith((".txt"))):
        return True
    return False

def stripExtension(path):
    return os.path.splitext(path)[0]

def findImagePath(images, annotation):
    for image in images:
        if(stripExtension(image) == stripExtension(annotation)):
            return image
    return None

def main():
    global dataSetDir
    logs = []
    argv = sys.argv[1:]
    showBbox = False
    logFile = None
    try:
        opts, args = getopt.getopt(argv,"d:l:s",["dir=","logfile=","showbbox"])
        for opt, arg in opts:
            if opt in ("-d", "--dir"):
                dataSetDir = arg
            elif opt in ("-l", "--logfile"):
                logFile = arg
            elif opt in ("-s", "--showbbox"):
                showBbox = True
    except getopt.GetoptError:
        print("verify_dataset.py -d <datasetdir> -l <logfile> -s")
        sys.exit(2)

    annotations = list(filter(isAnnotationFile, os.listdir(dataSetDir)))
    strippedAnnotations = list(map(stripExtension, annotations))

    images = list(filter(isImage, os.listdir(dataSetDir)))
    strippedImages = list(map(stripExtension, images))

    #images with no annotation
    invalidImages = []
    for image in images:
        if(stripExtension(image) not in strippedAnnotations):
            invalidImages.append(image)
            logs.append("Missing annotation file for image {}".format(os.path.join(dataSetDir, image)))

    #annotations with no image
    invalidAnnotations = []
    for annotation in annotations:
        #check if corresponding file exist
        if(stripExtension(annotation) not in strippedImages):
            invalidAnnotations.append(annotation)
            logs.append("Missing image file for annotation {}".format(os.path.join(dataSetDir, annotation)))

    annotations = list(set(annotations) - set(invalidAnnotations))
    images = list(set(images) - set(invalidImages))
    assert(len(annotations) == len(images))

    #check for valid bounding box
    for annotation in annotations:
        with open(os.path.join(dataSetDir, annotation)) as f:
            #check for negatives - may be intended
            lines = list(filter(str.strip, f.readlines()))
            if(len(lines) == 0):
                logs.append("Negative annotation file found: {}".format(os.path.join(dataSetDir, annotation)))
            for line in lines:
                line = line.split(" ")

                #find the corresponding image and read it in as numpy array
                imagePath = os.path.join(dataSetDir, findImagePath(images, annotation))
                image = cv2.imread(imagePath)
                if np.shape(image) == ():
                    logs.append("Can not read image {}".format(imagePath))
                    continue

                imHeight = np.shape(image)[0]
                imWidth = np.shape(image)[1]
                centerX = int(float(line[1]) * imWidth)
                centerY = int(float(line[2]) * imHeight)
                w = int(float(line[3]) * imWidth)
                h = int(float(line[4]) * imHeight)
                x = int(centerX - w / 2)
                y = int(centerY - h / 2)

                try:
                    bboxImage = image[y:y+h, x:x+w]
                    if(bboxImage.shape == (0,0,3)):
                        raise ValueError("Invalid bounding box")
                    elif showBbox:
                        title = imagePath + "  from  " + os.path.join(dataSetDir, annotation)
                        cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),1)
                        cv2.imshow(title, image)
                        cv2.waitKey(0)
                        cv2.destroyWindow(title)
                except:
                    logs.append("Invalid bounding box: {} {} {} {} in file {}".format(x,y,w,h, os.path.join(dataSetDir, annotation)))

    logs = "\n".join(logs)
    if(logFile != None):
        with open(logFile, "w") as f:
            f.write(logs)
    else:
        print(logs)

if __name__ == "__main__":
    main()