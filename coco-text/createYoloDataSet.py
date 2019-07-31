import os
import shutil
import sys
import coco_text
import argparse

def convertBBox(img, cocoBbox):
    # turn bbox into yolo format- bbox center relative to img width and height
    #voc formar x,y,w,h
    dw = 1. / img['width']
    dh = 1. / img['height']

    centerX = cocoBbox[0] + cocoBbox[2] / 2.0
    centerX = centerX * dw

    centerY = cocoBbox[1] + cocoBbox[3] / 2.0
    centerY = centerY * dh

    rw = cocoBbox[2] * dw
    rh = cocoBbox[3] * dh
    return (centerX, centerY, rw, rh)
    

def writeAnnotations(yoloAnnPath, img, anns):
    if(len(anns) == 0):
        return 
    
    with open(yoloAnnPath, "w") as yoloAnnFile:
        for ann in anns:
            yoloBox = convertBBox(img, ann['bbox'])
            classIdx = labels.index(ann['class'] + " " + ann['legibility']) 
            yoloAnnFile.write(str(classIdx) + " " + " ".join([str(a) for a in yoloBox]) + '\n')
            
def createDataSet(imgIds, imgDataFile, targetImgDir):    
    srcImgDir = args.imagedir;    
    
    with open(imgDataFile, 'w') as imgDataFileH:
        for idx, imgId in enumerate(imgIds):
            print("processing ", idx+1, " out of ", len(imgIds))
            img = ct.imgs[imgId]
            imgFileName = img['file_name']
            srcImg = os.path.join(srcImgDir, imgFileName)
            annotationFileName = os.path.splitext(imgFileName)[0] + ".txt"
                
            annIds = ct.imgToAnns[imgId]
            anns = ct.loadAnns(annIds)
            if(len(anns) > 0):
                targetImg = os.path.join(targetImgDir, imgFileName) 
                targetAnn = os.path.join(targetImgDir, annotationFileName)
                shutil.copyfile(srcImg, targetImg)
                writeAnnotations(targetAnn, img, anns);    
                imgDataFileH.write(targetImg + "\n")    
    
    
        
        
parser = argparse.ArgumentParser()
parser.add_argument("-a", "--annotationfile", type=str, required=True, help="Json annotatation file containing categories and bboxes"
                                                                                       "i.e. COCO_Text.json")
parser.add_argument("-i", "--imagedir", type=str, required=True, help="Directory containing the train images - coco text uses" 
                    "coco 2014 train images.")
parser.add_argument("-t", "--targetdir", type=str, required=True,
                               help="Directory that will contain the yolo dataset.")
args = parser.parse_args()

ct = coco_text.COCO_Text(args.annotationfile)
ct.info()

#in contrast to other coco scripts i don't feel like it should be possible to specify labels to use for now
labels = ["machine printed legible", "machine printed illegible", "handwritten legible", 
           "handwritten illegible", "others legible", "others illegible"]
dsTypes = ["train", "valid"]

if (not os.path.exists(args.targetdir)):
    os.makedirs(args.targetdir)
    
backUpDir = os.path.join(args.targetdir, "backup")  
if (not os.path.exists(backUpDir)):
    os.makedirs(backUpDir)  
    
with open(os.path.join(args.targetdir, "coco_text.data"), 'w') as dataFile:
    dataFile.write("classes = "+str(len(labels))+ "\n")  
    labelsFile = os.path.join(args.targetdir, "labels.txt")      
    with open(os.path.join(labelsFile), "w") as labelsFileH:
        line = "\n".join(labels)
        labelsFileH.write(line)
    dataFile.write("names = "+labelsFile + "\n")    
    dataFile.write("backup = "+backUpDir + "\n")
    
    for dsType in dsTypes:
        print("creating the ", dsType + "dataset");
        
        targetImgDir = os.path.join(args.targetdir, dsType);
        imgDataFile = os.path.join(args.targetdir, dsType + ".txt");
        if (not os.path.exists(targetImgDir)):
            os.makedirs(targetImgDir)

        imgIds = []
        if(dsType == "train"):
            imgIds = ct.train
        else:
            imgIds = ct.val 
    
        dataLine = dsType + " = " + imgDataFile + "\n"
        dataFile.write(dataLine)
        createDataSet(imgIds, imgDataFile, targetImgDir)    

        
        



#print("annotationFileName size: ", len(anns))


#dataDir='../../../Desktop/MSCOCO/data'
#dataType='train2014'