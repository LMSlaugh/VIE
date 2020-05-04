# Author: Lisa Slaughter <lisa.m.slaughter@gmail.com>
# Last update: May 02, 2019

# This code generates the vacancy relationship for an individual sensor. The vacancy relationship maps the
# raw sensor value to the probability of vacancy. 
# ----------------------------------------------------------------------------------------------------------
import pandas as pd
import numpy as np
import math
import helper_figureGenerator as figen

def Sigmoid(x, p1, p2):
    return 1-1/(1+np.exp((p1-x)/p2))

def GetCumulativeDist(sensor, data):
    import scipy.optimize as opt
    import matplotlib.pyplot as plt
    cumsum = 0
    rawprobas = []

    # Remove outliers
    data = pd.DataFrame(data)
    stats_pre = data.describe()
    std_pre = stats_pre.loc["std",0]
    mean_pre = stats_pre.loc["mean",0]
    sensorvals = data[data.values < ( mean_pre + 3 * std_pre )]
    sensorvals = sensorvals[sensorvals.values > ( mean_pre - 3 * std_pre )]

    # Normalize (place values between zero and one)
    sensorvals = sensorvals.iloc[:,0]
    sensorvals_normed = ( sensorvals - min(sensorvals) ) / ( max(sensorvals) - min(sensorvals) )
    summation = sum(sensorvals_normed)
    sensorvals = sensorvals.sort_values(ascending=True)
    sensorvals_normed = sensorvals_normed.sort_values(ascending=True)
    for datum in sensorvals_normed:
        cumsum = cumsum + datum
        rawprobas.append(1-cumsum/summation) # dividing by the sum makes area under the curve equal to 1
    rawprobas = pd.Series(rawprobas)
    popt, pcov = opt.curve_fit(Sigmoid, sensorvals, rawprobas, p0=[mean_pre, std_pre])

    fitprobas = Sigmoid(sensorvals, popt[0], popt[1])

    # Generate figures
    titlesz = 16
    labs = 12
    legs = 12
    fig, ax = plt.subplots(figsize=(12,6))
    if sensor.sensortype=="electricity demand":
        sensorvals = sensorvals*.001
        ax.plot(sensorvals, rawprobas, "r-", label="Raw")
        ax.plot(sensorvals,fitprobas, "b-", label="Generated")
    else:
        ax.plot(sensorvals, rawprobas, "r-", label="Raw")
        ax.plot(sensorvals, fitprobas, "b-", label="Generated")
    ax.legend(loc="upper right", fontsize=legs)
    ax.set_ylim([0,1.2])
    ax.set_xlim([min(sensorvals),max(sensorvals)])
    ax.xaxis.set_major_locator(plt.MaxNLocator(20))
    ax.xaxis.set_tick_params(labelsize=labs)
    ax.yaxis.set_tick_params(labelsize=labs)
    ax.set_title("Vacancy Relationship Accuracy for Sensor: " + sensor.sensorname, fontsize=titlesz, fontweight="bold")
    ax.set_ylabel("Probability of Vacancy (%)", fontsize=labs)
    if sensor.sensortype=="wifi connections":
        ax.set_xlabel("Raw Sensor Value (counts)", fontsize=labs)
    elif sensor.sensortype=="electricity demand":
        ax.set_xlabel("Raw Sensor Value (kW)", fontsize=labs)
    elif sensor.sensortype=="carbon dioxide":
        ax.set_xlabel("Raw Sensor Value (ppm)", fontsize=labs)
    ax.grid(b=True, which='major', color='#666666', linestyle=':', linewidth=1, alpha=0.8)
    fig.savefig("Figures\\sigmoid-comparison_full_" + sensor.sensorname + ".png", format="png", bbox_inches="tight")
    plt.close(fig)
    return

