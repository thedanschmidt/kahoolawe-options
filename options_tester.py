import numpy as np
import pandas as pd
import math
from datetime import date
from rolldice import roll_dice


# TODO convert models 
#       -Black-Scholes, Rachel 
#       -roll dice, Andrew 
#       -propogation model, Dan 


# Example pricing interface
def bs_price_option(strike, underlying, expiration_date, side):
    alpha = 0.01
    volatility= 0.02 
    return black_scholes()

def rolldice_price_option(strike, underlying, expiration_date, side):
    alpha = 0.00
    volatility = 0.045
    days = datetime_to_days(expiration_date)
    return roll_dice(underlying, strike, days, alpha, volatility, side)

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
    stp = float(143.8)
    strike = float(142)
    days = float(10)
    expiry = date(2017, 5, 13)
    print(datetime_to_days(expiry))
    print(rolldice_price_option(strike, stp, expiry, True))
