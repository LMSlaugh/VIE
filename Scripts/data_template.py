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

def GetHistoricalData(sensor):
    client = pc.pi_client()
    point = sensor.dataaccesstype
    # TODO implement window of time from now to x months ago
    sensor.histdata = client.get_stream_by_point(point, start="2019-03-01 12:00:00", end="*", calculation="recorded")
    sensor = sensor.PreprocessData()
    return sensor