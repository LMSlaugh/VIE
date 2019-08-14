from os import listdir, remove, rename
from shutil import copyfile

# -----------Function Definitions------------------
# -------------------------------------------------

# -----------INPUT DEFINITIONS---------------------
root = "GroundTruthVideos"
biggerDirectoryPath = root + "\\Done"
smallerDirectoryPath = root + "\\Processed"
outputDirectoryPath = root + "\\Differences" # This directory must already exist
# -------------------------------------------------

# -------------MAIN PROGRAM------------------------
#biggerFilenames = listdir(biggerDirectoryPath) # Done
#for filename in biggerFilenames:
#    try:
#        rename(biggerDirectoryPath + "\\" + filename, biggerDirectoryPath + "\\" + filename[:-21] + ".mp4")
#    except Exception as ex:
#        print(ex)
biggerFilenames = listdir(biggerDirectoryPath)
smallerFilenames = listdir(smallerDirectoryPath)

for filename in biggerFilenames:
    if filename in smallerFilenames:
        continue
    else:
        try:
            copyfile(biggerDirectoryPath + "\\" + filename, outputDirectoryPath + "\\" + filename)
        except Exception as ex:
            print(ex)

for filename in biggerFilenames:
    try:
        rename(biggerDirectoryPath + "\\" + filename, biggerDirectoryPath + "\\" + filename[:-4] + "_cropped_filtered.avi")
    except Exception as ex:
        print(ex)

stopgap = "thisisastopgap"
# -------------------------------------------------