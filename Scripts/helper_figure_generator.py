
# Author: Lisa Slaughter <lisa.m.slaughter@gmail.com>
# Last update: Jan 28 2019

# {Description here}

# ----------------------------------------------------------------------------------------------------------
import pandas as pd
import numpy as np
import math as math
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

labs = 11 # figure label size
legs = "medium"

def PlotHistoricalIns(historicaldata):
    # Plot Historical outputs and inputs
    historicalfig, ax = plt.subplots(figsize=(20,10))
    ax.plot(historicaldata["wifidt"], historicaldata["wifival"], "b", label="Wifi (counts)")
    ax.plot(historicaldata["co2dt"], historicaldata["co2val"], "r", label="CO2 (ppm)")
    ax.plot(historicaldata["elecdt"], historicaldata["elecval"], "g", label="Elec (kW*10)")
    ax.legend(loc='best', fontsize=legs)
    ax.set_ylabel("Sensor Value", fontsize=labs)
    ax.xaxis.set_major_locator(mdates.HourLocator(byhour=[0,6,12,18,24]))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%a %H:%M"))
    ax.xaxis.set_tick_params(labelsize=labs)
    ax.yaxis.set_tick_params(labelsize=labs)
    ax.grid(b=True, which='major', color='k', linestyle=':', linewidth=1)
    historicalfig.autofmt_xdate()
    historicalfig.suptitle("Inputs: Raw Sensor Data", fontsize=18, fontweight="bold")
    historicalfig.savefig("Figures\\historical-method-inputs-fig.png", format='png', bbox_inches='tight')
    return

def PlotHistoricalOuts(historicaldata):
    # Plot Historical outputs and inputs
    historicalfig, ax = plt.subplots(figsize=(20,10))
    ax.plot(historicaldata["wifidt"], historicaldata["wifiproba"], "b", label="Wifi (%)")
    ax.plot(historicaldata["co2dt"], historicaldata["co2proba"], "r", label="CO2 (%)")
    ax.plot(historicaldata["elecdt"], historicaldata["elecproba"], "g", label="Elec (%)")
    ax.plot(historicaldata["overallprobadt"], historicaldata["overallproba_rss"], label="Fused: RSS (%)")
    ax.plot(historicaldata["overallprobadt"], historicaldata["overallproba_rms"], label="Fused: RMS (%)")
    ax.plot(historicaldata["overallprobadt"], historicaldata["overallproba_max"], label="Fused: Max (%)")
    ax.plot(historicaldata["overallprobadt"], historicaldata["overallproba_avg"], label="Fused: Avg (%)")
    ax.plot(historicaldata["overallprobadt"], historicaldata["overallproba_mult"], label="Fused: Mult (%)")
    #ax.plot(historicaldata["overallprobadt"], historicaldata["overallproba_linreg"], "k.", label="Fused: LinReg (%)")
    plt.ylim([0,1])
    ax.legend(loc='best', fontsize=legs)
    ax.set_ylabel("Probability of Vacancy (%)", fontsize=labs)
    ax.xaxis.set_major_locator(mdates.HourLocator(byhour=[0,6,12,18,24]))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%a %H:%M"))
    ax.xaxis.set_tick_params(labelsize=labs)
    ax.yaxis.set_tick_params(labelsize=labs)
    ax.grid(b=True, which='major', color='k', linestyle=':', linewidth=1)
    historicalfig.autofmt_xdate()
    historicalfig.suptitle("Outputs: Probabilities of Vacancy", fontsize=18, fontweight="bold")
    historicalfig.savefig("Figures\\historical-method-outputs-fig.png", format='png', bbox_inches='tight')
    return

def PlotRealtimeIns(realtimedata):
    # Plot realtime outputs and inputs
    realtimefig, ax = plt.subplots(figsize=(20,10))
    ax.plot(realtimedata["wifidt"], realtimedata["wifival"], "b.", label="Wifi (counts)")
    ax.plot(realtimedata["co2dt"], realtimedata["co2val"], "r.", label="CO2 (ppm)")
    ax.plot(realtimedata["elecdt"], realtimedata["elecval"], "g.", label="Elec (kW*10)")
    ax.legend(loc='best', fontsize=legs)
    ax.set_ylabel("Sensor Value", fontsize=labs)
    ax.xaxis.set_major_locator(mdates.HourLocator(byhour=[0,6,12,18,24]))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%a %H:%M"))
    ax.xaxis.set_tick_params(labelsize=labs)
    ax.yaxis.set_tick_params(labelsize=labs)
    ax.grid(b=True, which='major', color='k', linestyle=':', linewidth=1)
    realtimefig.autofmt_xdate()
    realtimefig.suptitle("Inputs: Raw Sensor Data", fontsize=18, fontweight="bold")
    realtimefig.savefig("Figures\\realtime-method-inputs-fig.png", format='png', bbox_inches='tight')
    return

