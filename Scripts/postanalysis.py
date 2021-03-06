# Author: Lisa Slaughter <lisa.m.slaughter@gmail.com>
# Last update: May 02, 2019

# This code runs the following analyses to evaluate model performance:
#     Receiver-Operating Characteristic curve (plot) and the area underneath it
#     COR-MOR Characteristic curve (plot) and the area underneath it 
#     Accuracy of "vacant" prediction for all cutoff values (plot)
#     Accuracy of "occupied" prediction for all cutoff values (plot)
#     Accuracy of the all predictions for all cutoff values (plot)
# Additionally, the optimal cutoff value is calculated.
# ----------------------------------------------------------------------------------------------------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

titlesz = 14
ticksz = 9
labs = 10
legs = 11

def GenerateConfusionMatrixNMetrics(data, params, threshold, sufx):
    # Calculate number of true positives, true negatives, false positives, and false negatives for a given cutoff (threshold).
    datacop = data.copy()
    ind = ["predicted:Vacant(1)","predicted:Occupied(0)","-","True Vacancy Ratio","Optimum Cutoff","Accuracy: Overall","Accuracy: Vacant","Accuracy: Occupied","Complaint Opportunity Rate","Missed Opportunity Rate"]
    col = ["truth:Vacant(1)","truth:Occupied(0)"]
    confmtx = pd.DataFrame(index=ind,columns=col)

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
    confmtx.iloc[3,0] = str(round(occ_vac_ratio,3)*100) + "%"
    confmtx.iloc[4,0] = str(round(threshold,3)*100) + "%"
    confmtx.iloc[5,0] = str(round(overacc,3)*100) + "%"
    confmtx.iloc[6,0] = str(round(vacc,3)*100) + "%"
    confmtx.iloc[7,0] = str(round(oacc,3)*100) + "%"
    confmtx.iloc[8,0] = str(round(comp_rate,3)*100) + "%"
    confmtx.iloc[9,0] = str(round(miss_opp_rate,3)*100) + "%"
    #confmtx.to_csv("DataFiles\\" + params.buildtype + "\\" + params.traintype + "\\" + params.fusetype + "\\VIE-confusion-matrix" + sufx + ".csv")
    #data.to_csv("DataFiles\\" + params.buildtype + "\\" + params.traintype + "\\" + params.fusetype + "\\conf_matrix_one_thresh-" + str(threshold) + ".csv")

    return metrics, confmtx
    
def GenerateKPIs(data, metrics):
    # Calculate model performance evaluation metrics
    # Note: This is a bad measure if one class occurs much more than the other, i.e. anything more disparate than 60/40 occurrences. Hence, check ratios: 
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
    # Varies the cutoff threshold from 0 to 100 percent, generating the four confusion matrix metrics each time
    metrics_vthresh = pd.DataFrame(columns=["TPs","FPs","FNs","TNs"])
    thresholds = np.array(range(0,1001,1))
    thresholds = thresholds/1000
    i = 0
    for threshold in thresholds:
        met_arr_tmp, cm = GenerateConfusionMatrixNMetrics(data, params, threshold, "")
        metrics_vthresh.loc[i,"TPs"] = met_arr_tmp.loc[0,"TPs"]
        metrics_vthresh.loc[i,"FPs"] = met_arr_tmp.loc[0,"FPs"]
        metrics_vthresh.loc[i,"FNs"] = met_arr_tmp.loc[0,"FNs"]
        metrics_vthresh.loc[i,"TNs"] = met_arr_tmp.loc[0,"TNs"]
        i = i + 1
    return metrics_vthresh, thresholds

