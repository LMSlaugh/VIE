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

def UpdateSnapshot(sensor):
    # Brings in the most recent data point from passed sensor. Sourced from the OSIsoft PI data historian owned by UC Davis Facilities Management
    client = pc.pi_client()
    # ...builidng dummy data for required variables
    current = dt.datetime.now()
    window = dt.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=1, weeks=0)
    start = current - window
    s1 = client.get_stream_by_point(sensor.dataaccesstype, calculation="end", start=start, end=current)
    # ...TODO some handling for no data returned from historian
    c = s1.columns
    # Convert from UTC to local timezone (Los Angeles)
    timestamp = s1.loc["Timestamp",c[0]]
    timestamp = timestamp[0:19]
    timestamp = dt.datetime.strptime(timestamp,"%Y-%m-%dT%H:%M:%S")
    timestamp = timestamp.replace(tzinfo=tz('UTC'))
    timestamp = timestamp.astimezone(tz("US/Pacific"))
    sensor.snapshottimestamp = timestamp
    if sensor.sensortype == "carbondioxide":
        d = s1.loc["Value",c[0]]
        if ( isinstance(d,int) | isinstance(d,float) ):
            sensor.snapshotvalue = d
        else:
            sensor.snapshotvalue = d["Value"]
    else:
        sensor.snapshotvalue = s1.loc["Value",c[0]]
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

    #client = pc.pi_client()
    #point = sensor.dataaccesstype
    #sensor.histdata = client.get_stream_by_point(point, start="2019-07-06 00:00:00", end="2019-07-20 00:00:00", calculation="interpolated", interval="10m")
    #sensor = sensor.PreprocessData()
    return sensor