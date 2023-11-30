# -*- coding: utf-8 -*-
"""
Created on Thu May 25 12:30:06 2023

@author: Horsting

GTDR

Assignment 1: GDP from OECD Data
Clean(er) start for github


"""

#%% Change log + to do list
"""
To do: 
- Remove hardcoding as much as possible
- Check if outcomes are the same as in gtdr_1_gdp.py

Change log: 
- Converted to use with functions file. 
 



"""
#%% Import packages

import pandas as pd
import numpy as np

import gtdr_functions as functions

#%% Data import/read + checks

table_30 = "OECD_Data_downloads\Table_30.xlsx"  # supply
table_43 = "OECD_Data_downloads\Table_43.xlsx"  # use
table_41 = "OECD_Data_downloads\Table_41.xlsx"  # va

# table 43
# import
t_43 = functions.excel_df(table_43, 43, 3)
# drop total columns/rows
t_43_wo_totals = functions.drop_int_totals(t_43, 43, 1)
# slice transactions
t_43_transactions = t_43_wo_totals.iloc[:,0:65]
# t43_total_inputs = t_43_wo_totals.iloc[:,0:65].sum()

# table 30
# import
t_30 = functions.excel_df(table_30, 30, 3)
# drop total columns/rows
t_30_wo_totals = functions.drop_int_totals(t_30, 30, 2)    # fault in code: probably need to change the levels when 
# dropping the intermediate totals

# slice transactions
t_30_transactions = t_30_wo_totals.iloc[:,0:65]
# t43_total_outputs = t_43_wo_totals.iloc[:,0:65].sum()

# table 41 (VA)
# import
t_41 = functions.excel_df(table_41, 41, 1)
# remove totals columns (THIS FUNCTION DOES NOT WORK FOR ROWS)
# But not necessary, implemented only VA rows selected
t_41_wo_totals = functions.drop_int_totals(t_41, 41, 0)

# slice 41
t_41_transactions = functions.VA_of_which_strip(t_41_wo_totals, 41)

#%% GDP calc with functions file

GDP_results = functions.gdp(t_30_transactions, 
                            t_41_transactions, 
                            t_43_transactions,
                            t_30_wo_totals,
                            t_43_wo_totals,
                            t_30)

#%% GDP comparison
print(GDP_results)
print("Difference between production and expenditure GDP calculations: ", 
      GDP_results["expenditure"] - GDP_results["production"])



