# Author: Lisa Slaughter <lisa.m.slaughter@gmail.com>
# Last update: Jan 28 2019

# {Description here}

# ----------------------------------------------------------------------------------------------------------
import pandas as pd
import numpy as np
import PI_client_LMS as pc
import figure_generator as fg
import time as time
import datetime as dt
import matplotlib.pyplot as plt

def BuildVacancyRelationship(sensor):
    client = pc.pi_client()
    point = sensor.dataaccesstype
    # TODO implement window of time from now to x months ago
    sensor.histdata = client.get_stream_by_point(point, start="2018-10-01 12:00:00", end="*", calculation="recorded")
    sensor = sensor.PreprocessData()
    # TODO implement vacancy start and end times in the config file for each sensor
    mask_vac = ( (sensor.histdata.index.hour >= 3 ) & (sensor.histdata.index.hour <= 4) ) # slice data for vacant times and days
    #mask_occ = (((data.index.hour > 7) & (data.index.hour < 23 )) & (data.index.dayofweek < 5))
    #mask_vac = (((data.index.hour <= 7) | (data.index.hour >= 23 )) | (data.index.dayofweek >= 5))
    data_v = sensor.histdata[mask_vac]
    if sensor.vacancyrelationship==0: # sigmoid
        stats_v = data_v.describe()
        mean = stats_v.iloc[1][0]
        std = stats_v.iloc[2][0]
        sensor.vrparam1 = mean
        sensor.vrparam2 = std
        fg.PlotSigmoids(sensor)
    elif sensor.vacancyrelationship==1: # ???
        pass
    else:
        pass # error out
    sensor.histdata = pd.DataFrame()
    return sensor
       