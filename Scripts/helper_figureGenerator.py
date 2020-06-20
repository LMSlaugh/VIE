# Author: Lisa Slaughter <lisa.m.slaughter@gmail.com>
# Last update: May 02, 2019

# Allows for generating diagnostic figures of the data as it progresses through the model and predict process.

# ----------------------------------------------------------------------------------------------------------
import pandas as pd
import numpy as np
import math as math
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

titlesz = 14
labs = 11 # figure label size
legs = 11

def PlotIns(data, in_type, sufx, hrtx):
    # Plots sensor inputs against time; single axis
    fig, ax = plt.subplots(figsize=(8,8))
    if (in_type=="Elec"):
        ax.plot(data["fused-proba-dt"], data["Elec-val"]/1000, "g", linewidth="1", label="Elec (kW)")
    elif (in_type=="WiFi"):
        ax.plot(data["fused-proba-dt"], data["WiFi-val"], "b", linewidth="1", label="Wifi (counts)")
    elif (in_type=="CO2"):
        ax.plot(data["fused-proba-dt"], data["CO2-val"], "r", linewidth="1", label="CO2 (ppm)")
    elif (in_type=="comp"):
        data["Elec-val-s"] = data["Elec-val"]*0.01
        ax.plot(data["fused-proba-dt"], data["Elec-val-s"], "g", linewidth="1", label="Elec (W*.01)")
        data["WiFi-val-s"] = data["WiFi-val"]*10
        ax.plot(data["fused-proba-dt"], data["WiFi-val-s"], "b", linewidth="1", label="Wifi (counts*10)")
        ax.plot(data["fused-proba-dt"], data["CO2-val"], "r", linewidth="1", label="CO2 (ppm)")
    ax.legend(loc="upper right", fontsize=legs)
    ax.set_ylabel("Sensor Value", fontsize=labs)
    ax.xaxis.set_major_locator(mdates.HourLocator(byhour=hrtx))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%a %H:%M"))
    ax.xaxis.set_tick_params(labelsize=labs)
    ax.yaxis.set_tick_params(labelsize=labs)
    ax.grid(b=True, which='major', color='#666666', linestyle=':', linewidth=1, alpha=0.8)
    fig.autofmt_xdate()
    fig.suptitle("Raw Sensor Input: " + in_type, fontsize=titlesz, fontweight="bold")
    fig.savefig("Figures\\Input-" + in_type + "_" + sufx + ".png", format='png', bbox_inches='tight')
    plt.close(fig)
    return

def PlotInsNMids(data, in_type, sufx, hrtx, params):
    # Two plots, vertical arrangement.
    #   Upper plot: sensor inputs against time.
    #   Lower plot: probability of vacancy predicted by each sensor.
    fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(8,8))
    # plot inputs...
    if (in_type=="Elec"):
        ax[0].plot(data["fused-proba-dt"], data["Elec-val"], "g", linewidth="1", label="Elec (W)")
    elif (in_type=="WiFi"):
        ax[0].plot(data["fused-proba-dt"], data["WiFi-val"], "b", linewidth="1", label="Wifi (counts)")
    elif (in_type=="CO2"):
        ax[0].plot(data["fused-proba-dt"], data["CO2-val"], "r", linewidth="1", label="CO2 (ppm)")
    elif (in_type=="comp"):
        data["Elec-val-s"] = data["Elec-val"]*0.01
        ax[0].plot(data["fused-proba-dt"], data["Elec-val-s"], "g", linewidth="1", label="Elec (W*.01)")
        data["WiFi-val-s"] = data["WiFi-val"]*10
        ax[0].plot(data["fused-proba-dt"], data["WiFi-val-s"], "b", linewidth="1", label="Wifi (counts*10)")
        ax[0].plot(data["fused-proba-dt"], data["CO2-val"], "r", linewidth="1", label="CO2 (ppm)")
    ax[0].legend(loc="upper right", fontsize=legs)
    ax[0].set_title("Raw Sensor Input: " + in_type)
    ax[0].set_ylabel("Sensor Value", fontsize=labs)
    ax[0].xaxis.set_major_locator(mdates.HourLocator(byhour=hrtx))
    ax[0].xaxis.set_major_formatter(mdates.DateFormatter("%a %H:%M"))
    ax[0].xaxis.set_tick_params(labelsize=labs)
    ax[0].yaxis.set_tick_params(labelsize=labs)
    ax[0].grid(b=True, which='major', color='#666666', linestyle=':', linewidth=1, alpha=0.8)
    # plot intermediates...
    if (in_type=="Elec"):
        ax[1].plot(data["fused-proba-dt"], data["Elec-proba"], "g", linewidth="1", label="Elec (W)")
    elif (in_type=="WiFi"):
        ax[1].plot(data["fused-proba-dt"], data["WiFi-proba"], "b", linewidth="1", label="Wifi (counts)")
    elif (in_type=="CO2"):
        ax[1].plot(data["fused-proba-dt"], data["CO2-proba"], "r", linewidth="1", label="CO2 (ppm)")
    elif (in_type=="comp"):
        ax[1].plot(data["fused-proba-dt"], data["Elec-proba"], "g", linewidth="1", label="Elec (%)")
        ax[1].plot(data["fused-proba-dt"], data["WiFi-proba"], "b", linewidth="1", label="Wifi (%)")
        ax[1].plot(data["fused-proba-dt"], data["CO2-proba"], "r", linewidth="1", label="CO2 (%)")
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
    fig.suptitle("Raw Sensor Input vs Intermediate Probability of Vacancy: " + in_type, fontsize=titlesz, fontweight="bold")
    fig.savefig("Figures\\" + params.buildtype + "\\" + params.traintype + "\\Intermediates vs Inputs-" + in_type + "_" + sufx + ".png", format='png', bbox_inches='tight')
    plt.close(fig)
    return

def PlotMidsNOut(data, in_type, sufx, hrtx, params):
    # Two plots, vertical arrangement.
    #   Upper plot: probability of vacancy predicted by each sensor.
    #   Lower plot: fused probability of vacancy.
    fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(8,8))
    # plot intermediates
    if (in_type=="Elec"):
        ax[0].plot(data["fused-proba-dt"], data["Elec-proba"], "g", linewidth="1", label="Elec (%)")
    elif (in_type=="WiFi"):
        ax[0].plot(data["fused-proba-dt"], data["WiFi-proba"], "b", linewidth="1", label="Wifi (%)")
    elif (in_type=="CO2"):
        ax[0].plot(data["fused-proba-dt"], data["CO2-proba"], "r", linewidth="1", label="CO2 (%)")
    elif (in_type=="comp"):
        ax[0].plot(data["fused-proba-dt"], data["Elec-proba"], "g", linewidth="1", label="Elec (%)")
        ax[0].plot(data["fused-proba-dt"], data["WiFi-proba"], "b", linewidth="1", label="Wifi (%)")
        ax[0].plot(data["fused-proba-dt"], data["CO2-proba"], "r", linewidth="1", label="CO2 (%)")
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
    fig.suptitle("Intermediate Probability of Vacancy vs. Fused Probability of Vacancy", fontsize=titlesz, fontweight="bold")
    fig.savefig("Figures\\" + params.buildtype + "\\" + params.traintype + "\\" + params.fusetype + "\\Intermediates vs Output-" + in_type + "_" + sufx + ".png", format='png', bbox_inches='tight')
    plt.close(fig)
    return

