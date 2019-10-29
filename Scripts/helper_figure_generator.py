
# Author: Lisa Slaughter <lisa.m.slaughter@gmail.com>
# Last update: Jan 28 2019

# {Description here}

# ----------------------------------------------------------------------------------------------------------
import pandas as pd
import numpy as np
import math as math
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

labs = 9 # figure label size
legs = "medium"

def PlotIns(data, in_type, sufx, hrtx):
    fig, ax = plt.subplots(figsize=(20,10))
    # plot inputs
    if (in_type=="elec"):
        ax.plot(data["fused-proba-dt"], data["elec-val"], "g", linewidth="1", label="Elec (W)")
    elif (in_type=="wifi"):
        ax.plot(data["fused-proba-dt"], data["wifi-val"], "b", linewidth="1", label="Wifi (counts)")
    elif (in_type=="co2"):
        ax.plot(data["fused-proba-dt"], data["co2-val"], "r", linewidth="1", label="CO2 (ppm)")
    elif (in_type=="comp"):
        data["elec-val-s"] = data["elec-val"]*0.01
        ax.plot(data["fused-proba-dt"], data["elec-val-s"], "g", linewidth="1", label="Elec (W*.01)")
        data["wifi-val-s"] = data["wifi-val"]*10
        ax.plot(data["fused-proba-dt"], data["wifi-val-s"], "b", linewidth="1", label="Wifi (counts*10)")
        ax.plot(data["fused-proba-dt"], data["co2-val"], "r", linewidth="1", label="CO2 (ppm)")
    ax.legend(loc="upper right", fontsize=legs)
    ax.set_ylabel("Sensor Value", fontsize=labs)
    ax.xaxis.set_major_locator(mdates.HourLocator(byhour=hrtx))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%a %H:%M"))
    ax.xaxis.set_tick_params(labelsize=labs)
    ax.yaxis.set_tick_params(labelsize=labs)
    ax.grid(b=True, which='major', color='#666666', linestyle=':', linewidth=1, alpha=0.8)
    fig.autofmt_xdate()
    fig.suptitle("Raw Sensor Input: " + in_type, fontsize=18, fontweight="bold")
    fig.savefig("Figures\\Input-" + in_type + "_" + sufx + ".png", format='png', bbox_inches='tight')
    plt.close(fig)
    return

def PlotInsNMids(data, in_type, sufx, hrtx, params):
    fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(20,10))
    # plot inputs
    if (in_type=="elec"):
        ax[0].plot(data["fused-proba-dt"], data["elec-val"], "g", linewidth="1", label="Elec (W)")
    elif (in_type=="wifi"):
        ax[0].plot(data["fused-proba-dt"], data["wifi-val"], "b", linewidth="1", label="Wifi (counts)")
    elif (in_type=="co2"):
        ax[0].plot(data["fused-proba-dt"], data["co2-val"], "r", linewidth="1", label="CO2 (ppm)")
    elif (in_type=="comp"):
        data["elec-val-s"] = data["elec-val"]*0.01
        ax[0].plot(data["fused-proba-dt"], data["elec-val-s"], "g", linewidth="1", label="Elec (W*.01)")
        data["wifi-val-s"] = data["wifi-val"]*10
        ax[0].plot(data["fused-proba-dt"], data["wifi-val-s"], "b", linewidth="1", label="Wifi (counts*10)")
        ax[0].plot(data["fused-proba-dt"], data["co2-val"], "r", linewidth="1", label="CO2 (ppm)")
    ax[0].legend(loc="upper right", fontsize=legs)
    ax[0].set_title("Raw Sensor Input: " + in_type)
    ax[0].set_ylabel("Sensor Value", fontsize=labs)
    ax[0].xaxis.set_major_locator(mdates.HourLocator(byhour=hrtx))
    ax[0].xaxis.set_major_formatter(mdates.DateFormatter("%a %H:%M"))
    ax[0].xaxis.set_tick_params(labelsize=labs)
    ax[0].yaxis.set_tick_params(labelsize=labs)
    ax[0].grid(b=True, which='major', color='#666666', linestyle=':', linewidth=1, alpha=0.8)
    # plot intermediates
    if (in_type=="elec"):
        ax[1].plot(data["fused-proba-dt"], data["elec-proba"], "g", linewidth="1", label="Elec (W)")
    elif (in_type=="wifi"):
        ax[1].plot(data["fused-proba-dt"], data["wifi-proba"], "b", linewidth="1", label="Wifi (counts)")
    elif (in_type=="co2"):
        ax[1].plot(data["fused-proba-dt"], data["co2-proba"], "r", linewidth="1", label="CO2 (ppm)")
    elif (in_type=="comp"):
        ax[1].plot(data["fused-proba-dt"], data["elec-proba"], "g", linewidth="1", label="Elec (%)")
        ax[1].plot(data["fused-proba-dt"], data["wifi-proba"], "b", linewidth="1", label="Wifi (%)")
        ax[1].plot(data["fused-proba-dt"], data["co2-proba"], "r", linewidth="1", label="CO2 (%)")
    ax[1].set_ylim([0,1.2])
    ax[1].legend(loc="upper right", fontsize=legs)
    ax[1].set_title("Intermediate Probability of Vacancy")
    ax[1].set_ylabel("Probability of Vacancy (%)", fontsize=labs)
    ax[1].xaxis.set_major_locator(mdates.HourLocator(byhour=hrtx))
    ax[1].xaxis.set_major_formatter(mdates.DateFormatter("%a %H:%M"))
    ax[1].xaxis.set_tick_params(labelsize=labs)
    ax[1].yaxis.set_tick_params(labelsize=labs)
    ax[1].grid(b=True, which='major', color='#666666', linestyle=':', linewidth=1, alpha=0.8)
    fig.autofmt_xdate()
    fig.suptitle("Raw Sensor Input vs Intermediate Probability of Vacancy: " + in_type, fontsize=18, fontweight="bold")
    fig.savefig("Figures\\" + params.buildtype + "\\" + params.traintype + "\\Intermediates vs Inputs-" + in_type + "_" + sufx + ".png", format='png', bbox_inches='tight')
    plt.close(fig)
    return

