import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def GenerateConfusionMatrixNMetrics(data, params, threshold):
    datacop = data.copy()
    ind = ["predicted:Vacant(1)","predicted:Occupied(0)","-","True Vacancy Ratio","Optimum Cutoff","Accuracy: Overall","Accuracy: Vacant","Accuracy: Occupied","Complaint Rate","Missed Opportunity Rate"]
    col = ["truth:Vacant(1)","truth:Occupied(0)"]
    confmtx = pd.DataFrame(index=ind,columns=col)
    ## Should we instead define 1 as non-vacant, since that is what we are actually testing for? Because it is easier to show occupied than it is to show vacant.
    # Generate 1's and 0's based on threshold to represent vacant and non-vacant, respectively, for predicted values
    lout = len(data.index)
    data["predicteddt"] = data["fused-proba-dt"]
    data["predictedval"] = [0] * lout
    data.loc[ data["fused-proba-" + params.fusetype] >= threshold , "predictedval"] = 1  #...where 1 = vacant

    # add onto output a new column for each outcome: TP, TN, FP, FN. Populate each column with 1 when true
    # True positives (predicted vacant and is vacant), place at 0,0
    data["TP"] = [0] * lout
    TP_mask = ( (data["predictedval"]==1) & (data["truth-val"]==1) )
    data.loc[data[TP_mask].index,["TP"]] = 1
    TPs = data["TP"].sum()
    confmtx.iloc[0,0] = TPs

    # True negatives (predicted occupied and is occupied), place at 1,1
    data["TN"] = [0] * lout
    TN_mask = ( (data["predictedval"]==0) & (data["truth-val"]==0) )
    data.loc[data[TN_mask].index,["TN"]] = 1
    TNs = data["TN"].sum()
    confmtx.iloc[1,1] = TNs

    # False positives (predicted vacant and is occupied - reduced service), place at 0,1
    data["FP"] = [0] * lout
    FP_mask = ( (data["predictedval"]==1) & (data["truth-val"]==0) )
    data.loc[data[FP_mask].index,["FP"]] = 1
    FPs = data["FP"].sum()
    confmtx.iloc[0,1] = FPs

    # False negatives (predicted occupied and is vacant - missed opportunity), place at 1,0
    data["FN"] = [0] * lout
    FN_mask = ( (data["predictedval"]==0) & (data["truth-val"]==1) )
    data.loc[data[FN_mask].index,["FN"]] = 1
    FNs = data["FN"].sum()
    confmtx.iloc[1,0] = FNs


    metrics = pd.DataFrame(index=[0],columns=["TPs","FPs","FNs","TNs"])
    metrics["TPs"] = TPs
    metrics["FPs"] = FPs
    metrics["FNs"] = FNs
    metrics["TNs"] = TNs

    overacc, vacc, oacc, occ_vac_ratio, comp_rate, miss_opp_rate = GenerateKPIs(datacop, metrics)
    confmtx.iloc[3,0] = round(occ_vac_ratio,3)
    confmtx.iloc[4,0] = round(threshold,3)
    confmtx.iloc[5,0] = round(overacc,3)
    confmtx.iloc[6,0] = round(vacc,3)
    confmtx.iloc[7,0] = round(oacc,3)
    confmtx.iloc[8,0] = round(comp_rate,3)
    confmtx.iloc[9,0] = round(miss_opp_rate,3)
    confmtx.to_csv("DataFiles\\" + params.buildtype + "\\" + params.traintype + "\\" + params.fusetype + "\\VIE-confusion-matrix.csv")

    return metrics, confmtx
    
def GenerateKPIs(data, metrics):
    # keep in mind that this is a bad measure if one class occurs much more than the other, i.e. anything more disparate than 60/40 occurrences.
    # Check ratios: 
    vacant_cnt = data["truth-val"].sum()
    vac_ratio = vacant_cnt / len(data["truth-val"]) # Prevalence
    
    # Also keep in mind that these calculations do not work the same for irregularly timed data - need to weight by time period over which each data point was taken
    TPs = metrics["TPs"] 
    TNs = metrics["TNs"] 
    FPs = metrics["FPs"] 
    FNs = metrics["FNs"] 
    overall_acc = (TPs + TNs)/(TPs + TNs + FPs + FNs)
    overall_acc = overall_acc[0]
    vacant_acc = TPs/(TPs + FNs) # True Positive Rate
    vacant_acc = vacant_acc[0]
    occupied_acc = TNs/(FPs + TNs) # True Negative Rate
    occupied_acc = occupied_acc[0]
    comp_rate = FPs/(FPs + FNs + TPs + TNs)
    comp_rate = comp_rate[0]
    miss_opp_rate = FNs/(FPs + FNs + TPs + TNs)
    miss_opp_rate = miss_opp_rate[0]
    return overall_acc, vacant_acc, occupied_acc, vac_ratio, comp_rate, miss_opp_rate

