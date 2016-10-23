# -*- coding: utf-8 -*-
"""
Created on Fri Jul 01 12:24:13 2016

@author: eczaj
"""

import requests
from bs4 import BeautifulSoup as bs
import common_mods as mods
import datetime
import collections

def Get_ROE(stock):        
    '''Go to Yahoo Finance. Get the results from the Key Statistics page, Income Statement, and Balance Sheet.
	Determine if the results are positive for a good return on equity. Return the results as a JSON object.'''
    
    key_stats = 'http://ca.finance.yahoo.com/q/ks?s=' + stock + '+Key+Statistics'
    income_statement = 'http://ca.finance.yahoo.com/q/is?s=' + stock + '+Income+Statement&annual'
    balance_sheet = 'http://ca.finance.yahoo.com/q/bs?s=' + stock + '+Balance+Sheet&annual'
    
    #Get Last 12 Months ROE
    key_stats_web = requests.get(key_stats)
    key_stats_text = key_stats_web.content
    
    key_stats_soup = bs(key_stats_text, "lxml")
    
    for n in key_stats_soup.find_all('tr'):
        if n.text[0:16] == 'Return on Equity':          
            amount = n.text.split(':')
            amount = str(amount[1])
            roe_12month = float(amount[0:-1])
       
    # Get Last Three Years of Return on Equity (Net Income/Stock Holder's Equity)
    # First get the Last Three Years of Net Income from Income Statement
    income_statement_web = requests.get(income_statement)
    income_statement_text = income_statement_web.content
    
    income_statement_soup = bs(income_statement_text)
    
    income_statement_rows = income_statement_soup.findAll('tr')
    #i = 0
    try:
        for row in income_statement_rows:
            row = str(row)
            if mods.Match('<tr><td colspan="2">\n<strong>\n\s+Net Income', row):  
                row = row.split('\n')
                last_reported_ni, second_reported_ni, third_reported_ni =  row[6].strip(), row[10].strip(), row[14].strip()
                last_reported_ni, second_reported_ni, third_reported_ni = float(last_reported_ni[0:-4].replace(',', '')),float(second_reported_ni[0:-4].replace(',', '')), float(third_reported_ni[0:-4].replace(',', ''))
    
        # Second get the Last Three Years of StockHolder's Equity from Balance Sheet
        balance_sheet_web = requests.get(balance_sheet)
        balance_sheet_text = balance_sheet_web.content
        
        balance_sheet_soup = bs(balance_sheet_text, 'lxml')
        
        balance_sheet_rows = balance_sheet_soup.findAll('tr')
        for row in balance_sheet_rows:
            row = str(row)
            if mods.Match('<tr><td colspan="2">\n<strong>\n\s+Total Stockholder Equity', row):
                row = row.split('\n')
                last_reported_se, second_reported_se, third_reported_se =  row[6].strip(), row[10].strip(), row[14].strip()
                last_reported_se, second_reported_se, third_reported_se = float(last_reported_se[0:-4].replace(',', '')),float(second_reported_se[0:-4].replace(',', '')), float(third_reported_se[0:-4].replace(',', ''))
        
        #Third Calculate ROE (Net Income/Stock Holders Equity)
        last_reported_roe, second_reported_roe, third_reported_roe = last_reported_ni/last_reported_se, second_reported_ni/second_reported_se, third_reported_ni/third_reported_se
        #Get Dates for Last Three Reported Years
        last_reported_dt, year_before_reported_dt, two_yr_before_reported_dt = mods.get_reported_dates(stock)
    
        is_positive_rev = False
        now = datetime.datetime.now()
        if int(last_reported_dt[0:2]) - now.month < 6:
            if roe_12month > second_reported_roe and second_reported_roe > third_reported_roe:
                is_positive_rev = True
        # Time since last annual reported revenue was less than 6 months
        else:
            if last_reported_roe > second_reported_roe and second_reported_roe > third_reported_roe:
                is_positive_rev = True
        
        #Create Ditionary of Results
        
        results = collections.OrderedDict()
        results['Stock'] = stock
        results['DateRun'] = mods.Today()
        results['TestRun'] = 'Positive_Return_on_Equity'
        results['Result'] = is_positive_rev
        results[last_reported_dt] = last_reported_roe
        results[year_before_reported_dt] = second_reported_roe
        results[two_yr_before_reported_dt] = third_reported_roe
        results['12 Month Return On Equity'] = roe_12month 
        return results
    
    except:
        results = collections.OrderedDict()
        results['stock'] = stock
        results['TestRun'] = 'Positive_Return_on_Equity'
        results['DateRun'] = mods.Today()
        results['Result'] = 'Test Failed'
        return results
#Testing:
#stock = 'aapl'
#print Get_ROE(stock)
