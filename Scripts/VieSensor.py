# Author: Lisa Slaughter <lisa.m.slaughter@gmail.com>
# Last update: May 02, 2020

# This class represents an individual sensor. Metadata fields are pre-defined in a .csv file, where 
# each row defines an individual sensor. See "VIE-sensor-metdatabase.csv" for an example. 
# Field definitions:
#    | "sensorname": String. Name of sensor; Must be unique.
#    | "sensortype": String. Defines what the sensor is measuring. Options:
#         | "carbon dioxide": Air concentration of carbon dioxide.
#         | "wifi": Count of active Wi-Fi connections.
#         | "elec": Electricity demand.
#    | "frequency": String. Data sample rate in minutes (optional).
#    | "units": String. Units attached to sensor measurement.
#    | "dataaccesstype": String. Location information for data retrieval (optional).
#    | "vacancyrelationship": String. Defines the modeling approach. Options:
#         | "logistic": Uses logistic regression to model vacancy.
#         | "percentile": Uses the proposed percentile method to model vacancy.
#    | "trainingdataset": Determines what parts of the training set is used. Options:
#         | "full": Use the full training data set.
#         | "cherry": Use only times of near-sure vacancy from the training set (between midnight and 4am).
#    | "histdata": Dictionary<Datetime, String>. Placeholder for the full data set (test + train).
#    | "vachistdata": Dictionary<Datetime, String>. Placeholder for data (train + test) during times of expected vacancy.
#    | "occhistdata": Dictionary<Datetime, String>. Placeholder for data (train + test) during times of expected ocupancy.
#    | "datafilename": String. Name of data extraction file for this sensor (.py file; omit extension).
#    | "prepfilename": String. Name of preprocessing file for this sensor (.py file; omit extension).
#    | "bldrfilename": String. Name of percentile method training file for this sensor (.py file; omit extension).
#    | "std": Float. Standard deviation of the training set.
#    | "vrparam1": Object. Placeholder for a model coefficient (optional).
#    | "vrparam2": Object. Placeholder for a model coefficient (optional).
#    | "vrparam3": Object. Placeholder for a model coefficient (optional).
#    | "vrparam4": Object. Placeholder for a model coefficient (optional).
#    | "snapshotvalue": Float. Value corresponding to the current data point being processed.
#    | "snapshottimestamp": Datetime. Timestamp corresponding to the current data point being processed.
#    | "snapshotvacancyprobability": Float. Probability of vacancy corresponding to the current data point being processed.
#    | "trainstart": Datetime. Defines the beginning of the training period.
#    | "trainend": Datetime. Defines the end of the training period.

# ----------------------------------------------------------------------------------------------------------
import numpy as np
import math
import datetime as dt
from scipy.special import expit

class VieSensor:
    def __init__(self, sensorName, sensorType, frequency, measurementUnits, dataAccessType, vacancyRelationship, trainingDataSet, dataRetrievalFileName, preprocessingFileName, relationshipBuilderFileName, stdDev, vrParameter1, vrParameter2, vrParameter3, vrParameter4, trainStart, trainEnd, historicalData=[], vacantData=[], occupiedData=[]):       
    # Initializes an instance of this class. Performs percentile-type training if needed. 
        self.sensorname = sensorName
        self.sensortype = sensorType
        self.frequency = frequency 
        self.units = measurementUnits
        self.dataaccesstype = dataAccessType
        self.vacancyrelationship = vacancyRelationship
        self.trainingdataset = trainingDataSet
        self.histdata = historicalData
        self.vachistdata = vacantData
        self.occhistdata = occupiedData
        # TODO implement the following properties upstream
        #self.vacancystart = vacancyStart
        #self.vacancyend = vacancyEnd
        self.datafilename = dataRetrievalFileName
        self.prepfilename = preprocessingFileName
        self.bldrfilename = relationshipBuilderFileName
        self.std = stdDev
        self.vrparam1 = vrParameter1
        self.vrparam2 = vrParameter2
        self.vrparam3 = vrParameter3
        self.vrparam4 = vrParameter4
        self.snapshotvalue = -1
        self.snapshottimestamp = dt.datetime.now()
        self.snapshotvacancyprobability = -1
        self.trainstart = trainStart
        self.trainend = trainEnd
        if ( math.isnan(self.vrparam1) | math.isnan(self.vrparam2) | math.isnan(self.std)):
            self.BuildVacancyRelationship()
        else:
            pass

    def PreprocessData(self):
        prep = __import__(self.prepfilename)
        prep.PreprocessData(self)
        return self

    def GetHistoricalData(self):
        dta = __import__(self.datafilename)
        dta.GetHistoricalData(self, self.trainstart, self.trainend)
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
        # Predicts the probability of vacancy by applying the functional relationship between sensor data and vacancy to the snapshot value.

        if self.vacancyrelationship=="Percentile":
            self.snapshotvacancyprobability = 1 - 1/(1 + np.exp((self.vrparam1-self.snapshotvalue)/self.vrparam2))         
        elif self.vacancyrelationship=="Logistic":
            self.snapshotvacancyprobability = expit(self.snapshotvalue * self.vrparam1 + self.vrparam2)

        if self.snapshotvacancyprobability < 0.001:
            self.snapshotvacancyprobability = 0
        return