def GenerateMetricsForAllThresholds(data, params):
    metrics_vthresh = pd.DataFrame(columns=["TPs","FPs","FNs","TNs"])
    thresholds = np.array(range(0,1001,1))
    thresholds = thresholds/1000
    i = 0
    for threshold in thresholds:
        met_arr_tmp, cm = GenerateConfusionMatrixNMetrics(data, params, threshold)
        metrics_vthresh.loc[i,"TPs"] = met_arr_tmp.loc[0,"TPs"]
        metrics_vthresh.loc[i,"FPs"] = met_arr_tmp.loc[0,"FPs"]
        metrics_vthresh.loc[i,"FNs"] = met_arr_tmp.loc[0,"FNs"]
        metrics_vthresh.loc[i,"TNs"] = met_arr_tmp.loc[0,"TNs"]
        i = i + 1
    return metrics_vthresh, thresholds

def GenerateAccuracyCurves(metrics_vthresh, thresh, params):
    # for different thresholds from 0 -> 1....
    TPs = metrics_vthresh["TPs"] 
    TNs = metrics_vthresh["TNs"] 
    FPs = metrics_vthresh["FPs"] 
    FNs = metrics_vthresh["FNs"] 
    # get False Positive Rate/Fall-Out/1-Sensitivity
    #FPRs = FPs/(FPs + TNs)
    # get True Positive Rate/Sensitivity/Recall
    #TPRs = TPs/(TPs + FNs)
    # get False Negative Rate
    #FNRs = FNs/(TPs + FNs)

    # Get complaint rate and plot against thresholds
    CR = FPs/(FPs + FNs + TPs + TNs)
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(thresh, CR)
    #ax.set_ylim([0,1.1])
    #ax.set_xlim([0,1.0])
    ax.set_title("Complaint Rate for different thresholds", fontsize=18, fontweight="bold")
    #ax.set_ylabel("True Positive Rate: TP/(TP + FN)", fontsize=9)
    ax.set_ylabel("Complaint Rate: FP/(TP + TN + FN + FP) (%)", fontsize=9)
    ax.set_xlabel("Threshold for Vacancy/Occupancy Determination (%)", fontsize=9)
    fig.savefig("Figures\\" + params.buildtype + "\\" + params.traintype + "\\" + params.fusetype + "\\Complaint-Rate.png", format="png", bbox_inches="tight")
    plt.close(fig)

    # Get missed opportunity rate and plot against thresholds
    MOR = FNs/(FPs + FNs + TPs + TNs)
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(thresh, MOR)
    #ax.set_ylim([0,1.1])
    #ax.set_xlim([0,1.0])
    ax.set_title("Missed Opportunity Rate for different thresholds", fontsize=18, fontweight="bold")
    ax.set_ylabel("Missed Opportunity Rate: FN/(TP + TN + FN + FP) (%)", fontsize=9)
    ax.set_xlabel("Threshold for Vacancy/Occupancy Determination (%)", fontsize=9)
    fig.savefig("Figures\\" + params.buildtype + "\\" + params.traintype + "\\" + params.fusetype + "\\Missed-Opportunity-Rate.png", format="png", bbox_inches="tight")
    plt.close(fig)

    # Plot missed opportunity rate and complaint rate against eachother
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(MOR, CR)
    #ax.set_ylim([0,1.1])
    #ax.set_xlim([0,1.1])
    ax.set_title("Missed Opportunity Rate vs. Complaint Rate for different thresholds", fontsize=18, fontweight="bold")
    ax.set_xlabel("Missed Opportunity Rate: FN/(TP + TN + FN + FP) (%)", fontsize=9)
    ax.set_ylabel("Complaint Rate: FP/(TP + TN + FN + FP) (%)", fontsize=9)
    fig.savefig("Figures\\" + params.buildtype + "\\" + params.traintype + "\\" + params.fusetype + "\\Complaint-Missed-Opp-Rate-Comp.png", format="png", bbox_inches="tight")
    plt.close(fig)

    # Get overall accuracy and plot against thresholds
    overall_acc = (TPs + TNs)/(TPs + TNs + FPs + FNs)
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(thresh, overall_acc)
    #ax.set_ylim([0,1.1])
    #ax.set_xlim([0,1.0])
    ax.set_title("Overall Accuracy for different thresholds", fontsize=18, fontweight="bold")
    ax.set_ylabel("Overall Accuracy: (TP + TN)/(TP + TN + FN + FP) (%)", fontsize=9)
    ax.set_xlabel("Threshold for Vacancy/Occupancy Determination (%)", fontsize=9)
    fig.savefig("Figures\\" + params.buildtype + "\\" + params.traintype + "\\" + params.fusetype + "\\Overall-Accuracy-Rate.png", format="png", bbox_inches="tight")
    plt.close(fig)

    # Get accuracy of vacancy and plot against thresholds
    vacant_acc = TPs/(TPs + FNs) # True Positive Rate
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(thresh, vacant_acc)
    #ax.set_ylim([0,1.1])
    #ax.set_xlim([0,1.0])
    ax.set_title("Vacancy Detection Accuracy for different thresholds", fontsize=18, fontweight="bold")
    ax.set_ylabel("Accuracy of Detecting \"Vacant\": TP/(TP + FN) (%)", fontsize=9)
    ax.set_xlabel("Threshold for Vacancy/Occupancy Determination (%)", fontsize=9)
    fig.savefig("Figures\\" + params.buildtype + "\\" + params.traintype + "\\" + params.fusetype + "\\Vacant-Accuracy-Rate.png", format="png", bbox_inches="tight")
    plt.close(fig)

    # Get accuracy of occupancy and plot against thrsholds
    occupied_acc = TNs/(FPs + TNs) # True Negative Rate
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(thresh, occupied_acc)
    #ax.set_ylim([0,1.1])
    #ax.set_xlim([0,1.0])
    ax.set_title("Occupancy Detection Accuracy for different thresholds", fontsize=18, fontweight="bold")
    ax.set_ylabel("Accuracy of Detecting \"Occupied\": TN/(TN + FP) (%)", fontsize=9)
    ax.set_xlabel("Threshold for Vacancy/Occupancy Determination (%)", fontsize=9)
    fig.savefig("Figures\\" + params.buildtype + "\\" + params.traintype + "\\" + params.fusetype + "\\Occupied-Accuracy-Rate.png", format="png", bbox_inches="tight")
    plt.close(fig)

    # Plot vac_acc and occ_acc against eachother
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(occupied_acc, vacant_acc)
    #ax.set_ylim([0,1.1])
    #ax.set_xlim([0,1.1])
    ax.set_title("Vacancy Detection Accuracy vs. Occupancy Detection Accuracy for different thresholds", fontsize=18, fontweight="bold")
    ax.set_ylabel("Accuracy of Detecting \"Vacant\": TP/(TP + FN) (%)", fontsize=9)
    ax.set_xlabel("Accuracy of Detecting \"Occupied\": TN/(TN + FP) (%)", fontsize=9)
    fig.savefig("Figures\\" + params.buildtype + "\\" + params.traintype + "\\" + params.fusetype + "\\Occupied-Vacant-Acc-Rate-Comp.png", format="png", bbox_inches="tight")
    plt.close(fig)
    return

