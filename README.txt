This model is to easily compare an option pricing model with many different option prices.
Before beginning, you must have the following

Things to install
Pandas: 		pip install pandas
Yahoo finance: 		pip install yahoo-finance
Scikit Learn:		pip install -U scikit-learn

The 3 models you can use is:
KDE model
Black Scholes Model
Roll Dice Model

You then can name a range of expiration dates(exp_start, exp_end) and a range of strike prices (strike_low, strike_high)
that you want to compare you model on. You can also specify if you want to look at put vs call (side = 'put' or 'call).
Lastly, enter the ticket symbol and you are good to go.