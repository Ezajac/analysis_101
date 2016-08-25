# -*- coding: utf-8 -*-
"""
Created on Sat Jul 09 06:27:48 2016

@author: eczaj
"""

import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup as bs
from dateutil import parser 
from pymongo import MongoClient

def Match(pattern, string):
    if re.match(pattern, string):
        return True
    else:
        return False 
        
def Today():
    today = datetime.now() 
    return format(today.year, '04') + '-' + format(today.month, '02') + '-' + format(today.day, '02')

def month_converter(month):
    '''Returns Month of the Year using a 3 character Month (eg. 'Jan' returns 1) '''
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    return months.index(month) + 1

def Parse_Dates(dates_list):
    new_list = []    
    for date in dates_list:
        date = date.split('/')
        date[0] = '00' + date[0]
        new_list.append(date[0][-2:] + '-' + date[1] + '-' + date[2])
    return new_list

def get_reported_dates(stock):
    #Get Dates for Last Three Reported Years
    income_statement = 'http://www.nasdaq.com/symbol/' + stock + '/financials?query=income-statement'
    income_statement_web = requests.get(income_statement)
    income_statement_text = income_statement_web.content
    
    income_statement_soup = bs(income_statement_text)
    income_statement_rows = income_statement_soup.findAll('th')    
    dates = []
    for row in income_statement_rows:   
        row = str(row)
        if Match('<th>\d/\d+/\d+', row):            
                dates.append(row.replace('<th>', '').replace('</th>', ''))
    dates = str(dates[0]), str(dates[1]), str(dates[2])
    dates = Parse_Dates(dates)
    return dates

def income_statement_wrangler(stock, attribute):
    income_statement = 'http://www.nasdaq.com/symbol/'+ stock + '/financials?query=income-statement'
    # Get Last Three Years of Revenue
    income_statement_web = requests.get(income_statement)
    income_statement_text = income_statement_web.content
    
    income_statement_soup = bs(income_statement_text)
    
    income_statement_rows = income_statement_soup.findAll('tr')
    i = 0
    for row in income_statement_rows:     
        #print str(i) + ':' + row
        i += 1
        #print row
        row = str(row)
        if Match('<tr>\n(.*?)' + attribute + '</th>', row):
            values = row.split('<td>')
            return [values[-4].strip().replace('</td>', '').replace('$', '').replace(',', ''), values[-3].strip().replace('</td>', '').replace('$', '').replace(',', ''), values[-2].strip().replace('</td>', '').replace('$', '').replace(',', '')]

def get_net_income(stock, attribute):
    income_statement = 'http://www.nasdaq.com/symbol/'+ stock + '/financials?query=income-statement'
    # Get Last Three Years of Revenue
    income_statement_web = requests.get(income_statement)
    income_statement_text = income_statement_web.content
    
    income_statement_soup = bs(income_statement_text)
    
    income_statement_rows = income_statement_soup.findAll('tr')
    i = 0
    for row in income_statement_rows:     
        #print str(i) + ':' + row
        i += 1
        row = str(row)
        if Match('<tr>\n(.*?)' + attribute, row):
            values = row.split('<td>')
            return [values[-4].strip().replace('</td>', '').replace('$', '').replace(',', ''), values[-3].strip().replace('</td>', '').replace('$', '').replace(',', ''), values[-2].strip().replace('</td>', '').replace('$', '').replace(',', '')]
        i += 1

def get_balance_sheet(stock, attribute):
    balance_sheet = 'http://www.nasdaq.com/symbol/' + stock + '/financials?query=balance-sheet'
    # Get Last Three Years of Revenue
    balance_sheet_web = requests.get(balance_sheet)
    balance_sheet_text = balance_sheet_web.content

    balance_sheet_soup = bs(balance_sheet_text, 'lxml')
    
    balance_sheet_rows = balance_sheet_soup.findAll('tr')
    i = 0
    for row in balance_sheet_rows:     
        i += 1
        row = str(row)
        if Match('<tr>\n(.*?)' + attribute, row):
            values = row.split('<td>')
            return [values[-4].strip().replace('</td>', '').replace('$', '').replace(',', ''), values[-3].strip().replace('</td>', '').replace('$', '').replace(',', ''), values[-2].strip().replace('</td>', '').replace('$', '').replace(',', '')]
        i += 1

def Day_of_Week(dt_var):
    return parser.parse(dt_var).strftime('%a')

def Insert_Data(connection, database, collection, json):
    client = MongoClient(connection)
    db = client.database
    db.collection.insert(json)
    
def Is_Negative(lst):
    for i in range(len(lst)):
        if lst[i][0] == '(':
            lst[i] = lst[i].replace('(', '-').replace(')', '')
    return lst
            
#test_lst = ['(5)', '6', '(7)', '8']
#print Is_Negative(test_lst)
                  
#stock = 'goog'
#print get_reported_dates('aapl')
#print get_balance_sheet(stock, 'Common Stocks')
#print get_balance_sheet(stock, '>Long-Term Debt')
#print get_balance_sheet(stock, 'Treasury Stock')
#t0day = Today()
#print type(t0day)
#print get_reported_dates('aapl')
#num = 'Sep'
#print month_converter(num)

