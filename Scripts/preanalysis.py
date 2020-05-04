# Author: Lisa Slaughter <lisa.m.slaughter@gmail.com>
# Last update: May 02, 2019

# This code contains methods for exploring the statistical nature of the input data.
# TODO: **This code needs to be cleaned up**
# ----------------------------------------------------------------------------------------------------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats as st

def CorrelationAnalysis(traindata, build_type, train_set):
    #Generates the correlation coefficient matrix and pairs plot for the input sensor data
    traindata = traindata.iloc[:,:-1]
    corr_mtx = np.corrcoef([traindata.iloc[:,1], traindata.iloc[:,2], traindata.iloc[:,3]])
    corr_mtx = pd.DataFrame(corr_mtx)
    corr_mtx.to_csv("DataFiles\\" + build_type + "\\" + train_set + "\\CorrelationMatrix.csv", header=True, index=True)
    import seaborn as sns
    sns.set(style="ticks")
    pairs = sns.pairplot(traindata)
    pairs.savefig("Figures\\" + build_type + "\\" + train_set + "\\Pairs.png", format="png", bbox_inches="tight")
    return

def CumulativeDistributions_Vac_Occ(sensorname, traindata, build_type, train_set):
    vaccumsum = 0
    vacprobas = []
    vacdata = traindata[traindata["truth-val"]==1]
    vacdata = vacdata[sensorname + "-val"]
    vacsum = sum(vacdata)
    vacdata = vacdata.sort_values(ascending=True)
    for datum in vacdata:
        vaccumsum = vaccumsum + datum
        vacprobas.append(vaccumsum/vacsum) 
        occcumsum = 0
    occprobas = []
    occdata = traindata[traindata["truth-val"]==0]
    occdata = occdata[sensorname + "-val"]
    occsum = sum(occdata)
    occdata = occdata.sort_values(ascending=True)
    for datum in occdata:
        occcumsum = occcumsum + datum
        occprobas.append(occcumsum/occsum)

    labs = 9
    legs = "medium"
    cumsumfig, axcs = plt.subplots(figsize=(11,5))
    axcs.plot(vacdata, vacprobas, label="Vacant")
    axcs.plot(occdata, occprobas, label="Occupied")
    axcs.legend(loc='best', fontsize=legs)
    plt.ylim([0,1])
    plt.xlim([0,max(occdata)])
    axcs.xaxis.set_major_locator(plt.MaxNLocator(20))
    axcs.xaxis.set_tick_params(labelsize=labs)
    axcs.yaxis.set_tick_params(labelsize=labs)
    axcs.set_title("Cumulative Probability Distributions for Sensor: " + sensorname, fontsize=18, fontweight="bold")
    axcs.set_ylabel("Probability (%)", fontsize=labs)
    axcs.set_xlabel("Raw Sensor Value", fontsize=labs)
    axcs.grid(b=True, which='major', color='k', linestyle=':', linewidth=1)
    plt.savefig("Figures\\" + build_type + "\\" + train_set + "\\Cumulative-Proba-Dists-" + sensorname + "_" + train_set + ".png", format="png", bbox_inches="tight")
    plt.close(cumsumfig)
    return

def Histograms_Vac_Occ(bins, sensorname, traindata, build_type, train_set):
    vacdata = traindata[traindata["truth-val"]==1]
    vacdata = vacdata[sensorname + "-val"]
    occdata = traindata[traindata["truth-val"]==0]
    occdata = occdata[sensorname + "-val"]

    labs = 9
    legs = "medium"

    histfig, ax = plt.subplots(figsize=(11,5))
    vcounts, vbins, vpatches = ax.hist(vacdata, bins=bins, label="Vacant: Hist", histtype="step", density=True)
    ocounts, obins, opatches = ax.hist(occdata, bins=bins, label="Occupied: Hist", histtype="step", density=True)
    
    vacparam = st.logistic.fit(vacdata)
    vacfit = st.logistic.pdf(bins, loc=vacparam[0], scale=vacparam[1])
    occparam = st.logistic.fit(occdata)
    occfit = st.logistic.pdf(bins, loc=occparam[0], scale=occparam[1])
    
    ax.plot(bins, vacfit, "b-", label="Vacant: Fit")
    ax.plot(bins, occfit, "r-", label="Occupied: Fit")
    ax.legend(loc='best', fontsize=legs)
    ax.xaxis.set_tick_params(labelsize=labs)
    ax.yaxis.set_tick_params(labelsize=labs)
    ax.set_title("Probability Distributions for Sensor: " + sensorname, fontsize=18, fontweight="bold")
    ax.set_ylabel("Probability (%)", fontsize=labs)
    ax.set_xlabel("Raw Sensor Value", fontsize=labs)
    ax.grid(b=True, which='major', color='k', linestyle=':', linewidth=1)
    plt.savefig("Figures\\" + build_type + "\\" + train_set + "\\Histograms-" + sensorname + ".png", format="png", bbox_inches="tight")
    plt.close(histfig)
    return