def PlotMidsNOut(data, in_type, sufx, hrtx, params):
    fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(20,10))
    # plot intermediates
    if (in_type=="elec"):
        ax[0].plot(data["fused-proba-dt"], data["elec-proba"], "g", linewidth="1", label="Elec (%)")
    elif (in_type=="wifi"):
        ax[0].plot(data["fused-proba-dt"], data["wifi-proba"], "b", linewidth="1", label="Wifi (%)")
    elif (in_type=="co2"):
        ax[0].plot(data["fused-proba-dt"], data["co2-proba"], "r", linewidth="1", label="CO2 (%)")
    elif (in_type=="comp"):
        ax[0].plot(data["fused-proba-dt"], data["elec-proba"], "g", linewidth="1", label="Elec (%)")
        ax[0].plot(data["fused-proba-dt"], data["wifi-proba"], "b", linewidth="1", label="Wifi (%)")
        ax[0].plot(data["fused-proba-dt"], data["co2-proba"], "r", linewidth="1", label="CO2 (%)")
    plt.ylim([0,1.2])
    ax[0].legend(loc="upper right", fontsize=legs)
    ax[0].set_title("Intermediate Probability of Vacancy: " + in_type)
    ax[0].set_ylabel("Probability of Vacancy (%)", fontsize=labs)
    ax[0].xaxis.set_major_locator(mdates.HourLocator(byhour=hrtx))
    ax[0].xaxis.set_major_formatter(mdates.DateFormatter("%a %H:%M"))
    ax[0].xaxis.set_tick_params(labelsize=labs)
    ax[0].yaxis.set_tick_params(labelsize=labs)
    ax[0].grid(b=True, which='major', color='#666666', linestyle=':', linewidth=1, alpha=0.8)
    # plot fusion result
    ax[1].plot(data["fused-proba-dt"], data["fused-proba-" + params.fusetype], color="xkcd:pumpkin", linewidth="1", label="Fused: " + params.fusetype + " (%)")
    ax[1].set_ylim([0,1.2])
    ax[1].legend(loc="upper right", fontsize=legs)
    ax[1].set_title("Fused Probability of Vacancy")
    ax[1].set_ylabel("Probability of Vacancy (%)", fontsize=labs)
    ax[1].xaxis.set_major_locator(mdates.HourLocator(byhour=hrtx))
    ax[1].xaxis.set_major_formatter(mdates.DateFormatter("%a %H:%M"))
    ax[1].xaxis.set_tick_params(labelsize=labs)
    ax[1].yaxis.set_tick_params(labelsize=labs)
    ax[1].grid(b=True, which='major', color='#666666', linestyle=':', linewidth=1, alpha=0.8)
    fig.autofmt_xdate()
    fig.suptitle("Intermediate Probability of Vacancy vs. Fused Probability of Vacancy", fontsize=18, fontweight="bold")
    fig.savefig("Figures\\" + params.buildtype + "\\" + params.traintype + "\\" + params.fusetype + "\\Intermediates vs Output-" + in_type + "_" + sufx + ".png", format='png', bbox_inches='tight')
    plt.close(fig)
    return

def PlotInsNOut(data, in_type, sufx, hrtx, params):
    # plot inputs
    fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(20,10))
    if (in_type=="elec"):
        ax[0].plot(data["fused-proba-dt"], data["elec-val"], "g", linewidth="1", label="Elec (W)")
    elif (in_type=="wifi"):
        ax[0].plot(data["fused-proba-dt"], data["wifi-val"], "b", linewidth="1", label="Wifi (counts)")
    elif (in_type=="co2"):
        ax[0].plot(data["fused-proba-dt"], data["co2-val"], "r", linewidth="1", label="CO2 (ppm)")
    elif (in_type=="comp"):
        data["elec-val-s"] = data["elec-val"]*0.01
        ax[0].plot(data["fused-proba-dt"], data["elec-val-s"], "g", linewidth="1", label="Elec (W*.01)")
        data["wifi-val-s"] = data["wifi-val"]*10
        ax[0].plot(data["fused-proba-dt"], data["wifi-val-s"], "b", linewidth="1", label="Wifi (counts*10)")
        ax[0].plot(data["fused-proba-dt"], data["co2-val"], "r", linewidth="1", label="CO2 (ppm)")
    ax[0].legend(loc="upper right", fontsize=legs)
    ax[0].set_title("Raw Sensor Input: " + in_type)
    ax[0].set_ylabel("Sensor Value", fontsize=labs)
    ax[0].xaxis.set_major_locator(mdates.HourLocator(byhour=hrtx))
    ax[0].xaxis.set_major_formatter(mdates.DateFormatter("%a %H:%M"))
    ax[0].xaxis.set_tick_params(labelsize=labs)
    ax[0].yaxis.set_tick_params(labelsize=labs)
    ax[0].grid(b=True, which='major', color='#666666', linestyle=':', linewidth=1, alpha=0.8)
    # plot fusion result
    ax[1].plot(data["fused-proba-dt"], data["fused-proba-" + params.fusetype], color="xkcd:pumpkin", linewidth="1", label="Fused: " + params.fusetype + " (%)")
    ax[1].set_ylim([0,1.2])
    ax[1].legend(loc="upper right", fontsize=legs)
    ax[1].set_title("Fused Probability of Vacancy")
    ax[1].set_ylabel("Probability of Vacancy (%)", fontsize=labs)
    ax[1].xaxis.set_major_locator(mdates.HourLocator(byhour=hrtx))
    ax[1].xaxis.set_major_formatter(mdates.DateFormatter("%a %H:%M"))
    ax[1].xaxis.set_tick_params(labelsize=labs)
    ax[1].yaxis.set_tick_params(labelsize=labs)
    ax[1].grid(b=True, which='major', color='#666666', linestyle=':', linewidth=1, alpha=0.8)
    fig.autofmt_xdate()
    fig.suptitle("Raw Sensor Input vs Fused Probability of Vacancy", fontsize=18, fontweight="bold")
    fig.savefig("Figures\\" + params.fusetype + "\\" + params.buildtype + "\\" + params.traintype + "\\Output vs. Inputs-" + in_type + "_" + sufx + ".png", format='png', bbox_inches='tight')
    plt.close(fig)
    return

