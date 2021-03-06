# -*- coding: utf-8 -*-
"""
Created on Fri Jul 01 12:24:13 2016

@author: eczaj
"""

import requests
from bs4 import BeautifulSoup as bs
import helper.common_mods as mods
import collections

def Get_Earnings_Forecast(stock):
    '''Go to Yahoo Finance and scrape the Analyst Estimates. Determine if the Earnings Forecast is postive.
    Return the results in a JSON object.'''
	
    forecast = 'http://ca.finance.yahoo.com/q/ae?s=' + stock + '+Analyst+Estimates'
    #Get Last 4 Quarters of Earnings Forecasts
    forecast_web = requests.get(forecast)
    forecast_text = forecast_web.content   
    forecast_soup = bs(forecast_text)
    forecast_rows = forecast_soup.findAll('tr')
    #i = 0
    try:
        lists = []
        for n in forecast_rows:
            n = str(n) 
            if mods.Match('<tr><th class="yfnc_tablehead1"(.*?)Earnings Est', n):                 
                n = n.split('<th class="yfnc_tablehead1" scope="col" style="font-size:11px; font-weight:normal;text-align:right;" width="18%">')
                dates_list = [n[1], n[2], n[3], n[4]]
                for lst, item in enumerate(dates_list):
                    dates_list[lst] = item.replace('</tr>', '').replace('</td>', '').replace('</th>', '').replace('<br/>', ' ')
            elif mods.Match('<tr><td class="yfnc_tablehead1"(.*?)Avg. Estimate', n):                   
                n = n.split('<td class="yfnc_tabledata1">')
                forecast_list = [n[1], n[2], n[3], n[4]]
                try:            
                    for lst, item in enumerate(forecast_list):
                        forecast_list[lst] = float(item.replace('</tr>', '').replace('</td>', ''))
                    lists.append(forecast_list)
                except:
                    dummy = 0
        
        #Test for Positive Forecasts
        is_positive_earnings_forecast = False
        if lists[0][0] < lists[0][1] and lists[0][1] < lists[0][2] and lists[0][2] < lists[0][3]:
            is_positive_earnings_forecast = True
    
    
        #Create Ditionary of Results
       
        results = collections.OrderedDict()
        results['Stock'] = stock
        results['TestRun'] = 'Earnings_Forecast'    
        results['DateRun'] = mods.Today() 
        results['Result'] = is_positive_earnings_forecast
        results['Current Qtr'] = lists[0][0]
        results['Next Qtr'] = lists[0][1]
        results['Current Year'] = lists[0][2]
        results['Next Year'] = lists[0][3]
        return results
    
    except:
        results = collections.OrderedDict()
        results['stock'] = stock
        results['TestRun'] = 'Earnings_Forecast'
        results['DateRun'] = mods.Today()
        results['Result'] = 'Test Failed'
        return results

##Testing:
#stock = 'AAPL'
#print Get_Earnings_Forecast(stock)