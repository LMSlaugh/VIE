# Author: Lisa Slaughter <lisa.m.slaughter@gmail.com>
# Last update: Jan 28 2019

# This code determines the standard deviation and mean of a sensor data set. These values are passed
# to VIE.py in order to create the logit-normal cumulative distribution function for that sensor. Input
# data must only be for periods where vacancy is nearly 100% certain.
# Currently, a sigmoid is assumed. Later, perhaps an entire function can be generated and provided to VIE.py, 
# where it would be stored in a dictionary of sensors and their functions.
 

# ----------------------------------------------------------------------------------------------------------
import math as math
import datetime as dt
import PI_client_LMS as pc

class VieSensor:
    def __init__(self, sensorType, frequency, dataAccessType, vacancyRelationship, dataRetrievalFileName, preprocessingFileName, relationshipBuilderFileName, parameter1, parameter2, parameter3, parameter4):       
        self.sensortype = sensorType
        self.frequency = frequency # frequency of new values being added (data sample rate) in minutes.
        self.dataaccesstype = dataAccessType # tag for data stream in OSIsoft PI data historian. TODO Change to path for data retrieval file (read from config file)
        self.vacancyrelationship = vacancyRelationship # encoded types, represented by an enumeration (0=sigmoid, 1=...)
        self.datafilename = dataRetrievalFileName # Namespace of .py file (without ".py") that retrieves data and preprocesses it for use. File must be present in root folder. Two tasks may be disaggregated into two separate files later.
        self.prepfilename = preprocessingFileName # Namespace of .py file (without ".py") that retrieves data and preprocesses it for use. File must be present in root folder. Two tasks may be disaggregated into two separate files later.
        self.bldrfilename = relationshipBuilderFileName # Namespace of .py file (without ".py") that retrieves data and preprocesses it for use. File must be present in root folder. Two tasks may be disaggregated into two separate files later.
        self.param1 = parameter1 # mean for sigmoid, threshold for step
        self.param2 = parameter2 # spread for sigmoid
        self.param3 = parameter3 # unused
        self.param4 = parameter4 # unused
        self.snapshotvalue = -1 # value of most recent data update from this sensor: dummy value
        self.snapshottimestamp = dt.datetime.now() # timestamp (datetime) of most recent data update from this sensor: dummy value
        self.vacancyprobability = -1 # probability of vacancy corresponding to this sensor's snapshot value

    def PreprocessData(self):
        prep = __import__(self.prepfilename)
        prep.PreprocessData(self)
        return self
    
    def UpdateSnapshot(self):
        # Brings in the most recent data point from passed sensor. Sourced from the OSIsoft PI data historian owned by UC Davis Facilities Management
        client = pc.pi_client()
        # ...builidng dummy data for required variables
        current = dt.datetime.now()
        window = dt.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=1, weeks=0)
        start = current - window
        s1 = client.get_stream_by_point(self.dataaccesstype, calculation="end", start=start, end=current)
        # ...TODO some handling for no data returned from historian
        c = s1.columns
        self.snapshottimestamp = s1.loc["Timestamp",c[0]]
        self.snapshotvalue = s1.loc["Value",c[0]]
        return

    def BuildVacancyRelationship(self):
        bldr = __import__(self.bldrfilename)
        bldr.BuildVacancyRelationship(self)
        return self

    def PredictVacancyProbability(self):
        # This function is called by main.py to predict probability of vacancy.
        # Applies the functional relationship between sensor data and vacancy to the sensor's snapshot value.

        # case 0: sigmoid
        self.vacancyprobability = 1 - 1/(1 + math.exp((self.param1-self.snapshotvalue)/self.param2))         
        if self.vacancyprobability < 0.01:
            self.vacancyprobability = 0
        else:
            pass
        # case 1: step
        # TODO build for step function (Just sigmoid with mean = threshold and low, hardcoded spread?)
        return