def PlotInsNTruth_2plots(data, in_type, sufx, hrtx, params):
    # plot inputs
    fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(20,10))
    if (in_type=="elec"):
        ax[0].plot(data["fused-proba-dt"], data["elec-val"], "g", linewidth="1", label="Elec (W)")
    elif (in_type=="wifi"):
        ax[0].plot(data["fused-proba-dt"], data["wifi-val"], "b", linewidth="1", label="Wifi (counts)")
    elif (in_type=="co2"):
        ax[0].plot(data["fused-proba-dt"], data["co2-val"], "r", linewidth="1", label="CO2 (ppm)")
    elif (in_type=="comp"):
        data["elec-val-s"] = data["elec-val"]*0.01
        ax[0].plot(data["fused-proba-dt"], data["elec-val-s"], "g", linewidth="1", label="Elec (W*.01)")
        data["wifi-val-s"] = data["wifi-val"]*10
        ax[0].plot(data["fused-proba-dt"], data["wifi-val-s"], "b", linewidth="1", label="Wifi (counts*10)")
        ax[0].plot(data["fused-proba-dt"], data["co2-val"], "r", linewidth="1", label="CO2 (ppm)")
    ax[0].legend(loc="upper right", fontsize=legs)
    ax[0].set_title("Raw Sensor Input: " + in_type)
    ax[0].set_ylabel("Sensor Value", fontsize=labs)
    ax[0].xaxis.set_major_locator(mdates.HourLocator(byhour=hrtx))
    ax[0].xaxis.set_major_formatter(mdates.DateFormatter("%a %H:%M"))
    ax[0].xaxis.set_tick_params(labelsize=labs)
    ax[0].yaxis.set_tick_params(labelsize=labs)
    ax[0].grid(b=True, which='major', color='#666666', linestyle=':', linewidth=1, alpha=0.8)
    # plot ground truth
    ax[1].plot(data["fused-proba-dt"], data["truth-val"], "k", linewidth="1", label="Truth: 1=vac, 0=occ ")
    ax[1].set_ylim([0,1.2])
    ax[1].legend(loc="upper right", fontsize=legs)
    ax[1].set_title("Raw Sensor Input vs. Ground Truth")
    ax[1].set_ylabel("Probability of Vacancy (%)", fontsize=labs)
    ax[1].xaxis.set_major_locator(mdates.HourLocator(byhour=hrtx))
    ax[1].xaxis.set_major_formatter(mdates.DateFormatter("%a %H:%M"))
    ax[1].xaxis.set_tick_params(labelsize=labs)
    ax[1].yaxis.set_tick_params(labelsize=labs)
    ax[1].grid(b=True, which='major', color='#666666', linestyle=':', linewidth=1, alpha=0.8)
    fig.autofmt_xdate()
    fig.savefig("Figures\\" + params.buildtype + "\\Inputs vs. Truth" + "_" + in_type + "_2plots_" + sufx + ".png", format='png', bbox_inches='tight')
    plt.close(fig)
    return

def PlotInsNTruth_1plot(data, in_type, sufx, hrtx, params):
    # plot inputs
    fig, ax = plt.subplots(figsize=(20,10))
    if (in_type=="elec"):
        ax.plot(data["fused-proba-dt"], data["elec-val"], "g", linewidth="1", label="Elec (W)")
    elif (in_type=="wifi"):
        ax.plot(data["fused-proba-dt"], data["wifi-val"], "b", linewidth="1", label="Wifi (counts)")
    elif (in_type=="co2"):
        ax.plot(data["fused-proba-dt"], data["co2-val"], "r", linewidth="1", label="CO2 (ppm)")
    elif (in_type=="comp"):
        data["elec-val-s"] = data["elec-val"]*0.01
        ax.plot(data["fused-proba-dt"], data["elec-val-s"], "g", linewidth="1", label="Elec (W*.01)")
        data["wifi-val-s"] = data["wifi-val"]*10
        ax.plot(data["fused-proba-dt"], data["wifi-val-s"], "b", linewidth="1", label="Wifi (counts*10)")
        ax.plot(data["fused-proba-dt"], data["co2-val"], "r", linewidth="1", label="CO2 (ppm)")
    # plot ground truth
    ax.plot(data["fused-proba-dt"], data["truth-val"], "k", linewidth="1", label="Truth: high=vac, low=occ ")
    ax.legend(loc="upper right", fontsize=legs)
    ax.set_title("Ground Truth vs. Raw Sensor Input: " + in_type)
    ax.set_ylabel("Sensor Value", fontsize=labs)
    ax.xaxis.set_major_locator(mdates.HourLocator(byhour=hrtx))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%a %H:%M"))
    ax.xaxis.set_tick_params(labelsize=labs)
    ax.yaxis.set_tick_params(labelsize=labs)
    ax.grid(b=True, which='major', color='#666666', linestyle=':', linewidth=1, alpha=0.8)
    fig.savefig("Figures\\" + params.buildtype + "\\Inputs vs. Truth" + "_" + in_type + "_1plot_" + sufx + ".png", format='png', bbox_inches='tight')
    plt.close(fig)
    return

