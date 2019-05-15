import pandas as pd

class YoloReport:
    def __init__(self, classes):
        self.classes = classes
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
        imgCount = df.imageid.nunique()
        imgIds = df.imageid.unique()

        if(showImgIds):
            for imgId in imgIds:
                print(imgId)
            return

        groupByImage = df.groupby(['imageid']).sum()
        summaryColumns = ['Class', 'Nr.Images', 'Nr.Object', '%Image', '%Object']

        #get total nr of objects
        totalObjects = 0
        for cls in self.classes:
            totalObjects = totalObjects + groupByImage[cls].sum()

        summaryData = []
        for cls in self.classes:
            filterRows = groupByImage.loc[groupByImage[cls] > 0]
            imgsPerClass = len(filterRows.index)
            objectsPerClass = groupByImage[cls].sum()
            percentageImage = (100 * imgsPerClass) / imgCount
            percentageObjects = (100 * objectsPerClass) / totalObjects
            row = [cls, imgsPerClass, objectsPerClass, percentageImage, percentageObjects]
            summaryData.append(row)

        summary = pd.DataFrame(data=summaryData, columns=summaryColumns)
        summary.sort_values(by=['Nr.Images'], inplace=True, ascending=False)
        print(summary.to_string())