def PlotInsNOut(data, in_type, sufx, hrtx, params):
    # Two plots, vertical arrangement.
    #   Upper plot: sensor inputs against time.
    #   Lower plot: fused probability of vacancy.
    fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(8,8))
    # plot inputs
    if (in_type=="Elec"):
        ax[0].plot(data["fused-proba-dt"], data["Elec-val"], "g", linewidth="1", label="Elec (W)")
    elif (in_type=="WiFi"):
        ax[0].plot(data["fused-proba-dt"], data["WiFi-val"], "b", linewidth="1", label="Wifi (counts)")
    elif (in_type=="CO2"):
        ax[0].plot(data["fused-proba-dt"], data["CO2-val"], "r", linewidth="1", label="CO2 (ppm)")
    elif (in_type=="comp"):
        data["Elec-val-s"] = data["Elec-val"]*0.01
        ax[0].plot(data["fused-proba-dt"], data["Elec-val-s"], "g", linewidth="1", label="Elec (W*.01)")
        data["WiFi-val-s"] = data["WiFi-val"]*10
        ax[0].plot(data["fused-proba-dt"], data["WiFi-val-s"], "b", linewidth="1", label="Wifi (counts*10)")
        ax[0].plot(data["fused-proba-dt"], data["CO2-val"], "r", linewidth="1", label="CO2 (ppm)")
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
    fig.suptitle("Raw Sensor Input vs Fused Probability of Vacancy", fontsize=titlesz, fontweight="bold")
    fig.savefig("Figures\\" + params.buildtype + "\\" + params.traintype + "\\" + params.fusetype + "\\Output vs. Inputs-" + in_type + "_" + sufx + ".png", format='png', bbox_inches='tight')
    plt.close(fig)
    return

def PlotInsNTruth_2plots(data, in_type, sufx, hrtx, params):
    # Two plots, vertical arrangement.
    #   Upper plot: sensor inputs against time.
    #   Lower plot: ground truth against time.
    fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(8,8))
    # plot inputs
    if (in_type=="Elec"):
        ax[0].plot(data["fused-proba-dt"], data["Elec-val"], "g", linewidth="1", label="Elec (W)")
    elif (in_type=="WiFi"):
        ax[0].plot(data["fused-proba-dt"], data["WiFi-val"], "b", linewidth="1", label="Wifi (counts)")
    elif (in_type=="CO2"):
        ax[0].plot(data["fused-proba-dt"], data["CO2-val"], "r", linewidth="1", label="CO2 (ppm)")
    elif (in_type=="comp"):
        data["Elec-val-s"] = data["Elec-val"]*0.01
        ax[0].plot(data["fused-proba-dt"], data["Elec-val-s"], "g", linewidth="1", label="Elec (W*.01)")
        data["WiFi-val-s"] = data["WiFi-val"]*10
        ax[0].plot(data["fused-proba-dt"], data["WiFi-val-s"], "b", linewidth="1", label="Wifi (counts*10)")
        ax[0].plot(data["fused-proba-dt"], data["CO2-val"], "r", linewidth="1", label="CO2 (ppm)")
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
    # Plots sensor inputs and ground truth against time.
    fig, ax = plt.subplots(figsize=(8,8))
    # plot inputs
    if (in_type=="Elec"):
        ax.plot(data["fused-proba-dt"], data["Elec-val"], "g", linewidth="1", label="Elec (W)")
    elif (in_type=="WiFi"):
        ax.plot(data["fused-proba-dt"], data["WiFi-val"], "b", linewidth="1", label="Wifi (counts)")
    elif (in_type=="CO2"):
        ax.plot(data["fused-proba-dt"], data["CO2-val"], "r", linewidth="1", label="CO2 (ppm)")
    elif (in_type=="comp"):
        data["Elec-val-s"] = data["Elec-val"]*0.01
        ax.plot(data["fused-proba-dt"], data["Elec-val-s"], "g", linewidth="1", label="Elec (W*.01)")
        data["WiFi-val-s"] = data["WiFi-val"]*10
        ax.plot(data["fused-proba-dt"], data["WiFi-val-s"], "b", linewidth="1", label="Wifi (counts*10)")
        ax.plot(data["fused-proba-dt"], data["CO2-val"], "r", linewidth="1", label="CO2 (ppm)")
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
    # Plots the probability of vacancy for each sensor and ground truth against time.
    fig, ax = plt.subplots(figsize=(8,8))
    # plot intermediates
    if (in_type=="Elec"):
        ax.plot(data["fused-proba-dt"], data["Elec-proba"], "g", linewidth="1", label="Elec (%)")
    elif (in_type=="WiFi"):
        ax.plot(data["fused-proba-dt"], data["WiFi-proba"], "b", linewidth="1", label="Wifi (%)")
    elif (in_type=="CO2"):
        ax.plot(data["fused-proba-dt"], data["CO2-proba"], "r", linewidth="1", label="CO2 (%)")
    elif (in_type=="comp"):
        ax.plot(data["fused-proba-dt"], data["Elec-proba"], "g", linewidth="1", label="Elec (%)")
        ax.plot(data["fused-proba-dt"], data["WiFi-proba"], "b", linewidth="1", label="Wifi (%)")
        ax.plot(data["fused-proba-dt"], data["CO2-proba"], "r", linewidth="1", label="CO2 (%)")
    # plot ground truth
    ax.plot(data["fused-proba-dt"], data["truth-val"], "k", linewidth="1", label="Truth: 1=vac, 0=occ ")
    ax.set_ylim([0,1.2])
    ax.legend(loc="upper right", fontsize=legs)
    ax.set_title("Intermediate Probability of Vacancy vs. Ground Truth", fontsize=titlesz, fontweight="bold")
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
    # Two plots, vertical arrangement.
    #   Upper plot: probability of vacancy predicted by each sensor against time.
    #   Lower plot: ground truth against time.
    fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(8,8))
    # plot inputs
    if (in_type=="Elec"):
        ax[0].plot(data["fused-proba-dt"], data["Elec-proba"], "g", linewidth="1", label="Elec (%)")
    elif (in_type=="WiFi"):
        ax[0].plot(data["fused-proba-dt"], data["WiFi-proba"], "b", linewidth="1", label="Wifi (%)")
    elif (in_type=="CO2"):
        ax[0].plot(data["fused-proba-dt"], data["CO2-proba"], "r", linewidth="1", label="CO2 (%)")
    elif (in_type=="comp"):
        ax[0].plot(data["fused-proba-dt"], data["Elec-proba"], "g", linewidth="1", label="Elec (%)")
        ax[0].plot(data["fused-proba-dt"], data["WiFi-proba"], "b", linewidth="1", label="Wifi (%)")
        ax[0].plot(data["fused-proba-dt"], data["CO2-proba"], "r", linewidth="1", label="CO2 (%)")
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
    # Plots the fused probability of vacancy and ground truth against time.
    fig, ax = plt.subplots(figsize=(8,8))
    # plot fusion result
    ax.plot(data["fused-proba-dt"], data["fused-proba-" + params.fusetype], color="xkcd:pumpkin", linewidth="1", label="Fused: " + params.fusetype + " (%)")
    # plot ground truth
    ax.plot(data["fused-proba-dt"], data["truth-val"], "k", linewidth="1", label="Truth: 1=vac, 0=occ ")
    ax.set_ylim([0,1.2])
    ax.legend(loc="upper right", fontsize=legs)
    ax.set_title("Fused Probability of Vacancy vs. Ground Truth", fontsize=titlesz, fontweight="bold")
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
    # Three plots, vertical arrangement.
    #   Upper plot: sensor inputs against time.
    #   Middle plot: probability of vacancy predicted by each sensor against time.
    #   Lower plot: fused probability of vacancy and ground truth against time.
    fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(8,8))
    # plot inputs
    if (in_type=="Elec"):
        ax[0].plot(data["fused-proba-dt"], data["Elec-val"]/1000, "g", linewidth="1", label="Elec (kW)")
    elif (in_type=="WiFi"):
        ax[0].plot(data["fused-proba-dt"], data["WiFi-val"], "b", linewidth="1", label="Wifi (counts)")
    elif (in_type=="CO2"):
        ax[0].plot(data["fused-proba-dt"], data["CO2-val"], "r", linewidth="1", label="CO2 (ppm)")
    elif (in_type=="comp"):
        data["Elec-val-s"] = data["Elec-val"]*0.01
        ax[0].plot(data["fused-proba-dt"], data["Elec-val-s"], "g", linewidth="1", label="Elec (W*.01)")
        data["WiFi-val-s"] = data["WiFi-val"]*10
        ax[0].plot(data["fused-proba-dt"], data["WiFi-val-s"], "b", linewidth="1", label="Wifi (counts*10)")
        ax[0].plot(data["fused-proba-dt"], data["CO2-val"], "r", linewidth="1", label="CO2 (ppm)")
    ax[0].legend(loc="upper right", fontsize=legs)
    ax[0].set_title("Raw Sensor Input: " + in_type)
    ax[0].set_ylabel("Sensor Value", fontsize=labs)
    ax[0].xaxis.set_major_locator(mdates.HourLocator(byhour=hrtx))
    ax[0].xaxis.set_major_formatter(mdates.DateFormatter("%a %H:%M"))
    ax[0].xaxis.set_tick_params(labelsize=labs)
    ax[0].yaxis.set_tick_params(labelsize=labs)
    ax[0].grid(b=True, which='major', color='#666666', linestyle=':', linewidth=1, alpha=0.8)
    # plot intermediates
    if (in_type=="Elec"):
        ax[1].plot(data["fused-proba-dt"], data["Elec-proba"], "g", linewidth="1", label="Elec (%)")
    elif (in_type=="WiFi"):
        ax[1].plot(data["fused-proba-dt"], data["WiFi-proba"], "b", linewidth="1", label="Wifi (%)")
    elif (in_type=="CO2"):
        ax[1].plot(data["fused-proba-dt"], data["CO2-proba"], "r", linewidth="1", label="CO2 (%)")
    elif (in_type=="comp"):
        ax[1].plot(data["fused-proba-dt"], data["Elec-proba"], "g", linewidth="1", label="Elec (%)")
        ax[1].plot(data["fused-proba-dt"], data["WiFi-proba"], "b", linewidth="1", label="Wifi (%)")
        ax[1].plot(data["fused-proba-dt"], data["CO2-proba"], "r", linewidth="1", label="CO2 (%)")
    
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
    fig.suptitle("Inputs, Intermediate Probability of Vacancy, and Fused Probability of Vacancy vs. Ground Truth", fontsize=titlesz, fontweight="bold")
    fig.savefig("Figures\\" + params.buildtype + "\\" + params.traintype + "\\" + params.fusetype + "\\Ins-Mids-Out&GroundTruth_" + in_type + "_" + sufx + ".png", format='png', bbox_inches='tight')
    plt.close(fig)
    return

