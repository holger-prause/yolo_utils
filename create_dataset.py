import os
import sys, getopt
import argparse
import xml.etree.ElementTree as ET
import shutil

defaultVocClasses = ["aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
              "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]


#sets=[('2012', 'train'), ('2012', 'val'), ('2007', 'train'), ('2007', 'val'), ('2007', 'test')]
sets=[('2012', 'train')]

classes = ["aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]


def isValidDir(dir):
    return (os.path.exists(dir) and os.path.isdir(dir))

def isValidFile(file):
    return (os.path.exists(file) and os.path.isfile(file))

def convertBBox(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def createAnnotation(src, target):
    srcFile = open(src)
    targetFile = open(target, 'w')
    tree=ET.parse(srcFile)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convertBBox((w,h), b)
        targetFile.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

    srcFile.close()
    targetFile.close()

def createVocDataSet(vocDir, targetDir):
    #iterate the sub datasets
    for year, image_set in sets:
        ##get the image base names (without extension)
        imgIds = open("%s/VOCdevkit/VOC%s/ImageSets/Main/%s.txt"%(vocDir, year, image_set)).read().strip().split()
        imgSrcDir = "%s/VOCdevkit/VOC%s/JPEGImages"%(vocDir, year)
        imgTargetDir = "%s/VOCdevkit/VOC%s/"%(targetDir, year)
        #copy the images so the voc dir stays unpolluted
        shutil.copytree(imgSrcDir, imgTargetDir)

        #read in the xml annotatiuon and convert it to yolo format
        #place the result annotation file along with the copied image
        for imgId in imgIds:
            srcAnnotation = '%s/VOCdevkit/VOC%s/Annotations/%s.xml'%(vocDir, year, imgId)
            targetAnnotation = '%s/%s.txt'%(imgTargetDir, imgId)
            createAnnotation(srcAnnotation, targetAnnotation)
    return

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--vocdir", type=str, required=True, help="Directory containing the 'VOCdevkit' folder")
    parser.add_argument("-d", "--datasetdir", type=str, default=os.curdir, help="Directory containing the custom images with annotations."
                                                             "Working dir is default.")
    parser.add_argument("-t", "--target",  type=str, required=True, help="The directory that will contain the dataset to create.")
    parser.add_argument("-p", "--positives", nargs='+', default=defaultVocClasses, help="List of space separated voc classes to us as positives. "
                                                           "Use option -l to list the default values(all).")
    parser.add_argument("-n", "--negatives", nargs='+', default=defaultVocClasses, help="List of space separated voc classes to use as negatives."
                                                             "Use option -l to list the default values(all).")
    parser.add_argument("-l", "--listvoc", action='store_true', help="Lists all available classes from the voc dataset.")

    args = parser.parse_args()
    targetDir = args.target
    vocdir =  args.vocdir

    if(args.listvoc):
        print(defaultVocClasses)
        sys.exit()

    if(os.path.exists(targetDir)):
        print("File or directory \"%s\" already exists - make sure the target directory does not exists and can be created."%(targetDir))
        sys.exit()

    createVocDataSet(vocdir, targetDir)

if __name__ == "__main__":
    main()