def PlotMidsNTruth_1plot(data, in_type, sufx, hrtx, params):
    fig, ax = plt.subplots(figsize=(20,10))
    # plot intermediates
    if (in_type=="elec"):
        ax.plot(data["fused-proba-dt"], data["elec-proba"], "g", linewidth="1", label="Elec (%)")
    elif (in_type=="wifi"):
        ax.plot(data["fused-proba-dt"], data["wifi-proba"], "b", linewidth="1", label="Wifi (%)")
    elif (in_type=="co2"):
        ax.plot(data["fused-proba-dt"], data["co2-proba"], "r", linewidth="1", label="CO2 (%)")
    elif (in_type=="comp"):
        ax.plot(data["fused-proba-dt"], data["elec-proba"], "g", linewidth="1", label="Elec (%)")
        ax.plot(data["fused-proba-dt"], data["wifi-proba"], "b", linewidth="1", label="Wifi (%)")
        ax.plot(data["fused-proba-dt"], data["co2-proba"], "r", linewidth="1", label="CO2 (%)")
    # plot ground truth
    ax.plot(data["fused-proba-dt"], data["truth-val"], "k", linewidth="1", label="Truth: 1=vac, 0=occ ")
    ax.set_ylim([0,1.2])
    ax.legend(loc="upper right", fontsize=legs)
    ax.set_title("Intermediate Probability of Vacancy vs. Ground Truth")
    ax.set_ylabel("Probability of Vacancy (%)", fontsize=labs)
    ax.xaxis.set_major_locator(mdates.HourLocator(byhour=hrtx))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%a %H:%M"))
    ax.xaxis.set_tick_params(labelsize=labs)
    ax.yaxis.set_tick_params(labelsize=labs)
    ax.grid(b=True, which='major', color='#666666', linestyle=':', linewidth=1, alpha=0.8)
    fig.autofmt_xdate()
    fig.savefig("Figures\\" + params.buildtype + "\\" + params.traintype + "\\Intermediates vs. Truth" + "_" + in_type + "_1plot_" + sufx + ".png", format='png', bbox_inches='tight')
    plt.close(fig)
    return

def PlotMidsNTruth_2plots(data, in_type, sufx, hrtx, params):
    # plot inputs
    fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(20,10))
    if (in_type=="elec"):
        ax[0].plot(data["fused-proba-dt"], data["elec-proba"], "g", linewidth="1", label="Elec (%)")
    elif (in_type=="wifi"):
        ax[0].plot(data["fused-proba-dt"], data["wifi-proba"], "b", linewidth="1", label="Wifi (%)")
    elif (in_type=="co2"):
        ax[0].plot(data["fused-proba-dt"], data["co2-proba"], "r", linewidth="1", label="CO2 (%)")
    elif (in_type=="comp"):
        ax[0].plot(data["fused-proba-dt"], data["elec-proba"], "g", linewidth="1", label="Elec (%)")
        ax[0].plot(data["fused-proba-dt"], data["wifi-proba"], "b", linewidth="1", label="Wifi (%)")
        ax[0].plot(data["fused-proba-dt"], data["co2-proba"], "r", linewidth="1", label="CO2 (%)")
    ax[0].legend(loc="upper right", fontsize=legs)
    ax[0].set_title("Raw Sensor Input: " + in_type)
    ax[0].set_ylabel("Sensor Value", fontsize=labs)
    ax[0].xaxis.set_major_locator(mdates.HourLocator(byhour=hrtx))
    ax[0].xaxis.set_major_formatter(mdates.DateFormatter("%a %H:%M"))
    ax[0].xaxis.set_tick_params(labelsize=labs)
    ax[0].yaxis.set_tick_params(labelsize=labs)
    ax[0].grid(b=True, which='major', color='#666666', linestyle=':', linewidth=1, alpha=0.8)
    # plot ground truth
    ax[1].plot(data["fused-proba-dt"], data["truth-val"], "k", linewidth="1", label="Truth: 1=vac, 0=occ ")
    ax[1].set_ylim([0,1.2])
    ax[1].legend(loc="upper right", fontsize=legs)
    ax[1].set_title("Raw Sensor Input vs. Ground Truth")
    ax[1].set_ylabel("Probability of Vacancy (%)", fontsize=labs)
    ax[1].xaxis.set_major_locator(mdates.HourLocator(byhour=hrtx))
    ax[1].xaxis.set_major_formatter(mdates.DateFormatter("%a %H:%M"))
    ax[1].xaxis.set_tick_params(labelsize=labs)
    ax[1].yaxis.set_tick_params(labelsize=labs)
    ax[1].grid(b=True, which='major', color='#666666', linestyle=':', linewidth=1, alpha=0.8)
    fig.autofmt_xdate()
    fig.savefig("Figures\\" + params.buildtype + "\\Inputs vs. Truth" + "_" + in_type + "_2plots_" + sufx + ".png", format='png', bbox_inches='tight')
    plt.close(fig)
    return

def PlotOutNTruth(data, sufx, hrtx, params):
    fig, ax = plt.subplots(figsize=(20,10))
    # plot fusion result
    ax.plot(data["fused-proba-dt"], data["fused-proba-" + params.fusetype], color="xkcd:pumpkin", linewidth="1", label="Fused: " + params.fusetype + " (%)")
    # plot ground truth
    ax.plot(data["fused-proba-dt"], data["truth-val"], "k", linewidth="1", label="Truth: 1=vac, 0=occ ")
    ax.set_ylim([0,1.2])
    ax.legend(loc="upper right", fontsize=legs)
    ax.set_title("Fused Probability of Vacancy vs. Ground Truth")
    ax.set_ylabel("Probability of Vacancy (%)", fontsize=labs)
    ax.xaxis.set_major_locator(mdates.HourLocator(byhour=hrtx))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%a %H:%M"))
    ax.xaxis.set_tick_params(labelsize=labs)
    ax.yaxis.set_tick_params(labelsize=labs)
    ax.grid(b=True, which='major', color='#666666', linestyle=':', linewidth=1, alpha=0.8)
    fig.autofmt_xdate()
    fig.savefig("Figures\\" + params.buildtype + "\\" + params.traintype + "\\" + params.fusetype + "\\Output vs. Truth" + "_" + sufx + ".png", format='png', bbox_inches='tight')
    plt.close(fig)
    return

