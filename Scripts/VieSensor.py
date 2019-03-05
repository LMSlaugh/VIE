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
from pytz import timezone as tz
import PI_client_LMS as pc

class VieSensor:
    def __init__(self, sensorName, sensorType, frequency, measurementUnits, dataAccessType, vacancyRelationship, dataRetrievalFileName, preprocessingFileName, relationshipBuilderFileName, vrParameter1, vrParameter2, vrParameter3, vrParameter4, historicalData=[]):       
        self.sensorname = sensorName # Must be unique
        self.sensortype = sensorType
        self.frequency = frequency # frequency of new values being added (data sample rate) in minutes.
        self.units = measurementUnits # units of sensor measurement
        self.dataaccesstype = dataAccessType # tag for data stream in OSIsoft PI data historian. TODO Change to path for data retrieval file (read from config file)
        self.vacancyrelationship = vacancyRelationship # encoded types, represented by an enumeration (0=sigmoid, 1=...)
        self.histdata = historicalData
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
        # Convert from UTC to local timezone (Los Angeles)
        timestamp = s1.loc["Timestamp",c[0]]
        timestamp = timestamp[0:19]
        timestamp = dt.datetime.strptime(timestamp,"%Y-%m-%dT%H:%M:%S")
        timestamp = timestamp.replace(tzinfo=tz('UTC'))
        timestamp = timestamp.astimezone(tz("US/Pacific"))


        self.snapshottimestamp = timestamp
        if self.sensortype == "carbondioxide":
            d = s1.loc["Value",c[0]]
            if ( isinstance(d,int) | isinstance(d,float) ):
                self.snapshotvalue = d
            else:
                self.snapshotvalue = d["Value"]
        else:
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
        self.snapshotvacancyprobability = 1 - 1/(1 + np.exp((self.vrparam1-self.snapshotvalue)/self.vrparam2))         
        if self.snapshotvacancyprobability < 0.01:
            self.snapshotvacancyprobability = 0
        else:
            pass
        # case 1: step
        # TODO build for step function (Just sigmoid with mean = threshold and low, hardcoded spread?)
        return

