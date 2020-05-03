# Filename: ModelParameters.py
# Author: Lisa Slaughter <lisa.m.slaughter@gmail.com>
# Last update: November 19, 2019

# This class holds information about the model state. 
# Field descriptions:
#    | retrain: Boolean. A value of 1 forces redetermination of in-model parameters.
#    | trainstart: Datetime. Defines the beginning of the training period.
#    | trainend: Datetime. Defines the end of the training period.
#    | teststart: Datetime. Defines the beginning of the testing period.
#    | testend: Datetime. Defines the end of the testing period.
#    | traintype: String. Defines what portion of the training set is used.
#         | "full": Uses all available data in the training set.
#         | "cherry": Uses only data that falls between 
#    | buildtype: String. Defines which modelling approach.
#         | "logistic": Uses logistic regression to model vacancy.
#         | "percentile": Uses the proposed percentile method to model vacancy.
#    | fusetype: String. Defines the method used to fuse the probabilities of vacancy from each sensor. 
#         | "MAX": Maximum
#         | "MULT": Product
#         | "SM": Simple mean
#         | "SDWM": Standard deviation weighted mean
#         | "HM": Harmonic mean
#         | "RSS": Root sum square
#         | "RMS": Root mean square
#         | "SDWRMA": Standard deviation weighted root mean square
# ----------------------------------------------------------------------------------------------------------

class ModelParameters:
    def __init__(self, buildFlag, trainStart, trainEnd, testStart, testEnd, trainType, buildType, fuseType):
        self.buildflag = buildFlag
        self.trainstart = trainStart
        self.trainend = trainEnd
        self.teststart = testStart
        self.testend = testEnd
        self.traintype = trainType
        self.buildtype = buildType
        self.fusetype = fuseType