def PlotInsNMidsNOutNTruth(data, in_type, sufx, hrtx, params):
    fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(20,10))
    # plot inputs
    if (in_type=="elec"):
        ax[0].plot(data["fused-proba-dt"], data["elec-val"], "g", linewidth="1", label="Elec (W)")
    elif (in_type=="wifi"):
        ax[0].plot(data["fused-proba-dt"], data["wifi-val"], "b", linewidth="1", label="Wifi (counts)")
    elif (in_type=="co2"):
        ax[0].plot(data["fused-proba-dt"], data["co2-val"], "r", linewidth="1", label="CO2 (ppm)")
    elif (in_type=="comp"):
        data["elec-val-s"] = data["elec-val"]*0.01
        ax[0].plot(data["fused-proba-dt"], data["elec-val-s"], "g", linewidth="1", label="Elec (W*.01)")
        data["wifi-val-s"] = data["wifi-val"]*10
        ax[0].plot(data["fused-proba-dt"], data["wifi-val-s"], "b", linewidth="1", label="Wifi (counts*10)")
        ax[0].plot(data["fused-proba-dt"], data["co2-val"], "r", linewidth="1", label="CO2 (ppm)")
    ax[0].legend(loc="upper right", fontsize=legs)
    ax[0].set_title("Raw Sensor Input: " + in_type)
    ax[0].set_ylabel("Sensor Value", fontsize=labs)
    ax[0].xaxis.set_major_locator(mdates.HourLocator(byhour=hrtx))
    ax[0].xaxis.set_major_formatter(mdates.DateFormatter("%a %H:%M"))
    ax[0].xaxis.set_tick_params(labelsize=labs)
    ax[0].yaxis.set_tick_params(labelsize=labs)
    ax[0].grid(b=True, which='major', color='#666666', linestyle=':', linewidth=1, alpha=0.8)
    # plot intermediates
    if (in_type=="elec"):
        ax[1].plot(data["fused-proba-dt"], data["elec-proba"], "g", linewidth="1", label="Elec (%)")
    elif (in_type=="wifi"):
        ax[1].plot(data["fused-proba-dt"], data["wifi-proba"], "b", linewidth="1", label="Wifi (%)")
    elif (in_type=="co2"):
        ax[1].plot(data["fused-proba-dt"], data["co2-proba"], "r", linewidth="1", label="CO2 (%)")
    elif (in_type=="comp"):
        ax[1].plot(data["fused-proba-dt"], data["elec-proba"], "g", linewidth="1", label="Elec (%)")
        ax[1].plot(data["fused-proba-dt"], data["wifi-proba"], "b", linewidth="1", label="Wifi (%)")
        ax[1].plot(data["fused-proba-dt"], data["co2-proba"], "r", linewidth="1", label="CO2 (%)")
    
    ax[1].set_ylim([0,1.2])
    ax[1].legend(loc="upper right", fontsize=legs)
    ax[1].set_title("Intermediate Probability of Vacancy: " + in_type)
    ax[1].set_ylabel("Probability of Vacancy (%)", fontsize=labs)
    ax[1].xaxis.set_major_locator(mdates.HourLocator(byhour=hrtx))
    ax[1].xaxis.set_major_formatter(mdates.DateFormatter("%a %H:%M"))
    ax[1].xaxis.set_tick_params(labelsize=labs)
    ax[1].yaxis.set_tick_params(labelsize=labs)
    ax[1].grid(b=True, which='major', color='#666666', linestyle=':', linewidth=1, alpha=0.8)
    # plot fusion result
    ax[2].plot(data["fused-proba-dt"], data["fused-proba-" + params.fusetype], color="xkcd:pumpkin", linewidth="1", label="Fused: " + params.fusetype + " (%)")
    # Plot ground truth
    ax[2].plot(data["fused-proba-dt"], data["truth-val"], "k", linewidth="1", label="Truth: 1=vac, 0=occ ")
    ax[2].set_ylim([0,1.2])
    ax[2].legend(loc="upper right", fontsize=legs)
    ax[2].set_title("Fused Probability of Vacancy vs. Ground Truth")
    ax[2].set_ylabel("Probability of Vacancy (%)", fontsize=labs)
    ax[2].xaxis.set_major_locator(mdates.HourLocator(byhour=hrtx))
    ax[2].xaxis.set_major_formatter(mdates.DateFormatter("%a %H:%M"))
    ax[2].xaxis.set_tick_params(labelsize=labs)
    ax[2].yaxis.set_tick_params(labelsize=labs)
    ax[2].grid(b=True, which='major', color='#666666', linestyle=':', linewidth=1, alpha=0.8)
    fig.autofmt_xdate()
    fig.suptitle("Inputs, Intermediate Probability of Vacancy, and Fused Probability of Vacancy vs. Ground Truth", fontsize=18, fontweight="bold")
    fig.savefig("Figures\\" + params.buildtype + "\\" + params.traintype + "\\" + params.fusetype + "\\Ins-Mids-Out&GroundTruth_" + in_type + "_" + sufx + ".png", format='png', bbox_inches='tight')
    plt.close(fig)
    return

