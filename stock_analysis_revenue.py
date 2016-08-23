# -*- coding: utf-8 -*-
"""
Created on Fri Jul 01 12:24:13 2016

@author: eczaj
"""

import requests
from bs4 import BeautifulSoup as bs
import collections
import common_mods as mods
import json

def Get_Revenue(stock):
    #Go to Street Insider and Pull the Last Three Years of Revenue Results and Determine if Revenue Passes or Fails Test
    
    earnings_report = 'http://www.streetinsider.com/ec_earnings.php?q=' + stock

#    #Get Last 12 Months Revenue
    earnings_report_web = requests.get(earnings_report)
    earnings_report_text = earnings_report_web.content

    earnings_report_soup = bs(earnings_report_text, 'lxml') 
    i = 0
    for n in earnings_report_soup.find_all('tr'):
                
        print str(i) + ':' + str(n.text)
        i += 1

    # Get Last Three Years of Revenue
    revenue =  mods.income_statement_wrangler(stock, 'Total Revenue') 
    revenue = mods.Is_Negative(revenue)
    last_reported_rev, second_reported_rev, third_reported_rev = float(revenue[0]), float(revenue[1]), float(revenue[2])

    #Get Dates for Last Three Reported Years
    dates = mods.get_reported_dates(stock)
    last_reported_dt, year_before_reported_dt, two_yr_before_reported_dt = dates[0], dates[1], dates[2]
    
    #Test if Revenue Results are Positive
    is_positive_rev = False
    if last_reported_rev > second_reported_rev and second_reported_rev > third_reported_rev:
        is_positive_rev = True
    
    #Create Ditionary of Results  
    results = collections.OrderedDict()
    results['stock'] = stock
    results['Date Run'] = mods.Today()
    results['Revenue_Test'] = is_positive_rev
    results[last_reported_dt] = last_reported_rev
    results[year_before_reported_dt] = second_reported_rev
    results[two_yr_before_reported_dt] = third_reported_rev    
    return json.dumps(results)

#Testing:
#stock = 'goog'
#print Get_Revenue(stock)

