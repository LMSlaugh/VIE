# Author: Lisa Slaughter <lisa.m.slaughter@gmail.com>
# Last update: Jan 28 2019

# {Add description here}

# ----------------------------------------------------------------------------------------------------------

# import needed packages
import pandas as pd
import numpy as np
import VieSensor as snsr
import time as time
import datetime as dt
import math as math
import scipy.optimize as opt
import matplotlib.pyplot as plt
import helper_figure_generator as figen
import results_analysis as ra

## Global variables

#linreg_flag = True
linreg_flag = False

#fusetype = "rss"       #root sum square
#fusetype = "rms"       #root mean square
#fusetype = "max"       #maximum
#fusetype = "linreg"    #linear regression

def SigmoidFinal(x, p1, p2): # This should really be called from bldr_template.py
    return 1/(1+np.exp((p1-x)/p2))

def Plot_Final_Sigmoid(p1, p2, sensorvals, probas): # This should really be called from bldr_template.py
    labs = 11 # figure label size
    legs = "medium"
    
    sigmoidcompfig, axcs = plt.subplots(figsize=(11,5))
    axcs.plot(sensorvals, probas, label="Raw")
    #plt.savefig("sigmoid-value-check-final" + ".png", format="png", bbox_inches="tight")
    axcs.plot(sensorvals, SigmoidFinal(sensorvals,p1,p2), label="Generated")
    axcs.legend(loc='best', fontsize=legs)
    plt.ylim([0,1])
    plt.xlim([0,max(sensorvals)])
    axcs.xaxis.set_major_locator(plt.MaxNLocator(20))
    axcs.xaxis.set_tick_params(labelsize=labs)
    axcs.yaxis.set_tick_params(labelsize=labs)
    axcs.set_title("Vacancy Relationship for Virtual Sensor", fontsize=18, fontweight="bold")
    axcs.set_ylabel("Probability of Vacancy (%)", fontsize=labs)
    axcs.set_xlabel("Abstract Sensor Value", fontsize=labs)
    axcs.grid(b=True, which='major', color='k', linestyle=':', linewidth=1)
    plt.savefig("Figures\\sigmoid-final" + ".png", format="png", bbox_inches="tight")
    plt.close(sigmoidcompfig)
    return

def IterProdFusion(sensors):
    # pull final sigmoid values
    params = pd.DataFrame(index=[0], columns=["p1", "p2"])
    params_temp = pd.read_csv("ConfigFiles\\Final_Parameters.csv") # Can treat as a new sensor in the metadatabase?
    p_sz = params_temp.shape
    sensornames = []
    for k, v in sensors.items():
        sensornames.append(v.sensorname)
    if( p_sz == (0,2) ): # If the parameters don't exist...
        # Build vector of abstract input values
        x_vec = np.linspace(1,-1,100) # should cover all possible inputs, which range from zero to one
        # input abstract vector into functional form, get y-values out
        zero_data = np.zeros(shape=(len(x_vec), len(sensors)))
        y_mtrx = pd.DataFrame(zero_data, columns=sensornames)
        #y_mtrx["x_vec"] = x_vec
        y_vec = []
        prod_vec = []
        for k, v in sensors.items():
            y_vec = []
            prod_vec = []
            #Dividing "all values" by 2*mean to get them all between 1 and 0. This means the new mean is at 0.5 for all sensors.
            mean_old = v.vrparam1
            mean_new = 0.5 # Need to correct x-values. Mean_new = mean_old/(2*mean_old)
            #The second fit parameter doesn't actually correlate to standard deviation. Need to figure out how to correct it 
            std_old = v.vrparam2
            std_new = std_old/(2*mean_old)
            for x in x_vec:
                y_vec.append(SigmoidFinal(x,mean_new,std_new))
            #temp_df = pd.DataFrame(data=y_vec)
            #stats = temp_df.describe()
            #avg = stats.loc["mean",0]
            #y_vec = y_vec-avg
            y_mtrx[v.sensorname] = y_vec  # May error here
        # Normalize so that integral equals 1? Later. They may alrady be normalized...?
        # Multiply together the y-mtrx columns across each row.
        prod_vec = np.prod(y_mtrx, axis = 1) # len(prod_vec) should equal that of x_vec
        # Curve fit it
        stats_fin = prod_vec.describe()
        popt, pcov = opt.curve_fit(SigmoidFinal, x_vec, prod_vec, p0=[stats_fin["mean"], stats_fin["std"]])
        mean_final = popt[0]
        std_final = popt[1]
        # Save those parameters somwhere because it only needs to be done once 
        params["p1"] = mean_final
        params["p2"] = std_final
        params.to_csv("ConfigFiles\\Final_Parameters_new.csv", index=False)  # Can treat as a new sensor in the metadatabase?
        Plot_Final_Sigmoid(mean_final, std_final, x_vec, prod_vec)
    else:
        params["p1"] = params_temp.iloc[0,0]
        params["p2"] = params_temp.iloc[0,1]
    # Now predict on inputs
    abstract_input = 1
    for k, v in sensors.items():
        abstract_input = abstract_input * v.snapshotvacancyprobability
    overallproba = SigmoidFinal(abstract_input, params["p1"] , params["p2"])
    overallproba = overallproba[0]
    if overallproba < 0.01:
        overallproba = 0
    else:
        pass
    return overallproba

