# Author: Lisa Slaughter <lisa.m.slaughter@gmail.com>
# Last update: May 02, 2019

# This code controls how the Vacancy Inference Engine (VIE) is run. Use a line of code at the bottom of this
# file to make a call to Main(). Parameters are defined as follows:
#   build_type: String. Defines the modeling approach. Options:
#       Logistic: Uses Logistic regression to model vacancy.
#       Percentile: Uses the proposed Percentile method to model vacancy.
#   train_type: Determines what parts of the training set is used. Options:
#       Full: Use the Full training data set.
#       Cherry: Use only times of near-sure vacancy from the training set (between midnight and 4am).
#   fuse_type: String. Defines the method used to fuse the probabilities of vacancy from each sensor. 
#         MAX: Maximum
#         MULT: Product
#         SM: Simple mean
#         SDWM: Standard deviation weighted mean
#         HM: Harmonic mean
#         RSS: Root sum square
#         RMS: Root mean square
#         SDWRMS: Standard deviation weighted root mean square
#   train_start: Datetime. Defines the beginning of the training period.
#   train_end: Datetime. Defines the end of the training period.
#   test_start: Datetime. Defines the beginning of the testing period.
#   test_end: Datetime. Defines the end of the testing period.
# 
# ----------------------------------------------------------------------------------------------------------
import model_controller as mc
import VieSensor as snsr
import ModelParameters as mp
import helper_figureGenerator as figen
import preanalysis
import postanalysis

def Main(build_type, train_type, fuse_type, train_start, train_end, test_start, test_end):
    params = mp.ModelParameters(train_start, train_end, test_start, test_end, train_type, build_type, fuse_type)
    sensors = mc.CreateVirtualSensors(params)
    traindata, testdata = mc.GetTrainTestData(params)
    #for k,v in sensors.items():
       #preanalysis.RunExploration(v.sensorname, traindata, params.buildtype, params.traintype)
    #mc.GenerateOutput(testdata, sensors, params)
    postanalysis.GenerateAnalytics(params)
    #mc.GeneratePlots(params)
    return

# --------- MAIN PROGRAM ----------

# The following lines of code can be un/commented to in/exclude different model runs

#Main("Logistic", "Full", "SM", "2019-07-02 00:00:00", "2019-07-16 00:00:00", "2019-07-16 00:00:00", "2019-08-06 00:00:00")
#Main("Logistic", "Cherry", "SM", "2019-07-02 00:00:00", "2019-07-16 00:00:00", "2019-07-16 00:00:00", "2019-08-06 00:00:00")
#Main("Percentile", "Full", "SM", "2019-07-02 00:00:00", "2019-07-16 00:00:00", "2019-07-16 00:00:00", "2019-08-06 00:00:00")
#Main("Percentile", "Cherry", "SM", "2019-07-02 00:00:00", "2019-07-16 00:00:00", "2019-07-16 00:00:00", "2019-08-06 00:00:00")

Main("Logistic", "Full", "RMS", "2019-07-02 00:00:00", "2019-07-16 00:00:00", "2019-07-16 00:00:00", "2019-08-06 00:00:00")
#Main("Logistic", "Cherry", "RMS", "2019-07-02 00:00:00", "2019-07-16 00:00:00", "2019-07-16 00:00:00", "2019-08-06 00:00:00")
#Main("Percentile", "Full", "RMS", "2019-07-02 00:00:00", "2019-07-16 00:00:00", "2019-07-16 00:00:00", "2019-08-06 00:00:00")
Main("Percentile", "Cherry", "RMS", "2019-07-02 00:00:00", "2019-07-16 00:00:00", "2019-07-16 00:00:00", "2019-08-06 00:00:00")

#Main("Logistic", "Full", "SDWM", "2019-07-02 00:00:00", "2019-07-16 00:00:00", "2019-07-16 00:00:00", "2019-08-06 00:00:00")
#Main("Logistic", "Cherry", "SDWM", "2019-07-02 00:00:00", "2019-07-16 00:00:00", "2019-07-16 00:00:00", "2019-08-06 00:00:00")
#Main("Percentile", "Full", "SDWM", "2019-07-02 00:00:00", "2019-07-16 00:00:00", "2019-07-16 00:00:00", "2019-08-06 00:00:00")
#Main("Percentile", "Cherry", "SDWM", "2019-07-02 00:00:00", "2019-07-16 00:00:00", "2019-07-16 00:00:00", "2019-08-06 00:00:00")

#Main("Logistic", "Full", "SDWRMS", "2019-07-02 00:00:00", "2019-07-16 00:00:00", "2019-07-16 00:00:00", "2019-08-06 00:00:00")
#Main("Logistic", "Cherry", "SDWRMS", "2019-07-02 00:00:00", "2019-07-16 00:00:00", "2019-07-16 00:00:00", "2019-08-06 00:00:00")
#Main("Percentile", "Full", "SDWRMS", "2019-07-02 00:00:00", "2019-07-16 00:00:00", "2019-07-16 00:00:00", "2019-08-06 00:00:00")
#Main("Percentile", "Cherry", "SDWRMS", "2019-07-02 00:00:00", "2019-07-16 00:00:00", "2019-07-16 00:00:00", "2019-08-06 00:00:00")

#Main("Logistic", "Full", "HM", "2019-07-02 00:00:00", "2019-07-16 00:00:00", "2019-07-16 00:00:00", "2019-08-06 00:00:00")
#Main("Logistic", "Cherry", "HM", "2019-07-02 00:00:00", "2019-07-16 00:00:00", "2019-07-16 00:00:00", "2019-08-06 00:00:00")
#Main("Percentile", "Full", "HM", "2019-07-02 00:00:00", "2019-07-16 00:00:00", "2019-07-16 00:00:00", "2019-08-06 00:00:00")
#Main("Percentile", "Cherry", "HM", "2019-07-02 00:00:00", "2019-07-16 00:00:00", "2019-07-16 00:00:00", "2019-08-06 00:00:00")