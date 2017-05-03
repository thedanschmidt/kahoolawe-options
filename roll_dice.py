# rolldice.py  in PyGo\PyFTR
# This is the experimental model for integrating a stock distribution, designed as 
# a basis for our own version of an options pricing model, including the Aruba model.
# Code is arranged here in order to teach or explain the logical steps taken.
# Designed in Python 2.7.11 for Econ 136
# First edition dated March 1, 2017   Professor Gary R. Evans
# This is version 2.0, dated March 3, 2017
#
import math
import numpy as np
import matplotlib.pyplot as plt


#
# Normally we would call our SN cumulative density function from our library, but it is written 
# here so others can see what we are doing. We are using the version that draws upon the Gaussian
# error function, which is an unusual but fruitful approach. This will be used below.
# 
def csnd(point):
	return (1.0 + math.erf(point/math.sqrt(2.0)))/2.0
#
# An elementary function for calculating the stock price adjusted for drift (alpha).
#
def drift(alpha,time):
	return 1.0*math.exp(alpha*time)
#
# An elementary multiplier function for converting daily volatility to duration volatility.
#
def durvol(time):
	return 1.0*math.sqrt(time)
#
# An elementary price expected-mean-value adjustment multiplier for log distributed prices.
# The mean of a log-distributed pdf is adjusted by minus one-half variance.
#
def lnmeanshift(sigma):
	return 1.0*math.exp(-1.0*(sigma*sigma/2))