def CompareHistogramsNFits_Full_Cherry_Vac(bins, sensorname, td_full, td_cherry, build_type, train_set):
    vacdata_cherry = td_cherry[td_cherry["truth-val"]==1]
    vacdata_cherry = vacdata_cherry[sensorname + "-val"]
    
    vacdata_full = td_full[td_full["truth-val"]==1]
    vacdata_full = vacdata_full[sensorname + "-val"]
    
    labs = 9
    legs = "medium"

    histfig, ax = plt.subplots(figsize=(11,5))
    vcounts_cherry, vbins_cherry, vpatches_cherry = ax.hist(vacdata_cherry, bins=bins, density=True, histtype="step", label="Vacant_cherry: Hist")
    vcounts_full, vbins_full, vpatches_full = ax.hist(vacdata_full, bins=bins, density=True, histtype="step", label="Vacant_full: Hist")
    
    vacparam_cherry = st.logistic.fit(vacdata_cherry)
    vacfit_cherry = st.logistic.pdf(bins, loc=vacparam_cherry[0], scale=vacparam_cherry[1])
    vacparam_full = st.logistic.fit(vacdata_full)
    vacfit_full = st.logistic.pdf(bins, loc=vacparam_full[0], scale=vacparam_full[1])

    ax.plot(bins, vacfit_cherry, "k", label="Vacant_cherry: Fit")
    ax.plot(bins, vacfit_full, "k--", label="Vacant_full: Fit")
    ax.legend(loc='best', fontsize=legs)
    ax.xaxis.set_tick_params(labelsize=labs)
    ax.yaxis.set_tick_params(labelsize=labs)
    ax.set_title("Probability Distributions for Sensor: " + sensorname, fontsize=18, fontweight="bold")
    ax.set_ylabel("Probability (%)", fontsize=labs)
    ax.set_xlabel("Raw Sensor Value", fontsize=labs)
    ax.grid(b=True, which='major', color='k', linestyle=':', linewidth=1)
    plt.savefig("Figures\\" + build_type + "\\Histograms-Vacancy-Comparison_cherry_full_" + sensorname + ".png", format="png", bbox_inches="tight")
    plt.close(histfig)
    return

