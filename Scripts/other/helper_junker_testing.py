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

def MatchInputAmbiDaqTimestampsByMinute():
    #input1 = pd.read_csv("DataFiles\\WCEC_CO2_01FEB2019_to_10APR2019.csv", parse_dates=["dt"])
    #input2 = pd.read_csv("DataFiles\\WCEC_ElecData_01FEB2019_thru_10APR2019.csv", parse_dates=["dt"])
    #input3 = pd.read_csv("DataFiles\\WCEC_WifiData_fake_01FEB2018_thru_10APR2019.csv", parse_dates=["dt"])
    ##remove rows containing "Nan"
    #input1.dropna()
    #input2.dropna()
    #input3.dropna()
    #inputs = input1.append(input2)
    #inputs = inputs.append(input3)
    #inputs.to_csv("DataFiles\\WCEC_AllTestData_01FEB2019_thru_10APR2019.csv")
    inputs = pd.read_csv("DataFiles\\WCEC_AllTestData_01FEB2019_thru_10APR2019.csv", parse_dates=["dt"])
    inputs.set_index(inputs["dt"], inplace=True)
    inputs = inputs.drop(["CO2_16","CO2_18","CO2_20","CO2_21","CO2_22"], axis=1)
    dt = inputs.groupby(by=[inputs.index.year,inputs.index.month,inputs.index.day,inputs.index.hour,inputs.index.minute])
    temp_df = pd.DataFrame(index=[0],columns=["wifi1-dt","wifi1-val","co21-dt","co21-val","elec1-dt","elec1-val"])
    temp_df.to_csv("DataFiles\\WCEC_AllTestData_Horiz_01FEB2019_thru_10APR2019.csv", mode="w", header=True, index=False)
    
    for t,g in dt: #foreach group....
        try:
            tdt = g["dt"][0] #  ...extract the datetime (to the minute) for that group
            tdt = tdt.replace(second=0)
            temp_df["wifi1-dt"][0] = tdt
            temp_df["co21-dt"][0] = tdt
            temp_df["elec1-dt"][0] = tdt
        except Exception as ex:
            ex_ = ex
        
        try:
            for index, row in g.iterrows(): #   ...then foreach row in the group
                if ( not(math.isnan(row["elec_val"])) ):
                    temp_df.loc[0,"elec1-val"] = row["elec_val"] # ...extract the existing values (there will not be more than one, as none of the sensors update at sub-minute intervals)
                
                if ( not(math.isnan(row["wifi_val"])) ):
                    temp_df.loc[0,"wifi1-val"] = row["wifi_val"]
                
                if ( not(math.isnan(row["co2_val"])) ):
                    temp_df.loc[0,"co21-val"] = row["co2_val"]
           
            temp_df.to_csv("DataFiles\\WCEC_AllTestData_Horiz_01FEB2019_thru_10APR2019.csv", mode="a", header=False, index=False)
            temp_df.iloc[0,:] = [math.nan, math.nan, math.nan, math.nan, math.nan, math.nan]
        except Exception as ex:
            ex_ = ex

    x = "thisisastopgap"
    return


#ProcessAmbiDaqFile()
#MatchInputAmbiDaqTimestampsByMinute()
#temp_df = pd.read_csv("DataFiles\\WCEC_AllTestData_Horiz_01FEB2019_thru_10APR2019.csv", parse_dates=["wifi1-dt","co21-dt","elec1-dt"])  
#temp_df = temp_df.dropna()
#temp_df.to_csv("DataFiles\\WCEC_AllTestData_Horiz_nafree_01FEB2019_thru_10APR2019.csv", header=True, index=False)

client = pc.pi_client()
l, r = client.search_by_point("*roess*ahu*")
#l, r = client.search_by_point("*viridian2*")
points = l
data = client.get_stream_by_point(points, start="2018-06-01 10:00:00", end="2019-04-01 0:00:00", calculation="recorded")
data.to_csv("DataFiles\\WCEC_WifiData_real.csv", mode='a', index=False, header=False)

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