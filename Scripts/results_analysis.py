import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def GenerateConfusionMatrixNMetrics(data, params, threshold, sufx):
    datacop = data.copy()
    ind = ["predicted:Vacant(1)","predicted:Occupied(0)","-","True Vacancy Ratio","Optimum Cutoff","Accuracy: Overall","Accuracy: Vacant","Accuracy: Occupied","Complaint Opportunity Rate","Missed Opportunity Rate"]
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
    confmtx.iloc[3,0] = str(round(occ_vac_ratio,3)*100) + "%"
    confmtx.iloc[4,0] = str(round(threshold,3)*100) + "%"
    confmtx.iloc[5,0] = str(round(overacc,3)*100) + "%"
    confmtx.iloc[6,0] = str(round(vacc,3)*100) + "%"
    confmtx.iloc[7,0] = str(round(oacc,3)*100) + "%"
    confmtx.iloc[8,0] = str(round(comp_rate,3)*100) + "%"
    confmtx.iloc[9,0] = str(round(miss_opp_rate,3)*100) + "%"
    confmtx.to_csv("DataFiles\\" + params.buildtype + "\\" + params.traintype + "\\" + params.fusetype + "\\VIE-confusion-matrix" + sufx + ".csv")

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
        met_arr_tmp, cm = GenerateConfusionMatrixNMetrics(data, params, threshold, "")
        metrics_vthresh.loc[i,"TPs"] = met_arr_tmp.loc[0,"TPs"]
        metrics_vthresh.loc[i,"FPs"] = met_arr_tmp.loc[0,"FPs"]
        metrics_vthresh.loc[i,"FNs"] = met_arr_tmp.loc[0,"FNs"]
        metrics_vthresh.loc[i,"TNs"] = met_arr_tmp.loc[0,"TNs"]
        i = i + 1
    return metrics_vthresh, thresholds

