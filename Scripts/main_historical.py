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

## Global variables

#linreg_flag = True
linreg_flag = False

#fusetype = "rss"       #root sum square
#fusetype = "rms"       #root mean square
#fusetype = "max"       #maximum
#fusetype = "linreg"    #linear regression

def MonteCarloFusion():
    overallproba = 0.00
    return overallproba

def CreateVirtualSensors(metadatabasePath):
    # Purpose: read each sensor into a list from the sensor metadatabase
    metadata = pd.read_csv(metadatabasePath)
    sensors = {} # Create sensor dictionary. Enforces unique sensor names!!
    for index, row in metadata.iterrows():
        sn = row["Sensor-Name"]
        st = row["Sensor-Type"]
        uf = row["Update-Frequency"]
        mu = row["Measurement-Units"]
        dat = row["Data-Access-Type"] # Remove this?
        vrt = row["Vacancy-Relationship-Type"]
        drfn = row["Data-Retrieval-File-Name"]
        ppfn = row["Preprocessing-File-Name"]
        rbfn = row["Relationship-Builder-File-Name"]
        p1 = row["Parameter-1"]
        p2 = row["Parameter-2"]
        p3 = row["Parameter-3"]
        p4 = row["Parameter-4"]
        #newSensor = snsr.VieSensor(linreg_flag, sn, st, uf, mu, dat, vrt, drfn, ppfn, rbfn, p1, p2, p3, p4)
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

def FuseVacancyProbabilities(probabilities, fusetype="rss"):
    if fusetype=="rss":
        probasq = [i ** 2 for i in probabilities]
        overallproba = sum(probasq) ** 0.5
    elif fusetype=="rms":
        probasq = [i ** 2 for i in probabilities]
        overallproba = (sum(probasq) / len(probabilities)) ** 0.5
    elif fusetype=="max":
        overallproba = max(probabilities)
    elif fusetype=="avg":
        overallproba = sum(probabilities) / len(probabilities)        
    elif fusetype=="mult":
        overallproba = np.prod(probabilities)
    elif fusetype=="linreg":
        overallproba = -1
    elif fusetype=="montecarlo":
        overallproba = MonteCarloFusion()
    else: # Default to "mult" - multiplying together the probabilities
        overallproba = np.prod(probabilities)
    return overallproba

def FuseVacancyTimestamps(timestamps, fusetype="rss"):
    overalldt = max(timestamps)
    return overalldt

# Create the following variables once...
output = pd.DataFrame(index=[0],columns=["runtimedt", "overallprobadt", "overallproba_rss", "overallproba_rms", "overallproba_max", "overallproba_avg", "overallproba_mult", "overallproba_linreg","wifidt","wifival","wifiproba","co2dt","co2val","co2proba","elecdt","elecval","elecproba"])
output.to_csv("DataFiles\\VIE-output-historical.csv", header=True, index=False) # Apply headers to csv and remove existing entries

#sensors = CreateVirtualSensors("VIE-sensor-metadatabase-new.csv") # Read sensors from file, instantiate dictionary. If missing data, fill with dummy data ("") and move on to next sensor
sensors = CreateVirtualSensors("VIE-sensor-metadatabase.csv") # Read sensors from file, instantiate dictionary. If missing data, fill with dummy data ("") and move on to next sensor

# Import csv historical data to dataframe
histdata = pd.read_csv("DataFiles\\VIE-input-historical_WCEC.csv") # In order: timestamp for sensor 1 (wifi), timestamp for sensor 2 (co2), timestamp for sensor 3 (elec), etc.
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
        probabilities.append(v.snapshotvacancyprobability) # Capture datetime in a list

    # fuse predictions for all sensors
    overallprobabilityvalue_rss = FuseVacancyProbabilities(probabilities,"rss")
    overallprobabilityvalue_rms = FuseVacancyProbabilities(probabilities,"rms")
    overallprobabilityvalue_max = FuseVacancyProbabilities(probabilities,"max")
    overallprobabilityvalue_avg = FuseVacancyProbabilities(probabilities,"avg")
    overallprobabilityvalue_mult = FuseVacancyProbabilities(probabilities,"mult")

    if linreg_flag:
        overallprobabilityvalue_linreg = FuseVacancyProbabilities(probabilities,"linreg")

    #overallprobabilityvalue = FuseVacancyProbabilities(probabilities,fusetype)
    overallprobabilitytimestamp = FuseVacancyTimestamps(timestamps,fusetype="rss")

    # TODO build up output dataframe based on sensorname. Hardcoded by sensorname for now, see below...
    #for k, v in sensors:
    #    #build the data frame column by column

    wifi = sensors["wifi1"]
    co2 = sensors["co21"]
    elec = sensors["elec1"]
    #output.iloc[0] = [dt.datetime.now(), overallprobabilitytimestamp, overallprobabilityvalue_rss, overallprobabilityvalue_rms, overallprobabilityvalue_max, overallprobabilityvalue_avg, overallprobabilityvalue_mult, overallprobabilityvalue_linreg, wifi.snapshottimestamp, wifi.snapshotvalue, wifi.snapshotvacancyprobability, co2.snapshottimestamp, co2.snapshotvalue, co2.snapshotvacancyprobability, elec.snapshottimestamp, elec.snapshotvalue, elec.snapshotvacancyprobability]
    output.to_csv("DataFiles\\VIE-output-historical.csv", mode="a", header=False, index=False)

figen.PlotMain()
thisisastopgap = "stopgap"