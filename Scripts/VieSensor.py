# Author: Lisa Slaughter <lisa.m.slaughter@gmail.com>
# Last update: Jan 28 2019

# This code determines the standard deviation and mean of a sensor data set. These values are passed
# to VIE.py in order to create the logit-normal cumulative distribution function for that sensor. Input
# data must only be for periods where vacancy is nearly 100% certain.
# Currently, a sigmoid is assumed. Later, perhaps an entire function can be generated and provided to VIE.py, 
# where it would be stored in a dictionary of sensors and their functions.
 

# ----------------------------------------------------------------------------------------------------------
import numpy as np
import math as math
import datetime as dt
import PI_client_LMS as pc

class VieSensor:
    def __init__(self, sensorName, sensorType, frequency, measurementUnits, dataAccessType, vacancyRelationship, dataRetrievalFileName, preprocessingFileName, relationshipBuilderFileName, vrParameter1, vrParameter2, vrParameter3, vrParameter4, historicalData=[], vacantData=[], occupiedData=[]):       
        self.sensorname = sensorName # Must be unique
        self.sensortype = sensorType
        self.frequency = frequency # frequency of new values being added (data sample rate) in minutes.
        self.units = measurementUnits # units of sensor measurement
        self.dataaccesstype = dataAccessType # tag for data stream in OSIsoft PI data historian. TODO Change to path for data retrieval file (read from config file)
        self.vacancyrelationship = vacancyRelationship # encoded types, represented by an enumeration (0=sigmoid, 1=...)
        self.histdata = historicalData
        self.vachistdata = vacantData
        self.occhistdata = occupiedData
        # TODO implement the following properties
        #self.vacancystart = vacancyStart # implement this upstream
        #self.vacancyend = vacancyEnd # implement this upstream
        self.datafilename = dataRetrievalFileName # Namespace of .py file (without ".py") that retrieves data and preprocesses it for use. File must be present in root folder. Two tasks may be disaggregated into two separate files later.
        self.prepfilename = preprocessingFileName # Namespace of .py file (without ".py") that retrieves data and preprocesses it for use. File must be present in root folder. Two tasks may be disaggregated into two separate files later.
        self.bldrfilename = relationshipBuilderFileName # Namespace of .py file (without ".py") that retrieves data and preprocesses it for use. File must be present in root folder. Two tasks may be disaggregated into two separate files later.
        self.vrparam1 = vrParameter1 # mean for sigmoid, threshold for step
        self.vrparam2 = vrParameter2 # std dev for sigmoid
        self.vrparam3 = vrParameter3 # unused
        self.vrparam4 = vrParameter4 # unused
        self.snapshotvalue = -1 # value of most recent data update from this sensor: dummy value
        self.snapshottimestamp = dt.datetime.now() # timestamp (datetime) of most recent data update from this sensor: dummy value
        self.snapshotvacancyprobability = -1 # probability of vacancy corresponding to this sensor's snapshot value
        if ( (self.vacancyrelationship == 0) & ( math.isnan(self.vrparam1) | math.isnan(self.vrparam2) ) ):
            self.BuildVacancyRelationship()
        elif ( (self.vacancyrelationship == 1) & ( math.isnan(self.vrparam1) | math.isnan(self.vrparam2) | math.isnan(self.vrparam3) ) ):
            self.BuildVacancyRelationship()
        else:
            pass

    def PreprocessData(self):
        prep = __import__(self.prepfilename)
        prep.PreprocessData(self)
        return self

    def GetHistoricalData(self):
        dta = __import__(self.datafilename)
        dta.GetHistoricalData(self)
        return self    

    def UpdateSnapshot(self):
        dta = __import__(self.datafilename)
        dta.UpdateSnapshot(self)
        return self

    def BuildVacancyRelationship(self):
        bldr = __import__(self.bldrfilename)
        bldr.BuildVacancyRelationship(self)
        return self

    def PredictVacancyProbability(self):
        # This function is called by main.py to predict probability of vacancy.
        # Applies the functional relationship between sensor data and vacancy to the sensor's snapshot value.

        # case 0: sigmoid
        self.snapshotvacancyprobability = 1 - 1/(1 + np.exp((self.vrparam1-self.snapshotvalue)/self.vrparam2))         
        if self.snapshotvacancyprobability < 0.01:
            self.snapshotvacancyprobability = 0
        else:
            pass
        # case 1: step
        # TODO build for step function (Just sigmoid with mean = threshold and low, hardcoded spread?)
        return

