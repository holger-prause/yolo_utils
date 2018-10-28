# yolo_utils
Some python scripts for building or verifying a yolo dataset based on the voc dataset.

### create_from_voc.py
This creates a yolo dataset based on the voc dataset.

* **Requirements:**
Download the voc dataset and extract them to a folder.
    * [http://pjreddie.com/media/files/VOCtrainval_11-May-2012.tar](http://pjreddie.com/media/files/VOCtrainval_11-May-2012.tar)
    * [http://pjreddie.com/media/files/VOCtrainval_06-Nov-2007.tar](http://pjreddie.com/media/files/VOCtrainval_06-Nov-2007.tar)
    * [http://pjreddie.com/media/files/VOCtest_06-Nov-2007.tar](http://pjreddie.com/media/files/VOCtest_06-Nov-2007.tar)

* **Usage:**
The following is the help output of the script.

```javascript
usage: create_from_voc.py [-h] -v VOCDIR -t TARGET
                          [-p POSITIVES [POSITIVES ...]] [-i IMAGEIDFILE] [-e]
                          [-s]

optional arguments:
  -h, --help            show this help message and exit
  -p POSITIVES [POSITIVES ...], --positives POSITIVES [POSITIVES ...]
                        List of space separated voc labels to use as
                        positives.See voc_info.py for more details to list the
                        available labels.
  -i IMAGEIDFILE, --imageidfile IMAGEIDFILE
                        File containing image ids in each line.These images
                        will be included or excluded.Per default images will
                        be included, using the -e option excludes them.
  -e, --exclude         If specified, images listed in the image id file will
                        be excluded instead of included.
  -s, --skipnegatives   Flag determining if negatives should be included or
                        not.If specified - negatives will not be
                        created.Default value is False.

required arguments:
  -v VOCDIR, --vocdir VOCDIR
                        Directory containing the 'VOCdevkit' folder
  -t TARGET, --target TARGET
                        The directory that will contain the dataset to
                        create.This folder must not exists and wil be created
                        by this script.
```


### voc_info.py
This script gives some basic information about the voc dataset.

* **Usage:**
The following is the help output of the script.

```javascript
usage: voc_info.py [-h] -v VOCDIR [-l] [-i IMAGES [IMAGES ...]]

optional arguments:
  -h, --help            show this help message and exit
  -l, --listvoc         Lists all available labels from the voc dataset.
  -i IMAGES [IMAGES ...], --images IMAGES [IMAGES ...]
                        Lists the image ids for the given label(s).Can be
                        either single label or space separated list of labels

required arguments:
  -v VOCDIR, --vocdir VOCDIR
                        Directory containing the 'VOCdevkit' folder
```




    
    
    

