# Author: Lisa Slaughter <lisa.m.slaughter@gmail.com>
# Last update: Jan 28 2019

# {Description here}

# ----------------------------------------------------------------------------------------------------------
import pandas as pd
import numpy as np
import requests as req
import logging


def UpdateSnapshot(sensor):
    return sensor

def GetHistoricalData(sensor):
    historicaldata = pd.read_csv("DataFiles\\WCEC_ElecData.csv", parse_dates=["Date"])
    historicaldata.set_index(historicaldata["Date"],inplace=True)
    data = pd.DataFrame(index=historicaldata["Date"])
    data["Total Demand (W)"] = historicaldata["Total Demand (W)"]
    # Get X weeks worth of data only
    sensor.histdata = data[0:8064,:]
    return sensor

def GetHistoricalDataFromAPI(): # Currently not called anywhere. Having trouble parsing results (appears to be in .csv format)
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
        logging.error("Hobolink HTTP request timed out (30 seconds)")
    return