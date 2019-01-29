# Author: Lisa Slaughter <lisa.m.slaughter@gmail.com>
# Last update: Jan 28 2019

# This code performs the following preprocessing functions on the incoming data:
#    1) Checks for staleness

# ----------------------------------------------------------------------------------------------------------
import pandas as pd
import numpy as np

def PreprocessData(sensor):
    # Check for staleness by comparing to most recent values. Requires addition of a list (recentvalues) to VieSensor.py



    # Some junk code...
    # by function type
    if sensor.vacancyrelationship==0: # sigmoid
        pass
    elif sensor.vacancyrelationship==1: # ???
        pass
    else:
        pass # error out

    # by sensor type
    if sensor.sensortype=="carbondioxide":
        pass
    elif sensor.sensortype=="wifi":
        pass
    elif sensor.sensortype=="electricitydemand":
        pass
    elif sensor.sensortype=="domesticwaterdemand":
        pass
    elif sensor.sensortype=="absolutehumidity":
        pass
    elif sensor.sensortype=="schedule":
        pass
    elif sensor.sensortype=="": # placeholder
        pass
    else:
        pass # error out

    # ...Does value make sense? Could be different for each sensor. May need a pre-processing function for each type.
    # ...Need a way to handle different timestamps between sensors (use most recent timestamp for vacancy prediction?)

    return sensor