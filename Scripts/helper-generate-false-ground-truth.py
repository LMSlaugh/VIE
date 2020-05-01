import pandas as pd
import numpy as np

def SimulateGroundTruth():
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

def CalculateLHR():
    #from hart et al, 2004
    # take mean of daily elec data
    # add 0.5 std dev for "high" occupancy threshold
    # subtract 0.5 std dev for "low" occupancy threshold
    # avg(highs)/avg(lows) - LHR

    return []

def SloanApproach():
    # See page 21 of Alex's thesis
    # for each measurement, average it with the seven previous to it
    # Choose the lowest of these per day, mark as vacant
    #One day is defined as noon - noon

    #Then calculate standard deviation of the 8 lowest data points from above, and figure out range of +/- 2 std devs

    #slice electricty data for vacant times, divide by all usage for metric.

    data = pd.read_csv("DataFiles\\VIE-historical-input_WCEC.csv", parse_dates=["timestamp"]) # columns: timestamp, {sensorname}-val, {sensorname}-val, ..., truth-val
    data.index = data["timestamp"]
    data = data.drop("timestamp")


    # need timestamp and whether alex's method predicts vacant or occupied.
    return []