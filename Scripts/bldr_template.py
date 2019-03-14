# Author: Lisa Slaughter <lisa.m.slaughter@gmail.com>
# Last update: Jan 28 2019

# {Description here}

# ----------------------------------------------------------------------------------------------------------
import pandas as pd
import numpy as np
import math as math
import scipy.optimize as opt
import PI_client_LMS as pc
import matplotlib.pyplot as plt

def Sigmoid(x, a, b):
    return 1-1/(1+np.exp((a-x)/b))

def PlotSigmoids(sensor, sensorvals, probas):
    labs = 11 # figure label size
    legs = "medium"
    
    sigmoidcompfig, axcs = plt.subplots(figsize=(20,10))
    axcs.plot(sensorvals, probas, label="sigmoidcompfig")
    #plt.savefig("sigmoid-value-check-" + sensor.sensorname + ".png", format="png", bbox_inches="tight")
    axcs.plot(sensorvals, Sigmoid(sensorvals, sensor.vrparam1, sensor.vrparam2))
    plt.ylim([0,1])
    plt.xlim([0,max(sensorvals)])
    axcs.xaxis.set_major_locator(plt.MaxNLocator(20))
    axcs.xaxis.set_tick_params(labelsize=labs)
    axcs.yaxis.set_tick_params(labelsize=labs)
    axcs.set_title("Vacancy Relationship Accuracy for Sensor: " + sensor.sensorname, fontsize=18, fontweight="bold")
    axcs.set_ylabel("Probability of Vacancy (%)", fontsize=labs)
    axcs.set_xlabel("Raw Sensor Value", fontsize=labs)
    axcs.grid(b=True, which='major', color='k', linestyle=':', linewidth=1)
    plt.savefig("Figures\\sigmoid-comparison-" + sensor.sensorname + ".png", format="png", bbox_inches="tight")
    plt.close(sigmoidcompfig)
    return

def GetHistoricalVacancyData(sensor):
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
    sensor.vachistdata = data_v[np.logical_not(np.isnan(data_v))]
    #sensor.occhistdata = sensor.histdata[mask_occ]
    return sensor

def BuildVacancyRelationship(sensor):
    GetHistoricalVacancyData(sensor)
    if sensor.vacancyrelationship==0: # sigmoid
        cumsum = 0
        probas = []
        cols = sensor.vachistdata.columns
        sensorvals = sensor.vachistdata[cols[0]]
        summary = sum(sensorvals)
        sensorvals = sensorvals.sort_values(ascending=True)
        for datum in sensorvals:
            cumsum = cumsum + datum
            probas.append(1-cumsum/summary)
        probas = pd.Series(probas)
        stats_v = sensorvals.describe()
        mean = stats_v["mean"]
        std = stats_v["std"]
        popt, pcov = opt.curve_fit(Sigmoid, sensorvals, probas, p0=[mean, std])
        sensor.vrparam1 = popt[0]
        sensor.vrparam2 = popt[1]
        sensor.probas = probas
        PlotSigmoids(sensor, sensorvals, probas)
    elif sensor.vacancyrelationship==1: # ???
        pass
    else:
        pass # error out
    sensor.histdata = pd.DataFrame()
    sensor.vachistdata = pd.DataFrame()
    sensor.occhistdata = pd.DataFrame()
    return sensor
       