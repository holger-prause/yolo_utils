# yolo_utils

A collection of python scripts for building a yolo dataset.
In the **voc** and **coco** folder you will find create scripts 
which allows you to specify the classes to use.

This project is mainly for myself.

## Requirements
* Opencv and numpy for reading in the bounding boxes.

  These dependencies can be installed with pip install -r requirements.txt

### verify_dataset.py
This script verifies a yolo dataset. Missing annotations or corrupt images will be reported.
It is also possible to review the bounding boxes and their corresponding labels.

* **Usage:**
The following is the help output of the script.

```javascript
usage: verify_dataset.py [-h] [-o OUTFILE] [-s] [-c CONFIG]

optional arguments:
  -h, --help            show this help message and exit
  -o OUTFILE, --outfile OUTFILE
                        Path to a file that will contain the error messages.
                        None is the default value.In that case errors will be
                        print to console.
  -s, --showbbox        Flag. If specified, the bounding boxes within the
                        original image will be shown.False is the default
                        value.
  -c CONFIG, --config CONFIG
                        Yolo training config file. Will contain the references
                        to the label and train/val files.obj.data is the
                        default value
```

    
### merge_dataset.py
This merges two datasets. Source classes not contained in the target set will be appended.
Existing classes will keep their index. The target classes file will be rewritten 
and contain the new classes(if there are any)

* **Usage:**
The following is the help output of the script.

```javascript
usage: merge_dataset.py [-h] -s SOURCEDIR -t TARGETDIR -sc SOURCECLASSES -tc
                        TARGETCLASSES

optional arguments:
  -h, --help            show this help message and exit

required arguments:
  -s SOURCEDIR, --sourcedir SOURCEDIR
                        Directory containing the source annotations/images
  -t TARGETDIR, --targetdir TARGETDIR
                        Directory containing the target annotations/images
  -sc SOURCECLASSES, --sourceclasses SOURCECLASSES
                        File containing the classes/labels for the source
                        annotations
  -tc TARGETCLASSES, --targetclasses TARGETCLASSES
                        File containing the classes/labels for the target
                        annotations
```

### clean_annotations.py
Cleans up a yolo dataset, removes duplicate boxes or boxes which are out of the screen.
It also attempts to repair boxes which are just slightly out of screen but could fit otherwise.
Boxes smaller than 1px in width or height will also be removed. Its possible to filter based
on width and height of boxes too. The repaired annotations will be in a subfolder 
of the source dir with the name "review".

* **Usage:**
The following is the help output of the script.

```javascript
usage: clean_annotations.py [-h] -s SOURCEDIR [-mw MINWIDTH] [-mh MINHEIGHT]
                            [-sr]

optional arguments:
  -h, --help            show this help message and exit
  -s SOURCEDIR, --sourcedir SOURCEDIR
                        Directory containing the annotations/images
  -mw MINWIDTH, --minwidth MINWIDTH
                        The minimum width a bounding box must have, default is
                        1px
  -mh MINHEIGHT, --minheight MINHEIGHT
                        The minimum height a bounding box must have, default
                        is 1px
  -sr, --skipreview     If flag is specified, the cleanup operation will be
                        applied directly on the source folder - not
                        recommended
```


### create_dataset.py
Creates a yolo dataset ready to train. The images must already be annotated.
It will also create automatically a validation dataset with 10 percent of the train images.

* **Usage:**
The following is the help output of the script.

```javascript
usage: create_dataset.py [-h] -s SOURCEDIR -t TARGETDIR -l LABELSFILE
                         [-v VALIDATIONDIR]

optional arguments:
  -h, --help            show this help message and exit
  -v VALIDATIONDIR, --validationdir VALIDATIONDIR
                        Directory containing the validation annotations and
                        images If not specified, 10 percent of the train
                        images will be used.

required arguments:
  -s SOURCEDIR, --sourcedir SOURCEDIR
                        Directory containing the annotations and images
  -t TARGETDIR, --targetdir TARGETDIR
                        The direcectory which will contain the yolo dataset
  -l LABELSFILE, --labelsfile LABELSFILE
                        File containing the label
```


### modify_dataset.py
Modifies a dataset by analyzing the source and target labels and modifying the annotations accordingly. 
Class indices will be updated and entries which are no longer present in the target label file will be removed.
**HANDLE WITH CARE - THIS CAN DESTROY YOUR DATASET IF LABELS ARE OUTDATED OR WRONG - BACKUP FIRST - YOU HAVE BEEN WARNED!!!**


* **Usage:**
The following is the help output of the script.

```javascript
usage: modify_dataset.py [-h] -s SOURCEDIR -sc SOURCECLASSES -tc TARGETCLASSES

optional arguments:
  -h, --help            show this help message and exit

required arguments:
  -s SOURCEDIR, --sourcedir SOURCEDIR
                        Source directory containing the images and annotation
  -sc SOURCECLASSES, --sourceclasses SOURCECLASSES
                        File containing the classes/labels for the source(old)
                        annotations
  -tc TARGETCLASSES, --targetclasses TARGETCLASSES
                        File containing the classes/labels for the target(new)
                        annotations
```

### yolo_info.py
Analyzes your yolo dataset and gives insight about class distribution. 
This is useful when balancing a dataset or checking previous modifications.

* **Usage:**
The following is the help output of the script.

```javascript
usage: yolo_info.py [-h] -s SOURCEDIR -c CLASSESFILE [-f FILTERCLASSESFILE]
                    [-i]

optional arguments:
  -h, --help            show this help message and exit
  -f FILTERCLASSESFILE, --filterclassesfile FILTERCLASSESFILE
                        File containing the classes to filter
  -i, --imagepath       If specified, the image paths are printed instead of
                        the summary

required arguments:
  -s SOURCEDIR, --sourcedir SOURCEDIR
                        Directory containing the images and annotations
  -c CLASSESFILE, --classesfile CLASSESFILE
                        File containing all classes for the dataset
```
