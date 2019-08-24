import numpy as np
from cv2 import cv2
from imageai.Detection import VideoObjectDetection
from os import listdir, remove
from shutil import copyfile

# -----------Function Definitions------------------
def GetCropBounds(camera_angle):
    # y0,x0         y1,x0
    #
    #
    # y0,x1         y1,x1
    if camera_angle == "1":
        return 166, 1000, 763, 1183
    elif camera_angle == "4":
        return 100, 550, 890, 1315
    elif camera_angle == "5":
        return 89, 800, 674, 1050
    elif camera_angle == "6":
        return 349, 980, 774, 1133
    elif camera_angle == "8":
        return 111, 900, 718, 1437
    else:
        return 0, 0, 0, 0 # y0, y1, x0, x1

def perVideo(output_arrays, count_arrays, average_output_count):
    global humanFlag
    humanFlag = False
    if "person" in average_output_count:
        humanFlag = True
        return
    else:
        return

def CropVideo(inputPath, outputPath):
    video = cv2.VideoCapture(inputPath)
    camera_angle = filename[3]     
    y0, y1, x0, x1 = GetCropBounds(camera_angle)
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    outputPath_modded = outputPath + "_cropped.avi"
    video_temp = cv2.VideoWriter(outputPath_modded, fourcc, 12, (x1-x0,y1-y0))
    i = 1
    while( video.isOpened() ):
        print("Cropping Frame :  " + str(i))
        i = i + 1
        success, frame = video.read()
        if (not success):
            break
        doorway = frame[y0:y1, x0:x1]
        video_temp.write(doorway) # can we do video = []; video.append(doorway) ??
    video.release()
    video_temp.release()
    return outputPath_modded
# -------------------------------------------------

# -----------INPUT DEFINITIONS---------------------
# Expected folder structure is 
# ..GroundTruthVideos >
#   XX JUN 2019 >
#       Processed
#       Temp
#       ToProcess >
#           "ch0#_yyyymmddhhMMss.mp4" (where # is 1,4,5,6, or 8)
#   XX JUN 2019 >
#       Processed
#       Temp
#       ToProcess >
#           "ch0#_yyyymmddhhMMss.mp4" (where # is 1,4,5,6, or 8)
# ...etc
root = "GroundTruthVideos_debug"
inDir = "ToProcess"
tempDir = "Temp" # This directory must already exist
outDir = "Processed" # This directory must already exist
# -------------------------------------------------

# -------------MAIN PROGRAM------------------------
detector = VideoObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath("DataFiles\\yolo.h5")
detector.loadModel(detection_speed="flash")

dateDirs = listdir(root)
for dateDir in dateDirs:
    dateDirPath = root + "\\" + dateDir
    inputFileNames = listdir(dateDirPath + "\\" + inDir)

    for filename in inputFileNames:
        vidPath_in = dateDirPath + "\\" + inDir + "\\" + filename
        vidPath_temp = dateDirPath + "\\" + tempDir + "\\" + filename[:-4]
        vidPath_out = dateDirPath + "\\" + outDir + "\\" + filename
        print("Now processing video: " + filename + " ...")
        # Crop the video to just the doorway in order to avoid detection of extraneous persons
        croppedPath = CropVideo(vidPath_in, vidPath_temp)
        # Load the cropped video and detect whether or not there is a person in it
        detectedPath = detector.detectObjectsFromVideo(input_file_path=croppedPath, output_file_path=vidPath_temp + "_detected", frames_per_second=12, minimum_percentage_probability=0.1, log_progress=True, video_complete_function=perVideo)
        if humanFlag:
            # Copy the original .mp4 into //Processed directory
            try:
                copyfile(vidPath_in, vidPath_out)
            except Exception as ex:
                print(ex)

        try:
            remove(croppedPath)
            remove(detectedPath)
        except Exception as ex:
            print(ex)

        print("Completed processing video: " + filename)

stopgap = "thisisastopgap"
# -------------------------------------------------