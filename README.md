# yolo_utils

A collection of python scripts for building a yolo dataset.
In the **voc** and **coco** folder you will find create scripts 
which allows you to specify the classes to use.

This project is mainly for myself.

## Requirments
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

### add_class.py
Allows you to shift the index in the annotation files. Usefull when adding a new class.


* **Usage:**
The following is the help output of the script.

```javascript
usage: add_class.py [-h] -d DIR -a AMOUNT -i INDEX

optional arguments:
  -h, --help            show this help message and exit

required arguments:
  -d DIR, --dir DIR     Directory containing the images and annotation
  -a AMOUNT, --amount AMOUNT
                        How many classes to add. This will shift all indices
                        starting at the start index with the given amount.
  -i INDEX, --index INDEX
                        The class start index
```
    

### merge_dataset.py
This merges two datasets. Source classes not contained in the target set will be appended.
Existing classes will keep their index. The target classes file will be rewritten 
and contain the new classes(if their are any)

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