def PlotSigmoids(sensor, sensorvals, rawprobas, fitprobas):
    # Plots the vacancy relationship for a single sensor stream generated using the percentile method
    # (aka sensor input value against probability of vacancy)
    fig, ax = plt.subplots(figsize=(8,5))
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
    ax.xaxis.set_major_locator(plt.MaxNLocator(10))
    ax.xaxis.set_tick_params(labelsize=labs)
    ax.yaxis.set_tick_params(labelsize=labs)
    sensorname = sensor.sensorname
    ax.set_ylabel("Confidence of Vacancy (%)", fontsize=labs)
    ax.set_title("Vacancy Relationship Accuracy for Sensor: " + sensor.sensorname, fontsize=titlesz)
    if sensor.sensortype=="wifi connections":
        ax.set_xlabel("Raw Sensor Value: WiFi Connections (count)", fontsize=labs)
    elif sensor.sensortype=="electricity demand":
        ax.set_xlabel("Raw Sensor Value: Electricity Demand (kW)", fontsize=labs)
    elif sensor.sensortype=="carbon dioxide":
        ax.set_xlabel(r"Raw Sensor Value: $\Delta$CO$_2$ (ppm)", fontsize=labs)
        ax.set_title(r"Vacancy Relationship Accuracy for Sensor: CO$_2$", fontsize=titlesz)

    ax.grid(b=True, which='major', color='#666666', linestyle=':', linewidth=1, alpha=0.8)
    fig.savefig("Figures\\" + sensor.vacancyrelationship + "\\" + sensor.trainingdataset + "\\sigmoid-comparison-" + sensor.sensorname + ".png", format="png", bbox_inches="tight")
    plt.close(fig)
    return

def PlotExpit(sensor, x, y, train_data):
    # Plots the vacancy relationship for a single sensor stream generated using the percentile method
    # (aka sensor input value against probability of vacancy)
    fig, ax = plt.subplots(figsize=(8,8))
    if sensor.sensortype=="electricity demand":
        x = x*.001
        x_raw = train_data[sensor.sensorname + "-val"]*.001
        ax.plot(x, y, "b-", label="Expit Fit")
        ax.plot(x_raw,train_data["truth-val"], "r.", label="Training Data")
        ax.set_xlim([0,max(train_data[sensor.sensorname + "-val"]/1000)])
    else:
        ax.plot(x, y, "b-", label="Expit Fit")
        ax.plot(train_data[sensor.sensorname + "-val"],train_data["truth-val"], "r.", label="Training Data")
        ax.set_xlim([0,max(train_data[sensor.sensorname + "-val"])])
    ax.legend(loc="upper right", fontsize=legs)
    ax.set_ylim([0,1.2])
    ax.xaxis.set_major_locator(plt.MaxNLocator(20))
    ax.xaxis.set_tick_params(labelsize=labs)
    ax.yaxis.set_tick_params(labelsize=labs)
    ax.set_title("Logistic Function Fit for Sensor: " + sensor.sensorname, fontsize=titlesz, fontweight="bold")
    ax.set_ylabel("Probability of Vacancy (%)", fontsize=labs)
    if sensor.sensortype=="wifi connections":
        ax.set_xlabel("Raw Sensor Value (counts)", fontsize=labs)
    elif sensor.sensortype=="electricity demand":
        ax.set_xlabel("Raw Sensor Value (kW)", fontsize=labs)
    elif sensor.sensortype=="carbon dioxide":
        ax.set_xlabel("Raw Sensor Value (ppm)", fontsize=labs)
    ax.grid(b=True, which='major', color='#666666', linestyle=':', linewidth=1, alpha=0.8)
    fig.savefig("Figures\\" + sensor.vacancyrelationship + "\\" + sensor.trainingdataset + "\\Logistic-Fit-" + sensor.sensorname + ".png", format="png", bbox_inches="tight")
    plt.close(fig)
    return

