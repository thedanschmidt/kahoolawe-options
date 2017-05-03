import numpy as np
import pandas as pd
import math
import pandas_datareader.data as web
from pandas_datareader.data import Options
from datetime import date
from roll_dice import roll_dice
from black_scholes import BlackScholes

# TODO convert models 
#       -Black-Scholes, Rachel 
#       -roll dice, Andrew 
#       -propogation model, Dan 

alpha = 0.00
volatility = 0.045
rfir = 0.010


def bs_price_option(strike, stock_price, expiration_date, side):
    days = datetime_to_days(expiration_date)
    bsm = BlackScholes(strike, stock_price, volatility, rfir, days)
    if side:
        return bsm.calculate_call_option()
    return bsm.calculate_put_option()

def rolldice_price_option(strike, stock_price, expiration_date, side):
    days = datetime_to_days(expiration_date)
    return roll_dice(stock_price, strike, days, alpha, volatility, side)

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
    stp = float(143.8)
    strike = float(142)
    expiry = date(2017, 5, 13)
    print(datetime_to_days(expiry))
    print(rolldice_price_option(strike, stp, expiry, True))
    print(bs_price_option(strike, stp, expiry, True))

    print(compute_model_error(rolldice_price_option, 'NFLX', 'call', ['2017-05-05'], [150]))
