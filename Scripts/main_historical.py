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
    topterms = []
    weights = []
    i = 0
    for k, v in sensors.items():
        topterms.append(v.snapshotvacancyprobability/v.std)
        weights.append(1/v.std)
        i = i + 1
    numer = sum(topterms)
    denom = sum(weights)
    overallproba = numer/denom
    return overallproba

def StdDevWeightedRMS(sensors):
    topterms = []
    weights = []
    i = 0
    for k, v in sensors.items():
        topterms.append(v.snapshotvacancyprobability**2/v.std)
        weights.append(1/v.std)
        i = i + 1
    numer = sum(topterms)
    denom = sum(weights)
    overallproba =  ( numer/(denom) )**0.5
    return overallproba

def CreateVirtualSensors(params):
    new = "_new"
    if params.buildflag:
        new = ""

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
        newSensor = snsr.VieSensor(sn, st, uf, mu, dat, vrt, trs, drfn, ppfn, rbfn, std, p1, p2, p3, p4, params.trainstart, params.trainend)
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

def FuseVacancyProbabilities(sensors, fusetype="RMS"):
    # Capture individual vacancy probability predictions into a list
    probabilities = []
    for k,v in sensors.items():
        probabilities.append(v.snapshotvacancyprobability)

    if fusetype=="RSS":
        probasq = [i ** 2 for i in probabilities]
        overallproba = sum(probasq) ** 0.5
    elif fusetype=="RMS":
        probasq = [i ** 2 for i in probabilities]
        overallproba = (sum(probasq) / len(probabilities)) ** 0.5
    elif fusetype=="MAX":
        overallproba = max(probabilities)
    elif fusetype=="AVG":
        overallproba = sum(probabilities) / len(probabilities)        
    elif fusetype=="MULT":
        overallproba = np.prod(probabilities)
    elif fusetype=="SDWA":
        overallproba = StdDevWeightedAverage(sensors)
    elif fusetype=="SDWRMS":
        overallproba = StdDevWeightedRMS(sensors)
    else: # Default to "mult" - multiplying together the probabilities
        overallproba = np.prod(probabilities)
    return overallproba

def FuseVacancyTimestamps(timestamps, fusetype="RMS"):
    overalldt = max(timestamps)
    return overalldt

def GetTrainTestData(params):
    data = pd.read_csv("DataFiles\\VIE-historical-input_WCEC.csv", parse_dates=["timestamp"]) # columns: timestamp, {sensorname}-val, {sensorname}-val, ..., truth-val
    data.index = data["timestamp"]
    testdata = data.loc[params.teststart:params.testend,:]
    traindata = data.loc[params.trainstart:params.trainend,:]
    return traindata, testdata

def GenerateOutput(testdata, sensors, params):
    temp_df = pd.DataFrame(index=[0], columns=["val","proba"])
    header_flag = 1
    for index, row in testdata.iterrows():
        output = pd.DataFrame(index=[0], columns=["fused-proba-dt", "fused-proba-" + params.fusetype, "truth-val"])
        output["truth-val"] = row["truth-val"]
        for k, v in sensors.items():
            v.snapshottimestamp = row["timestamp"]
            v.snapshotvalue = row[v.sensorname + "-val"]
            v.PreprocessData() # performs any needed preprocessing methods, i.e. conversions, etc. before predicting
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
            output.to_csv("DataFiles\\" + params.buildtype + "\\" + params.traintype + "\\" + params.fusetype + "\\VIE-historical-output.csv", header=True, index=False)
        else:
            output.to_csv("DataFiles\\" + params.buildtype + "\\" + params.traintype + "\\" + params.fusetype + "\\VIE-historical-output.csv", mode="a", header=False, index=False)
    return

def GeneratePlots(params):
    #figen.PlotMain("comp", "2019-07-16 00:00:00", "2019-07-23 23:50:00", "1week", params)
    #figen.PlotMain("elec", "2019-07-16 00:00:00", "2019-07-23 23:50:00", "1week", params)
    figen.PlotMain("wifi", "2019-07-16 00:00:00", "2019-07-23 23:50:00", "1week", params)
    #figen.PlotMain("co2", "2019-07-16 00:00:00", "2019-07-23 23:50:00", "1week", params)
    #figen.PlotMain("comp", "2019-07-16 00:00:00", "2019-08-05 23:50:00", "3week", params)
    #figen.PlotMain("elec", "2019-07-16 00:00:00", "2019-08-05 23:50:00", "3week", params)
    figen.PlotMain("wifi", "2019-07-16 00:00:00", "2019-08-05 23:50:00", "3week", params)
    #figen.PlotMain("co2", "2019-07-16 00:00:00", "2019-08-05 23:50:00", "3week", params)
    return

def Main(build_flag, build_type, train_type, fuse_type, train_start, train_end, test_start, test_end):
    params = mp.ModelParameters(build_flag, train_start, train_end, test_start, test_end, train_type, build_type, fuse_type)
    sensors = CreateVirtualSensors(params)
    #traindata, testdata = GetTrainTestData(params)
    #for k,v in sensors.items():
       #pa.RunExploration(v.sensorname, traindata, params.buildtype, params.traintype)
    #GenerateOutput(testdata, sensors, params)
    #ra.GenerateAnalytics(params)
    GeneratePlots(params)
    return

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^.....Function Definitions
# vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv.....Main Program 
# for reference: Main(build_flag, build_type, train_type, fuse_type, train_start, train_end, test_start, test_end)

