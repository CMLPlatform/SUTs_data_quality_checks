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


#%% balancing: 
# Columns sum should match row sum and the other way around
# Row sum 30 = col sum 43 + VA ? 
# or col sum 30 = row sum 43 + VA ?
# note from onenote earlier: Still seems to be col sum 30 = col sum 43 + VA
# I don't think they're shifted: in both tables, rows are products, and columns are transactions

sum_bp_supply = t_30_transactions.sum()
# sum_bp_col_supply = t_30_transactions.sum(axis=1) # different intermediate sums, but sum of the series is the same
tot_sup_bp = sum_bp_supply.sum()
# sum_bp_ind_supply = t_30_transactions.sum(axis=0)
# sum_bp_both_supply = t_30_transactions.sum(axis=None) # same as axis=0 and unspecified

sum_bp_use = t_43_transactions.sum() # gives total for the column; moving downwards by row
# sum_bp_col_use = t_43_transactions.sum(axis=1) # gives total for the row, because proceding by column index
int_con = sum_bp_use.sum()

# value added: 
gross_va_bp = t_41_transactions.sum().sum()
# check balancing
balance = tot_sup_bp - (int_con + gross_va_bp)

if balance == 0:
    print('The supply and use tables (with VA) are balanced: The difference is 0')
else:
    print('The tables are not balanced.There is a discrepancy of:', balance)