def PlotRealtimeOuts(realtimedata):
    # Plot realtime outputs and inputs
    realtimefig, ax = plt.subplots(figsize=(20,10))
    ax.plot(realtimedata["wifidt"], realtimedata["wifiproba"], "b.", label="Wifi (%)")
    ax.plot(realtimedata["co2dt"], realtimedata["co2proba"], "r.", label="CO2 (%)")
    ax.plot(realtimedata["elecdt"], realtimedata["elecproba"], "g.", label="Elec (%)")
    ax.plot(realtimedata["overallprobadt"], realtimedata["overallprobaval"], "k.", label="Fused (%)")
    plt.ylim([0,1])
    ax.legend(loc='best', fontsize=legs)
    ax.set_ylabel("Probability of Vacancy (%)", fontsize=labs)
    ax.xaxis.set_major_locator(mdates.HourLocator(byhour=[0,6,12,18,24]))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%a %H:%M"))
    ax.xaxis.set_tick_params(labelsize=labs)
    ax.yaxis.set_tick_params(labelsize=labs)
    ax.grid(b=True, which='major', color='k', linestyle=':', linewidth=1)
    realtimefig.autofmt_xdate()
    realtimefig.suptitle("Outputs: Probabilities of Vacancy", fontsize=18, fontweight="bold")
    realtimefig.savefig("Figures\\realtime-method-outputs-fig.png", format='png', bbox_inches='tight')
    return

def PlotHistoricalInOuts(historicaldata):
    # Plot Historical outputs and inputs
    historicalfig, ax = plt.subplots(nrows=2, ncols=1, figsize=(20,10))
    ax[0].plot(historicaldata["wifidt"], historicaldata["wifiproba"], "b", label="Wifi (%)")
    ax[0].plot(historicaldata["co2dt"], historicaldata["co2proba"], "r", label="CO2 (%)")
    ax[0].plot(historicaldata["elecdt"], historicaldata["elecproba"], "g", label="Elec (%)")
    ax[0].legend(loc='best', fontsize=legs)
    ax[0].set_title("Inputs: Probability of Vacancy from Each Sensor Input")
    ax[0].set_ylabel("Probability of Vacancy (%)", fontsize=labs)
    ax[0].xaxis.set_major_locator(mdates.HourLocator(byhour=[0,6,12,18,24]))
    ax[0].xaxis.set_major_formatter(mdates.DateFormatter("%a %H:%M"))
    ax[0].xaxis.set_tick_params(labelsize=labs)
    ax[0].yaxis.set_tick_params(labelsize=labs)
    ax[0].grid(b=True, which='major', color='k', linestyle=':', linewidth=1)
    ## Plot raw probas, no fusion
    #ax[1].plot(historicaldata["wifidt"], historicaldata["wifiproba"], "b", label="Wifi (%)")
    #ax[1].plot(historicaldata["co2dt"], historicaldata["co2proba"], "r", label="CO2 (%)")
    #ax[1].plot(historicaldata["elecdt"], historicaldata["elecproba"], "g", label="Elec (%)")
    ##
    # Plot fusion results:
    ax[1].plot(historicaldata["overallprobadt"], historicaldata["overallproba_rss"], label="Fused: RSS (%)")
    #ax[1].plot(historicaldata["overallprobadt"], historicaldata["overallproba_rms"], label="Fused: RMS (%)")
    #ax[1].plot(historicaldata["overallprobadt"], historicaldata["overallproba_max"], label="Fused: Max (%)")
    #ax[1].plot(historicaldata["overallprobadt"], historicaldata["overallproba_avg"], label="Fused: Avg (%)")
    #ax[1].plot(historicaldata["overallprobadt"], historicaldata["overallproba_mult"], label="Fused: Mult (%)")
    #
    plt.ylim([0,1])
    ax[1].legend(loc='best', fontsize=legs)
    ax[1].set_title("Outputs: Fused Probability of Vacancy via Different Methods")
    ax[1].set_ylabel("Probability of Vacancy (%)", fontsize=labs)
    ax[1].xaxis.set_major_locator(mdates.HourLocator(byhour=[0,6,12,18,24]))
    ax[1].xaxis.set_major_formatter(mdates.DateFormatter("%a %H:%M"))
    ax[1].xaxis.set_tick_params(labelsize=labs)
    ax[1].yaxis.set_tick_params(labelsize=labs)
    ax[1].grid(b=True, which='major', color='k', linestyle=':', linewidth=1)
    historicalfig.autofmt_xdate()
    historicalfig.suptitle("Comparison of Inputs and Outputs for Fusion Process", fontsize=18, fontweight="bold")
    historicalfig.savefig("Figures\\historical-method-diagnostic-fig.png", format='png', bbox_inches='tight')
    return

