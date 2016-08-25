# -*- coding: utf-8 -*-
"""
Created on Wed Aug 17 18:14:22 2016

@author: eczaj
"""

import common_mods as mods
import stock_analysis_revenue as revenue
import stock_analysis_key_indicators as key
import stock_analysis_analyst_opinion as opinion
import stock_analysis_earnings_forecast as forecast
import stock_analysis_earnings_per_share as eps
import pprint

stocks = ['AAPL', 'MSFT', 'NVDA', 'GOOG']
for stock in stocks:
    stock = stock.lower()
    if mods.get_balance_sheet(stock, 'Common Stocks') != None:
        revenue_result = revenue.Get_Revenue(stock)
        key_result = key.Get_Key_Indicators(stock)
        opinion_result = opinion.Get_Analyst_Opinion(stock)
        forecast_result = forecast.Get_Earnings_Forecast(stock)
        eps_result = eps.Get_EPS(stock)
        
        #pprint.pprint(revenues)
        #pprint.pprint(keys)    
    