def GenerateAccuracyCurves(metrics_vthresh, thresh, params):
    # Uses confusion matrix metrics to calculate values for the diagnostic curves.
    fusestr = ""
    if params.fusetype == "SM":
        fusestr = "Simple Mean"
    elif params.fusetype == "SDWM":
        fusestr = "Standard Deviation Weighted Mean"
    elif params.fusetype == "HM":
        fusestr = "Harmonic Mean"
    elif params.fusetype == "RMS":
        fusestr = "Root Mean Square"
    elif params.fusetype == "SDWRMS":
        fusestr = "Std. Dev. Weighted Root Mean Square"

    # for Different Thresholds from 0 -> 1....
    TPs = metrics_vthresh["TPs"] 
    TNs = metrics_vthresh["TNs"] 
    FPs = metrics_vthresh["FPs"] 
    FNs = metrics_vthresh["FNs"] 

    # Get complaint opportunity fraction and plot against thresholds
    COF = FPs/(FPs + FNs + TPs + TNs)
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(thresh, COF)
    ax.minorticks_on()
    ax.xaxis.set_tick_params(labelsize=ticksz)
    ax.yaxis.set_tick_params(labelsize=ticksz)
    ax.grid(b=True, which='major', color='#666666', linestyle='-', linewidth=1, alpha=0.7)
    ax.grid(b=True, which='minor', color='#999999', linestyle='-', linewidth=1, alpha=0.2)
    ax.set_title("COF vs. Threshold for " + fusestr, fontsize=titlesz, fontweight="bold")
    ax.set_ylabel("Complaint Opportunity Fraction: FP/(TP + TN + FN + FP) (%)", fontsize=9)
    ax.set_xlabel("Threshold for Vacancy/Occupancy Determination (%)", fontsize=labs)
    fig.savefig("Figures\\" + params.buildtype + "\\" + params.traintype + "\\" + params.fusetype + "\\COF.png", format="png", bbox_inches="tight")
    plt.close(fig)

    # Get complaint opportunity rate and plot against thresholds
    COR = FPs/(FPs + TNs)
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(thresh, COR)
    ax.minorticks_on()
    ax.xaxis.set_tick_params(labelsize=ticksz)
    ax.yaxis.set_tick_params(labelsize=ticksz)
    ax.grid(b=True, which='major', color='#666666', linestyle='-', linewidth=1, alpha=0.7)
    ax.grid(b=True, which='minor', color='#999999', linestyle='-', linewidth=1, alpha=0.2)
    ax.set_title("COR vs. Threshold for " + fusestr, fontsize=titlesz, fontweight="bold")
    ax.set_ylabel("Complaint Opportunity Rate: FP/(FP + TN) (%)", fontsize=labs)
    ax.set_xlabel("Threshold for Vacancy/Occupancy Determination (%)", fontsize=labs)
    fig.savefig("Figures\\" + params.buildtype + "\\" + params.traintype + "\\" + params.fusetype + "\\COR.png", format="png", bbox_inches="tight")
    plt.close(fig)

    # Get missed opportunity fraction and plot against thresholds
    MOF = FNs/(FPs + FNs + TPs + TNs)
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(thresh, MOF)
    ax.minorticks_on()
    ax.xaxis.set_tick_params(labelsize=ticksz)
    ax.yaxis.set_tick_params(labelsize=ticksz)
    ax.grid(b=True, which='major', color='#666666', linestyle='-', linewidth=1, alpha=0.7)
    ax.grid(b=True, which='minor', color='#999999', linestyle='-', linewidth=1, alpha=0.2)
    ax.set_title("MOF vs. Threshold for " + fusestr, fontsize=titlesz, fontweight="bold")
    ax.set_ylabel("Missed Opportunity Fraction: FN/(TP + TN + FN + FP) (%)", fontsize=labs)
    ax.set_xlabel("Threshold for Vacancy/Occupancy Determination (%)", fontsize=labs)
    fig.savefig("Figures\\" + params.buildtype + "\\" + params.traintype + "\\" + params.fusetype + "\\MOF.png", format="png", bbox_inches="tight")
    plt.close(fig)

    # Get missed opportunity rate and plot against thresholds
    MOR = FNs/(FNs + TPs)
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(thresh, MOR)
    ax.minorticks_on()
    ax.xaxis.set_tick_params(labelsize=ticksz)
    ax.yaxis.set_tick_params(labelsize=ticksz)
    ax.grid(b=True, which='major', color='#666666', linestyle='-', linewidth=1, alpha=0.7)
    ax.grid(b=True, which='minor', color='#999999', linestyle='-', linewidth=1, alpha=0.2)
    ax.set_title("MOR vs. Threshold for " + fusestr, fontsize=titlesz, fontweight="bold")
    ax.set_ylabel("Missed Opportunity Rate: FN/(TP + FN) (%)", fontsize=labs)
    ax.set_xlabel("Threshold for Vacancy/Occupancy Determination (%)", fontsize=labs)
    fig.savefig("Figures\\" + params.buildtype + "\\" + params.traintype + "\\" + params.fusetype + "\\MOR.png", format="png", bbox_inches="tight")
    plt.close(fig)

    # Plot missed opportunity rate and complaint opportunity rate against eachother
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(MOR, COR)
    n = round(len(thresh)-1, 0)
    step = int(round(n/10, 0))
    callout_locs = range(0,n+1,step)
    for val in callout_locs:
        if val==0:
            ax.plot(MOR.values[val], COR.values[val], 'xk', label="Decision Thresholds")
        else:
            ax.plot(MOR.values[val], COR.values[val], 'xk')
        ax.text(MOR.values[val]+.05,COR.values[val]+.004, str(round(val/10)) + "%", horizontalalignment='right', verticalalignment='bottom')
    ax.legend(loc="upper right", fontsize="medium")
    ax.minorticks_on()
    ax.xaxis.set_tick_params(labelsize=ticksz)
    ax.yaxis.set_tick_params(labelsize=ticksz)
    ax.grid(b=True, which='major', color='#666666', linestyle='-', linewidth=1, alpha=0.7)
    ax.grid(b=True, which='minor', color='#999999', linestyle='-', linewidth=1, alpha=0.2)
    ax.set_title("CMC Curve for " + fusestr, fontsize=titlesz, fontweight="bold")
    ax.set_xlabel("Missed Opportunity Rate: FN/(TP + FN) (%)", fontsize=labs)
    ax.set_ylabel("Complaint Opportunity Rate: FP/(FP + TN) (%)", fontsize=labs)
    fig.savefig("Figures\\" + params.buildtype + "\\" + params.traintype + "\\" + params.fusetype + "\\CMC.png", format="png", bbox_inches="tight")
    plt.close(fig)

    # Plot (complaint opportunity rate) / (missed opportunity rate) against threshold ZOOMED <= 1 ONLY
    fig, ax = plt.subplots(figsize=(10,5))
    ratio = COR/MOR
    zmask_1 = ratio<=1

    ax.plot(thresh[zmask_1], ratio[zmask_1])
    ax.set_title("COR/MOR < 1 vs. Threshold", fontsize=12)
    ax.set_xlabel("Threshold for Vacancy/Occupancy Determination (%)", fontsize=labs)
    ax.xaxis.set_tick_params(labelsize=ticksz)
    ax.yaxis.set_tick_params(labelsize=ticksz)
    ax.grid(b=True, which='major', color='#666666', linestyle='-', linewidth=1, alpha=0.7)
    ax.grid(b=True, which='minor', color='#999999', linestyle='-', linewidth=1, alpha=0.2)
    ax.minorticks_on()
    plt.grid(b=True, which='major', color='#666666', linestyle='-', linewidth=1, alpha=0.7)
    plt.grid(b=True, which='minor', color='#999999', linestyle='-', linewidth=1, alpha=0.2)
    fig.savefig("Figures\\" + params.buildtype + "\\" + params.traintype + "\\" + params.fusetype + "\\COR-MOR-Ratio-under-1.png", format="png", bbox_inches="tight")
    plt.close(fig)

    # Plot (complaint opportunity rate) / (missed opportunity rate) against threshold ZOOMED <= 100
    fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(16,8))
    ratio = COR/MOR
    zmask_100 = ratio<=100
    zmask_20 = ratio<=20
    zmask_5 = ratio<=5
    zmask_1 = ratio<=1
    ax[0,0].plot(thresh[zmask_100], ratio[zmask_100])
    ax[0,0].set_title("COR/MOR < 100 vs. Threshold", fontsize=12)
    ax[0,0].set_ylabel("COR/MOR: FP/FN", fontsize=labs)
    ax[0,0].xaxis.set_tick_params(labelsize=ticksz)
    ax[0,0].yaxis.set_tick_params(labelsize=ticksz)
    ax[0,0].grid(b=True, which='major', color='#666666', linestyle='-', linewidth=1, alpha=0.7)
    ax[0,0].grid(b=True, which='minor', color='#999999', linestyle='-', linewidth=1, alpha=0.2)
    ax[0,0].minorticks_on()

    ax[1,0].plot(thresh[zmask_20], ratio[zmask_20])
    ax[1,0].set_title("COR/MOR < 20 vs. Threshold", fontsize=12)
    ax[1,0].set_ylabel("COR/MOR: FP/FN", fontsize=labs)
    ax[1,0].set_xlabel("Threshold for Vacancy/Occupancy Determination (%)", fontsize=labs)
    ax[1,0].xaxis.set_tick_params(labelsize=ticksz)
    ax[1,0].yaxis.set_tick_params(labelsize=ticksz)
    ax[1,0].grid(b=True, which='major', color='#666666', linestyle='-', linewidth=1, alpha=0.7)
    ax[1,0].grid(b=True, which='minor', color='#999999', linestyle='-', linewidth=1, alpha=0.2)
    ax[1,0].minorticks_on()

    ax[0,1].plot(thresh[zmask_5], ratio[zmask_5])
    ax[0,1].set_title("COR/MOR < 5 vs. Threshold", fontsize=12)
    ax[0,1].xaxis.set_tick_params(labelsize=ticksz)
    ax[0,1].yaxis.set_tick_params(labelsize=ticksz)
    ax[0,1].grid(b=True, which='major', color='#666666', linestyle='-', linewidth=1, alpha=0.7)
    ax[0,1].grid(b=True, which='minor', color='#999999', linestyle='-', linewidth=1, alpha=0.2)
    ax[0,1].minorticks_on()

    ax[1,1].plot(thresh[zmask_1], ratio[zmask_1])
    ax[1,1].set_title("COR/MOR < 1 vs. Threshold", fontsize=12)
    ax[1,1].set_xlabel("Threshold for Vacancy/Occupancy Determination (%)", fontsize=labs)
    ax[1,1].xaxis.set_tick_params(labelsize=ticksz)
    ax[1,1].yaxis.set_tick_params(labelsize=ticksz)
    ax[1,1].grid(b=True, which='major', color='#666666', linestyle='-', linewidth=1, alpha=0.7)
    ax[1,1].grid(b=True, which='minor', color='#999999', linestyle='-', linewidth=1, alpha=0.2)
    ax[1,1].minorticks_on()

    plt.grid(b=True, which='major', color='#666666', linestyle='-', linewidth=1, alpha=0.7)
    plt.grid(b=True, which='minor', color='#999999', linestyle='-', linewidth=1, alpha=0.2)
    plt.suptitle("COR/MOR vs. Threshold for " + fusestr, fontsize=titlesz, fontweight="bold")
    fig.savefig("Figures\\" + params.buildtype + "\\" + params.traintype + "\\" + params.fusetype + "\\COR-MOR-Ratio.png", format="png", bbox_inches="tight")
    plt.close(fig)

    # Plot missed opportunity fraction and complaint opportunity rate against eachother
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(MOF, COR)
    n = round(len(thresh)-1, 0)
    step = int(round(n/10, 0))
    callout_locs = range(0,n+1,step)
    for val in callout_locs:
        if val==0:
            ax.plot(MOF.values[val], COR.values[val], 'xk', label="Decision Thresholds")
        else:
            ax.plot(MOF.values[val], COR.values[val], 'xk')
        ax.text(MOF.values[val]+.03,COR.values[val]+.004, str(round(val/10)) + "%", horizontalalignment='right', verticalalignment='bottom')
    ax.legend(loc="upper right", fontsize="medium")
    ax.minorticks_on()
    ax.xaxis.set_tick_params(labelsize=ticksz)
    ax.yaxis.set_tick_params(labelsize=ticksz)
    ax.grid(b=True, which='major', color='#666666', linestyle='-', linewidth=1, alpha=0.7)
    ax.grid(b=True, which='minor', color='#999999', linestyle='-', linewidth=1, alpha=0.2)
    ax.set_title("COR vs. MOF by Threshold for " + fusestr, fontsize=titlesz, fontweight="bold")
    ax.set_xlabel("Missed Opportunity Fraction: FN/(TP + FP + FN + TN) (%)", fontsize=labs)
    ax.set_ylabel("Complaint Opportunity Rate: FP/(FP + TN) (%)", fontsize=labs)
    fig.savefig("Figures\\" + params.buildtype + "\\" + params.traintype + "\\" + params.fusetype + "\\COR-MOF-Comp.png", format="png", bbox_inches="tight")
    plt.close(fig)

    # Plot (complaint opportunity fraction) / (missed opportunity rate) against threshold
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(thresh, COF/MOR)
    ax.minorticks_on()
    ax.xaxis.set_tick_params(labelsize=ticksz)
    ax.yaxis.set_tick_params(labelsize=ticksz)
    ax.grid(b=True, which='major', color='#666666', linestyle='-', linewidth=1, alpha=0.7)
    ax.grid(b=True, which='minor', color='#999999', linestyle='-', linewidth=1, alpha=0.2)
    ax.set_title("COF/MOR vs. Threshold for " + fusestr, fontsize=titlesz, fontweight="bold")
    ax.set_ylabel("COF/MOR: FP(TP + FN)/FN(TP + TN + FN + FP)", fontsize=labs)
    ax.set_xlabel("Threshold for Vacancy/Occupancy Determination (%)", fontsize=labs)
    fig.savefig("Figures\\" + params.buildtype + "\\" + params.traintype + "\\" + params.fusetype + "\\COF-MOR-Ratio.png", format="png", bbox_inches="tight")
    plt.close(fig)

    # Get overall accuracy and plot against thresholds
    overall_acc = (TPs + TNs)/(TPs + TNs + FPs + FNs)
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(thresh, overall_acc)
    ax.minorticks_on()
    ax.xaxis.set_tick_params(labelsize=ticksz)
    ax.yaxis.set_tick_params(labelsize=ticksz)
    ax.grid(b=True, which='major', color='#666666', linestyle='-', linewidth=1, alpha=0.7)
    ax.grid(b=True, which='minor', color='#999999', linestyle='-', linewidth=1, alpha=0.2)
    ax.set_title("Overall Accuracy by Threshold for " + fusestr, fontsize=titlesz, fontweight="bold")
    ax.set_ylabel("Overall Accuracy: (TP + TN)/(TP + TN + FN + FP) (%)", fontsize=labs)
    ax.set_xlabel("Threshold for Vacancy/Occupancy Determination (%)", fontsize=labs)
    fig.savefig("Figures\\" + params.buildtype + "\\" + params.traintype + "\\" + params.fusetype + "\\OverAcc.png", format="png", bbox_inches="tight")
    plt.close(fig)

    # Get vacancy detection accuracy and plot against thresholds
    vacant_acc = TPs/(TPs + FNs) # True Positive Rate
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(thresh, vacant_acc)
    ax.minorticks_on()
    ax.xaxis.set_tick_params(labelsize=ticksz)
    ax.yaxis.set_tick_params(labelsize=ticksz)
    ax.grid(b=True, which='major', color='#666666', linestyle='-', linewidth=1, alpha=0.7)
    ax.grid(b=True, which='minor', color='#999999', linestyle='-', linewidth=1, alpha=0.2)
    ax.set_title("VDA by Threshold  for " + fusestr, fontsize=titlesz, fontweight="bold")
    ax.set_ylabel("Vacancy Detection Accuracy: TP/(TP + FN) (%)", fontsize=labs)
    ax.set_xlabel("Threshold for Vacancy/Occupancy Determination (%)", fontsize=labs)
    fig.savefig("Figures\\" + params.buildtype + "\\" + params.traintype + "\\" + params.fusetype + "\\VDA.png", format="png", bbox_inches="tight")
    plt.close(fig)

    # Get occupancy detection accuracy and plot against thresholds
    occupied_acc = TNs/(FPs + TNs) # True Negative Rate
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(thresh, occupied_acc)
    ax.minorticks_on()
    ax.xaxis.set_tick_params(labelsize=ticksz)
    ax.yaxis.set_tick_params(labelsize=ticksz)
    ax.grid(b=True, which='major', color='#666666', linestyle='-', linewidth=1, alpha=0.7)
    ax.grid(b=True, which='minor', color='#999999', linestyle='-', linewidth=1, alpha=0.2)
    ax.set_title("ODA by Threshold for " + fusestr, fontsize=titlesz, fontweight="bold")
    ax.set_ylabel("Occupancy Detection Accuracy: TN/(TN + FP) (%)", fontsize=labs)
    ax.set_xlabel("Threshold for Vacancy/Occupancy Determination (%)", fontsize=labs)
    fig.savefig("Figures\\" + params.buildtype + "\\" + params.traintype + "\\" + params.fusetype + "\\ODA.png", format="png", bbox_inches="tight")
    plt.close(fig)

    # Plot VDA and ODA against eachother
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(occupied_acc, vacant_acc)
    n = round(len(thresh)-1, 0)
    step = int(round(n/10, 0))
    callout_locs = range(0,n+1,step)
    for val in callout_locs:
        if val==0:
            ax.plot(occupied_acc.values[val], vacant_acc.values[val], 'xk', label="Decision Thresholds")
        else:
            ax.plot(occupied_acc.values[val], vacant_acc.values[val], 'xk')
        ax.text(occupied_acc.values[val]+.005,vacant_acc.values[val]-.05, str(round(val/10)) + "%", horizontalalignment='right', verticalalignment='bottom')
    ax.legend(loc="lower left", fontsize="medium")
    ax.minorticks_on()
    ax.xaxis.set_tick_params(labelsize=ticksz)
    ax.yaxis.set_tick_params(labelsize=ticksz)
    ax.grid(b=True, which='major', color='#666666', linestyle='-', linewidth=1, alpha=0.7)
    ax.grid(b=True, which='minor', color='#999999', linestyle='-', linewidth=1, alpha=0.2)
    ax.set_title("VDA vs. ODA by Threshold for " + fusestr, fontsize=titlesz, fontweight="bold")
    ax.set_ylabel("Vacancy Detection Accuracy: TP/(TP + FN) (%)", fontsize=labs)
    ax.set_xlabel("Occupancy Detection Accuracy: TN/(TN + FP) (%)", fontsize=labs)
    fig.savefig("Figures\\" + params.buildtype + "\\" + params.traintype + "\\" + params.fusetype + "\\ODA-VDA-Comp.png", format="png", bbox_inches="tight")
    plt.close(fig)

    # Generate ROC curve
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(COR, vacant_acc)
    n = round(len(COR)-1, 0)
    step = int(round(n/10, 0))
    callout_locs = range(0,n+1,step)
    for val in callout_locs:
        if val==0:
            ax.plot(COR.values[val], vacant_acc.values[val], 'xk', label="Decision Thresholds")
        else:
            ax.plot(COR.values[val], vacant_acc.values[val], 'xk')
        ax.text(COR.values[val]+.05,vacant_acc.values[val]-.05, str(round(val/10)) + "%", horizontalalignment='right', verticalalignment='bottom')
    ax.legend(loc="lower right", fontsize="medium")
    ax.minorticks_on()
    ax.xaxis.set_tick_params(labelsize=ticksz)
    ax.yaxis.set_tick_params(labelsize=ticksz)
    ax.grid(b=True, which='major', color='#666666', linestyle='-', linewidth=1, alpha=0.7)
    ax.grid(b=True, which='minor', color='#999999', linestyle='-', linewidth=1, alpha=0.2)
    ax.set_title("ROC Curve for " + fusestr, fontsize=titlesz, fontweight="bold")
    ax.set_ylabel("Vacancy Detection Accuracy: TP/(TP + FN) (%)", fontsize=labs)
    ax.set_xlabel("Complaint Opportunity Rate: FP/(TN + FP) (%)", fontsize=labs)
    fig.savefig("Figures\\" + params.buildtype + "\\" + params.traintype + "\\" + params.fusetype + "\\ROC.png", format="png", bbox_inches="tight")
    plt.close(fig)
    return

