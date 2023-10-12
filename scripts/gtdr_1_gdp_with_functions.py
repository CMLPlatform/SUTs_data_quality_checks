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

#%% GDP by income approach - Leave to last
# GDP = Gross VA at BP (other table) + taxes less subsidies on products (ST)
# Gross VA at BP = compensation of employees + other net taxes on production + consumption of fixed capital + net operating surplus
# use table 41

# create dictionary for storing results of GDP calcs
SU_GDP_approaches_results = {"income": None, "expenditure": None, "production": None}

# Calculate gdp

gross_va_bp = [
    t_41_transactions.iloc[t_41_transactions.index.get_level_values(0)=='Compensation of employees',:].iloc[0,:],
    # all compensation instead of only wages and salaries.
    # makes gdp by income and production the same.
    t_41_transactions.iloc[t_41_transactions.index.get_level_values(0)=='Other taxes less other subsidies on production',:],
    t_41_transactions.iloc[t_41_transactions.index.get_level_values(1)=='Consumption of fixed capital',:],
    # not sure if the below one is really only the 'net operating surplus'
    t_41_transactions.iloc[t_41_transactions.index.get_level_values(1)=='Operating surplus and mixed income, net',:]
    ]

gross_va_bp = pd.concat(gross_va_bp, axis=0)
gross_va_bp_sum = gross_va_bp.sum().sum()
# gdp calc and input into dict after the production approach 
# because they both use taxes less subsidies on products: tls_op

t41_coe = t_41_transactions.iloc[t_41_transactions.index.get_level_values(0)=='Compensation of employees',:].iloc[0,:]

#%% GDP by expenditure approach
# GDP = FCE (UT) + GCF (UT) + exports of goods and services (UT) - imports of goods and services (ST)
# FCE = Household fce + NIPSH fce + govt ce
# GFC = GFCF + acquisistions less disposals of valuables + changes in inventories
# + acquisistions less disposals of valuables + changes in inventories + exports of goods and services (UT)

# no need for dropping columns and loops, if just using the names based on the manual for GDP calc from SUTs
# however, a solution needs to be found for the 'of which: Domestic purchases by non-residents' column (level 2)



## changing variable names
fd_hh = t_43_wo_totals.iloc[:, t_43_wo_totals.columns.get_level_values(1)=='Final consumption expenditure by households, domestic concept']
exports = t_43_wo_totals.iloc[:, t_43_wo_totals.columns.get_level_values(0)=='Exports']
exports_simple = exports.iloc[:,0]  # important: in absence of unique names for levels, slice resulting df.
necessary_columns_pos = [
    t_43_wo_totals.iloc[:, t_43_wo_totals.columns.get_level_values(1)=='Final consumption expenditure by households, domestic concept'].iloc[:,0],
    # t43_transactions.iloc[:, t43_clean_mi.columns.get_level_values(2)=='of which: Domestic purchases by non-residents'],
    t_43_wo_totals.iloc[:, t_43_wo_totals.columns.get_level_values(1)=='Final consumption expenditure by NIPSH'],
    t_43_wo_totals.iloc[:, t_43_wo_totals.columns.get_level_values(1)=='Final consumption expenditure by government'],
    t_43_wo_totals.iloc[:, t_43_wo_totals.columns.get_level_values(1)=='Gross fixed capital formation'],
    t_43_wo_totals.iloc[:, t_43_wo_totals.columns.get_level_values(1)=='Acquisitions less disposals of valuables'],
    t_43_wo_totals.iloc[:, t_43_wo_totals.columns.get_level_values(1)=='Changes in inventories'],
    
    # t43_transactions.iloc[:, t43_clean_mi.columns.get_level_values(0)=='Exports'].iloc[:,0] # works, but dim 78, instead of 78,1
    # additional slicing creates a series instead of a df. If this is a problem: resize
    # the following 
    # t43_transactions.iloc[:, t43_transactions.columns.get_level_values(0)=='Exports'].iloc[:,0] - t43_transactions.iloc[:, t43_clean_mi.columns.get_level_values(0)=='Exports'].iloc[:,1]
    t_43_wo_totals.iloc[:, t_43_wo_totals.columns.get_level_values(0)=='Exports']
    ]

