# -*- coding: utf-8 -*-
"""
Created on Fri Jul 01 12:24:13 2016

@author: eczaj
"""

import requests
from bs4 import BeautifulSoup as bs
import datetime
import helper.common_mods as mods
import collections

def Get_EPS(stock):

    #Go to Yahoo Finance and Pull the Last Three Years of Revenue Results and Determine if Revenue Passes or Fails Test
    #Current Year: http://finance.yahoo.com/q/ks?s=AAPL+Key+Statistics
    #Last Years Income Statement: http://finance.yahoo.com/q/is?s=AAPL+Income+Statement&annual 
    
    key_stats = 'http://ca.finance.yahoo.com/q/ks?s=' + stock + '+Key+Statistics'
    market_watch = 'http://www.marketwatch.com/investing/stock/' + stock + '/financials'
    
    #Get Last 12 Months Earnings Per Share
    key_stats_web = requests.get(key_stats)
    key_stats_text = key_stats_web.content
    
    key_stats_soup = bs(key_stats_text)
    
    for n in key_stats_soup.find_all('tr'):
        if n.text[0:11] == 'Diluted EPS':
            amount = n.text.split(':')
            eps_12month = float(amount[1])
    
    # Get Last Three Years of Earnings Per Share
    market_watch_web = requests.get(market_watch)
    market_watch_text = market_watch_web.content
    
    market_watch_soup = bs(market_watch_text)
    
    market_watch_rows = market_watch_soup.findAll('tr')
    
    #tag = '<tr class="mainRow"> \
    #<td class="rowTitle"><a data-ref="ratio_Eps1YrAnnualGrowth" href="#"><span class="expand"></span></a> EPS (Basic)</td>'
    
    #i = 0
    try:
        for row in market_watch_rows:
            row = str(row)
            if mods.Match('<tr class="mainRow">\n(.*?)EPS \(Diluted\)', row):
                row = row.split('<td class="valueCell">')
                last_reported_eps, second_reported_eps, third_reported_eps =  float(row[5][0:4].strip()), float(row[4][0:4].strip()), float(row[3][0:4].strip())
    
   
        #Get Dates for Last Three Reported Years
        last_reported_dt, year_before_reported_dt, two_yr_before_reported_dt = mods.get_reported_dates(stock)
        #print mods.get_reported_dates(stock)
        is_positive_eps = False
        now = datetime.datetime.now()
        if int(last_reported_dt[0:2]) - now.month < 6:
            
            if eps_12month > second_reported_eps and second_reported_eps > third_reported_eps:
                is_positive_eps = True
        # Time since last annual reported revenue was less than 6 months
        else:
            if last_reported_eps > second_reported_eps and second_reported_eps > third_reported_eps:
                is_positive_eps = True
        '''
        '''
        #Create Ditionary of Results
        results = collections.OrderedDict()
        results['stock'] = stock    
        results['TestRun'] = 'EPS'
        results['DateRun'] = mods.Today()
        results['Result'] = is_positive_eps
        results[last_reported_dt] = last_reported_eps
        results[year_before_reported_dt] = second_reported_eps
        results[two_yr_before_reported_dt] = third_reported_eps
        results['12 Month Reported EPS'] = eps_12month
        return results
    
    except:
        results = collections.OrderedDict()
        results['stock'] = stock
        results['TestRun'] = 'EPS'
        results['DateRun'] = mods.Today()
        results['Result'] = 'Test Failed'
        return results

#Testing:
#stock = 'AAPL'
#print Get_EPS(stock)