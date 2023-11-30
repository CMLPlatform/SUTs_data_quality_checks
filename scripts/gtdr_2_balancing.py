# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 11:34:29 2023

@author: Horsting

GTDR: Assignment 2 - Balancing

"""
#%% import packages & function file
import pandas as pd
import numpy as np

import gtdr_functions as functions

#%% Import files

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

# table 30
# import
t_30 = functions.excel_df(table_30, 30, 3)
# drop total columns/rows
t_30_wo_totals = functions.drop_int_totals(t_30, 30, 2)    # fault in code: probably need to change the levels when 
# dropping the intermediate totals
# slice transactions
t_30_transactions = t_30_wo_totals.iloc[:,0:65]


# table 41 (VA)
# import
t_41 = functions.excel_df(table_41, 41, 1)
# remove totals columns (THIS FUNCTION DOES NOT WORK FOR ROWS)
# But not necessary, implemented only VA rows selected
t_41_wo_totals = functions.drop_int_totals(t_41, 41, 0)
# slice 41
t_41_transactions = functions.VA_of_which_strip(t_41_wo_totals, 41)

#%% balancing

supply_use_balance = functions.balance(t_30_transactions, t_43_transactions, t_41_transactions)

if supply_use_balance == 0:
    print('The supply and use tables (with VA) are balanced: The difference is 0')
else:
    print('The tables are not balanced.There is a discrepancy of:', supply_use_balance)
    