def roll_dice(stp, strike, days, alpha, sigma, get_call_price):
        
        debug = False

        #
        # Adjust the stock price for drift. If drift is not desired, set the alpha above to zero, don't override this.
        #
        if debug:
                print("Pricing", strike)
                print("Stock price before drift:", stp)
        stp = stp*drift(alpha,days)
        if debug:
                print("Stock price adjusted for drift: ", stp)
                #
                # Adjust the daily volatility for duration volatility. If the adjustment is unneccesary, set days to zero.
                #
                print("Sigma before adjustment: ", sigma)
        
        sigma = sigma*durvol(days)
        if debug:
                print("Sigma after duration adjustment: ", sigma)
        #
        # Figure out the strike spread (sigma in the distribution)
        sspread = math.log(strike/stp)
        if debug:
                print("Strike spread: ", sspread)
        #
        # Establish the array of Bin values as a series of multiples of standard deviations
        # The centered-on-zero load array is appropriate (although it doesn't really matter).
        # Assuming symmetry, the binnumbers (num) will equal 2 X abs(deviation) X # of intervals + 1 e.g.(4.25*2*2+1)= 18
        #
        binborder = np.linspace(-5, 5, num=1000, dtype=float)
        size = len(binborder)
        if debug:
                print("Number of bins (size):", size)
        #
        # Given the stock price (stp) and sigma above, establish an array to associate a stock 
        # value (binprice) with each binborder. Then establish an array of integrated probabilities 
        # for each bin edge (binedgeprob) integrating from minus infinity to the sigma multiples. 
        #
        binprice = np.zeros(size)
        binedgeprob = np.zeros(size) 
        for i in range(0,size):
	        binprice[i] = stp*math.exp(binborder[i]*sigma)
	        binedgeprob[i] = csnd(binborder[i])

        #
        # Now calculate the bin (spread) probabilities.
        # Then calculate a mid-price bin value for each bin (COMPLICATED - source of major error if done wrong).
        # Look carefully at the adjusted binmidprice formula and see that we are not using the average of the two edge prices.
        # Then multiply binmidprice times the equivalent binprob to get the value of each bin.
        # Check/debug results by summing stepwise and in total.
        #
        size = size - 1
        binprob = np.zeros(size)
        binmidprice = np.zeros(size)
        binvalue = np.zeros(size)
        #print("Bin spread probabilities and accumulating sums:")
        #print("Midprice value, Bin Value, and sum."	)
        for i in range(0,size):
	        #print()
	        binprob[i] = binedgeprob[i+1] - binedgeprob[i]
	        binmidprice[i] = stp*math.exp(((binborder[i+1]+binborder[i])/2.0)*sigma)
	        #print("Range:", binborder[i], "to" , binborder[i+1])
	        #print("Binmidprice unadjusted: ", binmidprice[i])
	        binmidprice[i] = (stp*math.exp(((binborder[i+1]+binborder[i])/2.0)*sigma))*lnmeanshift(sigma)
	        #print("Binmidprice adjusted:", binmidprice [i])
	        binvalue[i] = binmidprice[i]*binprob[i]
	        #print("Binprobability: ", binprob[i])
	        #print("Probability of being in this range: ", binprob[i])
	        #print("Sum of probabilities to here:", np.sum(binprob[0:(i+1)]))
	        #print("Binvalue:", binvalue[i])
	        #print("Sum to this point:", np.sum(binvalue[0:(i+1)]))

        log_stp = math.log(stp)
        log_strike = math.log(strike)
        strike_sigma = (log_strike - log_stp) / sigma
        call_values = [x - strike if x - strike > 0 else 0.0 for x in binmidprice]

        if debug:
                fig, ax1 = plt.subplots()
                ax1.plot(binmidprice, binprob)
                ax2 = ax1.twinx()
                ax2.plot(binmidprice, call_values)
                plt.show()

        call_val = sum(call_values * binprob)
        if debug:
                print("Estimated call value: %.4f" % call_val)


        """call_write_vals = [strike if x >= strike else x for x in binmidprice]
        if debug:
        fig, ax1 = plt.subplots()
        ax1.plot(binmidprice, binprob)
        ax2 = ax1.twinx()
        ax2.plot(binmidprice, call_write_vals)
        plt.show()

        print("Estimated value of writing covered call %.2f" % (call_val + sum(call_write_vals * binprob)))
        """

        put_values = [strike - x if strike - x > 0 else 0.0 for x in binmidprice]
        put_val = sum(put_values * binprob)
        if debug:
                print("Estimated put value: %.4f" % put_val)

        if debug:
                fig, ax1 = plt.subplots()
                ax1.plot(binmidprice, binprob)
                ax2 = ax1.twinx()
                ax2.plot(binmidprice, put_values)
                plt.show()

        if debug:
                call_executed = [1 if x - strike > 0 else 0 for x in binmidprice]
                prob_call_executed = np.dot(binprob, call_executed)
                print("Probability call executed: %.4f" % prob_call_executed)

                put_executed = [1 if strike > x else 0 for x in binmidprice]
                prob_put_executed = np.dot(binprob, put_executed)
                print("Probability put executed: %.4f" % prob_put_executed)



                call_in_money = [x if x >= strike else 0 for x in binmidprice]
                call_out_of_money = [x if x < strike else 0 for x in binmidprice]
                val_of_call_in_money = np.dot(binprob, call_in_money)
                val_of_call_out_of_money = np.dot(binprob, call_out_of_money)
                print("Value of the call that is in the money %.4f" % val_of_call_in_money)
                print("Value of the call that is out of the money %.4f" % val_of_call_out_of_money)



                put_in_money = [x if strike >= x else 0 for x in binmidprice]
                put_out_of_money = [x if strike < x else 0 for x in binmidprice]
                val_of_put_in_money = np.dot(binprob, put_in_money)
                val_of_put_out_of_money = np.dot(binprob, put_out_of_money)
                print("Value of the put that is in the money %.4f" % val_of_put_in_money)
                print("Value of the put that is out of the money %.4f" % val_of_put_out_of_money)

        if get_call_price:
                return call_val
        return put_val

if __name__ == '__main__':
        # Establish the testing values of our stock price (stp), strike price (strike), drift (alpha)
        # and volatility (sigma). 
        #
        
        stp = float(143.8)
        strike = float(142)
        days = float(10)
        alpha = float(0.000)
        sigma = float(0.045)
        call = True
        roll_dice(stp, strike, days, alpha, sigma, call)