def PlotSigmoids(sensor, sensorvals, rawprobas, fitprobas):  
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(sensorvals, rawprobas, label="Raw")
    ax.plot(sensorvals, fitprobas, label="Generated")
    ax.legend(loc="upper right", fontsize=legs)
    ax.set_ylim([0,1.2])
    ax.set_xlim([min(sensorvals),max(sensorvals)])
    ax.xaxis.set_major_locator(plt.MaxNLocator(20))
    ax.xaxis.set_tick_params(labelsize=labs)
    ax.yaxis.set_tick_params(labelsize=labs)
    ax.set_title("Vacancy Relationship Accuracy for Sensor: " + sensor.sensorname, fontsize=18, fontweight="bold")
    ax.set_ylabel("Probability of Vacancy (%)", fontsize=labs)
    ax.set_xlabel("Raw Sensor Value", fontsize=labs)
    ax.grid(b=True, which='major', color='#666666', linestyle=':', linewidth=1, alpha=0.8)
    fig.savefig("Figures\\" + sensor.vacancyrelationship + "\\" + sensor.trainingdataset + "\\sigmoid-comparison-" + sensor.sensorname + ".png", format="png", bbox_inches="tight")
    plt.close(fig)
    return

def PlotExpit(sensor, x, y, train_data):
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(x, y, "b-", label="Expit Fit")
    ax.plot(train_data[sensor.sensorname + "-val"],train_data["truth-val"], "r.", label="Training Data")
    ax.legend(loc="upper right", fontsize=legs)
    ax.set_ylim([0,1.2])
    ax.set_xlim([0,max(train_data[sensor.sensorname + "-val"])])
    ax.xaxis.set_major_locator(plt.MaxNLocator(20))
    ax.xaxis.set_tick_params(labelsize=labs)
    ax.yaxis.set_tick_params(labelsize=labs)
    ax.set_title("Logistic Function Fit for Sensor: " + sensor.sensorname, fontsize=18, fontweight="bold")
    ax.set_ylabel("Probability of Vacancy (%)", fontsize=labs)
    ax.set_xlabel("Raw Sensor Value", fontsize=labs)
    ax.grid(b=True, which='major', color='#666666', linestyle=':', linewidth=1, alpha=0.8)
    fig.savefig("Figures\\" + sensor.vacancyrelationship + "\\" + sensor.trainingdataset + "\\Logistic-Fit-" + sensor.sensorname + ".png", format="png", bbox_inches="tight")
    plt.close(fig)
    return

def PlotInsNIns(data, sufx):
    # plot elec vs wifi
    fig, ax = plt.subplots(figsize=(20,10))
    ax.plot(data["wifi-val"], data["elec-val"], ".")
    ax.set_ylabel("Electricity Demand (W)", fontsize=labs)
    ax.set_xlabel("WiFi Connection Count", fontsize=labs)
    ax.xaxis.set_tick_params(labelsize=labs)
    ax.yaxis.set_tick_params(labelsize=labs)
    ax.grid(b=True, which='major', color='#666666', linestyle=':', linewidth=1, alpha=0.8)
    fig.suptitle("Independence Test: WiFi Connection Count vs. Electricity Demand", fontsize=18, fontweight="bold")
    fig.savefig("Figures\\Indep-Test_wifi_elec_" + sufx + ".png", format='png', bbox_inches='tight')
    plt.close(fig)

    # plot elec vs co2
    fig, ax = plt.subplots(figsize=(20,10))
    ax.plot(data["co2-val"], data["elec-val"], ".")
    ax.set_ylabel("Electricity Demand (W)", fontsize=labs)
    ax.set_xlabel("Carbon Dioxide Concentration (ppm)", fontsize=labs)
    ax.xaxis.set_tick_params(labelsize=labs)
    ax.yaxis.set_tick_params(labelsize=labs)
    ax.grid(b=True, which='major', color='#666666', linestyle=':', linewidth=1, alpha=0.8)
    fig.suptitle("Independence Test: Carbon Dioxide Concentration vs. Electricity Demand", fontsize=18, fontweight="bold")
    fig.savefig("Figures\\Indep-Test_co2_elec_" + sufx + ".png", format='png', bbox_inches='tight')
    plt.close(fig)

    # plot wifi vs co2
    fig, ax = plt.subplots(figsize=(20,10))
    ax.plot(data["wifi-val"], data["co2-val"], ".")
    ax.set_ylabel("Carbon Dioxide Concentration (ppm)", fontsize=labs)
    ax.set_xlabel("WiFi Connection Count", fontsize=labs)
    ax.xaxis.set_tick_params(labelsize=labs)
    ax.yaxis.set_tick_params(labelsize=labs)
    ax.grid(b=True, which='major', color='#666666', linestyle=':', linewidth=1, alpha=0.8)
    fig.suptitle("Independence Test: WiFi Connection Count vs. Carbon Dioxide Concentration", fontsize=18, fontweight="bold")
    fig.savefig("Figures\\Indep-Test_wifi_co2_" + sufx + ".png", format='png', bbox_inches='tight')
    plt.close(fig)
    return

#def PlotOutDistribution(data, fusetype, sufx, tick_hrs, build_type, train_set):
    #return

def PlotMain(in_type, start, end, save_suffix, params):
    tick_hrs = [0]
    historicaldata = pd.read_csv("DataFiles\\" + params.buildtype + "\\" + params.traintype + "\\" + params.fusetype + "\\VIE-historical-output.csv", parse_dates=["fused-proba-dt"])
    historicaldata.index = historicaldata["fused-proba-dt"]
    historicaldata = historicaldata.loc[start:end,:]
    #PlotIns(historicaldata, in_type, save_suffix, tick_hrs)
    #PlotInsNMids(historicaldata, in_type, save_suffix, tick_hrs, params)
    #PlotMidsNOut(historicaldata, in_type, save_suffix, tick_hrs, params)
    #PlotInsNOut(historicaldata, in_type, save_suffix, tick_hrs, params)
    #PlotInsNTruth_1plot(historicaldata, in_type, save_suffix, tick_hrs, params) # need to scale ground truth
    #PlotInsNTruth_2plots(historicaldata, in_type, save_suffix, tick_hrs, params)
    #PlotMidsNTruth_1plot(historicaldata, in_type, save_suffix, tick_hrs, params)
    #PlotMidsNTruth_2plots(historicaldata, in_type, save_suffix, tick_hrs, params) # not working for some reason
    PlotOutNTruth(historicaldata, save_suffix, tick_hrs, params)
    #PlotInsNMidsNOutNTruth(historicaldata, in_type, save_suffix, tick_hrs, params)
    #PlotOutputDistribution(historicaldata, save_suffix, tick_hrs, params)
    return