def IterRmsFusion(sensors):
    # pull final sigmoid values
    params = pd.DataFrame(index=[0], columns=["p1", "p2"])
    params_temp = pd.read_csv("ConfigFiles\\Final_Parameters_new.csv") # Can treat as a new sensor in the metadatabase?
    p_sz = params_temp.shape
    sensornames = []
    for k, v in sensors.items():
        sensornames.append(v.sensorname)
    if( p_sz == (0,2) ): # If the parameters don't exist...
        # Build vector of abstract input values
        x_vec = np.linspace(1,-1,100) # should cover all possible inputs, which range from zero to one
        # input abstract vector into functional form, get y-values out
        zero_data = np.zeros(shape=(len(x_vec), len(sensors)))
        y_mtrx = pd.DataFrame(zero_data, columns=sensornames)
        #y_mtrx["x_vec"] = x_vec
        y_vec = []
        for k, v in sensors.items():
            y_vec = []
            #Dividing "all values" by 2*mean to get them all between 1 and 0. This means the new mean is at 0.5 for all sensors.
            mean_old = v.vrparam1
            mean_new = 0.5 # Need to correct x-values. Mean_new = mean_old/(2*mean_old)
            #The second fit parameter doesn't actually correlate to standard deviation. Need to figure out how to correct it 
            std_old = v.vrparam2
            std_new = std_old/(2*mean_old)
            for x in x_vec:
                y_vec.append(SigmoidFinal(x,mean_new,std_new))
            y_mtrx[v.sensorname] = y_vec  # May error here
        # Normalize so that integral equals 1? Later. They may already be normalized...?
        # Take RMS of the y-mtrx columns across each row to get final (fused) output vector
        #prod_vec = np.prod(y_mtrx, axis = 1) # len(prod_vec) should equal that of x_vec
        y_mtrx = y_mtrx ** 2
        L = y_mtrx.shape
        L = L[1]
        rms_vec = (y_mtrx.sum(axis=1)/L ) ** 0.5
        
        # Curve fit it
        stats_fin = rms_vec.describe()
        popt, pcov = opt.curve_fit(SigmoidFinal, x_vec, rms_vec, p0=[stats_fin["mean"], stats_fin["std"]])
        mean_final = popt[0]
        std_final = popt[1]
        # Save those parameters somwhere because it only needs to be done once 
        params["p1"] = mean_final
        params["p2"] = std_final
        params.to_csv("ConfigFiles\\Final_Parameters_new.csv", index=False)  # Can treat as a new sensor in the metadatabase?
        Plot_Final_Sigmoid(mean_final, std_final, x_vec, rms_vec)
    else:
        params["p1"] = params_temp.iloc[0,0]
        params["p2"] = params_temp.iloc[0,1]
    # Now predict on inputs
    probabilities = []
    for k, v in sensors.items():
        probabilities.append(v.snapshotvacancyprobability)
    probabilities = [i ** 2 for i in probabilities]
    abstracted_input = ( sum(probabilities)/len(probabilities) ) ** 0.5 # take rms of all the inputs
    overallproba = SigmoidFinal(abstracted_input, params["p1"] , params["p2"])
    overallproba = overallproba[0]
    if overallproba < 0.01:
        overallproba = 0
    else:
        pass
    return overallproba

def StdDevWeightedAverage(sensors):
    # get std dev and snapshot val for each sensor input
    fusionparams = pd.DataFrame(index=range(len(sensors)), columns=range(2))
    stddevs = []
    i = 0
    for k, v in sensors.items():
        c = 1/(2*v.vrparam1)
        fusionparams.iloc[i,0] = v.snapshotvalue * c
        fusionparams.iloc[i,1] = v.std * c # standard deviation
        stddevs.append(v.std * c)
        i = i + 1
    corrected_vars = [1 / (i ** 2) for i in stddevs]
    #vardevs = [i ** 2 for i in stddevs]
    #vardevs = stddevs
    #varsum = sum(vardevs)
    varsum = sum(corrected_vars)
    overallproba = 0
    for index, row in fusionparams.iterrows():
        overallproba = overallproba + row[0] / (row[1] * varsum)
    return 1 - overallproba