def GenerateAccuracyCurves(metrics_vthresh, thresh, params):
    # for Different Thresholds from 0 -> 1....
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

    # Get complaint opportunity rate and plot against thresholds
    COR = FPs/(FPs + FNs + TPs + TNs)
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(thresh, COR)
    #ax.set_ylim([0,1.1])
    #ax.set_xlim([0,1.0])
    #start, end = ax.get_xlim()
    #ax.xaxis.set_ticks(np.arange(start, end, 0.05))
    ax.minorticks_on()
    ax.xaxis.set_tick_params(labelsize=9)
    ax.yaxis.set_tick_params(labelsize=9)
    ax.grid(b=True, which='major', color='#666666', linestyle='-', linewidth=1, alpha=0.7)
    ax.grid(b=True, which='minor', color='#999999', linestyle='-', linewidth=1, alpha=0.2)
    ax.set_title("COR by threshold", fontsize=18, fontweight="bold")
    #ax.set_ylabel("True Positive Rate: TP/(TP + FN)", fontsize=9)
    ax.set_ylabel("Complaint Opportunity Rate: FP/(TP + TN + FN + FP) (%)", fontsize=9)
    ax.set_xlabel("Threshold for Vacancy/Occupancy Determination (%)", fontsize=9)
    fig.savefig("Figures\\" + params.buildtype + "\\" + params.traintype + "\\" + params.fusetype + "\\COR.png", format="png", bbox_inches="tight")
    plt.close(fig)

    # Get missed opportunity rate and plot against thresholds
    MOR = FNs/(FPs + FNs + TPs + TNs)
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(thresh, MOR)
    #ax.set_ylim([0,1.1])
    #ax.set_xlim([0,1.0])
    #start, end = ax.get_xlim()
    #ax.xaxis.set_ticks(np.arange(start, end, 0.05))
    ax.minorticks_on()
    ax.xaxis.set_tick_params(labelsize=9)
    ax.yaxis.set_tick_params(labelsize=9)
    ax.grid(b=True, which='major', color='#666666', linestyle='-', linewidth=1, alpha=0.7)
    ax.grid(b=True, which='minor', color='#999999', linestyle='-', linewidth=1, alpha=0.2)
    ax.set_title("MOR by threshold", fontsize=18, fontweight="bold")
    ax.set_ylabel("Missed Opportunity Rate: FN/(TP + TN + FN + FP) (%)", fontsize=9)
    ax.set_xlabel("Threshold for Vacancy/Occupancy Determination (%)", fontsize=9)
    fig.savefig("Figures\\" + params.buildtype + "\\" + params.traintype + "\\" + params.fusetype + "\\MOR.png", format="png", bbox_inches="tight")
    plt.close(fig)

    # Get missed opportunity fraction and plot against thresholds
    MOF = FNs/(FNs + TPs)
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(thresh, MOF)
    #ax.set_ylim([0,1.1])
    #ax.set_xlim([0,1.0])
    #start, end = ax.get_xlim()
    #ax.xaxis.set_ticks(np.arange(start, end, 0.05))
    ax.minorticks_on()
    ax.xaxis.set_tick_params(labelsize=9)
    ax.yaxis.set_tick_params(labelsize=9)
    ax.grid(b=True, which='major', color='#666666', linestyle='-', linewidth=1, alpha=0.7)
    ax.grid(b=True, which='minor', color='#999999', linestyle='-', linewidth=1, alpha=0.2)
    ax.set_title("MOF by threshold", fontsize=18, fontweight="bold")
    ax.set_ylabel("Missed Opportunity Fraction: FN/(TP + FN) (%)", fontsize=9)
    ax.set_xlabel("Threshold for Vacancy/Occupancy Determination (%)", fontsize=9)
    fig.savefig("Figures\\" + params.buildtype + "\\" + params.traintype + "\\" + params.fusetype + "\\MOF.png", format="png", bbox_inches="tight")
    plt.close(fig)

    # Plot missed opportunity rate and complaint opportunity rate against eachother
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(MOR, COR)
    #ax.set_ylim([0,1.1])
    #ax.set_xlim([0,1.1])
    n = round(len(thresh)-1, 0)
    step = int(round(n/10, 0))
    callout_locs = range(0,n+1,step)
    for val in callout_locs:
        if val==0:
            ax.plot(MOR.values[val], COR.values[val], 'xk', label="Decision Thresholds")
        else:
            ax.plot(MOR.values[val], COR.values[val], 'xk')
        ax.text(MOR.values[val]+.03,COR.values[val]+.004, str(round(val/10)) + "%", horizontalalignment='right', verticalalignment='bottom')
    ax.legend(loc="upper right", fontsize="medium")
    ax.minorticks_on()
    ax.xaxis.set_tick_params(labelsize=9)
    ax.yaxis.set_tick_params(labelsize=9)
    ax.grid(b=True, which='major', color='#666666', linestyle='-', linewidth=1, alpha=0.7)
    ax.grid(b=True, which='minor', color='#999999', linestyle='-', linewidth=1, alpha=0.2)
    ax.set_title("MOR vs. COR by threshold", fontsize=18, fontweight="bold")
    ax.set_xlabel("Missed Opportunity Rate: FN/(TP + TN + FN + FP) (%)", fontsize=9)
    ax.set_ylabel("Complaint Opportunity Rate: FP/(TP + TN + FN + FP) (%)", fontsize=9)
    fig.savefig("Figures\\" + params.buildtype + "\\" + params.traintype + "\\" + params.fusetype + "\\COR-MOR-Comp.png", format="png", bbox_inches="tight")
    plt.close(fig)

    # Plot missed opportunity fraction and complaint opportunity rate against eachother
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(MOF, COR)
    #ax.set_ylim([0,1.1])
    #ax.set_xlim([0,1.1])
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
    ax.xaxis.set_tick_params(labelsize=9)
    ax.yaxis.set_tick_params(labelsize=9)
    ax.grid(b=True, which='major', color='#666666', linestyle='-', linewidth=1, alpha=0.7)
    ax.grid(b=True, which='minor', color='#999999', linestyle='-', linewidth=1, alpha=0.2)
    ax.set_title("MOF vs. COR by threshold", fontsize=18, fontweight="bold")
    ax.set_xlabel("Missed Opportunity Fraction: FN/(TP + FN) (%)", fontsize=9)
    ax.set_ylabel("Complaint Opportunity Rate: FP/(TP + TN + FN + FP) (%)", fontsize=9)
    fig.savefig("Figures\\" + params.buildtype + "\\" + params.traintype + "\\" + params.fusetype + "\\COR-MOF-Comp.png", format="png", bbox_inches="tight")
    plt.close(fig)

    # Get overall accuracy and plot against thresholds
    overall_acc = (TPs + TNs)/(TPs + TNs + FPs + FNs)
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(thresh, overall_acc)
    #ax.set_ylim([0,1.1])
    #ax.set_xlim([0,1.0])
    ax.minorticks_on()
    ax.xaxis.set_tick_params(labelsize=9)
    ax.yaxis.set_tick_params(labelsize=9)
    ax.grid(b=True, which='major', color='#666666', linestyle='-', linewidth=1, alpha=0.7)
    ax.grid(b=True, which='minor', color='#999999', linestyle='-', linewidth=1, alpha=0.2)
    ax.set_title("Overall Accuracy by threshold", fontsize=18, fontweight="bold")
    ax.set_ylabel("Overall Accuracy: (TP + TN)/(TP + TN + FN + FP) (%)", fontsize=9)
    ax.set_xlabel("Threshold for Vacancy/Occupancy Determination (%)", fontsize=9)
    fig.savefig("Figures\\" + params.buildtype + "\\" + params.traintype + "\\" + params.fusetype + "\\AR.png", format="png", bbox_inches="tight")
    plt.close(fig)

    # Get accuracy of vacancy and plot against thresholds
    vacant_acc = TPs/(TPs + FNs) # True Positive Rate
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(thresh, vacant_acc)
    #ax.set_ylim([0,1.1])
    #ax.set_xlim([0,1.0])
    ax.minorticks_on()
    ax.xaxis.set_tick_params(labelsize=9)
    ax.yaxis.set_tick_params(labelsize=9)
    ax.grid(b=True, which='major', color='#666666', linestyle='-', linewidth=1, alpha=0.7)
    ax.grid(b=True, which='minor', color='#999999', linestyle='-', linewidth=1, alpha=0.2)
    ax.set_title("Vacancy Detection Accuracy by threshold", fontsize=18, fontweight="bold")
    ax.set_ylabel("Accuracy of Detecting \"Vacant\": TP/(TP + FN) (%)", fontsize=9)
    ax.set_xlabel("Threshold for Vacancy/Occupancy Determination (%)", fontsize=9)
    fig.savefig("Figures\\" + params.buildtype + "\\" + params.traintype + "\\" + params.fusetype + "\\VAR.png", format="png", bbox_inches="tight")
    plt.close(fig)

    # Get accuracy of occupancy and plot against thresholds
    occupied_acc = TNs/(FPs + TNs) # True Negative Rate
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(thresh, occupied_acc)
    #ax.set_ylim([0,1.1])
    #ax.set_xlim([0,1.0])
    #start, end = ax.get_xlim()
    #ax.xaxis.set_ticks(np.arange(start, end, 0.05))
    ax.minorticks_on()
    ax.xaxis.set_tick_params(labelsize=9)
    ax.yaxis.set_tick_params(labelsize=9)
    ax.grid(b=True, which='major', color='#666666', linestyle='-', linewidth=1, alpha=0.7)
    ax.grid(b=True, which='minor', color='#999999', linestyle='-', linewidth=1, alpha=0.2)
    ax.set_title("Occupancy Detection Accuracy by threshold", fontsize=18, fontweight="bold")
    ax.set_ylabel("Accuracy of Detecting \"Occupied\": TN/(TN + FP) (%)", fontsize=9)
    ax.set_xlabel("Threshold for Vacancy/Occupancy Determination (%)", fontsize=9)
    fig.savefig("Figures\\" + params.buildtype + "\\" + params.traintype + "\\" + params.fusetype + "\\OAR.png", format="png", bbox_inches="tight")
    plt.close(fig)

    # Plot vac_acc and occ_acc against eachother
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
        ax.text(occupied_acc.values[val]-.005,vacant_acc.values[val]-.05, str(round(val/10)) + "%", horizontalalignment='right', verticalalignment='bottom')
    #ax.set_ylim([0,1.1])
    #ax.set_xlim([0,1.1])
    ax.legend(loc="lower left", fontsize="medium")
    ax.minorticks_on()
    ax.xaxis.set_tick_params(labelsize=9)
    ax.yaxis.set_tick_params(labelsize=9)
    ax.grid(b=True, which='major', color='#666666', linestyle='-', linewidth=1, alpha=0.7)
    ax.grid(b=True, which='minor', color='#999999', linestyle='-', linewidth=1, alpha=0.2)
    ax.set_title("\"Vacant\" Accuracy vs. \"Occupied\" Accuracy by threshold", fontsize=18, fontweight="bold")
    ax.set_ylabel("Accuracy of Detecting \"Vacant\": TP/(TP + FN) (%)", fontsize=9)
    ax.set_xlabel("Accuracy of Detecting \"Occupied\": TN/(TN + FP) (%)", fontsize=9)
    fig.savefig("Figures\\" + params.buildtype + "\\" + params.traintype + "\\" + params.fusetype + "\\OAR-VAR-Comp.png", format="png", bbox_inches="tight")
    plt.close(fig)
    return

