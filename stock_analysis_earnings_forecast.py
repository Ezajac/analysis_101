# -*- coding: utf-8 -*-
"""
Created on Fri Jul 01 12:24:13 2016

@author: eczaj
"""

import requests
from bs4 import BeautifulSoup as bs
import json
import common_mods as mods
import collections

def Get_Earnings_Forecast(stock):
    forecast = 'http://ca.finance.yahoo.com/q/ae?s=' + stock + '+Analyst+Estimates'
    #Get Last 4 Quarters of Earnings Forecasts
    forecast_web = requests.get(forecast)
    forecast_text = forecast_web.content
    
    forecast_soup = bs(forecast_text)
    
    forecast_rows = forecast_soup.findAll('tr')
    i = 0
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
    results['stock'] = stock
    results['Data'] = 'Earnings Forecast'    
    results['Date Run'] = mods.Today() 
    results['Is Positive Earnings Forecast'] = is_positive_earnings_forecast
    results['Current Qtr.'] = lists[0][0]
    results['Next Qtr.'] = lists[0][1]
    results['Current Year'] = lists[0][2]
    results['Next Year'] = lists[0][3]
    
    results = json.dumps(results)
    return results

##Testing:
#stock = 'AAPL'
#print Get_Earnings_Forecast(stock)