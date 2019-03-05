# Author: Lisa Slaughter <lisa.m.slaughter@gmail.com>
# Last update: Jan 28 2019

# {Add description here}

# ----------------------------------------------------------------------------------------------------------

# import needed packages
import pandas as pd
import numpy as np
import VieSensor as snsr
import time as time
import datetime as dt
import math as math
import helper_figure_generator as figen

def CreateVirtualSensors(metadatabasePath):
    # Purpose: read each sensor into a list from the sensor metadatabase
    metadata = pd.read_csv(metadatabasePath)
    sensors = {} # Create sensor dictionary. Enforces unique sensor names!!
    for index, row in metadata.iterrows():
        sn = row["Sensor-Name"]
        st = row["Sensor-Type"]
        uf = row["Update-Frequency"]
        mu = row["Measurement-Units"]
        dat = row["Data-Access-Type"]
        vrt = row["Vacancy-Relationship-Type"]
        drfn = row["Data-Retrieval-File-Name"]
        ppfn = row["Preprocessing-File-Name"]
        rbfn = row["Relationship-Builder-File-Name"]
        p1 = row["Parameter-1"]
        p2 = row["Parameter-2"]
        p3 = row["Parameter-3"]
        p4 = row["Parameter-4"]
        newSensor = snsr.VieSensor(sn, st, uf, mu, dat, vrt, drfn, ppfn, rbfn, p1, p2, p3, p4)
        sensors[newSensor.sensorname] = newSensor
    
    metadata_new = metadata
    for index, row in metadata.iterrows():
        metadata_new.loc[index,"Parameter-1"] = sensors[row["Sensor-Name"]].vrparam1
        metadata_new.loc[index,"Parameter-2"] = sensors[row["Sensor-Name"]].vrparam2
        metadata_new.loc[index,"Parameter-3"] = sensors[row["Sensor-Name"]].vrparam3
        metadata_new.loc[index,"Parameter-4"] = sensors[row["Sensor-Name"]].vrparam4
    
    metadata_new.to_csv("VIE-sensor-metadatabase-new.csv", header=True, index=False)

    return sensors

def FuseVacancyProbabilities(probabilities):
    overallproba = max(probabilities)
    return overallproba

def FuseVacancyTimestamps(timestamps):
    overalldt = max(timestamps)
    return overalldt


# Create the following variables once...
output = pd.DataFrame(index=[0],columns=["runtimedt","overallprobadt","overallprobaval","wifidt","wifival","wifiproba","co2dt","co2val","co2proba","elecdt","elecval","elecproba"])
output.to_csv("DataFiles\\VIE-output-historical.csv", header=True, index=False) # Apply headers to csv and remove existing entries

sensors = CreateVirtualSensors("VIE-sensor-metadatabase.csv") # Read sensors from file, instantiate dictionary. If missing data, fill with dummy data ("") and move on to next sensor

# Import csv historical data to dataframe
histdata = pd.read_csv("DataFiles\\VIE-input-historical.csv") # In order: timestamp for sensor 1 (wifi), timestamp for sensor 2 (co2), timestamp for sensor 3 (elec), etc.
for index, row in histdata.iterrows():
    probabilities = []
    timestamps = []
    for k, v in sensors.items():
        tempstr = v.sensorname + "-dt"
        v.snapshottimestamp = row[tempstr]
        v.snapshotvalue = row[v.sensorname + "-val"]
        v.PreprocessData() # currently does nothing (will perform any preprocessing methods on snapshot. methods must also work for historical data.)
        v.PredictVacancyProbability()
        timestamps.append(v.snapshottimestamp) # Capture datetime in a list
        probabilities.append(v.vacancyprobability) # Capture datetime in a list

    # fuse predictions for all sensors
    overallprobabilityvalue = FuseVacancyProbabilities(probabilities)
    overallprobabilitytimestamp = FuseVacancyTimestamps(timestamps)

    # TODO build up output dataframe based on sensorname. Hardcoded by sensorname for now, see below...
    #for k, v in sensors:
    #    #build the data frame column by column

    wifi = sensors["wifi1"]
    co2 = sensors["co21"]
    elec = sensors["elec1"]
    output.iloc[0] = [dt.datetime.now(), overallprobabilitytimestamp, overallprobabilityvalue, wifi.snapshottimestamp, wifi.snapshotvalue, wifi.vacancyprobability, co2.snapshottimestamp, co2.snapshotvalue, co2.vacancyprobability, elec.snapshottimestamp, elec.snapshotvalue, elec.vacancyprobability]
    output.to_csv("DataFiles\\VIE-output-historical.csv", mode="a", header=False, index=False)

figen.PlotMain()
thisisastopgap = "stopgap"