def PlotOutDistribution(data, fusetype, sufx, tick_hrs, build_type, train_set):
    # TODO: visualize the distribution of the ouput values.
    return

def PlotInsNIns(data, sufx):
    # Plots inputs against eachother to visualize degree of correlation

    # plot Elec vs WiFi
    fig, ax = plt.subplots(figsize=(8,8))
    ax.plot(data["WiFi-val"], data["Elec-val"], ".")
    ax.set_ylabel("Electricity Demand (W)", fontsize=labs)
    ax.set_xlabel("WiFi Connection Count", fontsize=labs)
    ax.xaxis.set_tick_params(labelsize=labs)
    ax.yaxis.set_tick_params(labelsize=labs)
    ax.grid(b=True, which='major', color='#666666', linestyle=':', linewidth=1, alpha=0.8)
    fig.suptitle("Independence Test: WiFi Connection Count vs. Electricity Demand", fontsize=titlesz, fontweight="bold")
    fig.savefig("Figures\\Indep-Test_wifi_elec_" + sufx + ".png", format='png', bbox_inches='tight')
    plt.close(fig)

    # plot Elec vs CO2
    fig, ax = plt.subplots(figsize=(8,8))
    ax.plot(data["CO2-val"], data["Elec-val"], ".")
    ax.set_ylabel("Electricity Demand (W)", fontsize=labs)
    ax.set_xlabel("Carbon Dioxide Concentration (ppm)", fontsize=labs)
    ax.xaxis.set_tick_params(labelsize=labs)
    ax.yaxis.set_tick_params(labelsize=labs)
    ax.grid(b=True, which='major', color='#666666', linestyle=':', linewidth=1, alpha=0.8)
    fig.suptitle("Independence Test: Carbon Dioxide Concentration vs. Electricity Demand", fontsize=titlesz, fontweight="bold")
    fig.savefig("Figures\\Indep-Test_co2_elec_" + sufx + ".png", format='png', bbox_inches='tight')
    plt.close(fig)

    # plot WiFi vs CO2
    fig, ax = plt.subplots(figsize=(8,8))
    ax.plot(data["WiFi-val"], data["CO2-val"], ".")
    ax.set_ylabel("Carbon Dioxide Concentration (ppm)", fontsize=labs)
    ax.set_xlabel("WiFi Connection Count", fontsize=labs)
    ax.xaxis.set_tick_params(labelsize=labs)
    ax.yaxis.set_tick_params(labelsize=labs)
    ax.grid(b=True, which='major', color='#666666', linestyle=':', linewidth=1, alpha=0.8)
    fig.suptitle("Independence Test: WiFi Connection Count vs. Carbon Dioxide Concentration", fontsize=titlesz, fontweight="bold")
    fig.savefig("Figures\\Indep-Test_wifi_co2_" + sufx + ".png", format='png', bbox_inches='tight')
    plt.close(fig)
    return

def IndependenceTest():
    # Visualizes degree of correlation between inputs
    trainingdata_e = pd.read_csv("DataFiles\\Logistic\\Cherry\\Training_Data_elec.csv", parse_dates=["timestamp"])
    trainingdata_e.index = trainingdata_e["timestamp"]
    trainingdata_c = pd.read_csv("DataFiles\\Logistic\\Cherry\\Training_Data_co2.csv", parse_dates=["timestamp"])
    trainingdata_c.index = trainingdata_c["timestamp"]
    trainingdata_w = pd.read_csv("DataFiles\\Logistic\\Cherry\\Training_Data_wifi.csv", parse_dates=["timestamp"])
    trainingdata_w.index = trainingdata_w["timestamp"]
    trainingdata = pd.concat([trainingdata_e["Elec-val"],trainingdata_c["CO2-val"],trainingdata_w["WiFi-val"]], axis=1, join="inner", sort=True)
    PlotInsNIns(trainingdata,"Cherry")

    trainingdata_e = pd.read_csv("DataFiles\\Logistic\\Full\\Training_Data_elec.csv", parse_dates=["timestamp"])
    trainingdata_e.index = trainingdata_e["timestamp"]
    trainingdata_c = pd.read_csv("DataFiles\\Logistic\\Full\\Training_Data_co2.csv", parse_dates=["timestamp"])
    trainingdata_c.index = trainingdata_c["timestamp"]
    trainingdata_w = pd.read_csv("DataFiles\\Logistic\\Full\\Training_Data_wifi.csv", parse_dates=["timestamp"])
    trainingdata_w.index = trainingdata_w["timestamp"]
    trainingdata = pd.concat([trainingdata_e["Elec-val"],trainingdata_c["CO2-val"],trainingdata_w["WiFi-val"]], axis=1, join="inner", sort=True)
    PlotInsNIns(trainingdata,"Full")
    return

def PlotOutcomeExplanation():
    # Generates a plot to describe the meaning of true positive, true negative, false positive, false negative.
    data = pd.read_csv("DataFiles\\Outcome-illustration.csv", parse_dates=["timestamp"])
    data.index = data["timestamp"]
    hrtx = [0,2,4,6,8,10,12,14,16,18,20,22]
    fig, ax = plt.subplots(figsize=(8,8))
    ax.plot(data["timestamp"], data["fused-val"] + 1.5, color="xkcd:pumpkin", linewidth=2, label="VIE Output")
    ax.plot(data["timestamp"], data["truth-val"], "k", linewidth=2, label="Ground Truth")
    ax.xaxis.set_major_locator(mdates.HourLocator(byhour=hrtx))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%a %H:%M"))
    ax.xaxis.set_tick_params(labelsize=labs)
    ax.yaxis.set_tick_params(labelsize=labs)
    ax.grid(b=True, which='major', color='#666666', linestyle=':', linewidth=1, alpha=0.8)
    ax.yaxis.grid(False)
    fig.autofmt_xdate()
    fig.savefig("Figures\\Outcome-Illustration.png", format='png', bbox_inches='tight')
    plt.close(fig)
    return

def CMCExplanation():
    # Shows the COR-MOR Characteristic curve of a perfectly good and of a perfectly bad model on a single plot.
    data = pd.read_csv("DataFiles\\CMC-illustration.csv")
    fig, ax = plt.subplots(figsize=(8,8))
    ax.plot(data["MOR"], data["COR"], "xkcd:pumpkin", linewidth=2, label="Perfect Model")
    ax.plot(data["random"], 1-data["random"], "b--", linewidth=2, label="Random Chance")
    ax.xaxis.set_tick_params(labelsize=labs)
    ax.yaxis.set_tick_params(labelsize=labs)
    ax.set_xlabel("False Negative Rate: FN/(TP + FN)", fontsize=labs)
    ax.set_ylabel("False Positive Rate: FP/(FP + TN)", fontsize=labs)
    ax.set_title("COR-MOR Characteristic (CMC) Curve: Extreme Examples", fontsize=titlesz)
    ax.legend(loc="best", fontsize=legs)
    ax.grid(b=True, which='major', color='#666666', linestyle=':', linewidth=1, alpha=0.8)
    fig.savefig("Figures\\CMC-Illustration.png", format='png', bbox_inches='tight')
    plt.close(fig)
    return

