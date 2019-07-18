# Author: Lisa Slaughter <lisa.m.slaughter@gmail.com>
# Last update: Jan 28 2019

# This code performs the following preprocessing functions on the incoming data:
#    1) Checks for staleness

# ----------------------------------------------------------------------------------------------------------
import pandas as pd
import numpy as np

def PreprocessData(sensor):
    # Check for staleness by comparing to most recent values. Requires addition of a list (recentvalues) to VieSensor.py
    # Check for correct format


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
        if sensor.units == 'kbtu':
            kwconversion = 0.293071
            sensor = ConvertSensorValues(sensor, kwconversion)
        elif sensor.units == 'btu':
            kwconversion = 0.000293071
            sensor = ConvertSensorValues(sensor, kwconversion)
        else:
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

def ConvertSensorValues(sensor, conversionValue):
    sensor.snapshotvalue = sensor.snapshotvalue * conversionValue
    if sensor.histdata.empty:
        sensor.histdata = sensor.histdata * conversionValue
    return sensor

def ProcessAmbiDaqFile():
    # starting .csv should include data from each DAQ appended to each other, with the "DAQ #" column replacing the existing identifier (MAC)
    datatat = pd.read_csv("DataFiles\\WCEC\\AmbiDAQ_all_.csv", parse_dates=["Datetime"])
    datatat.set_index(datatat["Datetime"],inplace=True)
    #datatat.drop("Datetime", axis=1, inplace=True)
    dt = datatat.groupby(by=[datatat.index.minute,datatat.index.hour,datatat.index.day,datatat.index.month,datatat.index.year])
    temp_df = pd.DataFrame(index=[0],columns=["Datetime","Year","Month","Day","Hour","Minute","T_16","RH_16","CO2_16","PIR_16","T_18","RH_18","CO2_18","PIR_18","T_20","RH_20","CO2_20","PIR_20","T_21","RH_21","CO2_21","PIR_21","T_22","RH_22","CO2_22","PIR_22"])
    temp_df.to_csv("DataFiles\\WCEC\\AmbiDAQ_group_output.csv", header=True, index=False)
    for t,g in dt:
        tdt = g.iloc[0,0:6]
        temp_df.iloc[0,:] = (tdt)
        for index, row in g.iterrows():
            daq = row["DAQ #"]

            temp = row["T"]
            new_temp = "T_" + str(daq)
            temp_df[new_temp] = temp

            hum = row["RH"]
            new_hum = "RH_" + str(daq)
            temp_df[new_hum] = hum

            co2 = row["CO2"]
            new_co2 = "CO2_" + str(daq)
            temp_df[new_co2] =co2

            pir = row["PIR"]
            new_pir = "PIR_" + str(daq)
            temp_df[new_pir] = pir

        temp_df.to_csv("DataFiles\\WCEC\\AmbiDAQ_group_output.csv", mode="a", header=False, index=False)
    x = "thisisastopgap"
    return

#ProcessAmbiDaqFile()