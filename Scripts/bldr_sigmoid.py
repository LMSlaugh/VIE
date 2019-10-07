# Author: Lisa Slaughter <lisa.m.slaughter@gmail.com>
# Last update: Jan 28 2019

# {Description here}

# ----------------------------------------------------------------------------------------------------------
import pandas as pd
import numpy as np
import math as math
import helper_figure_generator as figen

def Sigmoid(x, p1, p2):
    return 1-1/(1+np.exp((p1-x)/p2))

def BuildVacancyRelationship(sensor):
    GetHistData(sensor)
    if sensor.vacancyrelationship=="Percentile": # sigmoid
        import scipy.optimize as opt
        cumsum = 0
        rawprobas = []
        cols = sensor.vachistdata.columns
        sensorvals_raw = sensor.vachistdata[cols[0]]

        # Remove any outliers
        stats_pre = sensorvals_raw.describe()
        std_pre = stats_pre["std"]
        mean_pre = stats_pre["mean"]
        sensorvals = sensorvals_raw[sensorvals_raw.values < ( mean_pre + 6 * std_pre )]
        sensorvals = sensorvals[sensorvals.values > ( mean_pre - 6 * std_pre )]

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
        mean = stats_v["mean"] # Starting value for parameter 1
        std = stats_v["std"] # starting value for parameter 2
        popt, pcov = opt.curve_fit(Sigmoid, sensorvals, rawprobas, p0=[mean_pre, std_pre])
        sensor.vrparam1 = popt[0]
        sensor.vrparam2 = popt[1]
        sensor.std = std

        fitprobas = Sigmoid(sensorvals, sensor.vrparam1, sensor.vrparam2)
        figen.PlotSigmoids(sensor, sensorvals, rawprobas, fitprobas)

    elif sensor.vacancyrelationship=="Logistic": # Logistic Regression
        from sklearn import linear_model
        from scipy.special import expit
        o_data = sensor.occhistdata.copy()
        o_data["truth-val"] = 0
        # Remove any outliers from occupied data
        stats_o = o_data[sensor.sensorname + "-val"].describe()
        std_o = stats_o["std"]
        mean_o = stats_o["mean"]
        o_data = o_data[o_data[sensor.sensorname + "-val"] < ( mean_o + 6 * std_o )]
        o_data = o_data[o_data[sensor.sensorname + "-val"] > ( mean_o - 6 * std_o )]

        v_data = sensor.vachistdata.copy()
        v_data["truth-val"] = 1
        # Remove any outliers from vacant data
        stats_v = v_data[sensor.sensorname + "-val"].describe()
        std_v = stats_v["std"]
        mean_v = stats_v["mean"]
        v_data = v_data[v_data[sensor.sensorname + "-val"] < ( mean_v + 6 * std_v )]
        v_data = v_data[v_data[sensor.sensorname + "-val"] > ( mean_v - 6 * std_v )]
        sensor.std = std_v / ( max(v_data[sensor.sensorname + "-val"]) - min(v_data[sensor.sensorname + "-val"]) ) # normalize it

        data_train = pd.concat([o_data,v_data], join="outer")
        feature = data_train.loc[:,sensor.sensorname + "-val"].values.reshape(-1,1) # shape: (n,1)
        labels = data_train.loc[:,"truth-val"].ravel() # shape: (n, )
        clf = linear_model.LogisticRegression(C=1e5, solver='lbfgs')
        clf.fit(feature, labels)

        x_plot = np.linspace(min(feature), max(feature), 300)
        sensor.vrparam1 = clf.coef_[0][0]
        sensor.vrparam2 = clf.intercept_[0]
        proba = expit(x_plot * sensor.vrparam1 + sensor.vrparam2).ravel()
        figen.PlotExpit(sensor, x_plot, proba, data_train)
    else:
        pass # error out
    sensor.histdata = pd.DataFrame()
    sensor.vachistdata = pd.DataFrame()
    sensor.occhistdata = pd.DataFrame()
    return sensor
       
def GetHistData(sensor):
    sensor.GetHistoricalData()
    if sensor.trainingdataset=="Cherry":
        # TODO implement vacancy start and end times in the config file for each sensor
        mask_vac = ( (sensor.histdata.index.hour >= 0 ) & (sensor.histdata.index.hour <= 4) ) # slice data for times of ~100% certain vacancy
        data_v = sensor.histdata[mask_vac]
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