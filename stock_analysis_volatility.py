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

def norminv(prob, mu, sigma):
    x = sct.norm(mu, sigma)
    return x.ppf(prob)

def Get_Options(stock):
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


end = mods.Today()
start = '1/1/2015'
#print web.DataReader('AAPL', 'yahoo-actions', start, end)
import datetime
datetime.datetime.strptime('1/1/15')
print len(web.get_data_yahoo(stock, start, end))
