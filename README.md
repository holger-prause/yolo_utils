# yolo_utils

Some python scripts for building or verifying a yolo dataset.

## Requirments
* Opencv and numpy for reading in the bounding boxes.

  Can be installed with pip install -r requirements.txt

### verify_dataset.py
This will scan a directory(not recursivly) for images and annotation files.Any missing images and/or annotation files are reported.
Bounding boxes will be extracted and analyzed. It is also possible to review them.
Any obviously wrong coordinates(leading to empty bboxes) can be detected this way.

* **Usage:**
verify_dataset.py -d &lt;datasetdir&gt; -l &lt;logfile&gt; -s

All program arguments are optional and explained below:

* -d or --dir Optional: The path to the directory containing the images and annotation files. **os.curdir** as default
* -l or --logfile Optional: Path to a file that will contain the error messages. None as default. In that case errors will be print to console.
* -s or --showbbox Flag: Optional: If given, the bounding box within the original image will be shown. False as default.