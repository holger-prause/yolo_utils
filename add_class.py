import argparse
import os

parser = argparse.ArgumentParser()
requiredArguments = parser.add_argument_group("required arguments")
requiredArguments.add_argument("-d", "--dir", type=str, required=True, help="Directory containing the images and annotation")
requiredArguments.add_argument("-a", "--amount", type=str, required=True,
                    help="How many classes to add. This will shift all "
                         "indices starting at the start index with the given amount.")
requiredArguments.add_argument("-i", "--index", type=str, required=True, help="The class start index")
args = parser.parse_args()

imgDir = args.dir
startIdx = int(args.index)
amount = int(args.amount)

files = os.listdir(imgDir)
for file in files:
    baseName = os.path.splitext(file)[0]
    extension = os.path.splitext(file)[1]
    if extension == ".jpg":
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
                        if(oldIdx >= startIdx):
                            splitLine[0] = str(oldIdx + amount)
                        annNewFile.write(" ".join(splitLine)+"\n")
        os.remove(annOldPath)
        os.rename(annNewPath, annOldPath)
