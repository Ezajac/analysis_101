# -*- coding: utf-8 -*-
"""
Created on Fri Jul 01 12:24:13 2016

@author: eczaj
"""

import json
import helper.common_mods as mods
import collections

def Get_Key_Indicators(stock):  
    '''Use the Common Modules to scrape data from different websites for the stock. Determine if the results are positive.
    Return the results in JSON objects.'''
    try:
        # Get Last Three Years of Net Income
        net_income =  mods.get_net_income(stock, 'Net Income')
        net_income = mods.Is_Negative(net_income)    
        last_reported_ni, second_reported_ni, third_reported_ni = float(net_income[0]), float(net_income[1]), float(net_income[2])
       
        #Get Last Three Years of Common Stock
        common_stock = mods.get_balance_sheet(stock, 'Common Stocks')
        common_stock = mods.Is_Negative(common_stock)  
        last_reported_cs, second_reported_cs, third_reported_cs = float(common_stock[0]), float(common_stock[1]), float(common_stock[2])    
    
        treasury_stock = mods.get_balance_sheet(stock, 'Treasury Stock')  
        treasury_stock = mods.Is_Negative(treasury_stock)
        last_reported_ts, second_reported_ts, third_reported_ts = float(treasury_stock[0]), float(treasury_stock[1]), float(treasury_stock[2])      
    
        #Get Dates for Last Three Reported Years
        dates = mods.get_reported_dates(stock)
        last_reported_dt, year_before_reported_dt, two_yr_before_reported_dt = dates[0], dates[1], dates[2]
        
        #Test if EPS is postivie for last three years
        last_reported_eps, second_reported_eps, third_reported_eps  = last_reported_ni/(last_reported_cs - last_reported_ts),second_reported_ni/(second_reported_cs - second_reported_ts), third_reported_ni/(third_reported_cs - third_reported_ts)   
        is_positive_eps = False
        if last_reported_eps > second_reported_eps and second_reported_eps > third_reported_eps:
            is_positive_eps = True
        
        #Get Cash On Hand Last Three Years
        cash = mods.get_balance_sheet(stock, 'Cash')
        cash = mods.Is_Negative(cash)
        last_reported_cash, second_reported_cash, third_reported_cash = float(cash[0]), float(cash[1]), float(cash[2])
        
        #Get Long Term Debt
        debt = mods.get_balance_sheet(stock, '>Long-Term Debt')
        debt = mods.Is_Negative(debt)
        last_reported_debt, second_reported_debt, third_reported_debt = float(debt[0]), float(debt[1]), float(debt[2])
        
        #Determine Long Term Investments
        investments = mods.get_balance_sheet(stock, 'Long-Term Investments')
        investments = mods.Is_Negative(investments)
        last_reported_investments, second_reported_investments, third_reported_investments = float(investments[0]), float(investments[1]), float(investments[2])
        
        #Test if Net Income has been positive the last three years
        is_positive_ni = False
        if last_reported_ni > second_reported_ni and second_reported_ni > third_reported_ni:
            is_positive_ni = True
        
        #Test if Cash on Hand is positive
        is_positive_cash = False
        if last_reported_cash > 5000000:
            is_positive_cash = True     
            
        #Create Ditionarys of Results     
        results_cash = collections.OrderedDict()
        results_cash['Stock'] = stock
        results_cash['TestRun'] = 'Cash'
        results_cash['DateRun'] = mods.Today()
        results_cash['Result'] = is_positive_cash
        results_cash[last_reported_dt] = last_reported_cash
        results_cash[year_before_reported_dt] = second_reported_cash
        results_cash[two_yr_before_reported_dt] = third_reported_cash 
        
        results_ni = collections.OrderedDict()
        results_ni['Stock'] = stock    
        results_ni['TestRun'] = 'Net_Income'
        results_ni['DateRun'] = mods.Today()
        results_ni['Result'] = is_positive_ni
        results_ni[last_reported_dt] = last_reported_ni
        results_ni[year_before_reported_dt] = second_reported_ni
        results_ni[two_yr_before_reported_dt] = third_reported_ni 
        
        debt_data = collections.OrderedDict()
        debt_data['Stock'] = stock
        debt_data['TestRun'] = 'Long_Term_Debt'    
        debt_data['DateRun'] = mods.Today()
        debt_data['Result'] = 'Data_Only'
        debt_data[last_reported_dt] = last_reported_debt
        debt_data[year_before_reported_dt] = second_reported_debt
        debt_data[two_yr_before_reported_dt] = third_reported_debt
        
        invest_data = collections.OrderedDict()
        invest_data['Stock'] = stock
        invest_data['TestRun'] = 'Long_Term_Investment'    
        invest_data['DateRun'] = mods.Today()
        invest_data['Result'] = 'Data_Only'
        invest_data[last_reported_dt] = last_reported_investments
        invest_data[year_before_reported_dt] = second_reported_investments
        invest_data[two_yr_before_reported_dt] = third_reported_investments
        return [results_cash, results_ni, invest_data, debt_data]

    except:
        results_cash = collections.OrderedDict()
        results_cash['stock'] = stock
        results_cash['TestRun'] = 'Cash'
        results_cash['DateRun'] = mods.Today()
        results_cash['Result'] = 'Test Failed'
        
        results_ni = collections.OrderedDict()
        results_ni['stock'] = stock
        results_ni['TestRun'] = 'Net_Income'
        results_ni['DateRun'] = mods.Today()
        results_ni['Result'] = 'Test Failed'
        return [results_cash, results_ni]

#Testing:
#stock = 'aapl'
#print Get_Key_Indicators(stock)
#print mods.get_balance_sheet(stock, 'Treasury Stock')
#print get_balance_sh(stock, 'Common Stocks')