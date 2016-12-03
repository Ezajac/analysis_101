# -*- coding: utf-8 -*-
"""
Created on Fri Jul 01 12:24:13 2016

@author: eczaj
"""

import requests
from bs4 import BeautifulSoup as bs
import collections
import helper.common_mods as mods

def Get_Revenue(stock):
    '''Go to Yahoo Finance and Pull the Last Three Years of Revenue Results and Determine if Revenue Passes or Fails Test.
    Return the results as a JSON object.'''

    revenue = 'http://ca.finance.yahoo.com/q/is?s=' + stock + '&annual'
    #Get Revenue Data from Last Income Statement
    revenue_web = requests.get(revenue)
    revenue_text = revenue_web.content   
    revenue_soup = bs(revenue_text, "lxml") 
    try:
        # Get Last Three Years of Revenue
        revenue = []    
        for n in revenue_soup.find_all('tr'):
            n = str(n)
            if mods.Match('<tr><td colspan="2">\n<strong>\n\s+Total Revenue', n):
                n = n.replace('\n', '').replace('</strong>', '').replace('</td>', '').replace('<td align="right">', '').replace('</tr', '').strip()
                n = n.split('<strong>')
                for item in n:
                    item = item.strip()
                    if mods.Match('\d+', item):
                        item = item.replace(' ', '').replace('>', '').replace(',', '').replace('\xc2\xa0\xc2\xa0', '').strip()                  
                        revenue.append(item)

        last_reported_rev, second_reported_rev, third_reported_rev = float(revenue[0]), float(revenue[1]), float(revenue[2])
    #
    #    #Get Dates for Last Three Reported Years
        dates = mods.get_reported_dates(stock)
        last_reported_dt, year_before_reported_dt, two_yr_before_reported_dt = dates[0], dates[1], dates[2]
      
    #    #Test if Revenue Results are Positive
        is_positive_rev = False
        if last_reported_rev > second_reported_rev and second_reported_rev > third_reported_rev:
            is_positive_rev = True
    #    
    #    #Create Ditionary of Results  
        results = collections.OrderedDict()
        results['stock'] = stock
        results['TestRun'] = 'Revenue_Test'
        results['DateRun'] = mods.Today()
        results['Result'] = is_positive_rev
        results[last_reported_dt] = last_reported_rev
        results[year_before_reported_dt] = second_reported_rev
        results[two_yr_before_reported_dt] = third_reported_rev    
        return results
    except:
        results = collections.OrderedDict()
        results['stock'] = stock
        results['TestRun'] = 'Revenue_Test'
        results['DateRun'] = mods.Today()
        results['Result'] = 'Test Failed'
        return results


##Testing:
#stock = 'aapl'
#print Get_Revenue(stock)