def ROCExplanation():
    # Shows the Receiver Operator Characteristic curve of a perfectly good and of a perfectly bad model on a single plot.
    data = pd.read_csv("DataFiles\\ROC-illustration.csv")
    fig, ax = plt.subplots(figsize=(8,8))
    ax.plot(data["COR"], data["VAD"], "xkcd:pumpkin", linewidth=2, label="Perfect Model")
    ax.plot(data["random"], data["random"], "b--", linewidth=2, label="Random Chance")
    ax.xaxis.set_tick_params(labelsize=labs)
    ax.yaxis.set_tick_params(labelsize=labs)
    ax.set_xlabel("False Positive Rate: FP/(FP + TN)", fontsize=labs)
    ax.set_ylabel("True Positive Rate: TP/(TP + FN)", fontsize=labs)
    ax.set_title("Receiver-Operating Characteristic (ROC) Curve: Extreme Examples", fontsize=titlesz)
    ax.legend(loc="best", fontsize=legs)
    ax.grid(b=True, which='major', color='#666666', linestyle=':', linewidth=1, alpha=0.8)
    fig.savefig("Figures\\ROC-Illustration.png", format='png', bbox_inches='tight')
    plt.close(fig)
    return

def PlotCampusDemand():
    # Plots an example of electricity demand and wifi cnxn count across the UC Davis campus
    data = pd.read_csv("DataFiles\\Building_campus_elec_wifi.csv", parse_dates=["timestamp"])
    hrtx = [0]
    fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(8,8))
    x = data["timestamp"]
    elec = data["Campus_Total_Electricity_Demand"]/1000
    wifi = data["AP.Campus Wide WIFI Count"]/1000
    ax[0].plot(x, elec, "g", linewidth=1, label="Demand (MW)")
    ax[0].xaxis.set_major_locator(mdates.HourLocator(byhour=hrtx))
    ax[0].xaxis.set_major_formatter(mdates.DateFormatter("%a %H:%M"))
    ax[0].xaxis.set_tick_params(labelsize=labs)
    ax[0].yaxis.set_tick_params(labelsize=labs)
    ax[0].grid(b=True, which='major', color='#666666', linestyle=':', linewidth=1, alpha=0.8)
    #ax[0].yaxis.grid(False)
    ax[0].set_ylim(bottom=15)
    ax[0].set_ylabel("Electricity\nDemand (MW)", fontsize=labs)
    #ax[0].set_title("UC Davis Campus-Wide Electricity Demand", fontsize=titlesz)

    ax[1].plot(x, wifi, "b", linewidth=1, label="WiFi (count)")
    ax[1].xaxis.set_major_locator(mdates.HourLocator(byhour=hrtx))
    ax[1].xaxis.set_major_formatter(mdates.DateFormatter("%a %H:%M"))
    ax[1].xaxis.set_tick_params(labelsize=labs)
    ax[1].yaxis.set_tick_params(labelsize=labs)
    ax[1].grid(b=True, which='major', color='#666666', linestyle=':', linewidth=1, alpha=0.8)
    #ax[1].yaxis.grid(False)
    ax[1].set_ylim(bottom=0)
    ax[1].set_ylabel("WiFi Connections (count x1000)", fontsize=labs)
    fig.suptitle("UC Davis Campus-Wide Electricity Demand vs. WiFi Connections", fontsize=titlesz)
    #fig.legend(loc="upper right", fontsize=legs)
    fig.autofmt_xdate()
    fig.savefig("Figures\\Campus-Energy.png", format='png', bbox_inches='tight')
    plt.close(fig)
    return

def PlotBuildingDemand():
    # Plots an example of electricity demand for a single building on the UC Davis campus
    data = pd.read_csv("DataFiles\\Building_campus_elec_wifi.csv", parse_dates=["timestamp"])
    hrtx = [0]
    fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(8,8))
    x = data["timestamp"]
    elec = data["Haring_Hall_TOTAL/Electricity_Demand"]
    wifi = data["AP.HARING_Total_Count"]
    ax[0].plot(x, elec, "g", linewidth=1, label="Demand (MW)")
    ax[0].xaxis.set_major_locator(mdates.HourLocator(byhour=hrtx))
    ax[0].xaxis.set_major_formatter(mdates.DateFormatter("%a %H:%M"))
    ax[0].xaxis.set_tick_params(labelsize=labs)
    ax[0].yaxis.set_tick_params(labelsize=labs)
    ax[0].grid(b=True, which='major', color='#666666', linestyle=':', linewidth=1, alpha=0.8)
    #ax[0].yaxis.grid(False)
    ax[0].set_ylim(bottom=140)
    ax[0].set_ylabel("Electricity Demand (kW)", fontsize=labs)
    #ax[0].set_title("UC Davis Campus-Wide Electricity Demand", fontsize=titlesz)

    ax[1].plot(x, wifi, "b", linewidth=1, label="WiFi (count)")
    ax[1].xaxis.set_major_locator(mdates.HourLocator(byhour=hrtx))
    ax[1].xaxis.set_major_formatter(mdates.DateFormatter("%a %H:%M"))
    ax[1].xaxis.set_tick_params(labelsize=labs)
    ax[1].yaxis.set_tick_params(labelsize=labs)
    ax[1].grid(b=True, which='major', color='#666666', linestyle=':', linewidth=1, alpha=0.8)
    #ax[1].yaxis.grid(False)
    ax[1].set_ylim(bottom=0)
    ax[1].set_ylabel("WiFi Connections (count)", fontsize=labs)
    fig.suptitle("Haring Hall Electricity Demand vs. WiFi Connections", fontsize=titlesz)
    #fig.legend(loc="upper right", fontsize=legs)
    fig.autofmt_xdate()
    fig.savefig("Figures\\Building-Energy.png", format='png', bbox_inches='tight')
    plt.close(fig)
    return