# comented out the exports net, not used somewhere else? 
# exports_net = t43_transactions.iloc[:, t43_transactions.columns.get_level_values(0)=='Exports'].iloc[:,0] - t43_transactions.iloc[:, t43_transactions.columns.get_level_values(0)=='Exports'].iloc[:,1]

gdp_expenditure_use = pd.concat(necessary_columns_pos, axis=1)
gdp_expenditure_use_sum = gdp_expenditure_use.sum().sum()  # first sum creates a series, 2nd creates a float or int
# gdp_expenditure_use_sumsum = gdp_expenditure_use_sum.sum()
# imports = t30_table_30_mi.iloc[:, t30_table_30_mi.columns.get_level_values(1)=='Imports, cif']
# gdp_expenditure_supply_sum = imports.sum().sum()
# necessary_columns_neg = [
#     t30_table_30_mi.iloc[:, t30_table_30_mi.columns.get_level_values(1)=='Imports, cif']
#     ]

necessary_columns_neg = [
    t_30_wo_totals.iloc[:, t_30_wo_totals.columns.get_level_values(1)=='Imports, cif']
    ]
# need the cif/fob adjustments on imports, but the column contains a lot of non-floats ('..') and therefore cannot be summed
# below would work but contains also the total rows and columns.
# t30_ciffob_adj = t30_table_30_mi.iloc[:, t30_table_30_mi.columns.get_level_values(1)=='cif/fob adjustment on imports']
# t30_ciffob_adj_list = []
# for value in t30_ciffob_adj.iloc[:,0]:
#     if type(value) == float:
#         t30_ciffob_adj_list.append(value)
# t30_ciffob_adj_value = np.sum(t30_ciffob_adj_list)        

# gdp_expenditure_supply_sum = necessary_columns_neg[0].sum().sum() - np.abs(table_30_excel_.iloc[11,87])     # quick & dirty fix of estimated(!) ciffob adjustment values

ciffob_adj = -2267 # = table_30_excel_.iloc[11,87] --> in excel file: "cif/fob adjustment on imports"
gdp_expenditure_supply_sum = necessary_columns_neg[0].sum().sum() - np.abs(ciffob_adj)

gdp_expenditure = gdp_expenditure_use_sum - gdp_expenditure_supply_sum  # too high: mistake in exports? # still true?

SU_GDP_approaches_results["expenditure"] = gdp_expenditure
#%% GDP by production approach
# GDP = Gross VA (BP) + Taxes less subsidies on products (ST)
# Gross VA = Total output at BP (ST) - Intermediate consumption (UT)

total_supply_bp = t_30_transactions.sum().sum()

intermediate_consumption = t_43_transactions.sum().sum()

gross_va = total_supply_bp - intermediate_consumption
tls_op = t_30_wo_totals.iloc[:, t_30_wo_totals.columns.get_level_values(0)=='Taxes less subsidies on products'].sum().sum()
# tls_op calculation is FAULTY, taxes less subsidies should be 88095, instead of 154731
# not because a totals row is included
# t30_table_30_mi STILL CONTAINS THE INTERMEDIATE TOTALS ROWS (AND COLS?)
gdp_production = gross_va + tls_op
SU_GDP_approaches_results["production"] = gdp_production

#%% Adding the GDP by income:
    
gdp_income = gross_va_bp_sum + tls_op
SU_GDP_approaches_results["income"] = gdp_income

#check variable names for all GDP calcs

#%% GDP comparison
print(SU_GDP_approaches_results)
print("Difference between production and expenditure GDP calculations: ", 
      SU_GDP_approaches_results["expenditure"] - SU_GDP_approaches_results["production"])

#%% testing

#%% to do next list 
"""
To do next list
# - balancing using VA in table 43 (in that way checking 30, 41, 43)
# - correct/redo GDP calculations

"""

