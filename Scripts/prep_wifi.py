# Author: Lisa Slaughter <lisa.m.slaughter@gmail.com>
# Last update: May 02, 2019

# This code contains methods related to preprocessing the incoming data. Examples:
#    1) Check for staleness
#    2) Perform conversions
#    3) Check for formatting
#    4) Ensure the value makes sense
#    5) Etc...

# ----------------------------------------------------------------------------------------------------------
import pandas as pd
import numpy as np

def PreprocessData(sensor):
    # Put code here
    return sensor

def ConvertSensorValues(sensor, conversionMultiplier):
    sensor.snapshotvalue = sensor.snapshotvalue * conversionMultiplier
    if sensor.histdata.empty:
        sensor.histdata = sensor.histdata * conversionMultiplier
    return sensor