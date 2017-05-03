import numpy as np
import pandas as pd 

import datetime
from datetime import date
import math
from scipy import stats
from sklearn.neighbors.kde import KernelDensity


# Returns a numpy array of the continuous growth rate
def contGrowthRate(prices):
    dcgr = np.zeros( (len(prices)-1, 1) )
    for i in range(len(prices)-1):
        dcgr[i] = np.log(prices[i+1] / prices[i])
    return dcgr

def build_kde_model(prices):
    min_dcgr = -0.3
    max_dcgr = 0.3
    num_bins = 1e4
    bin_width = (max_dcgr - min_dcgr) / num_bins
    possible_cgr = np.linspace(min_dcgr, max_dcgr, num_bins)

    dcgr = contGrowthRate(prices)  
    silverman_bw = 1.06*np.std(dcgr[:, 0])*len(dcgr[:, 0])**(-1/5)
    kde = KernelDensity(kernel='gaussian', bandwidth=silverman_bw).fit(dcgr)
    kernel_estimate = np.exp(kde.score_samples(possible_cgr[:, np.newaxis]))

    return kernel_estimate

def price_kde_option(kernel_estimate, days, current_price, strike, side):
    min_dcgr = -0.3
    max_dcgr = 0.3
    num_bins = 1e4
    bin_width = (max_dcgr - min_dcgr) / num_bins
    possible_cgr = np.linspace(min_dcgr, max_dcgr, num_bins)
     
    dcgr_pdf = kernel_estimate
    for day in range(days-1):
        dcgr_pdf = dcgr_pdf * bin_width
        dcgr_pdf = np.convolve(kernel_estimate, dcgr_pdf, mode='same')

    poss_prices = current_price*np.exp(possible_cgr)
    if side:
        option_value = poss_prices - strike
    else:
        option_value = strike - poss_prices

    option_value[option_value < 0] = 0
    option_price = np.sum(option_value * dcgr_pdf * bin_width)

    return option_price


