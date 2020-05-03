# Author: Lisa Slaughter <lisa.m.slaughter@gmail.com>
# Last update: May 02, 2019

# Defines methods related to data acquisition for carbon dioxide.

# ----------------------------------------------------------------------------------------------------------
import pandas as pd
import numpy as np

def UpdateSnapshot(sensor): 
    # No real-time data stream is available for carbon dioxide. Prevents implementation of real-time method :(
    return sensor

def GetHistoricalData(sensor, start, end):
    start = pd.to_datetime(start, format="%Y-%m-%d %H:%M:%S")
    end = pd.to_datetime(end, format="%Y-%m-%d %H:%M:%S")
    historicaldata = pd.read_csv("DataFiles\\VIE-historical-input_WCEC.csv", parse_dates=["timestamp"])
    historicaldata.index = historicaldata["timestamp"]
    if sensor.trainingdataset=="Cherry":
        sensor.histdata = pd.DataFrame(historicaldata.loc[start:end,sensor.sensorname + "-val"])
    elif sensor.trainingdataset=="Full":
        sensor.histdata = pd.DataFrame(historicaldata.loc[start:end,[sensor.sensorname + "-val", "truth-val"]])
    return sensor