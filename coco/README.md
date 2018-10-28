# yolo_utils
Some python scripts for building or verifying a yolo dataset based on the coco dataset.

### create_from_coco.py
This creates a yolo dataset based on the coco dataset.

* **Requirements:**
Download the coco datasets and extract them to a folder.
    * http://cocodataset.org/#home

* **Usage:**
The following is the help output of the script.

```javascript
usage: create_from_coco.py [-h] -a ANNOTATIONFILE -t TARGETDIR
                           [-c CLASSES [CLASSES ...]] -s SOURCEDIR
                           [-i IMAGEIDFILE] [-e]

optional arguments:
  -h, --help            show this help message and exit
  -c CLASSES [CLASSES ...], --classes CLASSES [CLASSES ...]
                        List of space separated classes to use. If not
                        specified - all classes in the dataset will be
                        used.See coco_info.py for more details to list the
                        available classes.
  -s SOURCEDIR, --sourcedir SOURCEDIR
                        Source coco directory containing the images
  -i IMAGEIDFILE, --imageidfile IMAGEIDFILE
                        File containing image ids in each line.These images
                        will be included or excluded.Per default images will
                        be included, using the -e option excludes them.
  -e, --exclude         If specified, images listed in the image id file will
                        be excluded instead of included.

required arguments:
  -a ANNOTATIONFILE, --annotationfile ANNOTATIONFILE
                        Json annotatation file containing categories and
                        bboxesi.e. instances_val2014.json
  -t TARGETDIR, --targetdir TARGETDIR
                        Directory that will contain the yolo dataset.The
                        directory must not exist and will be created.
```


### coco_info.py
This script gives some basic information about the coco dataset.

* **Usage:**
The following is the help output of the script.

```javascript
usage: coco_info.py [-h] -a ANNOTATIONFILE [-c CLASSES [CLASSES ...]]

optional arguments:
  -h, --help            show this help message and exit
  -c CLASSES [CLASSES ...], --classes CLASSES [CLASSES ...]
                        List of space separated classes to use. If not
                        specified - all classes in the dataset will be
                        used.See coco_info.py for more details to list the
                        available classes.

required arguments:
  -a ANNOTATIONFILE, --annotationfile ANNOTATIONFILE
                        Json annotatation file containing categories and
                        bboxesi.e. instances_val2014.json
```




    
    
    

