import pandas as pd
import numpy as np
import PI_client_LMS as pc
import matplotlib.pyplot as plt
import sklearn as sk
import math

def PrepForHist(target):
    testd = pd.DataFrame(index=target.index, data=target.values, columns=["raw"])
    testd["vacant"] = target
    testd["occupied"] = target
    testd.loc[testd[mask_occ].index,["vacant"]] = float("NaN")
    testd.loc[testd[mask_vac].index,["occupied"]] = float("NaN")
    #testd.to_csv("Sanity_Check.csv")
    return testd

def ProcessAmbiDaqFile():
    #load up csv
    datatat = pd.read_csv("DataFiles\\AmbiDAQ_all_.csv", parse_dates=["Datetime"])
    datatat.set_index(datatat["Datetime"],inplace=True)
    #datatat.drop("Datetime", axis=1, inplace=True)
    dt = datatat.groupby(by=[datatat.index.minute,datatat.index.hour,datatat.index.day,datatat.index.month,datatat.index.year])
    temp_df = pd.DataFrame(index=[0],columns=["Datetime","Year","Month","Day","Hour","Minute","T_16","RH_16","CO2_16","PIR_16","T_18","RH_18","CO2_18","PIR_18","T_20","RH_20","CO2_20","PIR_20","T_21","RH_21","CO2_21","PIR_21","T_22","RH_22","CO2_22","PIR_22"])
    temp_df.to_csv("DataFiles\\AmbiDAQ_group_output.csv", header=True, index=False)
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

        temp_df.to_csv("DataFiles\\AmbiDAQ_group_output.csv", mode="a", header=False, index=False)
    return

def MatchInputTimestampsByMinute():
    input1 = pd.read_csv("DataFiles\\WCEC_CO2_01FEB2019_to_10APR2019.csv", parse_dates=["dt"])
    input2 = pd.read_csv("DataFiles\\WCEC_ElecData_01FEB2019_thru_10APR2019.csv", parse_dates=["dt"])
    input3 = pd.read_csv("DataFiles\\WCEC_WifiData_fake_01FEB2018_thru_10APR2019.csv", parse_dates=["dt"])
    #remove rows containing "Nan"
    input1.dropna()
    input2.dropna()
    input3.dropna()
    inputs = input1.append(input2)
    inputs = inputs.append(input3)
    inputs.to_csv("DataFiles\\WCEC_AllTestData_01FEB2019_thru_10APR2019.csv")
    inputs.set_index(inputs["dt"], inplace=True)
    dt = inputs.groupby(by=[inputs.index.minute,inputs.index.hour,inputs.index.day,inputs.index.month,inputs.index.year])
    temp_df = pd.DataFrame(index=[0],columns=["Datetime","wifi1_val","co21_val","elec1_val"])
    temp_df.to_csv("DataFiles\\WCEC_AllTestData_Horiz_01FEB2019_thru_10APR2019.csv", header=True, index=False)
    for t,g in dt:
        tdt = g.iloc["dt"]
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
    x = "thisisastopgap"
    return


#ProcessAmbiDaqFile()
MatchInputTimestampsByMinute()

client = pc.pi_client()
l, r = client.search_by_point("AP.UNIV-SVCS-270-743748")
#print(l)
points = l[0]
data = client.get_stream_by_point(points, start="2018-12-11 10:00:00", end="2019-04-10 10:00:00", calculation="recorded")
data.to_csv("DataFiles\\WCEC_WifiData_fake.csv")

plt.plot(data)
plt.savefig("Figures\\WV-wifi-raw.png", format='png', bbox_inches='tight')
mask_occ = (((data.index.hour > 7) & (data.index.hour < 23 )) & (data.index.dayofweek < 5))
mask_vac = (((data.index.hour <= 7) | (data.index.hour >= 23 )) | (data.index.dayofweek >= 5))
data["vacant"] = 2
data.loc[data[mask_vac].index,["vacant"]] = 1
data.loc[data[mask_occ].index,["vacant"]] = 0

#histd = PrepForHist(data["elec"])



#Plot in histogram

thisisastop = 12