def GetOptimalValues(metrics_vthresh, thresholds, params):
    opt_tab = pd.DataFrame(index=range(len(thresholds)), columns=["thresholds", "TP", "TN", "FP", "FN", "COR", "MOR", "MOF", "MCC", "dist to 0,0"])
    opt_tab["thresholds"] = thresholds
    opt_tab["TP"] = metrics_vthresh["TPs"] 
    opt_tab["TN"] = metrics_vthresh["TNs"] 
    opt_tab["FP"] = metrics_vthresh["FPs"] 
    opt_tab["FN"] = metrics_vthresh["FNs"]
    
    total = opt_tab["FP"] + opt_tab["FN"] + opt_tab["TP"] + opt_tab["TN"]
    opt_tab["COR"] = opt_tab["FP"]/total
    opt_tab["MOR"] = opt_tab["FN"]/total
    opt_tab["MOF"] = opt_tab["FN"]/(opt_tab["FN"] + opt_tab["TP"])
    
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

    opt_tab.to_csv("DataFiles\\" + params.buildtype + "\\" + params.traintype + "\\" + params.fusetype + "\\metrics.csv")

    return mor_opt_thresh.iloc[0,0], mof_opt_thresh.iloc[0,0]

def GenerateAnalytics(params):
    outputcsvlocation = "DataFiles\\" + params.buildtype + "\\" + params.traintype + "\\" + params.fusetype + "\\VIE-historical-output.csv"
    output = pd.read_csv(outputcsvlocation, parse_dates=["fused-proba-dt"])
    metrics_vthresh, thresholds = GenerateMetricsForAllThresholds(output.copy(), params)
    mor_opt, mof_opt = GetOptimalValues(metrics_vthresh, thresholds, params)
    GenerateAccuracyCurves(metrics_vthresh, thresholds, params)
    GenerateConfusionMatrixNMetrics(output.copy(), params, mor_opt, "_MOR")
    GenerateConfusionMatrixNMetrics(output.copy(), params, mof_opt, "_MOF")
    return
