# Author: Lisa Slaughter <lisa.m.slaughter@gmail.com>
# Last update: Jan 28 2019

# {Description here}

# ----------------------------------------------------------------------------------------------------------
import pandas as pd
import numpy as np
import requests as req
import logging


def UpdateSnapshot(sensor): 
    # No realtime option exists until API response can be parsed below.
    # Get historical results for a certain time window
    # Get most recent timestamp from that
    # Update sensor snapshot value
    return sensor

def GetHistoricalData(sensor):
    historicaldata = pd.read_csv("DataFiles\\WCEC_Elec.csv", parse_dates=["Date"])
    historicaldata.set_index(historicaldata["Date"],inplace=True)
    data = pd.DataFrame(index=historicaldata["Date"])
    data["Total Demand (W)"] = historicaldata["Total Demand (W)"]
    # Get 2 weeks worth of data only
    numWeeks = 3
    items = numWeeks*7*24*6
    sensor.histdata = data.iloc[0:items,:]
    return sensor

def GetHistoricalDataFromAPI(): # Currently not called anywhere. Having trouble parsing results (appears to be in .csv format?)
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