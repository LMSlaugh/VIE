# Author: Lisa Slaughter <lisa.m.slaughter@gmail.com>
# Last update: Jan 28 2019

# {Add description here}

# ----------------------------------------------------------------------------------------------------------

# import needed packages
import pandas as pd
import numpy as np
import datetime as dt
import VieSensor as snsr
import csv
import time as time
import datetime as dt
import math as math

def CreateVirtualSensors(metadatabasePath):
    # Purpose: read each sensor into a list from the sensor metadatabase
    metadata = pd.read_csv("VIE-sensor-metadatabase.csv")
    sensors = []
    for index, row in metadata.iterrows():
        st = row["Sensor-Type"]
        uf = row["Update-Frequency"]
        dat = row["Data-Access-Type"]
        vrt = row["Vacancy-Relationship-Type"]
        drfn = row["Data-Retrieval-File-Name"]
        ppfn = row["Preprocessing-File-Name"]
        rbfn = row["Relationship-Builder-File-Name"]
        p1 = row["Parameter-1"]
        p2 = row["Parameter-2"]
        p3 = row["Parameter-3"]
        p4 = row["Parameter-4"]
        newSensor = snsr.VieSensor(st, uf, dat, vrt, drfn, ppfn, rbfn, p1, p2, p3, p4)
        sensors.append(newSensor)
    return sensors

def FuseVacancyProbabilities(probabilities):
    overallproba = max(probabilities)
    return overallproba

def FuseVacancyTimestamps(timestamps):
    overalldt = max(timestamps)
    return overalldt


# Create the following variables once...
output = pd.DataFrame(index=[0],columns=["runtimedt","overallprobadt","overallprobaval","wifidt","wifival","wifiproba","co2dt","co2val","co2proba","elecdt","elecval","elecproba"])
sensors = CreateVirtualSensors("VIE-sensor-metadatabase.csv") # Read sensors from file, instantiate. If missing data, fill with dummy data ("") and move on to next sensor

# Reinitialize the following variables every cycle
probabilities = []
timestamps = []

while True:
    for sensor in sensors:
        sensor.UpdateSnapshot()
        sensor = sensor.PreprocessData() # Currently does nothing

        if sensor.vacancyrelationship == 0 : # In case of sigmoid, check if needed parameters exist. If not, calculate them
            p1_nanflag = math.isnan(sensor.param1)
            p2_nanflag = math.isnan(sensor.param2)
            if p1_nanflag | p2_nanflag : # if any parameters are nan, calculate them
                sensor = sensor.BuildVacancyRelationship() # Does nothing for now. May need separate relationship builders for each function type. Need to test this program flow.
    
        sensor.PredictVacancyProbability()
        timestamps.append(sensor.snapshottimestamp) # Capture datetime in a list
        probabilities.append(sensor.vacancyprobability) # Capture datetime in a list

    # fuse predictions for all sensors
    overallprobabilityvalue = FuseVacancyProbabilities(probabilities)
    overallprobabilitytimestamp = FuseVacancyTimestamps(timestamps)

    # output final vacancy probability to csv
    # put info into dataframe, then append to csv
    wifi = sensors[0]
    co2 = sensors[1]
    elec = sensors[2]
    output.iloc[0] = [dt.datetime.now(), overallprobabilitytimestamp, overallprobabilityvalue, wifi.snapshottimestamp, wifi.snapshotvalue, wifi.vacancyprobability, co2.snapshottimestamp, co2.snapshotvalue, co2.vacancyprobability, elec.snapshottimestamp, elec.snapshotvalue, elec.vacancyprobability]
    output.to_csv("VacancyPredictionTestFile.csv", mode="a", header=False, index=False)
    sleepminutes = 5
    time.sleep(sleepminutes*60)


thisisastopgap = "stopgap"


###### some notes ###############
# s1_cdf = 0.5*(1 + math.erf((math.log(s1_val/(1-s1_val))-s1_mean)/math.sqrt(2 * s1_stdev ^ 2))) # cumulative distribution of normally distributed data, for reference
#sigmoid = 1/(1+exp((a-x)/b))

