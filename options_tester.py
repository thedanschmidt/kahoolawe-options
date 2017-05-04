import numpy as np
import pandas as pd
import math
from pandas_datareader.data import Options
import datetime
from yahoo_finance import Share
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
def contGrowthRate(symbol, start_date, end_date):
    stock = web.DataReader(symbol, 'yahoo', start_date, end_date)
    prices = stock['Adj Close']
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
    def kde_price_option(strike, stock_price, expiration_date, side):
        days = datetime_to_days(expiration_date)
        return price_kde_option(kernel_estimate, days, stock_price, strike, side)
    return kde_price_option

def datetime_to_days(expiry):
    tnow = date.today()
    days2expiry = abs(expiry - tnow)
    return int(days2expiry.days)    
    
# Function that takes a pricing model and calculates its error in predicting
# a range of options values
# - Jon
def compute_model_error(model, symbol, side, exp_start, exp_end, strike_low, strike_high):
    
    #Get the option prices
    options_sym = Options(symbol, 'yahoo')
    options_sym.expiry_dates
    options_data = options_sym.get_all_data()
    options_data = options_data.loc[(slice(strike_low,strike_high), slice(exp_start, exp_end), side),:]

    #get yesterdays stock price
    stock_price = float(Share(symbol).get_price())

    labels = ["strike", "expiry", "option price", "predicted price", "error"]
    data = []
    for index, row in options_data.iterrows():
        strike = index[0]
        expiration_date = index[1].date()
        option_price = row['Last']
        pred_price = model(strike, stock_price, expiration_date, side)

        data.append([strike, expiration_date.strftime('%Y-%m-%d'), option_price, pred_price, option_price-pred_price])

    return labels, data

if __name__ == '__main__':
    #Variables to Change
    symbol = "NFLX"
    side = 'call'
    exp_start = date(2017, 5, 5)
    exp_end = date(2017, 5, 20)
    strike_low = 155
    strike_high = 160

    ####Calculate Alpha and volatility######
    start_date = datetime.datetime(2016, 5, 5)
    end_date = datetime.datetime(2017, 5, 13)
    dcgr = contGrowthRate(symbol, start_date, end_date)
    alpha = np.mean(dcgr)
    volatility = np.std(dcgr)
    ###########################################

    # print(datetime_to_days(expiry))
    # print(rolldice_price_option(strike, stp, expiry, True))
    # print(bs_price_option(strike, stp, expiry, True))
    kde_price_option = build_kde_option_pricer(symbol, start_date, end_date)
    # print(kde_price_option(strike, stp, expiry, True))

    labels, data = compute_model_error(kde_price_option, symbol, side, exp_start, exp_end, strike_low, strike_high)
    options_df = pd.DataFrame.from_records(data, columns=labels)
    print("stock: " + symbol)
    print("price: " + str(Share(symbol).get_price()))
    print(options_df)