def CompareHistogramFits_Full_Cherry_Vac_Occ(bins, sensorname, td_full, td_cherry, build_type, train_set):
    vacdata_cherry = td_cherry[td_cherry["truth-val"]==1]
    vacdata_cherry = vacdata_cherry[sensorname + "-val"]
    occdata_cherry = td_cherry[td_cherry["truth-val"]==0]
    occdata_cherry = occdata_cherry[sensorname + "-val"]
    
    vacdata_full = td_full[td_full["truth-val"]==1]
    vacdata_full = vacdata_full[sensorname + "-val"]
    occdata_full = td_full[td_full["truth-val"]==0]
    occdata_full = occdata_full[sensorname + "-val"]

    labs = 9
    legs = "medium"

    histfig, ax = plt.subplots(figsize=(11,5))
    vcounts_cherry, vbins_cherry, vpatches_cherry = ax.hist(vacdata_cherry, bins=bins, density=True, histtype="step", label="Vacant_cherry: Hist")
    ocounts_cherry, obins_cherry, opatches_cherry = ax.hist(occdata_cherry, bins=bins, density=True, histtype="step", label="Occupied_cherry: Hist")
    vcounts_full, vbins_full, vpatches_full = ax.hist(vacdata_full, bins=bins, density=True, histtype="step", label="Vacant_full: Hist")
    ocounts_full, obins_full, opatches_full = ax.hist(occdata_full, bins=bins, density=True, histtype="step", label="Occupied_full: Hist")
    plt.close(histfig)

    vacparam_cherry = st.logistic.fit(vacdata_cherry)
    vacfit_cherry = st.logistic.pdf(bins, loc=vacparam_cherry[0], scale=vacparam_cherry[1])
    occparam_cherry = st.logistic.fit(occdata_cherry)
    occfit_cherry = st.logistic.pdf(bins, loc=occparam_cherry[0], scale=occparam_cherry[1])
    vacparam_full = st.logistic.fit(vacdata_full)
    vacfit_full = st.logistic.pdf(bins, loc=vacparam_full[0], scale=vacparam_full[1])
    occparam_full = st.logistic.fit(occdata_full)
    occfit_full = st.logistic.pdf(bins, loc=occparam_full[0], scale=occparam_full[1])
    
    histfig2, ax2 = plt.subplots(figsize=(11,5))
    ax2.plot(bins, vacfit_cherry, "k", label="Vacant_cherry: Fit")
    ax2.plot(bins, occfit_cherry, "r", label="Occupied_cherry: Fit")
    ax2.plot(bins, vacfit_full, "k--", label="Vacant_full: Fit")
    ax2.plot(bins, occfit_full, "r--", label="Occupied_full: Fit")
    ax2.legend(loc='best', fontsize=legs)
    ax2.xaxis.set_tick_params(labelsize=labs)
    ax2.yaxis.set_tick_params(labelsize=labs)
    ax2.set_title("Probability Distributions for Sensor: " + sensorname, fontsize=18, fontweight="bold")
    ax2.set_ylabel("Probability (%)", fontsize=labs)
    ax2.set_xlabel("Raw Sensor Value", fontsize=labs)
    ax2.grid(b=True, which='major', color='k', linestyle=':', linewidth=1)
    plt.savefig("Figures\\" + build_type + "\\Histograms-Comparison_cherry_full_" + sensorname + ".png", format="png", bbox_inches="tight")
    plt.close(histfig2)
    return

def CompareCumulativeDistributions_Full_Cherry_Vac_Occ(sensorname, td_full, td_cherry, build_type, train_set):
    vaccumsum_cherry = 0
    vacprobas_cherry = []
    vacdata_cherry = td_cherry[td_cherry["truth-val"]==1]
    vacdata_cherry = vacdata_cherry[sensorname + "-val"]
    vacsum_cherry = sum(vacdata_cherry)
    vacdata_cherry = vacdata_cherry.sort_values(ascending=True)
    for datum in vacdata_cherry:
        vaccumsum_cherry = vaccumsum_cherry + datum
        vacprobas_cherry.append(vaccumsum_cherry/vacsum_cherry) 
    
    occcumsum_cherry = 0
    occprobas_cherry = []
    occdata_cherry = td_cherry[td_cherry["truth-val"]==0]
    occdata_cherry = occdata_cherry[sensorname + "-val"]
    occsum_cherry = sum(occdata_cherry)
    occdata_cherry = occdata_cherry.sort_values(ascending=True)
    for datum in occdata_cherry:
        occcumsum_cherry = occcumsum_cherry + datum
        occprobas_cherry.append(occcumsum_cherry/occsum_cherry)

    vaccumsum_full = 0
    vacprobas_full = []
    vacdata_full = td_full[td_full["truth-val"]==1]
    vacdata_full = vacdata_full[sensorname + "-val"]
    vacsum_full = sum(vacdata_full)
    vacdata_full = vacdata_full.sort_values(ascending=True)
    for datum in vacdata_full:
        vaccumsum_full = vaccumsum_full + datum
        vacprobas_full.append(vaccumsum_full/vacsum_full) 
    
    occcumsum_full = 0
    occprobas_full = []
    occdata_full = td_full[td_full["truth-val"]==0]
    occdata_full = occdata_full[sensorname + "-val"]
    occsum_full = sum(occdata_full)
    occdata_full = occdata_full.sort_values(ascending=True)
    for datum in occdata_full:
        occcumsum_full = occcumsum_full + datum
        occprobas_full.append(occcumsum_full/occsum_full)

    labs = 9 # figure label size
    legs = "medium"
    cumsumfig2, axcs = plt.subplots(figsize=(11,5))
    axcs.plot(vacdata_cherry, vacprobas_cherry, "b", label="Vacant_cherry")
    axcs.plot(vacdata_full, vacprobas_full, "b--", label="Vacant_full")
    axcs.plot(occdata_cherry, occprobas_cherry, "r", label="Occupied_cherry")
    axcs.plot(occdata_full, occprobas_full, "r--", label="Occupied_full")
    axcs.legend(loc='best', fontsize=legs)
    plt.ylim([0,1])
    plt.xlim([0,max(occdata_full)])
    axcs.xaxis.set_major_locator(plt.MaxNLocator(20))
    axcs.xaxis.set_tick_params(labelsize=labs)
    axcs.yaxis.set_tick_params(labelsize=labs)
    axcs.set_title("Cumulative Probability Distributions for Sensor: " + sensorname, fontsize=18, fontweight="bold")
    axcs.set_ylabel("Probability (%)", fontsize=labs)
    axcs.set_xlabel("Raw Sensor Value", fontsize=labs)
    axcs.grid(b=True, which='major', color='k', linestyle=':', linewidth=1)
    plt.savefig("Figures\\" + build_type + "\\Cumulative-Dists-Comparison_cherry_full_" + sensorname + ".png", format="png", bbox_inches="tight")
    plt.close(cumsumfig2)
    return