def PlotInputsExample():
    # Generates an example of sensor inputs against time for:
    #  Carbon dioxide
    #  Electricity demand
    #  Count of active wifi connections
    #  Air temperature
    #  Relative humidity

    # plot CO2
    data = pd.read_csv("DataFiles\\WCEC-inputs-10min_new.csv", parse_dates=["timestamp"])
    #data = pd.read_csv("DataFiles\\truncated_2.csv", parse_dates=["timestamp"])
    #data = pd.read_csv("DataFiles\\VIE-historical-input_WCEC.csv", parse_dates=["timestamp"])
    data.index = data["timestamp"]
    #data = data.loc["2019-07-08 00:00:00":"2019-07-16 00:00:00",:]
    #data = data[data.index.minute%10==0]
    #data.to_csv("DataFiles\\elecjunk.csv")
    hrtx = [8,17]
    fig, ax = plt.subplots(nrows=5, ncols=1, figsize=(8,8))
    ax[0].plot(data["timestamp"], data["co2"], "r", linewidth=1, label="CO2 (ppm)")
    ax[0].set_ylabel("Carbon\nDioxide (ppm)", fontsize=labs)
    ax[0].xaxis.set_major_locator(mdates.HourLocator(byhour=hrtx))
    ax[0].xaxis.set_major_formatter(mdates.DateFormatter("%a %H:%M"))
    ax[0].xaxis.set_tick_params(labelsize=labs)
    ax[0].yaxis.set_tick_params(labelsize=labs)
    ax[0].grid(b=True, which='major', color='#666666', linestyle=':', linewidth=1, alpha=0.8)

    # plot Elec
    ax[1].plot(data["timestamp"], data["elec_no_hvac"]/1000, "g", linewidth=1, label="Elec Demand (kW)")
    ax[1].set_ylabel("Electricity\nDemand\n(kW)", fontsize=labs)
    ax[1].xaxis.set_major_locator(mdates.HourLocator(byhour=hrtx))
    ax[1].xaxis.set_major_formatter(mdates.DateFormatter("%a %H:%M"))
    ax[1].xaxis.set_tick_params(labelsize=labs)
    ax[1].yaxis.set_tick_params(labelsize=labs)
    ax[1].grid(b=True, which='major', color='#666666', linestyle=':', linewidth=1, alpha=0.8)

    # plot Wifi
    ax[2].plot(data["timestamp"], data["wifi"], "b", linewidth=1, label="Wi-Fi connections")
    ax[2].set_ylabel("Wi-Fi\nConnections\n", fontsize=labs)
    ax[2].xaxis.set_major_locator(mdates.HourLocator(byhour=hrtx))
    ax[2].xaxis.set_major_formatter(mdates.DateFormatter("%a %H:%M"))
    ax[2].xaxis.set_tick_params(labelsize=labs)
    ax[2].yaxis.set_tick_params(labelsize=labs)
    ax[2].grid(b=True, which='major', color='#666666', linestyle=':', linewidth=1, alpha=0.8)

    # plot temp
    ax[3].plot(data["timestamp"], data["temp"], "m", linewidth=1, label="Temperature (°F)")
    ax[3].set_ylabel("Temperature\n(°F)\n", fontsize=labs)
    ax[3].xaxis.set_major_locator(mdates.HourLocator(byhour=hrtx))
    ax[3].xaxis.set_major_formatter(mdates.DateFormatter("%a %H:%M"))
    ax[3].xaxis.set_tick_params(labelsize=labs)
    ax[3].yaxis.set_tick_params(labelsize=labs)
    ax[3].grid(b=True, which='major', color='#666666', linestyle=':', linewidth=1, alpha=0.8)

    # plot Rh
    ax[4].plot(data["timestamp"], data["rh"], "c", linewidth=1, label="Relative Humidity (%)")
    ax[4].set_ylabel("Relative\nHumidity\n(%)", fontsize=labs)
    ax[4].xaxis.set_major_locator(mdates.HourLocator(byhour=hrtx))
    ax[4].xaxis.set_major_formatter(mdates.DateFormatter("%a %H:%M"))
    ax[4].xaxis.set_tick_params(labelsize=labs)
    ax[4].yaxis.set_tick_params(labelsize=labs)
    ax[4].grid(b=True, which='major', color='#666666', linestyle=':', linewidth=1, alpha=0.8)
    fig.suptitle("Potential Input Data: Weekly Pattern Exploration", fontsize=titlesz)
    fig.autofmt_xdate()
    fig.savefig("Figures\\Inputs-Example.png", format='png', bbox_inches='tight')
    plt.close(fig)
    return

def PlotOccupancyStepData():
    # Shows an example of a response in data due to a large step in occupancy
    data = pd.read_csv("DataFiles\\VIE-historical-input_WCEC_10min.csv", parse_dates=["timestamp"])
    data.index = data["timestamp"]
    data = data.loc["2019-07-23 07:00:00":"2019-07-23 19:00:00",:]
    hrtx = [0,2,4,6,8,10,12,14,16,18,20,22]
    
    fig, ax = plt.subplots(nrows=5, ncols=1, figsize=(7,8))
    ax[0].plot(data["timestamp"], data["CO2-val"], "r", linewidth=1, label="CO2 (ppm)")
    ax[0].set_ylabel("Carbon\nDioxide (ppm)", fontsize=labs, multialignment="center")
    ax[0].xaxis.set_major_locator(mdates.HourLocator(byhour=hrtx))
    ax[0].xaxis.set_major_formatter(mdates.DateFormatter("%a %H:%M"))
    ax[0].xaxis.set_tick_params(labelsize=labs)
    ax[0].yaxis.set_tick_params(labelsize=labs)
    ax[0].grid(b=True, which='major', color='#666666', linestyle=':', linewidth=1, alpha=0.8)

    # plot Elec    
    ax[1].plot(data["timestamp"], data["Elec-val"]/1000, "g", linewidth=1, label="Wi-Fi connections")
    ax[1].set_ylabel("Electricity\nDemand\n(kW)", fontsize=labs, multialignment="center")
    ax[1].xaxis.set_major_locator(mdates.HourLocator(byhour=hrtx))
    ax[1].xaxis.set_major_formatter(mdates.DateFormatter("%a %H:%M"))
    ax[1].xaxis.set_tick_params(labelsize=labs)
    ax[1].yaxis.set_tick_params(labelsize=labs)
    ax[1].grid(b=True, which='major', color='#666666', linestyle=':', linewidth=1, alpha=0.8)
    
    # plot WiFi    
    ax[2].plot(data["timestamp"], data["WiFi-val"], "b", linewidth=1, label="Wi-Fi connections")
    ax[2].set_ylabel("Wi-Fi\nConnections\n", fontsize=labs, multialignment="center")
    ax[2].xaxis.set_major_locator(mdates.HourLocator(byhour=hrtx))
    ax[2].xaxis.set_major_formatter(mdates.DateFormatter("%a %H:%M"))
    ax[2].xaxis.set_tick_params(labelsize=labs)
    ax[2].yaxis.set_tick_params(labelsize=labs)
    ax[2].grid(b=True, which='major', color='#666666', linestyle=':', linewidth=1, alpha=0.8)

    # plot Temp
    ax[3].plot(data["timestamp"], data["Max_T"], "m", linewidth=1, label="Temperature (°F)")
    ax[3].set_ylabel("Temperature\n(°F)", fontsize=labs, multialignment="center")
    ax[3].xaxis.set_major_locator(mdates.HourLocator(byhour=hrtx))
    ax[3].xaxis.set_major_formatter(mdates.DateFormatter("%a %H:%M"))
    ax[3].xaxis.set_tick_params(labelsize=labs)
    ax[3].yaxis.set_tick_params(labelsize=labs)
    ax[3].grid(b=True, which='major', color='#666666', linestyle=':', linewidth=1, alpha=0.8)

    # plot RH
    ax[4].plot(data["timestamp"], data["Max_RH"], "c", linewidth=1, label="Relative Humidity (%)")
    ax[4].set_ylabel("Relative\nHumidity\n(%)", fontsize=labs, multialignment="center")
    ax[4].xaxis.set_major_locator(mdates.HourLocator(byhour=hrtx))
    ax[4].xaxis.set_major_formatter(mdates.DateFormatter("%a %H:%M"))
    ax[4].xaxis.set_tick_params(labelsize=labs)
    ax[4].yaxis.set_tick_params(labelsize=labs)
    ax[4].grid(b=True, which='major', color='#666666', linestyle=':', linewidth=1, alpha=0.8)
    fig.suptitle("Potential Input Data: Response Exploration", fontsize=titlesz)
    fig.autofmt_xdate()
    fig.savefig("Figures\\Occupancy-Step-Example.png", format='png', bbox_inches='tight')
    plt.close(fig)
    return

