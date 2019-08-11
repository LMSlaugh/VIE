# This script determines if there is a person contained in each video. If so, it moves that video file to a new directory.
# See below section "INPUT DEFINITIONS" to manipulate directories for input and output videos

# -----------Package Definitions-------------------
from imageai.Detection import VideoObjectDetection
from os import remove, listdir

# -----------Function Definitions------------------
def perVideo(output_arrays, count_arrays, average_output_count):
    global humanFlag
    humanFlag = False
    if "person" in average_output_count:
        humanFlag = True
        return
    return

# -----------INPUT DEFINITIONS---------------------
root = "GroundTruthVideos"
inputVideoDirectoryPath = root + "\\ToProcess"
outputVideoDirectoryPath = root + "\\HumanDetected"
# -------------------------------------------------

global humanFlag
humanFlag = False
inputFileNames = listdir(inputVideoDirectoryPath)
detector = VideoObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath("DataFiles\\yolo.h5")
detector.loadModel(detection_speed="fastest")
for filename in inputFileNames:
    vidPath_in = inputVideoDirectoryPath + "\\" + filename
    vidPath_out = outputVideoDirectoryPath + "\\" + filename[:-4] + "_filtered"
    print("Now processing video: " + filename + " ...")
    detector.detectObjectsFromVideo(input_file_path=vidPath_in, output_file_path=vidPath_out, frames_per_second=12, minimum_percentage_probability=0.1, log_progress=True, video_complete_function=perVideo)
    if not humanFlag:
        try:
            remove(vidPath_out + ".avi")
        except OSError:
            print(OSError.strerror)
    print("Completed processing video: " + filename)


stopgap = "thisisastopgap"