# -*- coding: utf-8 -*-
"""
Created on Wed Aug 17 18:14:22 2016

@author: eczaj
"""

import common_mods as mods
import collections
#Test 1
import stock_analysis_revenue as revenue
#Test 2
import stock_analysis_key_indicators as key
#Test 3
import stock_analysis_roe as roe
import stock_analysis_analyst_opinion as opinion
import stock_analysis_earnings_forecast as forecast
import stock_analysis_earnings_per_share as eps
import stock_analysis_eps_surprise as surprise
#Test 7 Earnings Forecast
import stock_analysis_growth_forecast as growth_forecast
#Test 8
import stock_analysis_peg_ratio as peg
#Test 9
import stock_analysis_price_earnings_v_industry as industry
#Test 11
import stock_analysis_shares_short as shares_short
#import pprint


def Dict_Aggregator(data_dict, test_dict):
    if test_dict['Result'] == True or test_dict['Result'] == False:
        data_dict[test_dict['TestRun']] = test_dict['Result']
        mods.Insert_Data(export, test_dict['TestRun'], test_dict)
        return data_dict
        
def Evaluator(data_dict):
    t = 0
    f = 0
    for item in data:
        if data[item] == True:
            t += 1
        elif data[item] == False:
            f += 1
    data_dict['OverallPassed'] = t
    data_dict['OverallFailed'] = f
    if t > f:
        data_dict['Overall'] = True
    else:
        data_dict['Overall'] = False
    return data_dict


#Mongo DB Insert -> mods.Insert_Data('DB Name', 'Collection_Name', JSON Variable)
#Mongo DB Name -> export variable
export = 'test'
stocks = ['AAPL', 'NVDA']

def main():
    for stock in stocks:
        data = collections.OrderedDict()
        data['DateRun'] = mods.Today()
        data['Stock'] = stock
        stock = stock.lower()
        if mods.get_balance_sheet(stock, 'Common Stocks') != None:
            #Revenue Test        
            revenue_result = revenue.Get_Revenue(stock)
            Dict_Aggregator(data, revenue_result)      
            #4 Key Result Tests        
            key_result = key.Get_Key_Indicators(stock)
            for item in key_result:
                Dict_Aggregator(data, item)
            #Positive Return on Equity        
            roe_result = roe.Get_ROE(stock)
            Dict_Aggregator(data, roe_result)
            #Analyst Opinion
            opinion_result = opinion.Get_Analyst_Opinion(stock)
            Dict_Aggregator(data, opinion_result)
            #Earnings Forecast        
            forecast_result = forecast.Get_Earnings_Forecast(stock)
            Dict_Aggregator(data, forecast_result)
            #Earnings Per Share        
            eps_result = eps.Get_EPS(stock)
            Dict_Aggregator(data, eps_result)
            #Earnings Surprise        
            eps_surprise = surprise.Get_Earnings_Surprise(stock)
            Dict_Aggregator(data, eps_surprise)        
            #Growth Forecast
            growth = growth_forecast.Get_Growth_Forecast(stock)
            Dict_Aggregator(data, growth) 
            #PEG Ratio        
            peg_ratio = peg.Get_PEG_Ratio(stock)
            Dict_Aggregator(data, peg_ratio)
            #Earnings Versus Industry        
            pevi = industry.Get_Earnings_V_Industry(stock)
            Dict_Aggregator(data, pevi)
            #Insider Trading        
            short = shares_short.Get_Shares_Short(stock)
            Dict_Aggregator(data, short)
        mods.Insert_Data(export, 'Results', Evaluator(data))

if __name__ == '__main__':
    main()
'''
Test and Collections
1. Revenue #Done Revenue
2. Earnings Per Share #Done EPS
3. Return on Equity #Done ROE
4. Recommendations
5. Earnings Surprises #Done EPS_Surprise
6. Forecast #Done Forecast
7. Earnings Growth #Done
8. PEG Ratio
9. Industry Earnings #Done
10. Days to Cover
11. Insider Trading #Done Shares Short
12. Weighted Alpha
'''
    
    