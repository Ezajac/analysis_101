# -*- coding: utf-8 -*-
"""
Created on Fri Jul 01 12:24:13 2016

@author: eczaj
"""

import requests
from bs4 import BeautifulSoup as bs
import common_mods as mods
import collections

def Get_Earnings_Surprise(stock):
    '''Go to Yahoo Finance and scrape the Analyst Estimates. Determine if the Earning Suprises were positive.
    Return the results in a JSON object.'''
    
    analyst_estimates = 'http://ca.finance.yahoo.com/q/ae?s=' + stock + '+Analyst+Estimates'
    #Get Last 4 EPS Surprises
    analyst_estimates_web = requests.get(analyst_estimates)
    analyst_estimates_text = analyst_estimates_web.content
    
    analyst_estimates_soup = bs(analyst_estimates_text, "lxml")
    
    analyst_estimates_rows = analyst_estimates_soup.findAll('tr')
    #i = 0
    try:
        for n in analyst_estimates_rows:
            n = str(n)    
            if mods.Match('<tr><td class="yfnc_tablehead1"(.*?)EPS Est', n):                
                n = n.split('<td class="yfnc_tabledata1">')
                est_list = [n[1], n[2], n[3], n[4]]
                for lst, item in enumerate(est_list): 
                    est_list[lst] = float(item.replace('</tr>', '').replace('</td>', ''))      
            elif mods.Match('<tr><td class="yfnc_tablehead1"(.*?)EPS Actual', n):                     
                n = n.split('<td class="yfnc_tabledata1">')
                actual_list = [n[1], n[2], n[3], n[4]]
                for lst, item in enumerate(actual_list): 
                    actual_list[lst] = float(item.replace('</tr>', '').replace('</td>', ''))  
            elif mods.Match('<tr><th class="yfnc_tablehead1"(.*?)Revenue Est', n):
                n = n.split('<th class="yfnc_tablehead1" scope="col" style="font-size:11px;text-align:right;" width="18%">')
                dates = [n[1], n[2], n[3], n[4]]
                for lst, item in enumerate(dates): 
                    dates[lst] = item.replace('</tr>', '').replace('</td>', '').replace('</th>', '').replace('<br/>', ' ') 
        surprise1, surprise2, surprise3, surprise4 = 1 - est_list[0]/actual_list[0], 1 - est_list[1]/actual_list[1], 1 - est_list[2]/actual_list[2], 1 - est_list[3]/actual_list[3]
        
        #Test if Earnings Surprise was Positive
        is_postive_pes_surprise = False
        if surprise1 > 0 and surprise2 > 0 and surprise3 > 0 and surprise4 > 0:
            is_postive_pes_surprise = True
        
        #Create Ditionary of Results
        results = collections.OrderedDict()
        results['Stock'] = stock
        results['DateRun'] = mods.Today()
        results['TestRun'] = 'Earnings_Surprise'
        results[dates[0].replace('Qtr.', '').replace('Current', '',).replace('Next', '').replace('Year', '').strip()] = surprise1 
        results[dates[1].replace('Qtr.', '').replace('Current', '',).replace('Next', '').replace('Year', '').strip()] = surprise2 
        results[dates[2].replace('Qtr.', '').replace('Current', '',).replace('Next', '').replace('Year', '').strip()] = surprise3 
        results[dates[3].replace('Qtr.', '').replace('Current', '',).replace('Next', '').replace('Year', '').strip()] = surprise4 
        results['Actuals'] = actual_list
        results['EST'] = est_list
        results['Result'] = is_postive_pes_surprise
        return results

    except:
        results = collections.OrderedDict()
        results['stock'] = stock
        results['TestRun'] = 'Earnings_Surprise'
        results['DateRun'] = mods.Today()
        results['Result'] = 'Test Failed'
        return results
##Testing:       
#stock = 'aapl'
#print Get_Earnings_Surprise(stock)
