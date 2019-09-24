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

def ProcessAmbiDaqFile_New():
# This is for AmbiDAQ data from anytime post-July 01 2019 (data was moved to a MySQL server in June 2019)
# Note: Does not pull directly from server, but instead from a .csv file that horizontally appends columns for Timestamp and CO2 data, in that order, for each DAQ, in order.
# i.e. Timstamp_DAQ_01, Value_DAQ_01, Timestamp_DAQ_02, Value_DAQ_02, etc...
    value_type = "CO2"
    date_cols = list(range(0,44,2))
    my_date_parser = lambda x: pd.datetime.strptime(x, "%m/%d/%Y %H:%M:%S")
    bigD = pd.read_csv("DataFiles\\WCEC-CO2-shrt.csv", parse_dates=date_cols, date_parser=my_date_parser)
    cols = bigD.columns
    df_list = []
    i = 0
    for col in cols:
        if (i%2 == 0):
            df_temp = pd.DataFrame(index=range(0,len(bigD[col]),1), columns=[0,1])
            col_names = [col]
        if (i%2 == 1):
            col_names.append(col)
            df_temp.columns = col_names
        df_temp.iloc[:,i%2] = bigD[col]
        df_temp
        df_list.append(df_temp)
        i = i + 1

    j_list = list(range(0,len(df_list),1))
    for j in j_list:
        df_list[j].index = df_list[j].iloc[:,0]
    return

def ProcessAmbiDaqFile_Old(): 
# This is for AmbiDAQ .csv files downloaded from https://energyinstitute-data.com/Ambi-DAQXX/ , where XX must be replaced with a number 01 through 22 (pre-June 2019)
    # starting .csv should include data from each DAQ appended to each other, with the "DAQ #" column replacing the existing identifier (MAC address)
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
#ProcessAmbiDaqFile_New()