def IndependenceTest():
    trainingdata_e = pd.read_csv("DataFiles\\Logistic\\Cherry\\Training_Data_elec.csv", parse_dates=["timestamp"])
    trainingdata_e.index = trainingdata_e["timestamp"]
    trainingdata_c = pd.read_csv("DataFiles\\Logistic\\Cherry\\Training_Data_co2.csv", parse_dates=["timestamp"])
    trainingdata_c.index = trainingdata_c["timestamp"]
    trainingdata_w = pd.read_csv("DataFiles\\Logistic\\Cherry\\Training_Data_wifi.csv", parse_dates=["timestamp"])
    trainingdata_w.index = trainingdata_w["timestamp"]
    trainingdata = pd.concat([trainingdata_e["elec-val"],trainingdata_c["co2-val"],trainingdata_w["wifi-val"]], axis=1, join="inner", sort=True)
    PlotInsNIns(trainingdata,"Cherry")

    trainingdata_e = pd.read_csv("DataFiles\\Logistic\\Full\\Training_Data_elec.csv", parse_dates=["timestamp"])
    trainingdata_e.index = trainingdata_e["timestamp"]
    trainingdata_c = pd.read_csv("DataFiles\\Logistic\\Full\\Training_Data_co2.csv", parse_dates=["timestamp"])
    trainingdata_c.index = trainingdata_c["timestamp"]
    trainingdata_w = pd.read_csv("DataFiles\\Logistic\\Full\\Training_Data_wifi.csv", parse_dates=["timestamp"])
    trainingdata_w.index = trainingdata_w["timestamp"]
    trainingdata = pd.concat([trainingdata_e["elec-val"],trainingdata_c["co2-val"],trainingdata_w["wifi-val"]], axis=1, join="inner", sort=True)
    PlotInsNIns(trainingdata,"Full")
    return

def PlotOutcomeExplanation():
    # Generate the fake data
    data = pd.read_csv("DataFiles\\outcome-illustration.csv", parse_dates=["timestamp"])
    data.index = data["timestamp"]
    hrtx = [0,2,4,6,8,10,12,14,16,18,20,22]
    fig, ax = plt.subplots(figsize=(20,10))
    ax.plot(data["timestamp"], data["fused-val"] + 1.5, color="xkcd:pumpkin", linewidth="2", label="VIE Output")
    ax.plot(data["timestamp"], data["truth-val"], "k", linewidth="2", label="Ground Truth")
    #ax.legend(loc="upper right", fontsize=legs)
    ax.xaxis.set_major_locator(mdates.HourLocator(byhour=hrtx))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%a %H:%M"))
    ax.xaxis.set_tick_params(labelsize=labs)
    ax.yaxis.set_tick_params(labelsize=labs)
    ax.grid(b=True, which='major', color='#666666', linestyle=':', linewidth=1, alpha=0.8)
    ax.yaxis.grid(False)
    fig.autofmt_xdate()
    fig.savefig("Figures\\Outcomes-Illustration.png", format='png', bbox_inches='tight')
    plt.close(fig)
    return

def CMCExplanation():
    # Generate the fake data
    data = pd.read_csv("DataFiles\\CMC-illustration.csv")
    fig, ax = plt.subplots(nrows=1, ncols=2,figsize=(12,5))
    ax[0].plot(data["MOR"], data["COR"], "k", linewidth="2", label="Perfect Model")
    ax[0].xaxis.set_tick_params(labelsize=labs)
    ax[0].yaxis.set_tick_params(labelsize=labs)
    ax[0].set_xlabel("False Negative Rate: FN/(TP + FN)")
    ax[0].set_ylabel("False Positive Rate: FP/(FP + TN)")
    ax[0].set_title("CMC Example: Perfect Model")
    ax[0].grid(b=True, which='major', color='#666666', linestyle=':', linewidth=1, alpha=0.8)
    ax[1].plot(data["random"], 1-data["random"], "k", linewidth="2", label="Random Chance")
    ax[1].xaxis.set_tick_params(labelsize=labs)
    ax[1].yaxis.set_tick_params(labelsize=labs)
    ax[1].set_xlabel("False Negative Rate: FN/(TP + FN)")
    ax[1].set_ylabel("False Positive Rate: FP/(FP + TN)")
    ax[1].set_title("CMC Example: Random Chance")
    ax[1].grid(b=True, which='major', color='#666666', linestyle=':', linewidth=1, alpha=0.8)
    fig.savefig("Figures\\CMC-Illustration.png", format='png', bbox_inches='tight')
    plt.close(fig)
    return

def ROCExplanation():
    # Generate the fake data
    data = pd.read_csv("DataFiles\\ROC-illustration.csv")
    fig, ax = plt.subplots(nrows=1, ncols=2,figsize=(12,5))
    ax[0].plot(data["COR"], data["VAD"], "k", linewidth="2", label="Perfect Model")
    ax[0].xaxis.set_tick_params(labelsize=labs)
    ax[0].yaxis.set_tick_params(labelsize=labs)
    ax[0].set_xlabel("False Positive Rate: FP/(FP + TN)")
    ax[0].set_ylabel("True Positive Rate: TP/(TP + FN)")
    ax[0].set_title("ROC Example: Perfect Model")
    ax[0].grid(b=True, which='major', color='#666666', linestyle=':', linewidth=1, alpha=0.8)
    ax[1].plot(data["random"], data["random"], "k", linewidth="2", label="Random Chance")
    ax[1].xaxis.set_tick_params(labelsize=labs)
    ax[1].yaxis.set_tick_params(labelsize=labs)
    ax[1].set_xlabel("False Positive Rate: FP/(FP + TN)")
    ax[1].set_ylabel("True Positive Rate: TP/(TP + FN)")
    ax[1].set_title("ROC Example: Random Chance")
    ax[1].grid(b=True, which='major', color='#666666', linestyle=':', linewidth=1, alpha=0.8)
    fig.savefig("Figures\\ROC-Illustration.png", format='png', bbox_inches='tight')
    plt.close(fig)
    return

