import pandas as pd
import numpy as np

class YoloReport:
    def __init__(self, classes, filterClasses):
        self.classes = classes
        self.filterClasses = filterClasses
        self.data = []

        columns = ['imageid']
        columns.extend(classes)
        self.columns = columns

    def addRow(self, imgId, clsIdx):
        rowData = [imgId]
        classesData = []
        for idx, val in enumerate(self.classes):
            if idx == clsIdx:
                classesData.append(1)
            else:
                classesData.append(0)
        rowData.extend(classesData)
        self.data.append(rowData)

    def printReport(self, showImgIds):
        df = pd.DataFrame(data=self.data, columns=self.columns)
        totalImages = df.imageid.nunique()

        groupByImage = df.groupby(['imageid']).sum()
        summaryColumns = ['Class', 'Nr.Images', 'Nr.Object', '%Image', '%Object']

        #get total nr of objects
        totalObjects = 0
        for cls in self.classes:
            totalObjects = totalObjects + groupByImage[cls].sum()

        summaryData = []
        imgIds = []
        for cls in self.filterClasses:
            #get all images for class
            filterRows = groupByImage.loc[groupByImage[cls] > 0]
            imgIdsForClass = filterRows.index.tolist()
            imgIds.extend(imgIdsForClass)

            imgsPerClass = len(imgIdsForClass)
            objectsPerClass = groupByImage[cls].sum()
            percentageImage = (100 * imgsPerClass) / totalImages
            percentageObjects = (100 * objectsPerClass) / totalObjects
            row = [cls, imgsPerClass, objectsPerClass, percentageImage, percentageObjects]
            summaryData.append(row)

        summary = pd.DataFrame(data=summaryData, columns=summaryColumns)
        summary.sort_values(by=['Nr.Images'], inplace=True, ascending=False)
        if(showImgIds):
            for imgId in imgIds:
                print(imgId)
        else:
            print("total images: {0} ; total objects: {1}".format(totalImages, totalObjects))
            print(summary.to_string())