import pandas as pd
import numpy as np

histdata = pd.read_csv("DataFiles\\VIE-historical-input_WCEC.csv", parse_dates=["timestamp"])
data = histdata.loc[ :,["timestamp","truth-val"] ]
data.set_index(data["timestamp"], inplace=True)
mask_occ = (((data.index.hour >= 7) & (data.index.hour < 19 )) & (data.index.dayofweek < 5))
mask_vac = (((data.index.hour < 7) | (data.index.hour >= 19 )) | (data.index.dayofweek >= 5))
data["truth-val"] = 2
data.loc[data[mask_vac].index,["truth-val"]] = 1
data.loc[data[mask_occ].index,["truth-val"]] = 0
test = data.loc[ data["truth-val"] == 2 ]
data.set_index(histdata.index, inplace=True)
histdata["truth-val"] = data["truth-val"]

histdata.to_csv("DataFiles\\VIE-historical-input_WCEC.csv", header=True, index=False)
