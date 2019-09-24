# Author: Lisa Slaughter <lisa.m.slaughter@gmail.com>
# Last update: Jan 28 2019

# {Add description here}

# ----------------------------------------------------------------------------------------------------------

import VieSensor as snsr
import ModelParameters as mp
import pandas as pd
import numpy as np
import time as time
import datetime as dt
import math as math
import scipy.optimize as opt
import matplotlib.pyplot as plt
import pre_analysis as pa
import helper_figure_generator as figen
import results_analysis as ra

# vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv.....Function Definitions
def StdDevWeightedAverage(sensors):
    # get std dev and snapshot val for each sensor input
    fusionparams = pd.DataFrame(index=range(len(sensors)), columns=range(2))
    stddevs = []
    i = 0
    for k, v in sensors.items():
        c = 1/(2*v.vrparam1)
        fusionparams.iloc[i,0] = v.snapshotvalue * c
        fusionparams.iloc[i,1] = v.std * c # standard deviation
        stddevs.append(v.std * c)
        i = i + 1
    corrected_vars = [1 / (i ** 2) for i in stddevs]
    #vardevs = [i ** 2 for i in stddevs]
    #vardevs = stddevs
    #varsum = sum(vardevs)
    varsum = sum(corrected_vars)
    overallproba = 0
    for index, row in fusionparams.iterrows():
        overallproba = overallproba + row[0] / (row[1] * varsum)
    return 1 - overallproba

def CreateVirtualSensors(params):
    new = ""
    if params.buildflag:
        new = "_new"

    path = "ConfigFiles\\VIE-sensor-metadatabase_" + params.buildtype + "_" + params.traintype + new + ".csv"
    metadata = pd.read_csv(path)
    sensors = {} # Create sensor dictionary. Enforces unique sensor names!!
    for index, row in metadata.iterrows():
        sn = row["Sensor-Name"]
        st = row["Sensor-Type"]
        uf = row["Update-Frequency"]
        mu = row["Measurement-Units"]
        dat = row["Data-Access-Type"]
        vrt = row["Vacancy-Relationship-Type"]
        trs = row["Training-Data-Set"]
        drfn = row["Data-Retrieval-File-Name"]
        ppfn = row["Preprocessing-File-Name"]
        rbfn = row["Relationship-Builder-File-Name"]
        std = row["Std-Dev"]
        p1 = row["Parameter-1"]
        p2 = row["Parameter-2"]
        p3 = row["Parameter-3"]
        p4 = row["Parameter-4"]
        newSensor = snsr.VieSensor(sn, st, uf, mu, dat, vrt, trs, drfn, ppfn, rbfn, std, p1, p2, p3, p4, ts, te)
        sensors[newSensor.sensorname] = newSensor
    
    metadata_new = metadata
    for index, row in metadata.iterrows():
        metadata_new.loc[index,"Parameter-1"] = sensors[row["Sensor-Name"]].vrparam1
        metadata_new.loc[index,"Parameter-2"] = sensors[row["Sensor-Name"]].vrparam2
        metadata_new.loc[index,"Parameter-3"] = sensors[row["Sensor-Name"]].vrparam3
        metadata_new.loc[index,"Parameter-4"] = sensors[row["Sensor-Name"]].vrparam4
        metadata_new.loc[index,"Std-Dev"] = sensors[row["Sensor-Name"]].std
    
    metadata_new.to_csv("ConfigFiles\\VIE-sensor-metadatabase_" + params.buildtype + "_" + params.traintype + "_new.csv", header=True, index=False)
    return sensors

def FuseVacancyProbabilities(sensors, fusetype="rms"):
    # Capture individual vacancy probability predictions into a list
    probabilities = []
    for k,v in sensors.items():
        probabilities.append(v.snapshotvacancyprobability)

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
    elif fusetype=="wghtavg":
        overallproba = StdDevWeightedAverage(sensors)
    else: # Default to "mult" - multiplying together the probabilities
        overallproba = np.prod(probabilities)
    return overallproba

def FuseVacancyTimestamps(timestamps, fusetype="rms"):
    overalldt = max(timestamps)
    return overalldt