def CreateVirtualSensors(metadatabasePath):
    # Purpose: read each sensor into a list from the sensor metadatabase
    metadata = pd.read_csv(metadatabasePath)
    sensors = {} # Create sensor dictionary. Enforces unique sensor names!!
    for index, row in metadata.iterrows():
        sn = row["Sensor-Name"]
        st = row["Sensor-Type"]
        uf = row["Update-Frequency"]
        mu = row["Measurement-Units"]
        dat = row["Data-Access-Type"] # Remove this?
        vrt = row["Vacancy-Relationship-Type"]
        drfn = row["Data-Retrieval-File-Name"]
        ppfn = row["Preprocessing-File-Name"]
        rbfn = row["Relationship-Builder-File-Name"]
        std = row["Std-Dev"]
        p1 = row["Parameter-1"]
        p2 = row["Parameter-2"]
        p3 = row["Parameter-3"]
        p4 = row["Parameter-4"]
        #newSensor = snsr.VieSensor(linreg_flag, sn, st, uf, mu, dat, vrt, drfn, ppfn, rbfn, p1, p2, p3, p4)
        newSensor = snsr.VieSensor(sn, st, uf, mu, dat, vrt, drfn, ppfn, rbfn, std, p1, p2, p3, p4)
        sensors[newSensor.sensorname] = newSensor
    
    metadata_new = metadata
    for index, row in metadata.iterrows():
        metadata_new.loc[index,"Parameter-1"] = sensors[row["Sensor-Name"]].vrparam1
        metadata_new.loc[index,"Parameter-2"] = sensors[row["Sensor-Name"]].vrparam2
        metadata_new.loc[index,"Parameter-3"] = sensors[row["Sensor-Name"]].vrparam3
        metadata_new.loc[index,"Parameter-4"] = sensors[row["Sensor-Name"]].vrparam4
        metadata_new.loc[index,"Std-Dev"] = sensors[row["Sensor-Name"]].std
    
    metadata_new.to_csv("ConfigFiles\\VIE-sensor-metadatabase-new.csv", header=True, index=False)

    return sensors

def FuseVacancyProbabilities(sensors, fusetype="rms"):
    # Capture individual vacancy probability predictions into a list
    probabilities = []
    for k,v in sensors.items():
        probabilities.append(v.snapshotvacancyprobability)

    if fusetype=="rss":
        probasq = [i ** 2 for i in probabilities]
        overallproba = sum(probasq) ** 0.5
    elif fusetype=="rms":
        probasq = [i ** 2 for i in probabilities]
        overallproba = (sum(probasq) / len(probabilities)) ** 0.5
    elif fusetype=="max":
        overallproba = max(probabilities)
    elif fusetype=="avg":
        overallproba = sum(probabilities) / len(probabilities)        
    elif fusetype=="mult":
        overallproba = np.prod(probabilities)
    elif fusetype=="linreg":
        overallproba = -1
    elif fusetype=="iterprod":
        overallproba = IterProdFusion(sensors)
    elif fusetype=="iterrms":
        overallproba = IterRmsFusion(sensors)
    elif fusetype=="wghtavg":
        overallproba = StdDevWeightedAverage(sensors)
    else: # Default to "mult" - multiplying together the probabilities
        overallproba = np.prod(probabilities)
    return overallproba

def FuseVacancyTimestamps(timestamps, fusetype="rms"):
    overalldt = max(timestamps)
    return overalldt

# Create the following variables once...
#output = pd.DataFrame(index=[0],columns=["runtimedt", "overallprobadt", "overallproba_rss", "overallproba_rms", "overallproba_max", "overallproba_avg", "overallproba_mult", "overallproba_linreg","wifidt","wifival","wifiproba","co2dt","co2val","co2proba","elecdt","elecval","elecproba"])
output = pd.DataFrame(index=[0],columns=["runtimedt", "overallprobadt", "overallproba_wghtavg", "overallproba_iterprod", "overallproba_iterrms", "overallproba_rss", "overallproba_rms", "overallproba_max", "overallproba_avg", "overallproba_mult","wifidt","wifival","wifiproba","co2dt","co2val","co2proba","elecdt","elecval","elecproba","truthdt","truthval"])
output_header = pd.DataFrame(columns=output.columns)
output_header.to_csv("DataFiles\\VIE-output-historical.csv", header=True, index=False) # Apply headers to csv and remove existing entries

