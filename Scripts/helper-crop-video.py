from cv2 import cv2
import numpy as np
from os import listdir

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

# -----------INPUT DEFINITIONS---------------------
root = "GroundTruthVideos"
inputVideoDirectoryPath = root + "\\13 JUN 2019_ToCrop"
outputVideoDirectoryPath = root + "\\13 JUN 2019_Cropped"
# -------------------------------------------------

inputFileNames = listdir(inputVideoDirectoryPath)
for filename in inputFileNames:
    camera_angle = filename[3]     
    y0, y1, x0, x1 = GetCropBounds(camera_angle)
    vidPath_in = inputVideoDirectoryPath + "\\" + filename
    vidPath_out = outputVideoDirectoryPath + "\\" + filename[:-4] + "_cropped.avi"
    video_in = cv2.VideoCapture(vidPath_in)
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    video_out = cv2.VideoWriter(vidPath_out, fourcc, 12, (x1-x0,y1-y0))
    i = 1
    print("Now processing video: " + filename + " ...")

    while( video_in.isOpened() ):
        print("Cropping Frame :  " + str(i))
        i = i + 1
        success, frame = video_in.read()
        if (not success):
            break
        doorway = frame[y0:y1, x0:x1]
        #cv2.imshow("cropped video", doorway)
        #cv2.waitKey(5)
        video_out.write(doorway)

    video_in.release()
    video_out.release()
    cv2.destroyAllWindows()
    print("Completed processing video: " + filename)

stopgap = "thisisastopgap"