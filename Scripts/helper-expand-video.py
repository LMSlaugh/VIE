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

def CropVideo(input_video_path):
    cropped_video_location = "initialize"
    return cropped_video_location

def DetectPersons(input_video_path):
    video_person_detected = "initialize"
    return video_person_detected

# -----------INPUT DEFINITIONS---------------------
root = "GroundTruthVideos"
inputVideoDirectoryPath = root + "\\ToProcess"
tempVideoDirectoryPath = root + "\\Temp" # This directory must already exist
outputVideoDirectoryPath = root + "\\Processed" # This directory must already exist
# -------------------------------------------------
global humanFlag
humanFlag = False
inputFileNames = listdir(inputVideoDirectoryPath)
detector = VideoObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath("DataFiles\\yolo.h5")
detector.loadModel(detection_speed="flash")
for filename in inputFileNames:
    vidPath_in = inputVideoDirectoryPath + "\\" + filename
    vidPath_temp = outputVideoDirectoryPath + "\\" + filename[:-4]
    print("Now processing video: " + filename + " ...")
    video = cv2.VideoCapture(vidPath_in)
    # Crop the video to just the doorway in order to avoid detection of extraneous persons
    camera_angle = filename[3]     
    y0, y1, x0, x1 = GetCropBounds(camera_angle)
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    video_temp = cv2.VideoWriter(vidPath_temp + "_cropped.avi", fourcc, 12, (x1-x0,y1-y0))
    i = 1
    while( video.isOpened() ):
        print("Cropping Frame :  " + str(i))
        i = i + 1
        success, frame = video.read()
        if (not success):
            break
        doorway = frame[y0:y1, x0:x1]
        video_temp.write(doorway) # can we do video = []; video.append(doorway) ??
        
    # Load the cropped video and detect whether or not there is a person in it
    detector.detectObjectsFromVideo(input_file_path=vidPath_temp + "_cropped.avi", output_file_path=vidPath_temp + "_detected", frames_per_second=12, minimum_percentage_probability=0.1, log_progress=True, video_complete_function=perVideo)
    if humanFlag:
        # Copy the original .mp4 into //processed directory
        try:
            copyfile(vidPath_in, outputVideoDirectoryPath)
        except Exception as ex:
            print(ex)

    try:
        remove(vidPath_temp + "_cropped.avi")
        remove(vidPath_temp + "_detected.avi")
    except Exception:
        print(OSError.strerror)

    print("Completed processing video: " + filename)

stopgap = "thisisastopgap"