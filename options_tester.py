import numpy as np
import pandas as pd
import math
import datetime
from datetime import date
from roll_dice import roll_dice
from black_scholes import BlackScholes
from kde_model import build_kde_model
from kde_model import price_kde_option
import pandas_datareader.data as web

# TODO convert models 
#   X    -Black-Scholes, Rachel 
#   X    -roll dice, Andrew 
#   X    -propogation model, Dan 

# Constant that defines the risk free interest rate
rfir = 0.010

# Returns a numpy array of the continuous growth rate
def contGrowthRate(prices):
    dcgr = np.zeros( (len(prices)-1, 1) )
    for i in range(len(prices)-1):
        dcgr[i] = np.log(prices[i+1] / prices[i])
    return dcgr


def bs_price_option(strike, underlying, expiration_date, side):
    days = datetime_to_days(expiration_date)
    bsm = BlackScholes(strike, underlying, volatility, rfir, days)
    if side:
        return bsm.calculate_call_option()
    return bsm.calculate_put_option()

def rolldice_price_option(strike, underlying, expiration_date, side):
    days = datetime_to_days(expiration_date)
    return roll_dice(underlying, strike, days, alpha, volatility, side)

def build_kde_option_pricer(symbol, start_date, end_date):
    stock = web.DataReader(symbol, 'yahoo', start_date, end_date)
    prices = stock['Adj Close']
    kernel_estimate = build_kde_model(prices) 
    def kde_price_option(strike, underlying, expiration_date, side):
        days = datetime_to_days(expiration_date)
        return price_kde_option(kernel_estimate, days, underlying, strike, side)
    return kde_price_option

def datetime_to_days(expiry):
    tnow = date.today()
    days2expiry = abs(expiry - tnow)
    return int(days2expiry.days)    
    
# Function that takes a pricing model and calculates its error in predicting
# a range of options values
# - Jon
def compute_model_error(model, symbol_name, side, date_list=None, date_range=None):
    
    return 

if __name__ == '__main__':
    symbol = "NFLX"
    stp = float(155.59)
    strike = float(158)
    expiry = date(2017, 5, 13)
    start_date = datetime.datetime(2016, 5, 13)
    end_date = datetime.datetime(2017, 5, 13)
    stock = web.DataReader(symbol, 'yahoo', start_date, end_date)
    prices = stock['Adj Close']
    dcgr = contGrowthRate(prices)
    alpha = np.mean(dcgr)
    volatility = np.std(dcgr)

    print(datetime_to_days(expiry))
    print(rolldice_price_option(strike, stp, expiry, True))
    print(bs_price_option(strike, stp, expiry, True))
    kde_price_option = build_kde_option_pricer(symbol, start_date, end_date)
    print(kde_price_option(strike, stp, expiry, True))
