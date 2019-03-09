import csv
import os
import urllib
import urllib.request
import argparse
from PIL import Image

parser = argparse.ArgumentParser()
requiredArguments = parser.add_argument_group("required arguments")
requiredArguments.add_argument("-u", "--urlfile", type=str, required=True, help="csv file containing the original urls"
                                                                                       "i.e. test-images-with-rotation.csv")
requiredArguments.add_argument("-o", "--outdir", type=str, required=True, help="Directory that will contain the downloaded images")
parser.add_argument("-i", "--imageidfile", type=str, required=False,
                    help="File containing image ids in each line to download")
args = parser.parse_args()


imIds = []
with open(args.imageidfile) as imIdFile:
    imIds = imIdFile.read().splitlines()

if (not os.path.exists(args.outdir)):
    os.makedirs(args.outdir)


with open(args.urlfile, encoding="utf8", newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    for row in csvreader:
        url = row[2]
        imgId = row[0]
        if imgId in imIds:
            fileName = imgId+".jpg"
            dlPath = os.path.join(args.outdir, fileName)
            urllib.request.urlretrieve(url, dlPath)
            print("downloading from url: {0}".format(url))
            try:
                with Image.open(dlPath) as im:
                    im.close
            except IOError:
                print("corrupt download image for url {0}".format(url))
                os.remove(dlPath)