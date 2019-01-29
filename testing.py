import pandas as pd
import numpy as np
import PI_client as pc
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

client = pc.pi_client()
points = ["AP.STUD-COMM-CTR_Total_Count", "SCC_Electricity_Demand_kBtu"]
data = client.get_stream_by_point(points,start="2018-09-27", end="2018-10-26 3:00:00", calculation="recorded")
data.columns = ["wifi","elec"]

mask_occ = (((data.index.hour > 7) & (data.index.hour < 23 )) & (data.index.dayofweek < 5))
mask_vac = (((data.index.hour <= 7) | (data.index.hour >= 23 )) | (data.index.dayofweek >= 5))
data["vacant"] = 2
data.loc[data[mask_vac].index,["vacant"]] = 1
data.loc[data[mask_occ].index,["vacant"]] = 0

#histd = PrepForHist(data["elec"])



#Plot in histogram

testd.head(20)


thisisastop = 12