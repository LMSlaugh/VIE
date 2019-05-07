# Author: Lisa Slaughter <lisa.m.slaughter@gmail.com>
# Last update: Jan 28 2019

# {Description here}

# ----------------------------------------------------------------------------------------------------------
import pandas as pd
import numpy as np
import requests as req
import datetime as dt
from pytz import timezone as tz
import PI_client_LMS as pc

# Fix to retreive from csv

def UpdateSnapshot(sensor): 
    # No realtime option exists until API is used to access historical data.
    # Get historical results for a certain time window
    # Get most recent timestamp from that
    # Update sensor snapshot value
    return sensor

def GetHistoricalData(sensor):
    historicaldata = pd.read_csv("DataFiles\\WCEC_CO2.csv", parse_dates=["dt"])
    historicaldata.set_index(historicaldata["dt"],inplace=True)
    data = pd.DataFrame(index=historicaldata["dt"])
    data["CO2 (ppm)"] = historicaldata.max(axis=1)
    # Get 2 weeks worth of data only
    numWeeks = 3
    items = numWeeks*7*24*60
    sensor.histdata = data.iloc[0:items,:]
    return sensor