def GetOptimalValues(metrics_vthresh, thresholds, params):
    # Calculates the optimal value for cutoff threshold by minimizing distance to "perfect" (i.e. (0,1) for ROC; (0,0)for COR-MOR) 
    opt_tab = pd.DataFrame(index=range(len(thresholds)), columns=["thresholds", "TP", "TN", "FP", "FN", "VDA", "ODA", "COF", "COR", "MOF", "MOR", "COR/MOR", "COR/MOF", "MCC", "dist 0,0: COR-MOR", "dist 0,0: COR-MOF", "dist 0,1: ROC", "AUCOR-MOR", "AUROCC"])
    opt_tab["thresholds"] = thresholds
    opt_tab["TP"] = metrics_vthresh["TPs"] 
    opt_tab["TN"] = metrics_vthresh["TNs"] 
    opt_tab["FP"] = metrics_vthresh["FPs"] 
    opt_tab["FN"] = metrics_vthresh["FNs"]
    
    total = opt_tab["FP"] + opt_tab["FN"] + opt_tab["TP"] + opt_tab["TN"]
    opt_tab["VDA"] = opt_tab["TP"]/(opt_tab["FN"] + opt_tab["TP"])
    opt_tab["ODA"] = opt_tab["TN"]/(opt_tab["TN"] + opt_tab["FP"])
    opt_tab["COF"] = opt_tab["FP"]/total
    opt_tab["COR"] = opt_tab["FP"]/(opt_tab["TN"] + opt_tab["FP"])
    opt_tab["MOF"] = opt_tab["FN"]/total
    opt_tab["MOR"] = opt_tab["FN"]/(opt_tab["FN"] + opt_tab["TP"])

    opt_tab["COR/MOR"] = opt_tab["COR"]/opt_tab["MOR"]
    opt_tab["COR/MOF"] = opt_tab["COR"]/opt_tab["MOF"]
    
    num_mcc = opt_tab["TP"]*opt_tab["TN"] - opt_tab["FP"]*opt_tab["FN"]
    den_mcc =( (opt_tab["TP"]+opt_tab["FP"])*(opt_tab["TP"]+opt_tab["FN"])*(opt_tab["TN"]+opt_tab["FP"])*(opt_tab["TN"]+opt_tab["FN"]) )**0.5
    opt_tab["MCC"] = num_mcc/den_mcc
    
    opt_tab["dist 0,0: COR-MOR"] = (opt_tab["COR"] ** 2 + opt_tab["MOR"] ** 2) ** 0.5
    mor_min = min(opt_tab["dist 0,0: COR-MOR"])
    opt_mask = opt_tab["dist 0,0: COR-MOR"]==mor_min
    mor_opt_thresh = opt_tab.loc[opt_tab[opt_mask].index, ["thresholds"]]
    
    opt_tab["dist 0,0: COR-MOF"] = (opt_tab["COR"] ** 2 + opt_tab["MOF"] ** 2) ** 0.5
    mof_min = min(opt_tab["dist 0,0: COR-MOF"])
    opt_mask = opt_tab["dist 0,0: COR-MOF"]==mof_min
    mof_opt_thresh = opt_tab.loc[opt_tab[opt_mask].index, ["thresholds"]]

    opt_tab["dist 0,1: ROC"] = ( opt_tab["COR"] ** 2 + (1-opt_tab["VDA"] ** 2) ) ** 0.5
    roc_min = min(opt_tab["dist 0,1: ROC"])
    opt_mask = opt_tab["dist 0,1: ROC"]==roc_min
    roc_opt_thresh = opt_tab.loc[opt_tab[opt_mask].index, ["thresholds"]]
    
    mor_area = 0
    rng = range(0,len(opt_tab["MOR"])-1)
    for i in rng:
        mor_area = mor_area + opt_tab.loc[i,"COR"]*(opt_tab.loc[i+1,"MOR"]-opt_tab.loc[i,"MOR"])
    opt_tab.loc[0,"AUCOR-MOR"] = mor_area
    
    roc_area = 0
    for i in rng:
        y = opt_tab.loc[i,"VDA"]
        x0 = opt_tab.loc[i,"COR"]
        x1 = opt_tab.loc[i+1,"COR"]
        x = x0-x1
        roc_area = roc_area + y*x
    opt_tab.loc[0,"AUROCC"] = roc_area

    opt_tab.to_csv("DataFiles\\" + params.buildtype + "\\" + params.traintype + "\\" + params.fusetype + "\\metrics.csv")

    return mor_opt_thresh.iloc[0,0], mof_opt_thresh.iloc[0,0], roc_opt_thresh.iloc[0,0]

def GenerateAnalytics(params):
    # Controller for the post-analysis task. Un/comment to in/exclude methods.
    outputcsvlocation = "DataFiles\\" + params.buildtype + "\\" + params.traintype + "\\" + params.fusetype + "\\VIE-historical-output.csv"
    output = pd.read_csv(outputcsvlocation, parse_dates=["fused-proba-dt"])
    #metsarr, cm = GenerateConfusionMatrixNMetrics(output, params, 0.5, "")    
    #metsarr, cm = GenerateConfusionMatrixNMetrics(output, params, 0, "")    
    #metsarr, cm = GenerateConfusionMatrixNMetrics(output, params, 1, "")    
    metrics_vthresh, thresholds = GenerateMetricsForAllThresholds(output.copy(), params)
    mor_opt, mof_opt, roc_opt = GetOptimalValues(metrics_vthresh, thresholds, params)
    GenerateAccuracyCurves(metrics_vthresh, thresholds, params)
    #GenerateConfusionMatrixNMetrics(output.copy(), params, mor_opt, "_MOR")
    #GenerateConfusionMatrixNMetrics(output.copy(), params, mof_opt, "_MOF")
    #GenerateConfusionMatrixNMetrics(output.copy(), params, roc_opt, "_ROC")
    return
