import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def GenerateConfusionMatrix(output,threshold=0.5):
    confmtx = pd.DataFrame(index=["predicted:non-vacant(0)","predicted:vacant(1)"],columns=["truth:non-vacant(0)","truth:vacant(1)"])
    ## Should we instead define 1 as non-vacant, since that is what we are actually testing for? Because it is easier to show occupied than it is to show vacant.
    # TODO: Need to create truth columns in this file instead of main.
    # Generate 1's and 0's based on threshold to represent vacant and non-vacant, respectively, for predicted values
    lout = len(output.index)
    output["predicteddt"] = output["overallprobadt"]
    output["predictedval"] = [0] * lout
    output.loc[ output["overallproba_rms"] >= threshold , "predictedval"] = 1  #...where 1 = vacant

    # add onto output a new column for each outcome: TP, TN, FP, FN. Populate each column with 1 when true
    # True positives (predicted non-vacant and is non-vacant), place at 0,0
    output["TP"] = [0] * lout
    TP_mask = ( (output["predictedval"]==0) & (output["truthval"]==0) )
    output.loc[output[TP_mask].index,["TP"]] = 1
    TPs = output["TP"].sum()
    confmtx.iloc[0,0] = TPs

    # True negatives (predicted vacant and is vacant), place at 1,1
    output["TN"] = [0] * lout
    TN_mask = ( (output["predictedval"]==1) & (output["truthval"]==1) )
    output.loc[output[TN_mask].index,["TN"]] = 1
    TNs = output["TN"].sum()
    confmtx.iloc[1,1] = TNs

    # False positives (predicted non-vacant and is vacant - missed opportunity), place at 0,1
    output["FP"] = [0] * lout
    FP_mask = ( (output["predictedval"]==0) & (output["truthval"]==1) )
    output.loc[output[FP_mask].index,["FP"]] = 1
    FPs = output["FP"].sum()
    confmtx.iloc[0,1] = FPs

    # False negatives (predicted vacant and is non-vacant - reduced service), place at 1,0
    output["FN"] = [0] * lout
    FN_mask = ( (output["predictedval"]==1) & (output["truthval"]==0) )
    output.loc[output[FN_mask].index,["FN"]] = 1
    FNs = output["FN"].sum()
    confmtx.iloc[1,0] = FNs

    #confmtx.to_csv("DataFiles\\VIE-confusion-matrix.csv")

    metrics = pd.DataFrame(index=[0],columns=["TPs","FPs","FNs","TNs"])
    metrics["TPs"] = TPs
    metrics["FPs"] = FPs
    metrics["FNs"] = FNs
    metrics["TNs"] = TNs

    return metrics, confmtx
    
def GenerateAccuracy(output, metrics):
    # keep in mind that this is a bad measure if one class occurs much more than the other, i.e. anything more disparate than 60/40 occurrences.
    # Check ratios: 
    vacant_cnt = output["truthval"].sum()
    nonvacant_cnt = len(output["truthval"]) - vacant_cnt
    ratio = vacant_cnt / nonvacant_cnt
    validity = False
    if ( (ratio < 0.6) & (ratio > 0.4) ):
        validity = True
    # Also keep in mind that these calculations do not work the same for irregularly timed data - need to weight by time period over which each data point was taken
    TPs = metrics["TPs"] 
    TNs = metrics["TNs"] 
    FPs = metrics["FPs"] 
    FNs = metrics["FNs"] 
    accuracy = (TPs + TNs)/(TPs + TNs + FPs + FNs)
    return accuracy, validity

def GenerateMetricsForAllThresholds(output):
    metrics_vthresh = pd.DataFrame(columns=["TPs","FPs","FNs","TNs"])
    thresholds = np.array(range(0,105,5))
    thresholds = thresholds / 100
    i = 0
    for threshold in thresholds:
        met_arr_tmp, cm = GenerateConfusionMatrix(output, threshold)
        metrics_vthresh.loc[i,"TPs"] = met_arr_tmp.loc[0,"TPs"]
        metrics_vthresh.loc[i,"FPs"] = met_arr_tmp.loc[0,"FPs"]
        metrics_vthresh.loc[i,"FNs"] = met_arr_tmp.loc[0,"FNs"]
        metrics_vthresh.loc[i,"TNs"] = met_arr_tmp.loc[0,"TNs"]
        i = i + 1
    return metrics_vthresh, thresholds

def GenerateROCcurve(metrics_vthresh):
    # for different thresholds from 0 -> 1, generate FPR and FNR and plot against eachother
    TPs = metrics_vthresh["TPs"] 
    TNs = metrics_vthresh["TNs"] 
    FPs = metrics_vthresh["FPs"] 
    FNs = metrics_vthresh["FNs"] 
    # Get false positive rate aka fall-out aka 
    FPR = FPs/(FPs + TNs)
    # Get false negative rate aka miss rate aka
    #FNR = FNs/(FNs + TPs)
    # Get true positive rate aka 
    TPR = TPs/(TPs + FNs)
    ROC, ax = plt.subplots(figsize=(10,5))
    ax.plot(FPR, TPR)
    ROC.savefig("Figures\\ROC-curve.png", format="png", bbox_inches="tight")
    return

def GenerateAUROCcurve():
    
    return

def GenerateAnalytics(outputcsvlocation):
    # import output file
    output = pd.read_csv(outputcsvlocation, parse_dates=["runtimedt","overallprobadt","wifidt","co2dt","elecdt","truthdt"])
    metrics, confmtx = GenerateConfusionMatrix(output) # for 0.5 threshold
    accuracy, validity = GenerateAccuracy(output, metrics) # for 0.5 threshold
    metrics_vthresh, thresholds = GenerateMetricsForAllThresholds(output)
    GenerateROCcurve(metrics_vthresh)
    return

#GenerateAnalytics("DataFiles\\VIE-output-historical.csv")