sensors = CreateVirtualSensors("ConfigFiles\\VIE-sensor-metadatabase-new.csv") # Read sensors from file, instantiate dictionary. If missing data, fill with dummy data ("") and move on to next sensor
#sensors = CreateVirtualSensors("VIE-sensor-metadatabase.csv") # Read sensors from file, instantiate dictionary. If missing data, fill with dummy data ("") and move on to next sensor

# Import csv historical data to dataframe
histdata = pd.read_csv("DataFiles\\VIE-input-historical_WCEC.csv") # In order: timestamp for sensor 1 (wifi), timestamp for sensor 2 (co2), timestamp for sensor 3 (elec), etc.
for index, row in histdata.iterrows():
    probabilities = [] # unlabelled list of vacancy prediction values from individual sensors
    timestamps = [] # unlabelled list of vacancy prediciton timestamps from individual sensors
    truthval = row["truth-val"]
    truthdt = row["truth-dt"]
    for k, v in sensors.items(): # for each sensor (and for each instance)
        tempstr = v.sensorname + "-dt"
        v.snapshottimestamp = row[tempstr]
        v.snapshotvalue = row[v.sensorname + "-val"]
        v.PreprocessData() # performs any needed preprocessing methods, i.e. conversions, etc.
        v.PredictVacancyProbability()
        timestamps.append(v.snapshottimestamp) # Capture prediction datetime in a list
        probabilities.append(v.snapshotvacancyprobability) # Capture prediction value in a list

    # fuse predictions for all sensors
    overallprobabilityvalue_rss = FuseVacancyProbabilities(sensors,"rss")
    overallprobabilityvalue_rms = FuseVacancyProbabilities(sensors,"rms")
    overallprobabilityvalue_max = FuseVacancyProbabilities(sensors,"max")
    overallprobabilityvalue_avg = FuseVacancyProbabilities(sensors,"avg")
    overallprobabilityvalue_mult = FuseVacancyProbabilities(sensors,"mult")
    #overallprobabilityvalue_iterprod = FuseVacancyProbabilities(sensors,"iterprod") # Perform the iterative product method
    overallprobabilityvalue_iterprod = 0
    #overallprobabilityvalue_iterrms = FuseVacancyProbabilities(sensors,"iterrms") # Perform the iterative root-mean-square method
    overallprobabilityvalue_iterrms = 0
    overallprobabilityvalue_wghtavg = FuseVacancyProbabilities(sensors,"wghtavg")

    if linreg_flag:
        overallprobabilityvalue_linreg = FuseVacancyProbabilities(probabilities,"linreg")

    #overallprobabilityvalue = FuseVacancyProbabilities(probabilities,fusetype)
    overallprobabilitytimestamp = FuseVacancyTimestamps(timestamps,fusetype="rms")

    # TODO build up output dataframe based on sensorname. Hardcoded by sensorname for now, see below...
    #for k, v in sensors:
    ##build the data frame column by column

    wifi = sensors["wifi1"]
    co2 = sensors["co21"]
    elec = sensors["elec1"]
    output.iloc[0] = [dt.datetime.now(), overallprobabilitytimestamp, overallprobabilityvalue_wghtavg, overallprobabilityvalue_iterprod, overallprobabilityvalue_iterrms,overallprobabilityvalue_rss, overallprobabilityvalue_rms, overallprobabilityvalue_max, overallprobabilityvalue_avg, overallprobabilityvalue_mult, wifi.snapshottimestamp, wifi.snapshotvalue, wifi.snapshotvacancyprobability, co2.snapshottimestamp, co2.snapshotvalue, co2.snapshotvacancyprobability, elec.snapshottimestamp, elec.snapshotvalue, elec.snapshotvacancyprobability, truthdt, truthval]
    #output.iloc[0] = [dt.datetime.now(), overallprobabilitytimestamp, overallprobabilityvalue_iterprod, overallprobabilityvalue_rss, overallprobabilityvalue_rms, overallprobabilityvalue_max, overallprobabilityvalue_avg, overallprobabilityvalue_mult, overallprobabilityvalue_linreg, wifi.snapshottimestamp, wifi.snapshotvalue, wifi.snapshotvacancyprobability, co2.snapshottimestamp, co2.snapshotvalue, co2.snapshotvacancyprobability, elec.snapshottimestamp, elec.snapshotvalue, elec.snapshotvacancyprobability]
    output.to_csv("DataFiles\\VIE-output-historical.csv", mode="a", header=False, index=False)
ra.GenerateAnalytics("DataFiles\\VIE-output-historical.csv")
figen.PlotMain()
thisisastopgap = "stopgap"

# Build a 3x3 matrix out of the proba inputs 
# Write down minimum criteria
#  1) fused inference must be between 0 and 1
#  2) as you increase # of sensors, accuracy should improve (Alan expects probability to improve, does this make sense?)
