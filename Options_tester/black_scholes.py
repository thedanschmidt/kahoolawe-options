import math
import time
from datetime import date

class BlackScholes:
	def __init__(self, strike_price, stock_price, dayvol, rfir, days_to_expiry):
		self.strike_price = strike_price
		self.stock_price = stock_price
		self.dayvol = dayvol
		self.rfir = rfir
		self.days_to_expiry = days_to_expiry

		# calculate the common elements for call/put options pricing
		self.d1 = math.log(self.stock_price/self.strike_price) +\
			((self.rfir/365) + (self.dayvol**2)/2) * self.days_to_expiry
		self.durvol = self.dayvol * math.sqrt(self.days_to_expiry)
		self.discount = math.exp(-self.rfir * self.days_to_expiry/365)

	# calculate the standard normal distribution
	def std_normal(self, dval):
		return (1.0 + math.erf(dval/math.sqrt(2.0)))/2.0

	def calculate_call_option(self):
		cumd1 = self.std_normal(self.d1/self.durvol)
		cumd2 = self.std_normal((self.d1/self.durvol) - self.durvol)
		call_price = (self.stock_price * cumd1) - (self.strike_price * self.discount * cumd2)
		return call_price

	def calculate_put_option(self):
		cumd1 = self.std_normal(-self.d1/self.durvol)
		cumd2 = self.std_normal(-(self.d1/self.durvol - self.durvol))
		put_price = -(self.stock_price * cumd1) + (self.strike_price * self.discount * cumd2)
		return put_price