def GenerateOutput(testdata, sensors, params):
    header_flag = 1
    for index, row in testdata.iterrows():
        output = pd.DataFrame(index=[0], columns=["fused-proba-dt", "fused-proba-" + params.fusetype, "truth-val"])
        output["truth-val"] = row["truth-val"]
        for k, v in sensors.items():
            v.snapshottimestamp = row["timestamp"]
            v.snapshotvalue = row[v.sensorname + "-val"]
            v.PreprocessData() # performs any needed preprocessing methods, i.e. conversions, etc.
            v.PredictVacancyProbability()

            # Build up a dataframe row for the output data
            temp_df.columns=[v.sensorname + "-val", v.sensorname + "-proba"]
            temp_df.iloc[0,0] = v.snapshotvalue
            temp_df.iloc[0,1] = v.snapshotvacancyprobability
            output = pd.concat([output,temp_df], join="outer", axis=1)

        # fuse predictions for all sensors
        output["fused-proba-" + params.fusetype] = FuseVacancyProbabilities(sensors, params.fusetype)
        output["fused-proba-dt"] = row["timestamp"].strftime("%Y-%m-%d %H:%M:%S")

        if (header_flag==1):
            header_flag=0        
            output.to_csv("DataFiles\\" + params.buildtype + "\\" + params.trainset + "\\VIE-historical-output.csv", header=True, index=False)
        else:
            output.to_csv("DataFiles\\" + params.buildtype + "\\" + params.trainset + "\\VIE-historical-output.csv", mode="a", header=False, index=False)
    return
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^.....Function Definitions


# vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv.....Parameter Definitions
## uncomment one of these to run that fusion method
#fuse_type = "rss"       # root sum square
fuse_type = "rms"       # root mean square
#fuse_type = "max"       # maximum
#fuse_type = "avg"       # average
#fuse_type = "mult"      # multiplication
#fuse_type = "whtavg"    # standard-deviation-weighted average

build_flag = True # Use this to tell model to rebuild vacancy relationship (True = rebuild and re-plot)

train_start = "2019-07-02 00:00:00"
train_end = "2019-07-16 00:00:00"

test_start = train_end
test_end = "2019-08-06 00:00:00"

#train_type = "Cherry"
train_type = "Full"

build_type = "Percentile"
#build_type = "Logistic"

params = mp.ModelParameters(build_flag, train_start, train_end, test_start, test_end, train_type, build_type, fuse_type)
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^.....Parameter Definitions

# vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv.....Main Program 
sensors = CreateVirtualSensors(params)
temp_df = pd.DataFrame(index=[0], columns=["val","proba"])
data = pd.read_csv("DataFiles\\VIE-historical-input_WCEC.csv", parse_dates=["timestamp"]) # columns: timestamp, {sensorname}-val, {sensorname}-val, ..., truth-val
data.index = data["timestamp"]
testdata = data.loc[params.teststart:params.testend,:]
traindata = data.loc[params.trainstart:params.trainend,:]
#for k,v in sensors.items():
#   pa.RunExploration(v.sensorname, traindata, build_type, train_set)
GenerateOutput(testdata, sensors, params)
ra.GenerateAnalytics(params)
#figen.PlotMain("comp", "2019-07-16 00:00:00", "2019-07-23 23:50:00", "1week", params)
figen.PlotMain("elec", "2019-07-16 00:00:00", "2019-07-23 23:50:00", "1week", params)
figen.PlotMain("wifi", "2019-07-16 00:00:00", "2019-07-23 23:50:00", "1week", params)
figen.PlotMain("co2", "2019-07-16 00:00:00", "2019-07-23 23:50:00", "1week", params)
#figen.PlotMain("comp", "2019-07-16 00:00:00", "2019-08-05 23:50:00", "3week", params)
figen.PlotMain("elec", "2019-07-16 00:00:00", "2019-08-05 23:50:00", "3week", params)
figen.PlotMain("wifi", "2019-07-16 00:00:00", "2019-08-05 23:50:00", "3week", params)
figen.PlotMain("co2", "2019-07-16 00:00:00", "2019-08-05 23:50:00", "3week", params)

thisisastopgap = "stopgap"
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^.....Main Program



# Write down minimum criteria
#  1) fused inference must be between 0 and 1
#  2) as you increase # of sensors, accuracy should improve (Alan expects probability to improve, does this make sense?)