def GetOptimalThreshold(metrics_vthresh, thresholds, params):
    #CR = FPs/(FPs + FNs + TPs + TNs)
    #MOR = FNs/(FPs + FNs + TPs + TNs)

    opt_tab = pd.DataFrame(index=range(len(thresholds)), columns=["thresholds", "TP", "TN", "FP", "FN", "CR", "MOR", "dist to 0,0"])
    opt_tab["thresholds"] = thresholds
    opt_tab["TP"] = metrics_vthresh["TPs"] 
    opt_tab["TN"] = metrics_vthresh["TNs"] 
    opt_tab["FP"] = metrics_vthresh["FPs"] 
    opt_tab["FN"] = metrics_vthresh["FNs"]
    total = opt_tab["FP"] + opt_tab["FN"] + opt_tab["TP"] + opt_tab["TN"]
    opt_tab["CR"] = opt_tab["FP"]/total
    opt_tab["MOR"] = opt_tab["FN"]/total
    #opt_tab["CR"] = CR.values
    #opt_tab["MOR"] = MOR.values
    opt_tab["dist to 0,0"] = (opt_tab["CR"] ** 2 + opt_tab["MOR"] ** 2) ** 0.5
    opt_tab.to_csv("DataFiles\\" + params.buildtype + "\\" + params.traintype + "\\" + params.fusetype + "\\optimization_table.csv")
    dat = opt_tab["dist to 0,0"]
    metric_min = min(dat)
    opt_mask = opt_tab["dist to 0,0"]==metric_min
    optimal_threshold = opt_tab.loc[opt_tab[opt_mask].index, ["thresholds"]]
    return optimal_threshold.iloc[0,0]

def GenerateAnalytics(params):
    outputcsvlocation = "DataFiles\\" + params.buildtype + "\\" + params.traintype + "\\" + params.fusetype + "\\VIE-historical-output.csv"
    output = pd.read_csv(outputcsvlocation, parse_dates=["fused-proba-dt"])
    metrics_vthresh, thresholds = GenerateMetricsForAllThresholds(output.copy(), params)
    GenerateAccuracyCurves(metrics_vthresh, thresholds, params)
    opt_thresh = GetOptimalThreshold(metrics_vthresh, thresholds, params)
    metrics, confmtx = GenerateConfusionMatrixNMetrics(output.copy(), params, threshold=opt_thresh)

    # TODO generate confusion matrix @ optimal threshold for intermediates
    return
