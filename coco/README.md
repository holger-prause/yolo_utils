# yolo_utils
Some python scripts for building or verifying a yolo dataset based on the coco dataset.
The order they are usually used is 
1. coco_info.py to get the classes - then pick some classes you want
2. list_ids.py to get the image ids for the classes
   Note that it is a good idea to have ALL objects in the the pictures labeled 
   That's why one uses datasets.
3. create_from_coco.py to create the dataset based on the classes and images ids.

### coco_info.py
This script gives information about the coco dataset.
It can also be used to list the coco classes.

* **Usage:**
The following is the help output of the script.

```javascript
usage: coco_info.py [-h] -a ANNOTATIONFILE [-l]

optional arguments:
  -h, --help            show this help message and exit
  -l, --listclasses     If specified, the coco classes will be printed

required arguments:
  -a ANNOTATIONFILE, --annotationfile ANNOTATIONFILE
                        Json annotatation file containing categories and
                        bboxesi.e. instances_val2014.json
```


### list_ids.py
This script gives list image ids for the given classes.

* **Usage:**
The following is the help output of the script.

```javascript
usage: list_ids.py [-h] -a ANNOTATIONFILE -o OUTFILE -c CLASSESFILE [-e]
                   [-f FILTERDIMENSIONS [FILTERDIMENSIONS ...]]

optional arguments:
  -h, --help            show this help message and exit
  -e, --exclusive       If specified - all images not matching the classes or
                        filter dimensions will be excluded.
  -f FILTERDIMENSIONS [FILTERDIMENSIONS ...], --filterdimensions FILTERDIMENSIONS [FILTERDIMENSIONS ...]
                        Space separated width and height filter
                        values.Bounding boxes bigger than the given dimensions
                        will be filtered out.If the exclusive flag is
                        specified - the image will be excluded.

required arguments:
  -a ANNOTATIONFILE, --annotationfile ANNOTATIONFILE
                        Json annotatation file containing categories and
                        bboxesi.e. instances_val2014.json
  -o OUTFILE, --outfile OUTFILE
                        File that will contain the image ids
  -c CLASSESFILE, --classesfile CLASSESFILE
                        File contain the classes to use.See coco_info.py for
                        more details to list the available classes.
```


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


### add_class_from_coco.py
This lets you add bounding boxes from a coco dataset for specific classes
to an existing dataset. Handle with care and make a backup before.
Don't forget to update the labels file for training.
This script is most useful when building a custom dataset from coco.

* **Usage:**
The following is the help output of the script.

```javascript
usage: add_class_from_coco.py [-h] -a ANNOTATIONFILE -d DATASET -c CLASSES
                              [CLASSES ...] -i INDEX

optional arguments:
  -h, --help            show this help message and exit

required arguments:
  -a ANNOTATIONFILE, --annotationfile ANNOTATIONFILE
                        Json annotatation file containing categories and
                        bboxesi.e. instances_val2014.json
  -d DATASET, --dataset DATASET
                        Directory that contains the yolo dataset to modiy.
  -c CLASSES [CLASSES ...], --classes CLASSES [CLASSES ...]
                        List of space separated classes to add.
  -i INDEX, --index INDEX
                        The index on which the classes will be inserted.
                        Existing classes will be shifted if required.

```


    
    
    

