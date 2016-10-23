# -*- coding: utf-8 -*-
"""
Created on Fri Jul 01 12:24:13 2016

@author: eczaj
"""

import requests
from bs4 import BeautifulSoup as bs
import common_mods as mods
import collections

def Get_Shares_Short(stock):
    '''Got to Yahoo Finance and determine the Insider Tracking of the stock. Return the results as a 
    JSON object.'''
    insider_transactions = 'http://ca.finance.yahoo.com/q/it?s=' + stock + '+Insider+Transactions'
    #Get Insider Transaction Data (Last 6 Months and Last 3 Months)
    insider_transactions_web = requests.get(insider_transactions)
    insider_transactions_text = insider_transactions_web.content
    
    insider_transactions_soup = bs(insider_transactions_text)
    
    insider_transactions_rows = insider_transactions_soup.findAll('tr')
    i = 0
    insider_list = []    
    for n in insider_transactions_rows:       
        if n.text[0:10] == 'Net Shares':
            n = str(n)
            n = n.split('<td align="right" class="yfnc_tabledata1"')
            insider_list.append(n[1].replace('</td>', '').replace('</tr>', '').replace(' width="20%">', '').replace('>', '').replace(',', ''))
    try:
        #Test if Positive Insider Tracking (Positive Purchase of Stock in Last 3 Months)
        is_postive_insider = False
        if mods.Match('\(\d+\)', insider_list[1]):
            is_postive_insider = True
        
        #Create Ditionary of Results
        results = collections.OrderedDict()
        results['Stock'] = stock	
        results['DateRun'] = mods.Today()
        results['TestRun'] = 'Insider_Trading'
        results['Insider Purchasing 6 Month: ' + stock] = insider_list[0]
        results['Insider Purchasing 3 Month: ' + stock] = insider_list[1]
        results['Result'] = is_postive_insider
        return results
    
    except:
        results = collections.OrderedDict()
        results['stock'] = stock
        results['TestRun'] = 'Insider_Trading'
        results['DateRun'] = mods.Today()
        results['Result'] = 'Test Failed'
        return results

#Testing:       
#stock = 'aapl'
#print Get_Shares_Short(stock)