def PlotCampusDemand():
    data = pd.read_csv("DataFiles\\elec_raw.csv", parse_dates=["timestamp"])
    #data.index = data["timestamp"]
    hrtx = [0,12]
    fig, ax = plt.subplots(figsize=(16,8))
    x = data["timestamp"]
    #y = data["net"]/1000
    y = data["elec"]
    ax.plot(x, y, "k", linewidth="1")
    ax.xaxis.set_major_locator(mdates.HourLocator(byhour=hrtx))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%a %H:%M"))
    ax.xaxis.set_tick_params(labelsize=labs)
    ax.yaxis.set_tick_params(labelsize=labs)
    ax.grid(b=True, which='major', color='#666666', linestyle=':', linewidth=1, alpha=0.8)
    ax.yaxis.grid(False)
    ax.set_ylim(bottom=0)
    ax.set_ylabel("Electricity Demand (kW)")
    ax.set_title("Roessler Hall Electricity Demand", fontsize=16)
    #fig.autofmt_xdate()
    fig.savefig("Campus-Energy.png", format='png', bbox_inches='tight')
    plt.close(fig)
    return

def PlotInputsExample():
    # plot co2
    data = pd.read_csv("DataFiles\\WCEC-inputs-10min.csv", parse_dates=["timestamp"])
    data.index = data["timestamp"]
    data = data.loc["2019-07-08 00:00:00":"2019-07-16 00:00:00",:]
    hrtx = [0,8,17]

    fig, ax = plt.subplots(nrows=4, ncols=1, figsize=(20,10))
    ax[0].plot(data["timestamp"], data["co2"], "r", linewidth="1", label="CO2 (ppm)")
    #ax[0].plot(data["timestamp"], data["hours"]*max(data["co2"])+min(data["co2"]), "k", linewidth="1", label="Business Hours")
    ax[0].set_ylabel("Carbon Dioxide (ppm)", fontsize=labs)
    ax[0].xaxis.set_major_locator(mdates.HourLocator(byhour=hrtx))
    ax[0].xaxis.set_major_formatter(mdates.DateFormatter("%a %H:%M"))
    ax[0].xaxis.set_tick_params(labelsize=labs)
    ax[0].yaxis.set_tick_params(labelsize=labs)
    ax[0].grid(b=True, which='major', color='#666666', linestyle=':', linewidth=1, alpha=0.8)

    # plot elec    
    ax[1].plot(data["timestamp"], data["wifi"], "b", linewidth="1", label="Wi-Fi connections")
    #ax[1].plot(data["timestamp"], data["hours"]*max(data["elec"])+min(data["elec"]), "k", linewidth="1", label="Business Hours")
    ax[1].set_ylabel("Wi-Fi Connections", fontsize=labs)
    ax[1].xaxis.set_major_locator(mdates.HourLocator(byhour=hrtx))
    ax[1].xaxis.set_major_formatter(mdates.DateFormatter("%a %H:%M"))
    ax[1].xaxis.set_tick_params(labelsize=labs)
    ax[1].yaxis.set_tick_params(labelsize=labs)
    ax[1].grid(b=True, which='major', color='#666666', linestyle=':', linewidth=1, alpha=0.8)

    # plot wifi
    ax[2].plot(data["timestamp"], data["temp"], "m", linewidth="1", label="Temperature (°F)")
    #ax[2].plot(data["timestamp"], data["hours"]*max(data["wifi"])+min(data["wifi"]), "k", linewidth="1", label="Business Hours")
    ax[2].set_ylabel("Temperature (°F)", fontsize=labs)
    ax[2].xaxis.set_major_locator(mdates.HourLocator(byhour=hrtx))
    ax[2].xaxis.set_major_formatter(mdates.DateFormatter("%a %H:%M"))
    ax[2].xaxis.set_tick_params(labelsize=labs)
    ax[2].yaxis.set_tick_params(labelsize=labs)
    ax[2].grid(b=True, which='major', color='#666666', linestyle=':', linewidth=1, alpha=0.8)

    # plot temp
    ax[3].plot(data["timestamp"], data["rh"], "c", linewidth="1", label="Relative Humidity (%)")
    #ax[3].plot(data["timestamp"], data["hours"]*max(data["temp"])-min(data["temp"]), "k", linewidth="1", label="Business Hours")
    ax[3].set_ylabel("Relative Humidity (%)", fontsize=labs)
    ax[3].xaxis.set_major_locator(mdates.HourLocator(byhour=hrtx))
    ax[3].xaxis.set_major_formatter(mdates.DateFormatter("%a %H:%M"))
    ax[3].xaxis.set_tick_params(labelsize=labs)
    ax[3].yaxis.set_tick_params(labelsize=labs)
    ax[3].grid(b=True, which='major', color='#666666', linestyle=':', linewidth=1, alpha=0.8)
    
    #fig.legend(loc="upper right", fontsize=legs)
    fig.autofmt_xdate()
    fig.savefig("Inputs-Example.png", format='png', bbox_inches='tight')
    plt.close(fig)
    return


#IndependenceTest()
#PlotOutcomeExplanation()
#CMCExplanation()
#ROCExplanation()
#PlotCampusDemand()
PlotInputsExample()