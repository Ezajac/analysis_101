# -*- coding: utf-8 -*-
"""
Created on Fri Jul 01 12:24:13 2016

@author: eczaj
"""

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import common_mods as mods
import collections
        
def Get_Analyst_Opinion(stock):
    '''Go to Yahoo Finance and get the last three monts of Analyst Opinions, determine if the analyst optinion is postive,
    and return the results as a JSON object.'''

    analyst_opinion = 'http://ca.finance.yahoo.com/q/ao?s=' + stock + '+Analyst+Opinion'
    analyst_opinion_web = requests.get(analyst_opinion)
    analyst_opinion_text = analyst_opinion_web.content  
    analyst_opinion_soup = bs(analyst_opinion_text)
    
    #i = 0
    try:
        for n in analyst_opinion_soup.find_all('tr'):
            if n.text[0:6] == 'Strong':
                strong_buy = str(n)
                strong_buy = strong_buy.split('<td align="center" class="yfnc_tabledata1">')
                for lst, item in enumerate(strong_buy): 
                    strong_buy[lst] = item.replace('</td>', '')
                strong_buy[-1] = strong_buy[-1].replace('</tr>', '')
                strong_buy = [float(strong_buy[1]), float(strong_buy[2]), float(strong_buy[3]), float(strong_buy[4])]
            elif n.text[0:3] == 'Buy':
                buy = str(n)
                buy = buy.split('<td align="center" class="yfnc_tabledata1">')
                for lst, item in enumerate(buy): 
                    buy[lst] = item.replace('</td>', '')
                buy[-1] = buy[-1].replace('</tr>', '')
                buy = [float(buy[1]), float(buy[2]), float(buy[3]), float(buy[4])]
            elif n.text[0:4] == 'Hold':
                hold = str(n)
                hold = hold.split('<td align="center" class="yfnc_tabledata1">')
                for lst, item in enumerate(hold): 
                    hold[lst] = item.replace('</td>', '')
                hold[-1] = hold[-1].replace('</tr>', '')
                hold = [float(hold[1]), float(hold[2]), float(hold[3]), float(hold[4])]
            elif n.text[0:12] == 'Underperform':
                underperform = str(n)
                underperform = underperform.split('<td align="center" class="yfnc_tabledata1">')
                for lst, item in enumerate(underperform): 
                    underperform[lst] = item.replace('</td>', '')
                underperform[-1] = underperform[-1].replace('</tr>', '')
                underperform = [float(underperform[1]), float(underperform[2]), float(underperform[3]), float(underperform[4])]
            elif n.text[0:4] == 'Sell':
                sell = str(n)
                sell = sell.split('<td align="center" class="yfnc_tabledata1">')
                for lst, item in enumerate(sell): 
                    sell[lst] = item.replace('</td>', '')
                sell[-1] = sell[-1].replace('</tr>', '')
                sell = [float(sell[1]), float(sell[2]), float(sell[3]), float(sell[4])]
        #Create Pandas Dataframe
        table = [strong_buy, buy, hold, underperform, sell]
        columns = ['Strong Buy', 'Buy', 'Hold', 'Underperform', 'Sell']
        index=['This Month', 'Last Month', 'Two Months Ago', 'Three Months Ago']
        df = pd.DataFrame(table, columns, index) 
        #Determine if the analyst opinion suggests to buy the stock
        is_positive_analyst_opinion = False
        if df['This Month']['Strong Buy'] + df['This Month']['Buy'] > df['This Month']['Hold'] + df['This Month']['Underperform'] + df['This Month']['Sell']:
                is_positive_analyst_opinion = True
        
        
        #Create Ditionary of Results
        results = collections.OrderedDict()
        results['Stock'] = stock
        results['TestRun'] = 'Analyst_Opinion'    
        results['DateRun'] = mods.Today() 
        results['DataFrame'] = df.reset_index().to_json(orient='index')
        results['Result'] = is_positive_analyst_opinion
        return results
    
    except:
        results = collections.OrderedDict()
        results['stock'] = stock
        results['TestRun'] = 'Analyst_Opinion'
        results['DateRun'] = mods.Today()
        results['Result'] = 'Test Failed'
        return results
##Testing:
#stock = 'AAPL'
#print Get_Analyst_Opinion(stock)