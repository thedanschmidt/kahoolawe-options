import numpy as np
import pandas as pd
import math
<<<<<<< HEAD
import pandas_datareader.data as web
from pandas_datareader.data import Options
=======
import datetime
>>>>>>> d8124a1cc1dcaa7fc620854be928a4f502725c41
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


def bs_price_option(strike, stock_price, expiration_date, side):
    days = datetime_to_days(expiration_date)
    bsm = BlackScholes(strike, stock_price, volatility, rfir, days)
    if side:
        return bsm.calculate_call_option()
    return bsm.calculate_put_option()

def rolldice_price_option(strike, stock_price, expiration_date, side):
    days = datetime_to_days(expiration_date)
    return roll_dice(stock_price, strike, days, alpha, volatility, side)

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
def compute_model_error(model, symbol, side, date_list=None, strike_prices=None):
    
    #Get the option prices
    options_sym = Options(symbol, 'yahoo')
    options_sym.expiry_dates
    options_data = options_sym.get_all_data()

    #get stock price
    stock_price = web.DataReader(symbol, 'yahoo', date.today(), date.today())['Adj Close']
    error = 0

    for exp_date in date_list:
        for strike in strike_prices:
            option_price = options_data.loc[(strike, exp_date, side)]['Last']
            pred_price = model(strike, stock_price, expiration_date, side)
            error += math.pow(pred_price - option_price, 2)

    return math.sqrt(error)

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
    print(compute_model_error(rolldice_price_option, 'NFLX', 'call', ['2017-05-05'], [150]))
    kde_price_option = build_kde_option_pricer(symbol, start_date, end_date)
    print(kde_price_option(strike, stp, expiry, True))