def WhatsMyDistribution(sensorname, td_full, build_type, train_set):
    #distributions = [st.alpha, st.betaprime, st.burr, st.chi2, st.exponlogistic, st.exponweib, st.f, st.fisk, st.frechet_r, st.genextreme, st.gamma, st.gengamma, st.gumbel_r, st.invgamma, st.invgauss, st.invweibull, st.johnsonsb, st.kappa4, st.ksone, st.kstwobign, st.loglogistic, st.maxwell, st.mielke, st.moyal, st.ncx2, st.ncf, st.logisticinvgauss, st.powerloglogistic, st.rayleigh, st.rice, st.recipinvgauss, st.skewlogistic, st.wald, st.weibull_min]
    #distributions = [st.alpha, st.chi2, st.f, st.gamma, st.loglogistic, st.maxwell, st.ncf, st.rayleigh, st.skewlogistic] # a, df, dfn & dfd, a, s, 0, dfn & dfd & nc, 0, a
    distributions = [st.maxwell, st.rayleigh] # a, df, dfn & dfd, a, s, 0, dfn & dfd & nc, 0, a
    mles = []

    for distribution in distributions:
        try:
            pars = distribution.fit(td_full)
            mle = distribution.nnlf(pars, td_full)
            mles.append(mle)
        except Exception as e:
            agh = e

    results = [(distribution.name, mle) for distribution, mle in zip(distributions, mles)]
    best_fits = sorted(zip(distributions, mles), key=lambda d: d[1])[0]
    fitdf = pd.DataFrame(columns=[sensorname])
    fitdf[sensorname] = best_fits
    fitdf.to_csv("DataFiles\\" + build_type + "\\" + train_set + "\\Best_Fits_" + sensorname + ".csv", header=True, index=False)
    #print 'Best fit reached using {}, MLE value: {}'.format(best_fit[0].name, best_fit[1])
    return

def GetBins(sensorname, alldata):
    alldata = alldata[sensorname + "-val"]
    tempfig, tempax = plt.subplots()
    counts, bins, patches = tempax.hist(alldata, bins="auto", density=True)
    plt.close(tempfig)
    return bins

def RunExploration(sensorname, td_full, build_type, train_set):
    #WhatsMyDistribution(sensorname, td_full)
    CorrelationAnalysis(td_full, build_type, train_set)
    #bins = GetBins(sensorname, td_full)
    #if train_set=="Cherry":
        #td_cherry = pd.read_csv("DataFiles\\" + build_type + "\\" + train_set + "\\Training_Data_" + sensorname + ".csv", parse_dates=["timestamp"])
        #td_cherry.index = td_cherry["timestamp"]
        #Histograms_Vac_Occ(bins, sensorname, td_cherry, build_type, train_set)
        #CumulativeDistributions_Vac_Occ(sensorname, td_cherry, build_type, train_set)
        #CompareHistogramFits_Full_Cherry_Vac_Occ(bins,sensorname, td_full, td_cherry, build_type, train_set)
        #CompareHistogramsNFits_Full_Cherry_Vac(bins,sensorname, td_full, td_cherry, build_type, train_set)
        #CompareCumulativeDistributions_Full_Cherry_Vac_Occ(sensorname, td_full, td_cherry, build_type, train_set)

    #elif train_set=="Full":
        #Histograms_Vac_Occ(bins, sensorname, td_full, build_type, train_set)
        #CumulativeDistributions_Vac_Occ(sensorname, td_full, build_type, train_set)
    return
