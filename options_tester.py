import numpy as np
import pandas as pd
import math

# TODO convert models 
#       -Black-Scholes, Rachel 
#       -roll dice, Andrew 
#       -propogation model, Dan 


# Example pricing interface
def bs_price_option(strike, underlying, expiration_date, side):
    alpha = 0.01
    volatility= 0.02 
    return black_scholes()


# Function that takes a pricing model and calculates its error in predicting
# a range of options values
# - Jon
def compute_model_error(model, symbol_name, side, date_list=None, date_range=None):
    
    return 