def PlotRealtimeInOuts(realtimedata):
    # Plot realtime outputs and inputs
    realtimefig, ax = plt.subplots(nrows=2, ncols=1, figsize=(20,10))
    ax[0].plot(realtimedata["wifidt"], realtimedata["wifival"], "b", label="Wifi (counts)")
    ax[0].plot(realtimedata["co2dt"], realtimedata["co2val"], "r", label="CO2 (ppm)")
    ax[0].plot(realtimedata["elecdt"], realtimedata["elecval"], "g", label="Elec (kW*10)")
    ax[0].legend(loc='best', fontsize=legs)
    ax[0].set_title("Inputs: Raw Sensor Data")
    ax[0].set_ylabel("Sensor Value", fontsize=labs)
    ax[0].xaxis.set_major_locator(mdates.HourLocator(byhour=[0,6,12,18,24]))
    ax[0].xaxis.set_major_formatter(mdates.DateFormatter("a %H:%M"))
    ax[0].xaxis.set_tick_params(labelsize=labs)
    ax[0].yaxis.set_tick_params(labelsize=labs)
    ax[0].grid(b=True, which='major', color='k', linestyle=':', linewidth=1)
    ax[1].plot(realtimedata["wifidt"], realtimedata["wifiproba"], "b", label="Wifi (%)")
    ax[1].plot(realtimedata["co2dt"], realtimedata["co2proba"], "r", label="CO2 (%)")
    ax[1].plot(realtimedata["elecdt"], realtimedata["elecproba"], "g", label="Elec (%)")
    ax[1].plot(realtimedata["overallprobadt"], realtimedata["overallprobaval"], "k.", label="Fused (%)")
    plt.ylim([0,1])
    ax[1].legend(loc='best', fontsize=legs)
    ax[1].set_title("Outputs: Probabilities of Vacancy")
    ax[1].set_ylabel("Probability of Vacancy (%)", fontsize=labs)
    ax[1].xaxis.set_major_locator(mdates.HourLocator(byhour=[0,6,12,18,24]))
    ax[1].xaxis.set_major_formatter(mdates.DateFormatter("a %H:%M"))
    ax[1].xaxis.set_tick_params(labelsize=labs)
    ax[1].yaxis.set_tick_params(labelsize=labs)
    ax[1].grid(b=True, which='major', color='k', linestyle=':', linewidth=1)
    realtimefig.autofmt_xdate()
    realtimefig.suptitle("Comparison of Inputs and Outputs: Real-time Method", fontsize=18, fontweight="bold")
    realtimefig.savefig("Figures\\realtime-method-diagnostic-fig.png", format='png', bbox_inches='tight')
    return

def PlotOutputComparison(historicaldata, realtimedata):
    # Plot Historical and Real-time predictions against eachother
    comparepredictionsfig, ax = plt.subplots(figsize=(20,10))
    ax.plot(historicaldata["overallprobadt"], historicaldata["overallproba_rss"], "c", label="Historical (%)")
    ax.plot(realtimedata["overallprobadt"], realtimedata["overallproba_rss"], "m", label="Real-time (%)")
    plt.ylim([0,1])
    ax.legend(loc='best', fontsize=legs)
    comparepredictionsfig.autofmt_xdate()
    ax.set_title("Comparison of Vacancy Predictions Between Historical and Real-time Methods", fontsize=18, fontweight="bold")
    ax.set_ylabel("Probability of Vacancy (%)", fontsize=labs)
    ax.xaxis.set_major_locator(mdates.HourLocator(byhour=[0,6,12,18,24]))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%a %H:%M"))
    ax.xaxis.set_tick_params(labelsize=labs)
    ax.yaxis.set_tick_params(labelsize=labs)
    ax.grid(b=True, which='major', color='k', linestyle=':', linewidth=1)
    comparepredictionsfig.savefig("Figures\\overall-prediction-comparison-fig.png", format='png', bbox_inches='tight')
    return

#def PlotOutDistribution(historicaldata):


