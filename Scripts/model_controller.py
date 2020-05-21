# *This code is still under development*
# Author: Lisa Slaughter <lisa.m.slaughter@gmail.com>
# Last update: May 02, 2019

# This is the main entry point for the Vacancy Inference Engine (VIE). The VIE uses building sensor data to
# infer if the building is vacant or occupied.
# 
# This codebase has been built with flexibility and exploration in mind:
#    -Any number of sensors can be defined in ConfigFiles/VIE-sensor-metadatabase.csv. Each row represents an 
#     individual sensor. Multiple types of the same sensor are allowed as long as the names are unique.
#    -Each sensor has associated with it three files. The data file (prepended with "data_") defines
#     data acquisition and manipulation methods. The preprocessing file performs any cleaning, conversion, 
#     or manipulation (i.e. feature engineering) of the data before it is used in the model. This is applied 
#     to training, testing, and incoming data. The builder file defines how the mapping between raw sensor 
#     value and probability of vacancy is generated.
#    -Different methods of data fusion can be explored. See ModelParameters.py for more information.
#    -Currently, it is only possible to run the VIE for a .csv of historical data. However, initial development
#     included real-time capability, and little work would be required to provide this functionality.
# ----------------------------------------------------------------------------------------------------------
import numpy as np
import pandas as pd
import VieSensor as snsr
import ModelParameters as mp
import helper_figureGenerator as figen
import preanalysis
import postanalysis

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

def HarmonicAverage(probas):
    inv_probas = []
    for elem in probas:
        if elem==0:
            return 0 # Because anything / infinity = 0
        else:
            inv_probas.append(1/elem)
    overallproba = len(probas) / sum(inv_probas)
    return overallproba

def CreateVirtualSensors(params):
    path = "ConfigFiles\\VIE-sensor-metadatabase_" + params.buildtype + "_" + params.traintype + "_new.csv"
    metadata = pd.read_csv(path)
    sensors = {}
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
    elif fusetype=="SM":
        overallproba = sum(probabilities) / len(probabilities)        
    elif fusetype=="MULT":
        overallproba = np.prod(probabilities)
    elif fusetype=="SDWM":
        overallproba = StdDevWeightedAverage(sensors)
    elif fusetype=="SDWRMS":
        overallproba = StdDevWeightedRMS(sensors)
    elif fusetype=="HM":
        overallproba = HarmonicAverage(probabilities)
    else:
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
            v.PreprocessData()
            v.PredictVacancyProbability()

            # Build up a dataframe row for the output data
            temp_df.columns=[v.sensorname + "-val", v.sensorname + "-proba"]
            temp_df.iloc[0,0] = v.snapshotvalue
            temp_df.iloc[0,1] = v.snapshotvacancyprobability
            output = pd.concat([output,temp_df], join="outer", axis=1)

        # fuse predictions for all sensors
        tempy = FuseVacancyProbabilities(sensors, params.fusetype)
        output["fused-proba-" + params.fusetype] = tempy
        output["fused-proba-dt"] = row["timestamp"].strftime("%Y-%m-%d %H:%M:%S")

        if (header_flag==1):
            header_flag=0        
            output.to_csv("DataFiles\\" + params.buildtype + "\\" + params.traintype + "\\" + params.fusetype + "\\VIE-historical-output.csv", header=True, index=False)
        else:
            output.to_csv("DataFiles\\" + params.buildtype + "\\" + params.traintype + "\\" + params.fusetype + "\\VIE-historical-output.csv", mode="a", header=False, index=False)
    return

def GeneratePlots(params):
    # The following lines of code can be un/commented to in/exclude different plot configurations

    #figen.PlotMain("comp", "2019-07-16 00:00:00", "2019-07-23 23:50:00", "1week", params)
    figen.PlotMain("Elec", "2019-07-16 00:00:00", "2019-07-23 23:50:00", "1week", params)
    figen.PlotMain("WiFi", "2019-07-16 00:00:00", "2019-07-23 23:50:00", "1week", params)
    figen.PlotMain("CO2", "2019-07-16 00:00:00", "2019-07-23 23:50:00", "1week", params)
    #figen.PlotMain("comp", "2019-07-16 00:00:00", "2019-08-05 23:50:00", "3week", params)
    figen.PlotMain("Elec", "2019-07-16 00:00:00", "2019-08-05 23:50:00", "3week", params)
    figen.PlotMain("WiFi", "2019-07-16 00:00:00", "2019-08-05 23:50:00", "3week", params)
    figen.PlotMain("CO2", "2019-07-16 00:00:00", "2019-08-05 23:50:00", "3week", params)
    return
