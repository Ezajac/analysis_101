# -*- coding: utf-8 -*-
"""
Created on Fri Jul 01 12:24:13 2016

@author: eczaj
"""

import requests
from bs4 import BeautifulSoup as bs
import common_mods as mods
import collections

def Get_Earnings_V_Industry(stock):
    '''Go to Yahoo finance and pull information from Analyst Estimates. Determine if the earnings 
    are favorable compared to the industry. Return the results as a JSON object.'''
    
    analyst_estimates = 'http://ca.finance.yahoo.com/q/ae?s=' + stock + '+Analyst+Estimates'
    #Get Last 4 EPS Surprises
    analyst_estimates_web = requests.get(analyst_estimates)
    analyst_estimates_text = analyst_estimates_web.content
    
    analyst_estimates_soup = bs(analyst_estimates_text)
    
    analyst_estimates_rows = analyst_estimates_soup.findAll('tr')
    #i = 0
    try:
    
        for n in analyst_estimates_rows:       
            n = str(n)    
            if mods.Match('<tr><td class="yfnc_tablehead1"(.*?)Price/Earnings', n):
                n = n.split('<td class="yfnc_tabledata1">')
                pe_list = [n[1], n[2], n[3], n[4]]
                for lst, item in enumerate(pe_list): 
                    pe_list[lst] = float(item.replace('</tr>', '').replace('</td>', '').replace('%', ''))
    
    
        #Test if Earnings Surprise was Positive
        is_postive_pe_v_industry = False
        if pe_list[0] > pe_list[1]:
            is_postive_pe_v_industry = True
        
        #Create Ditionary of Results
        results = collections.OrderedDict()
        results['Stock'] = stock
        results['DateRun'] = mods.Today()
        results['TestRun'] = 'Earnings Versus Industry'
        results['PE Estimate: ' + stock] = pe_list[0]
        results['Industry Estimate:'] = pe_list[1]
        results['Result'] = is_postive_pe_v_industry
        return results
    
    except:
        results = collections.OrderedDict()
        results['stock'] = stock
        results['TestRun'] = 'Earnings Versus Industry'
        results['DateRun'] = mods.Today()
        results['Result'] = 'Test Failed'
        return results

##Testing:       
#stock = 'aapl'
#print Get_Earnings_V_Industry(stock)
