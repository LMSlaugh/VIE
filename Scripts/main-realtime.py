# Author: Lisa Slaughter <lisa.m.slaughter@gmail.com>
# Last update: Jan 28 2019

# {Add description here}

# ----------------------------------------------------------------------------------------------------------

# import needed packages
import pandas as pd
import numpy as np
import datetime as dt
import VieSensor as snsr
import time as time
import datetime as dt
import math as math

def CreateVirtualSensors(metadatabasePath):
    # Purpose: read each sensor into a list from the sensor metadatabase
    metadata = pd.read_csv(metadatabasePath)
    sensors = {} # Create sensor dictionary. Enforces unique sensor names!!
    for index, row in metadata.iterrows():
        sn = row["Sensor-Name"]
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
        newSensor = snsr.VieSensor(sn, st, uf, dat, vrt, drfn, ppfn, rbfn, p1, p2, p3, p4)
        sensors[newSensor.sensorname] = newSensor
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

while True:
    probabilities = []
    timestamps = []
    for k, v in sensors.items():
        v.UpdateSnapshot()
        v = v.PreprocessData() # Currently does nothing

        if v.vacancyrelationship == 0 : # In case of sigmoid, check if needed parameters exist. If not, calculate them
            p1_nanflag = math.isnan(v.param1)
            p2_nanflag = math.isnan(v.param2)
            if p1_nanflag | p2_nanflag : # if any parameters are nan, calculate them
                v = v.BuildVacancyRelationship() # Does nothing for now. May need separate relationship builders for each function type. Need to test this program flow.
    
        v.PredictVacancyProbability()
        timestamps.append(v.snapshottimestamp) # Capture datetime in a list
        probabilities.append(v.vacancyprobability) # Capture datetime in a list

    # fuse predictions for all sensors
    overallprobabilityvalue = FuseVacancyProbabilities(probabilities)
    overallprobabilitytimestamp = FuseVacancyTimestamps(timestamps)

    # output final vacancy probability to csv
    # put info into dataframe, then append to csv
    # TODO build up output dataframe based on sensorname
    #for k, v in sensors:
        # build the data frame column by column

    wifi = sensors["wifi1"]
    co2 = sensors["co21"]
    elec = sensors["elec1"]
    output.iloc[0] = [dt.datetime.now(), overallprobabilitytimestamp, overallprobabilityvalue, wifi.snapshottimestamp, wifi.snapshotvalue, wifi.vacancyprobability, co2.snapshottimestamp, co2.snapshotvalue, co2.vacancyprobability, elec.snapshottimestamp, elec.snapshotvalue, elec.vacancyprobability]
    output.to_csv("DataFiles\\" + "VIE-output-realtime.csv", mode="a", header=False, index=False)
    #"c:\\Users\\lisam\\Desktop\\Repositories\\VIE\\
    sleepminutes = 5
    time.sleep(sleepminutes*60)


thisisastopgap = "stopgap"


###### some notes ###############
# s1_cdf = 0.5*(1 + math.erf((math.log(s1_val/(1-s1_val))-s1_mean)/math.sqrt(2 * s1_stdev ^ 2))) # cumulative distribution of normally distributed data, for reference
#sigmoid = 1/(1+exp((a-x)/b))

