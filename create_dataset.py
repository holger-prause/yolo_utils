import os
import sys, getopt
import argparse

defaultVocClasses = ["aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
              "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]


def main():


    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--vocdir", type=str, default=os.curdir, help="Directory containing the voc folders."
                                                         "Working dir is default.")
    parser.add_argument("-d", "--datasetdir", type=str, default=os.curdir, help="Directory containing the custom images with annotations."
                                                             "Working dir is default.")
    parser.add_argument("-p", "--positives", nargs='+', default=defaultVocClasses, help="List of space separated voc classes to us as positives. "
                                                           "Use option -l to list the default values(all).")
    parser.add_argument("-n", "--negatives", nargs='+', default=defaultVocClasses, help="List of space separated voc classes to use as negatives."
                                                             "Use option -l to list the default values(all).")
    parser.add_argument("-l", "--listvoc", action='store_true', help="Lists all available classes from the voc dataset.")
    args = parser.parse_args()

    if(args.listvoc):
        print(defaultVocClasses)
        sys.exit()


    #print("args:", args)
    #print(defaultVocClasses)
    '''
    argv = sys.argv[1:]

    vocDir = os.curdir
    dataSetDir = os.curdir
    vocClasses = ["aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
                  "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]
    negativeVocClasses = vocClasses[:]




    try:
        #opts, args = getopt.getopt(argv,"v:d:c:n:",["vocdir=", "datasetdir=", "voclasses=", "negativevoclasses="])
        opts, args = getopt.getopt(argv, "c:")
        print("opts", opts)
        for opt, arg in opts:
            if opt in ("-v", "--vocdir"):
                vocDir = arg
            elif opt in ("-d", "--datasetdir"):
                dataSetDir = arg
            elif opt in ("-c", "--voclasses"):
                vocClasses = arg
            elif opt in ("-n", "--negativevoclasses"):
                negativeVocClasses = arg


    except getopt.GetoptError:
        print("verify_dataset.py -d <datasetdir> -l <logfile> -s")
        sys.exit(2)

    print(vocClasses)
    '''


if __name__ == "__main__":
    main()