def BuildVacancyRelationship(sensor):
    GetHistData(sensor)
    if sensor.vacancyrelationship=="Percentile":
        import scipy.optimize as opt
        cumsum = 0
        rawprobas = []
        cols = sensor.vachistdata.columns
        sensorvals_raw = sensor.vachistdata[cols[0]]

        # Remove outliers
        stats_pre = sensorvals_raw.describe()
        std_pre = stats_pre["std"]
        mean_pre = stats_pre["mean"]
        sensorvals = sensorvals_raw[sensorvals_raw.values < ( mean_pre + 3 * std_pre )]
        sensorvals = sensorvals[sensorvals.values > ( mean_pre - 3 * std_pre )]

        # Normalize (place values between zero and one)
        sensorvals_normed = ( sensorvals - min(sensorvals) ) / ( max(sensorvals) - min(sensorvals) )
        summation = sum(sensorvals_normed)
        
        sensorvals = sensorvals.sort_values(ascending=True)
        sensorvals_normed = sensorvals_normed.sort_values(ascending=True)
        for datum in sensorvals_normed:
            cumsum = cumsum + datum
            rawprobas.append(1-cumsum/summation) # dividing by the sum makes area under the curve equal to 1
        rawprobas = pd.Series(rawprobas)
        stats_v = sensorvals_normed.describe()
        std = stats_v["std"] # starting value for parameter 2
        popt, pcov = opt.curve_fit(Sigmoid, sensorvals, rawprobas, p0=[mean_pre, std_pre])
        sensor.vrparam1 = popt[0]
        sensor.vrparam2 = popt[1]
        sensor.std = std

        fitprobas = Sigmoid(sensorvals, sensor.vrparam1, sensor.vrparam2)
        figen.PlotSigmoids(sensor, sensorvals, rawprobas, fitprobas)

    elif sensor.vacancyrelationship=="Logistic":
        from sklearn import linear_model
        from scipy.special import expit
        o_data = sensor.occhistdata.copy()
        o_data["truth-val"] = 0

        # Remove outliers from occupied data
        stats_o = o_data[sensor.sensorname + "-val"].describe()
        std_o = stats_o["std"]
        mean_o = stats_o["mean"]
        o_data = o_data[o_data[sensor.sensorname + "-val"] < ( mean_o + 3 * std_o )]
        o_data = o_data[o_data[sensor.sensorname + "-val"] > ( mean_o - 3 * std_o )]
        v_data = sensor.vachistdata.copy()
        v_data["truth-val"] = 1

        # Remove outliers from vacant data
        stats_v = v_data[sensor.sensorname + "-val"].describe()
        std_v = stats_v["std"]
        mean_v = stats_v["mean"]
        v_data = v_data[v_data[sensor.sensorname + "-val"] < ( mean_v + 3 * std_v )]
        v_data = v_data[v_data[sensor.sensorname + "-val"] > ( mean_v - 3 * std_v )]
        
        # Normalize (place values between zero and one)
        sensor.std = std_v / ( max(v_data[sensor.sensorname + "-val"]) - min(v_data[sensor.sensorname + "-val"]) )

        data_train = pd.concat([o_data,v_data], join="outer")
        feature = data_train.loc[:,sensor.sensorname + "-val"].values.reshape(-1,1)
        labels = data_train.loc[:,"truth-val"].ravel()
        clf = linear_model.LogisticRegression(C=1e5, solver='lbfgs')
        clf.fit(feature, labels)
        #GetCumulativeDist(sensor, feature)
        x_plot = np.linspace(min(feature), max(feature), 300)
        sensor.vrparam1 = clf.coef_[0][0]
        sensor.vrparam2 = clf.intercept_[0]
        proba = expit(x_plot * sensor.vrparam1 + sensor.vrparam2).ravel()
        figen.PlotExpit(sensor, x_plot, proba, data_train)
    else:
        pass #TODO: send error
    sensor.histdata = pd.DataFrame()
    sensor.vachistdata = pd.DataFrame()
    sensor.occhistdata = pd.DataFrame()
    return sensor
       
def GetHistData(sensor):
    sensor.GetHistoricalData()
    if sensor.trainingdataset=="Cherry":
        # TODO implement expected vacancy start and end times
        # slice data for times of ~100% certain vacancy
        mask_vac = ( (sensor.histdata.index.hour >= 0 ) & (sensor.histdata.index.hour <= 4) )
        data_v = sensor.histdata[mask_vac]
        # slice data for times of ~100% certain occupancy
        mask_occ = (((sensor.histdata.index.hour > 10) & (sensor.histdata.index.hour < 14 )) & (sensor.histdata.index.dayofweek < 5))
        data_o = sensor.histdata[mask_occ]

    elif sensor.trainingdataset=="Full":
        data_v = sensor.histdata[sensor.histdata["truth-val"]==1]
        data_o = sensor.histdata[sensor.histdata["truth-val"]==0]
    
    sensor.vachistdata = data_v[np.logical_not(np.isnan(data_v))]
    sensor.occhistdata = data_o[np.logical_not(np.isnan(data_o))]
    data_v.loc[:,"truth-val"] = 1
    data_o.loc[:,"truth-val"] = 0
    data_train = pd.concat([data_o,data_v], join="outer")
    data_train.to_csv("DataFiles\\" + sensor.vacancyrelationship + "\\" + sensor.trainingdataset + "\\Training_Data_" + sensor.sensorname + ".csv", index=True, header=True)
    return