#def PlotSigmoids(sensor):
    #historicalvacantdata = sensor.histdata
    #histdat = historicalvacantdata.iloc[:,0]
    #n_bins = math.floor(len(histdat)/10)
    #histdat = histdat.dropna()
    #n, bins, patches = plt.hist(histdat, n_bins, cumulative=True, align="left")
    #bins = bins[0:-1]
    #normed_freq = 1 - n / len(histdat)
    
    #realsigmoidfig, axrs = plt.subplots(figsize=(10,5))
    #axrs.plot(bins, normed_freq)
    #plt.ylim([0,1])
    #plt.xlim([0,bins[-1]])
    #axrs.xaxis.set_major_locator(plt.MaxNLocator(20))
    #axrs.xaxis.set_tick_params(labelsize=labs)
    #axrs.yaxis.set_tick_params(labelsize=labs)
    #axrs.set_title("Actual Vacancy Relationship for Sensor: " + sensor.sensorname, fontsize=18, fontweight="bold")
    #axrs.set_ylabel("Probability of Vacancy (%)", fontsize=labs)
    #axrs.set_xlabel("Raw Sensor Value", fontsize=labs)
    #axrs.grid(b=True, which='major', color='k', linestyle=':', linewidth=1)
    #realsigmoidfig.savefig("Figures\\sigmoid-real-" + sensor.sensorname + ".png", format='png', bbox_inches='tight')
    
    #data_r = pd.DataFrame(bins, columns=["x"])
    #data_r = pd.DataFrame(histdat, columns=["x"])
    #y = []
    #for index, row in data_r.iterrows():
    #    y_temp = 1-1/(1+np.exp((sensor.vrparam1-row["x"])/sensor.vrparam2))
    #    y.append(y_temp)
    #data_r["y"] = y

    #gensigmoidfig, axgs = plt.subplots(figsize=(10,5))
    #axgs.plot(data_r["x"],data_r["y"])
    #plt.ylim([0,1])
    #plt.xlim([0,bins[-1]])
    #axgs.xaxis.set_major_locator(plt.MaxNLocator(20))
    #axgs.xaxis.set_tick_params(labelsize=labs)
    #axgs.yaxis.set_tick_params(labelsize=labs)
    #axgs.set_title("Generated Vacancy Relationship for Sensor: " + sensor.sensorname, fontsize=18, fontweight="bold")
    #axgs.set_ylabel("Probability of Vacancy (%)", fontsize=labs)
    #axgs.set_xlabel("Raw Sensor Value", fontsize=labs)
    #axgs.grid(b=True, which='major', color='k', linestyle=':', linewidth=1)
    #gensigmoidfig.savefig("Figures\\sigmoid-generated-" + sensor.sensorname + ".png", format="png", bbox_inches="tight")
    
    # plot generated sigmoid on top of the real one
    #compsigmoidfig, axcs = plt.subplots(figsize=(20,10))
    #axcs.plot(data_r["x"], data_r["y"], label="Actual")
    #axcs.plot(bins, normed_freq, label="Generated")
    #plt.ylim([0,1])
    #plt.xlim([0,bins[-1]])
    #axcs.xaxis.set_major_locator(plt.MaxNLocator(20))
    #axcs.xaxis.set_tick_params(labelsize=labs)
    #axcs.yaxis.set_tick_params(labelsize=labs)
    #axcs.set_title("Vacancy Relationship Accuracy for Sensor: " + sensor.sensorname, fontsize=18, fontweight="bold")
    #axcs.set_ylabel("Probability of Vacancy (%)", fontsize=labs)
    #axcs.set_xlabel("Raw Sensor Value", fontsize=labs)
    #axcs.grid(b=True, which='major', color='k', linestyle=':', linewidth=1)
    #compsigmoidfig.savefig("Figures\\sigmoid-comparison-" + sensor.sensorname + ".png", format="png", bbox_inches="tight")
    #return

def PlotMain():
    historicaldata = pd.read_csv("DataFiles\\VIE-output-historical.csv", parse_dates=["runtimedt","overallprobadt", "wifidt", "co2dt", "elecdt"])
    #realtimedata = pd.read_csv("DataFiles\\VIE-output-realtime-feb3-run.csv", parse_dates=["runtimedt","overallprobadt", "wifidt", "co2dt", "elecdt"])
    #realtimedata["elecval"] = realtimedata["elecval"] * 0.293071
    #PlotHistoricalIns(historicaldata)
    #PlotHistoricalOuts(historicaldata)
    PlotHistoricalInOuts(historicaldata)
    #PlotRealtimeIns(realtimedata)
    #PlotRealtimeOuts(realtimedata)
    #PlotRealtimeInOuts(realtimedata)
    #PlotOutDistribution(historicaldata)
    #PlotOutputComparison(historicaldata, realtimedata)
    return

#PlotMain()

stopgap = "this is a stopgap"