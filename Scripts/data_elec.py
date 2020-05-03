# Author: Lisa Slaughter <lisa.m.slaughter@gmail.com>
# Last update: May 02, 2019

# Defines methods related to data acquisition for electricty demand.

# ----------------------------------------------------------------------------------------------------------
import pandas as pd
import numpy as np


def UpdateSnapshot(sensor): 
    # No realtime option exists until API response can be parsed below.
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

def GetHistoricalDataFromAPI(): 
    import requests as req
    import logging as log
    # TODO: Non-standard response. Figure out how to parse.
    url = 'https://webservice.hobolink.com/restv2/data/custom/file'
    payload = {
        "query": "215_Last_30_Days",
        "authentication": {
            "password": "1605tilia",
            "user": "UHubDavis",
            "token": "Ei3pjgOLri",
        }
    }
    try:
        r = req.post(url, json=payload, timeout=30)
        #print(r.json)
        #a = r.json()
        b = r.text
        c = r.content
        data = pd.DataFrame(index=[0])
        d = c.rows.length
    except req.exceptions.Timeout:
        log.error("Hobolink HTTP request timed out (30 seconds)")
    return

def ResampleDataFile(freq):
    td = pd.read_csv("DataFiles\\WCEC-Elec-1min.csv", parse_dates=["Timestamp"])
    dts = pd.to_datetime(td["Timestamp"], format="%Y-%m-%d %H:%M:%S")
    td.index = dts
    td.drop(["Timestamp"], axis=1, inplace=True)
    td.index.name = "Timestamp"
    td2 = td["Demand (W)"].resample(freq).first()
    td2.to_csv("DataFiles\\WCEC-Elec-" + freq + ".csv", index=True, header=True)
    return

#ResampleDataFile("2min")