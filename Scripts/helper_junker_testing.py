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

client = pc.pi_client()
l, r = client.search_by_point("ap*wickson*total*")
#print(l)
points = ["AP.WICKSON_Total_Count"]
data = client.get_stream_by_point(points, start="2018-01-01 12:00:00", end="*", calculation="recorded")

mask_occ = (((data.index.hour > 7) & (data.index.hour < 23 )) & (data.index.dayofweek < 5))
mask_vac = (((data.index.hour <= 7) | (data.index.hour >= 23 )) | (data.index.dayofweek >= 5))
data["vacant"] = 2
data.loc[data[mask_vac].index,["vacant"]] = 1
data.loc[data[mask_occ].index,["vacant"]] = 0

#histd = PrepForHist(data["elec"])



#Plot in histogram

thisisastop = 12