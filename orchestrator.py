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
import pprint

stocks = ['AAPL', 'MSFT', 'NVDA', 'GOOG']
for stock in stocks:
    stock = stock.lower()
    if mods.get_balance_sheet(stock, 'Common Stocks') != None:
        revenues = revenue.Get_Revenue(stock)
        keys = key.Get_Key_Indicators(stock)
        opinions = opinion.Get_Analyst_Opinion(stock)
        forecasts = forecast.Get_Earnings_Forecast(stock)
        
        #pprint.pprint(revenues)
        pprint.pprint(keys)    
    