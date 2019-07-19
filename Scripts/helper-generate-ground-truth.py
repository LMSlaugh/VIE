import pandas as pd
import numpy as np

histdata = pd.read_csv("DataFiles\\VIE-input-historical_WCEC.csv", parse_dates=["truth-dt"])
data = histdata.loc[ :,["truth-dt","truth-val"] ]
data.set_index(data["truth-dt"], inplace=True)
mask_occ = (((data.index.hour >= 9) & (data.index.hour < 17 )) & (data.index.dayofweek < 5))
mask_vac = (((data.index.hour < 9) | (data.index.hour >= 17 )) | (data.index.dayofweek >= 5))
data["truth-val"] = 2
data.loc[data[mask_vac].index,["truth-val"]] = 1
data.loc[data[mask_occ].index,["truth-val"]] = 0
test = data.loc[ data["truth-val"] == 2 ]
data.set_index(histdata.index, inplace=True)
histdata["truth-val"] = data["truth-val"]

histdata.to_csv("DataFiles\\VIE-input-historical_WCEC.csv", header=True, index=False)
