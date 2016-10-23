# -*- coding: utf-8 -*-
"""
Created on Sat Aug 06 07:18:43 2016

@author: eczaj
"""

import numpy as np
import collections
import scipy.stats as sct
import pandas_datareader.data as web
import common_mods as mods
from dateutil import parser

def Day_of_Week(dt_var):
    return parser.parse(dt_var).strftime('%a')
    

def norminv(prob, mu, sigma):
    x = sct.norm(mu, sigma)
    return x.ppf(prob)

def Get_Options(stock, strike_price):
	# # Use Pandas Data Reader to pull data from Yahoo Finance
	all_data = {}
	#for ticker in symbol:
	all_data = web.get_data_yahoo(stock, '1/1/2015', mods.Today())

	lst = []
	last = 0
	for current in all_data['Adj Close']:
		if len(lst) == 0:
			lst.append(np.nan)
			last = current
		else:
			lst.append(current / last)
			last = current
	all_data['Percent Changed'] = lst

	# # Run Monte Carlo simulations. 1000 iterations for 60 weeks to determine number of times the value of the stock is greater than the strike price.

	simulation_end = []
	num_iters = 100
	num_weeks = 10
	changed_avg = all_data['Percent Changed'].mean()
	changed_stdev = all_data['Percent Changed'].std()
	for i in range(0, num_iters):
		for i in range(0, num_weeks):
			if i == 0:
				wk_end = all_data['Adj Close'][0]
			else:
				wk_end = norminv(np.random.random_sample(), changed_avg, changed_stdev) * wk_end
		simulation_end.append(max(0, wk_end - strike_price))
	return all_data

end = mods.Today()
start = '1/1/2015'
#print web.DataReader('AAPL', 'yahoo-actions', start, end)
import datetime
datetime.datetime.strptime('1/1/15')
print len(web.get_data_yahoo(stock, start, end))