def PlotElecSolar():
    # Shows how the electricity demand is affected by the ex/inclusion of rooftop solar generation
    data = pd.read_csv("DataFiles\\WCEC-Elec-my-way.csv", parse_dates=["Date"])
    data.index = data["Date"]
    data = data.loc["2019-03-11 00:00:00":"2019-03-12 00:00:00",:]
    hrtx = [0,2,4,6,8,10,12,14,16,18,20,22]
    
    # plot Elec, without solar
    fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(8,8))
    ax[0].plot(data["Date"], data["Total Demand (W)"]*.001, "g", linewidth=1)
    ax[0].set_ylabel("Electricity Demand (kW)", fontsize=labs)
    ax[0].xaxis.set_major_locator(mdates.HourLocator(byhour=hrtx))
    ax[0].xaxis.set_major_formatter(mdates.DateFormatter("%a %H:%M"))
    ax[0].xaxis.set_tick_params(labelsize=labs)
    ax[0].yaxis.set_tick_params(labelsize=labs)
    ax[0].grid(b=True, which='major', color='#666666', linestyle=':', linewidth=1, alpha=0.8)
    ax[0].set_title("Total Demand (solar generation excluded)")


    # plot Elec, with solar
    ax[1].plot(data["Date"], data["Net Demand (W)"]*0.001, "g", linewidth=1)
    ax[1].set_ylabel("Electricity Demand (kW)", fontsize=labs)
    ax[1].xaxis.set_major_locator(mdates.HourLocator(byhour=hrtx))
    ax[1].xaxis.set_major_formatter(mdates.DateFormatter("%a %H:%M"))
    ax[1].xaxis.set_tick_params(labelsize=labs)
    ax[1].yaxis.set_tick_params(labelsize=labs)
    ax[1].grid(b=True, which='major', color='#666666', linestyle=':', linewidth=1, alpha=0.8)
    ax[1].set_title("Net Demand (solar generation included)")
    fig.autofmt_xdate()
    fig.savefig("Figures\\Feature-Engineering-Example.png", format='png', bbox_inches='tight')
    plt.close(fig)
    return

def PlotElecHVAC():
    # Plots the electricity demand due to HVAC
    data = pd.read_csv("DataFiles\\WCEC-Elec-my-way.csv", parse_dates=["Date"])
    data.index = data["Date"]
    data = data.loc["2019-03-11 00:00:00":"2019-04-08 00:00:00",:]
    hrtx = [0,12]
    
    fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(8,8))
    ax[0].plot(data["Date"], data["Total Demand (W)"]*.001, "g", linewidth=1)
    ax[0].set_ylabel("Electricity Demand (kW)", fontsize=labs)
    ax[0].xaxis.set_major_locator(mdates.HourLocator(byhour=hrtx))
    ax[0].xaxis.set_major_formatter(mdates.DateFormatter("%a %H:%M"))
    ax[0].xaxis.set_tick_params(labelsize=labs)
    ax[0].yaxis.set_tick_params(labelsize=labs)
    ax[0].grid(b=True, which='major', color='#666666', linestyle=':', linewidth=1, alpha=0.8)
    ax[0].set_title("Total Demand, HVAC included")

    ax[1].plot(data["Date"], (data["Total Demand (W)"] + data["hvac"])*0.001, "g", linewidth=1)
    ax[1].set_ylabel("Electricity Demand (kW)", fontsize=labs)
    ax[1].xaxis.set_major_locator(mdates.HourLocator(byhour=hrtx))
    ax[1].xaxis.set_major_formatter(mdates.DateFormatter("%a %H:%M"))
    ax[1].xaxis.set_tick_params(labelsize=labs)
    ax[1].yaxis.set_tick_params(labelsize=labs)
    ax[1].grid(b=True, which='major', color='#666666', linestyle=':', linewidth=1, alpha=0.8)
    ax[1].set_title("Total Demand, HVAC excluded)")
    fig.autofmt_xdate()
    fig.savefig("Figures\\Elec-with-without-HVAC-Example.png", format='png', bbox_inches='tight')
    plt.close(fig)
    return

def PlotCOR_MORvsThreshComparison():
    # Plot (complaint opportunity rate) / (missed opportunity rate) against threshold ZOOMED <= 1 ONLY
    fig, ax = plt.subplots(figsize=(8,6))
    data = pd.read_csv("DataFiles\\CMC_comparison_logistic_percentile.csv")
    zmask = data["COR-MOR_percentile"]<=1

    ax.plot(data["threshold"][zmask], data["COR-MOR_percentile"][zmask], "r", label="Proposed Method")
    ax.plot(data["threshold"][zmask], data["COR-MOR_logistic"][zmask], "b", label="Logistic Regression")
    ax.plot(data["threshold"][zmask], data["COR-MOR_perfect"][zmask], "g--", label="Perfect Model")
    ax.set_title("Cost Valuation Ratio < 1 vs. Threshold", fontsize=labs)
    ax.set_xlabel("Threshold for Vacancy/Occupancy Determination (%)", fontsize=labs)
    ax.set_ylabel("Cost Valuation Ratio = COR/MOR = FP/FN", fontsize=labs)
    ax.xaxis.set_tick_params(labelsize=9)
    ax.yaxis.set_tick_params(labelsize=9)
    ax.grid(b=True, which='major', color='#666666', linestyle='-', linewidth=1, alpha=0.7)
    ax.grid(b=True, which='minor', color='#999999', linestyle='-', linewidth=1, alpha=0.2)
    ax.minorticks_on()
    ax.legend(loc="upper right", fontsize=legs)
    plt.grid(b=True, which='major', color='#666666', linestyle='-', linewidth=1, alpha=0.7)
    plt.grid(b=True, which='minor', color='#999999', linestyle='-', linewidth=1, alpha=0.2)
    fig.savefig("Figures\\COR_MOR_log_perc_comp-under_1.png", format="png", bbox_inches="tight")
    plt.close(fig)

    # Plot (complaint opportunity rate) / (missed opportunity rate) against threshold ZOOMED <= 1 ONLY, REVERSED AXES
    fig, ax = plt.subplots(figsize=(8,6))
    data = pd.read_csv("DataFiles\\CMC_comparison_logistic_percentile.csv")
    zmask = data["COR-MOR_percentile"]<=1

    ax.plot(data["COR-MOR_percentile"][zmask], data["threshold"][zmask], "r", label="Proposed Method")
    ax.plot(data["COR-MOR_logistic"][zmask], data["threshold"][zmask], "b", label="Logistic Regression")
    ax.plot(data["COR-MOR_perfect"][zmask], data["threshold"][zmask], "g--", label="Perfect Model")
    ax.set_title("Threshold vs. Cost Valuation Ratio < 1", fontsize=labs)
    ax.set_ylabel("Threshold for Vacancy/Occupancy Determination (%)", fontsize=labs)
    ax.set_xlabel("Cost Valuation Ratio = COR/MOR = FP/FN", fontsize=labs)
    ax.xaxis.set_tick_params(labelsize=9)
    ax.yaxis.set_tick_params(labelsize=9)
    ax.grid(b=True, which='major', color='#666666', linestyle='-', linewidth=1, alpha=0.7)
    ax.grid(b=True, which='minor', color='#999999', linestyle='-', linewidth=1, alpha=0.2)
    ax.minorticks_on()
    ax.legend(loc="upper right", fontsize=legs)
    plt.grid(b=True, which='major', color='#666666', linestyle='-', linewidth=1, alpha=0.7)
    plt.grid(b=True, which='minor', color='#999999', linestyle='-', linewidth=1, alpha=0.2)
    fig.savefig("Figures\\COR_MOR_log_perc_comp-under_1_switched_axes.png", format="png", bbox_inches="tight")
    plt.close(fig)
    return

