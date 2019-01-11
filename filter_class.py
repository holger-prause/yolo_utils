import argparse
import os

parser = argparse.ArgumentParser()
requiredArguments = parser.add_argument_group("required arguments")
requiredArguments.add_argument("-d", "--dir", type=str, required=True, help="Directory containing the images and annotation")
requiredArguments.add_argument("-i", "--index", type=str, required=True, help="The filter class index - all other classes will be removed.")
args = parser.parse_args()

imgDir = args.dir
filterIdx = int(args.index)
files = os.listdir(imgDir)



for file in files:
    baseName = os.path.splitext(file)[0]
    extension = os.path.splitext(file)[1].lower()

    fileExts = [".jpg", ".jpeg", ".png"]
    if(extension.lower() in fileExts):
        annOldPath = os.path.join(imgDir, baseName+".txt")
        if(not os.path.exists(annOldPath)):
            print("no annotation file for", file)
            continue


        annNewPath = os.path.join(imgDir, baseName+"_new.txt")
        with open(annOldPath) as annFile:
            with open(annNewPath, "w") as annNewFile:
                for oldLine in annFile:
                    if(oldLine.strip()):
                        splitLine = oldLine.split()
                        oldIdx = int(splitLine[0])
                        if(oldIdx == filterIdx):
                            splitLine[0] = str(0)
                            annNewFile.write(" ".join(splitLine)+"\n")
        os.remove(annOldPath)
        os.rename(annNewPath, annOldPath)