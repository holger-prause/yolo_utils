import xml.etree.ElementTree as ET

def convertBBox(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)

def getVocClassInfo(vocAnnotationFilePath, filterClasses):
    classInfo = []
    with open(vocAnnotationFilePath) as vocAnnotationFile:
        tree = ET.parse(vocAnnotationFile)
        root = tree.getroot()
        size = root.find('size')
        w = int(size.find('width').text)
        h = int(size.find('height').text)

        for obj in root.iter('object'):
            annotationDict = {}
            difficult = obj.find('difficult').text
            if int(difficult) == 1:
                continue

            cls = obj.find('name').text
            if(cls in filterClasses or len(filterClasses) == 0):
                xmlbox = obj.find('bndbox')
                b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
                     float(xmlbox.find('ymax').text))
                bb = convertBBox((w, h), b)
                annotationDict["label"] = cls
                annotationDict["bbox"] = bb

            if(len(annotationDict) > 0):
                classInfo.append(annotationDict)
    return classInfo