def PlotROCComparison():
    # Plot .......
    fig, ax = plt.subplots(figsize=(8,6))
    data = pd.read_csv("DataFiles\\CMC_comparison_logistic_percentile.csv")

    COR_perc= data["ROC_x_percentile"]
    vacant_acc_perc = data["ROC_y_percentile"]
    ax.plot(COR_perc, vacant_acc_perc, "r", label="Proposed Method")
    n = round(len(COR_perc)-1, 0)
    step = int(round(n/10, 0))
    callout_locs = range(0,n+1,step)
    for val in callout_locs:
        if val==0:
            ax.plot(COR_perc.values[val], vacant_acc_perc.values[val], 'xr', label="Decision Thresholds")
        else:
            ax.plot(COR_perc.values[val], vacant_acc_perc.values[val], 'xr')
        ax.text(COR_perc.values[val]+.05,vacant_acc_perc.values[val]-.05, str(round(val/10)) + "%", horizontalalignment='right', verticalalignment='bottom', color='r')

    COR_log= data["ROC_x_logistic"]
    vacant_acc_log = data["ROC_y_logistic"]
    ax.plot(COR_log, vacant_acc_log, "b", label="Logistic Regression")
    n = round(len(COR_log)-1, 0)
    step = int(round(n/10, 0))
    callout_locs = range(0,n+1,step)
    for val in callout_locs:
        if val==0:
            ax.plot(COR_log.values[val], vacant_acc_log.values[val], 'xb')
        else:
            ax.plot(COR_log.values[val], vacant_acc_log.values[val], 'xb')
        ax.text(COR_log.values[val]+.05,vacant_acc_log.values[val]-.05, str(round(val/10)) + "%", horizontalalignment='right', verticalalignment='bottom', color='b')
    
    ax.plot(data["ROC_x_perfect"], data["ROC_y_perfect"], "g--", label="Perfect Model")
    ax.set_title("Receiver-Operating Characteristic Curve", fontsize=titlesz)
    ax.set_xlabel("Complaint Opportunity Rate FP/(TN + FP) (%)", fontsize=labs)
    ax.set_ylabel("Vacancy Detection Accuracy TP/(TP + FN) (%)", fontsize=labs)
    
    
    ax.legend(loc="lower right", fontsize="medium")
    ax.minorticks_on()
    ax.xaxis.set_tick_params(labelsize=9)
    ax.yaxis.set_tick_params(labelsize=9)
    ax.grid(b=True, which='major', color='#666666', linestyle='-', linewidth=1, alpha=0.7)
    ax.grid(b=True, which='minor', color='#999999', linestyle='-', linewidth=1, alpha=0.2)
    fig.savefig("Figures\\ROC_log_perc_comp.png", format="png", bbox_inches="tight")
    plt.close(fig)
    return

def PlotCMCComparison():
    # Plot .......
    fig, ax = plt.subplots(figsize=(8,6))
    data = pd.read_csv("DataFiles\\CMC_comparison_logistic_percentile.csv")

    MOR_perc= data["CMC_x_percentile"]
    COR_perc = data["CMC_y_percentile"]
    ax.plot(MOR_perc, COR_perc, "r", label="Proposed Method")
    n = round(len(MOR_perc)-1, 0)
    step = int(round(n/10, 0))
    callout_locs = range(0,n+1,step)
    for val in callout_locs:
        if val==0:
            ax.plot(MOR_perc.values[val], COR_perc.values[val], 'xr', label="Decision Thresholds")
        else:
            ax.plot(MOR_perc.values[val], COR_perc.values[val], 'xr')
        ax.text(MOR_perc.values[val]+.05, COR_perc.values[val]+.004, str(round(val/10)) + "%", horizontalalignment='right', verticalalignment='bottom', color='r')

    MOR_log= data["CMC_x_logistic"]
    COR_log = data["CMC_y_logistic"]
    ax.plot(MOR_log, COR_log, "b", label="Logistic Regression")
    n = round(len(MOR_log)-1, 0)
    step = int(round(n/10, 0))
    callout_locs = range(0,n+1,step)
    for val in callout_locs:
        if val==0:
            ax.plot(MOR_log.values[val], COR_log.values[val], 'xb')
        else:
            ax.plot(MOR_log.values[val], COR_log.values[val], 'xb')
        ax.text(MOR_log.values[val]+.05, COR_log.values[val]+.004, str(round(val/10)) + "%", horizontalalignment='right', verticalalignment='bottom', color='b')
    
    ax.plot(data["CMC_x_perfect"], data["CMC_y_perfect"], "g--", label="Perfect Model")
    ax.set_title("COR-MOR Characteristic Curve", fontsize=titlesz)
    ax.set_ylabel("Complaint Opportunity Rate FP/(TN + FP) (%)", fontsize=labs)
    ax.set_xlabel("Missed Opportunity Rate FN/(TP + FN) (%)", fontsize=labs)
    
    ax.legend(loc="upper right", fontsize="medium")
    ax.minorticks_on()
    ax.xaxis.set_tick_params(labelsize=9)
    ax.yaxis.set_tick_params(labelsize=9)
    ax.grid(b=True, which='major', color='#666666', linestyle='-', linewidth=1, alpha=0.7)
    ax.grid(b=True, which='minor', color='#999999', linestyle='-', linewidth=1, alpha=0.2)
    fig.savefig("Figures\\CMC_log_perc_comp.png", format="png", bbox_inches="tight")
    plt.close(fig)
    return


def PlotMain(in_type, start, end, save_suffix, params):
    # Controller for the plotting task - un/comment lines to in/exclude
    tick_hrs = [0]
    historicaldata = pd.read_csv("DataFiles\\" + params.buildtype + "\\" + params.traintype + "\\" + params.fusetype + "\\VIE-historical-output.csv", parse_dates=["fused-proba-dt"])
    historicaldata.index = historicaldata["fused-proba-dt"]
    historicaldata = historicaldata.loc[start:end,:]

    PlotIns(historicaldata, in_type, save_suffix, tick_hrs)
    PlotInsNMids(historicaldata, in_type, save_suffix, tick_hrs, params)
    PlotMidsNOut(historicaldata, in_type, save_suffix, tick_hrs, params)
    PlotInsNOut(historicaldata, in_type, save_suffix, tick_hrs, params)
    #PlotInsNTruth_1plot(historicaldata, in_type, save_suffix, tick_hrs, params) # need to scale ground truth
    PlotInsNTruth_2plots(historicaldata, in_type, save_suffix, tick_hrs, params)
    PlotMidsNTruth_1plot(historicaldata, in_type, save_suffix, tick_hrs, params)
    #PlotMidsNTruth_2plots(historicaldata, in_type, save_suffix, tick_hrs, params) # not working for some reason
    PlotOutNTruth(historicaldata, save_suffix, tick_hrs, params)
    PlotInsNMidsNOutNTruth(historicaldata, in_type, save_suffix, tick_hrs, params)

    #PlotOutputDistribution(historicaldata, save_suffix, tick_hrs, params)
    #IndependenceTest()
    #PlotOutcomeExplanation()
    #CMCExplanation()
    #ROCExplanation()
    #PlotCampusDemand()
    #PlotBuildingDemand()
    #PlotInputsExample()
    #PlotOccupancyStepData()
    #PlotElecSolar()
    #PlotElecHVAC()
    return


#PlotCampusDemand()
#PlotBuildingDemand()
#PlotInputsExample()
#PlotOccupancyStepData()
PlotCOR_MORvsThreshComparison()
#PlotROCComparison()
#PlotCMCComparison()