# yolo_utils

Some python scripts for building or verifying a yolo dataset.

## Requirments
* Opencv and numpy for reading in the bounding boxes.

  These dependencies can be installed with pip install -r requirements.txt

### verify_dataset.py
This script verifies a yolo dataset. Missing annotations or corrupt images will be reported.
It is also possible to review the bounding boxes and their corresponding labels.

* **Usage:**
The following is the help output of the script.

```javascript
usage: create_dataset.py [-h] -v VOCDIR [-d DATASETDIR] -t TARGET
                         [-p POSITIVES [POSITIVES ...]]

optional arguments:
  -h, --help            show this help message and exit
  -v VOCDIR, --vocdir VOCDIR
                        Directory containing the 'VOCdevkit' folder
  -d DATASETDIR, --datasetdir DATASETDIR
                        Directory containing the custom images with
                        annotations.Working dir is default value.
  -t TARGET, --target TARGET
                        The directory that will contain the dataset to
                        create.This folder must not exists and wil be created
                        by this script.
  -p POSITIVES [POSITIVES ...], --positives POSITIVES [POSITIVES ...]
                        List of space separated voc labels to use as
                        positives.See voc_info.py for more details to list the
                        available labels.
```

### create_dataset.py
This creates a yolo dataset based on the voc dataset.

* **Requirements:**
Download the voc dataset and extract them to a folder.
    * [http://pjreddie.com/media/files/VOCtrainval_11-May-2012.tar](http://pjreddie.com/media/files/VOCtrainval_11-May-2012.tar)
    * [http://pjreddie.com/media/files/VOCtrainval_06-Nov-2007.tar](http://pjreddie.com/media/files/VOCtrainval_06-Nov-2007.tar)
    * [http://pjreddie.com/media/files/VOCtest_06-Nov-2007.tar](http://pjreddie.com/media/files/VOCtest_06-Nov-2007.tar)

* **Usage:**
The following is the help output of the script.

```javascript
usage: create_dataset.py [-h] -v VOCDIR [-d DATASETDIR] -t TARGET
                         [-p POSITIVES [POSITIVES ...]] [-i IGNORE]

optional arguments:
  -h, --help            show this help message and exit
  -v VOCDIR, --vocdir VOCDIR
                        Directory containing the 'VOCdevkit' folder
  -d DATASETDIR, --datasetdir DATASETDIR
                        Directory containing the custom images with
                        annotations.Working dir is default.
  -t TARGET, --target TARGET
                        The directory that will contain the dataset to
                        create.This folder must not exists and wil be created
                        by this script.
  -p POSITIVES [POSITIVES ...], --positives POSITIVES [POSITIVES ...]
                        List of space separated voc labels to use as
                        positives.See voc_info.py for more details to list the
                        available labels.
  -i IGNORE, --ignore IGNORE
                        Path to a file containing image ids which will be not
                        included.See voc_info.py on how to list image ids for
                        a given label.
```


### voc_info.py
This script gives some basic information about the voc dataset.

* **Usage:**
The following is the help output of the script.

```javascript
usage: voc_info.py [-h] -v VOCDIR [-l] [-i IMAGES [IMAGES ...]]

optional arguments:
  -h, --help            show this help message and exit
  -v VOCDIR, --vocdir VOCDIR
                        Directory containing the 'VOCdevkit' folder
  -l, --listvoc         Lists all available labels from the voc dataset.
  -i IMAGES [IMAGES ...], --images IMAGES [IMAGES ...]
                        Lists the image ids for the given label(s).Can be
                        either single label or space separated list of labels
```




    
    
    