Main(True, "Logistic", "Full", "AVG", "2019-07-02 00:00:00", "2019-07-16 00:00:00", "2019-07-16 00:00:00", "2019-08-06 00:00:00")
Main(False, "Logistic", "Cherry", "AVG", "2019-07-02 00:00:00", "2019-07-16 00:00:00", "2019-07-16 00:00:00", "2019-08-06 00:00:00")
Main(False, "Percentile", "Full", "AVG", "2019-07-02 00:00:00", "2019-07-16 00:00:00", "2019-07-16 00:00:00", "2019-08-06 00:00:00")
Main(False, "Percentile", "Cherry", "AVG", "2019-07-02 00:00:00", "2019-07-16 00:00:00", "2019-07-16 00:00:00", "2019-08-06 00:00:00")


#Main(False, "Logistic", "Full", "RMS", "2019-07-02 00:00:00", "2019-07-16 00:00:00", "2019-07-16 00:00:00", "2019-08-06 00:00:00")
#Main(False, "Logistic", "Cherry", "RMS", "2019-07-02 00:00:00", "2019-07-16 00:00:00", "2019-07-16 00:00:00", "2019-08-06 00:00:00")
#Main(False, "Percentile", "Full", "RMS", "2019-07-02 00:00:00", "2019-07-16 00:00:00", "2019-07-16 00:00:00", "2019-08-06 00:00:00")
#Main(False, "Percentile", "Cherry", "RMS", "2019-07-02 00:00:00", "2019-07-16 00:00:00", "2019-07-16 00:00:00", "2019-08-06 00:00:00")

#Main(False, "Logistic", "Full", "SDWA", "2019-07-02 00:00:00", "2019-07-16 00:00:00", "2019-07-16 00:00:00", "2019-08-06 00:00:00")
#Main(False, "Logistic", "Cherry", "SDWA", "2019-07-02 00:00:00", "2019-07-16 00:00:00", "2019-07-16 00:00:00", "2019-08-06 00:00:00")
#Main(False, "Percentile", "Full", "SDWA", "2019-07-02 00:00:00", "2019-07-16 00:00:00", "2019-07-16 00:00:00", "2019-08-06 00:00:00")
#Main(False, "Percentile", "Cherry", "SDWA", "2019-07-02 00:00:00", "2019-07-16 00:00:00", "2019-07-16 00:00:00", "2019-08-06 00:00:00")

#Main(False, "Logistic", "Full", "SDWRMS", "2019-07-02 00:00:00", "2019-07-16 00:00:00", "2019-07-16 00:00:00", "2019-08-06 00:00:00")
#Main(False, "Logistic", "Cherry", "SDWRMS", "2019-07-02 00:00:00", "2019-07-16 00:00:00", "2019-07-16 00:00:00", "2019-08-06 00:00:00")
#Main(False, "Percentile", "Full", "SDWRMS", "2019-07-02 00:00:00", "2019-07-16 00:00:00", "2019-07-16 00:00:00", "2019-08-06 00:00:00")
#Main(False, "Percentile", "Cherry", "SDWRMS", "2019-07-02 00:00:00", "2019-07-16 00:00:00", "2019-07-16 00:00:00", "2019-08-06 00:00:00")

#Main(False, "Logistic", "Full", "FEWA", "2019-07-02 00:00:00", "2019-07-16 00:00:00", "2019-07-16 00:00:00", "2019-08-06 00:00:00")
#Main(False, "Logistic", "Cherry", "FEWA", "2019-07-02 00:00:00", "2019-07-16 00:00:00", "2019-07-16 00:00:00", "2019-08-06 00:00:00")
#Main(False, "Percentile", "Full", "FEWA", "2019-07-02 00:00:00", "2019-07-16 00:00:00", "2019-07-16 00:00:00", "2019-08-06 00:00:00")
#Main(False, "Percentile", "Cherry", "FEWA", "2019-07-02 00:00:00", "2019-07-16 00:00:00", "2019-07-16 00:00:00", "2019-08-06 00:00:00")

#Main(False, "Logistic", "Full", "FEWRMS", "2019-07-02 00:00:00", "2019-07-16 00:00:00", "2019-07-16 00:00:00", "2019-08-06 00:00:00")
#Main(False, "Logistic", "Cherry", "FEWRMS", "2019-07-02 00:00:00", "2019-07-16 00:00:00", "2019-07-16 00:00:00", "2019-08-06 00:00:00")
#Main(False, "Percentile", "Full", "FEWRMS", "2019-07-02 00:00:00", "2019-07-16 00:00:00", "2019-07-16 00:00:00", "2019-08-06 00:00:00")
#Main(False, "Percentile", "Cherry", "FEWRMS", "2019-07-02 00:00:00", "2019-07-16 00:00:00", "2019-07-16 00:00:00", "2019-08-06 00:00:00")

thisisastopgap = "stopgap"
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^.....Main Program
