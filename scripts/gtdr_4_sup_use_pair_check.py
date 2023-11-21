# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 18:40:21 2023

@author: Horsting

GTDR: Assignment 4 - Supply but no use? And vice versa.

"""
#%% import packages & function file
import pandas as pd
import numpy as np

import gtdr_functions as functions

#%% Import files
table_30 = "OECD_Data_downloads\Table_30.xlsx"  # supply
table_43 = "OECD_Data_downloads\Table_43.xlsx"  # use
table_41 = "OECD_Data_downloads\Table_41.xlsx"  # factor inputs (VA)

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
# not necessary anymore(?) --> yes, used to compare differences!
t_41_transactions = functions.VA_of_which_strip(t_41_wo_totals, 41)

#%% create 1-D lists of products/industries/activities
t_30_indices_tuple = functions.indices_lists(t_30_transactions, 30)
t_30_product_list = t_30_indices_tuple[0]
t_30_industry_list = t_30_indices_tuple[1]

t_43_indices_tuple = functions.indices_lists(t_43_transactions, 43)
t_43_product_list = t_43_indices_tuple[0]
t_43_industry_list = t_43_indices_tuple[1]

t_41_indices_tuple = functions.indices_lists(t_41_wo_totals, 41)
t_41_fi_list = t_41_indices_tuple[0]
t_41_activity_list = t_41_indices_tuple[1]

#%% Check using functions file: 
    # for supply but no use, use but no supply, and large differences.
    
supply_use_results = functions.supply_use_pairs(t_30_transactions, t_43_transactions, t_41_transactions, t_41_wo_totals, 
                                                t_30_product_list, t_30_industry_list, t_43_product_list, t_43_industry_list,
                                                t_41_fi_list, t_41_activity_list)

print('The following products have supply while not being used:\n', supply_use_results[0], '\n')
print('The following products do not have supply but are used:\n', supply_use_results[1], '\n')
print('The following', len(supply_use_results[2]), 'products/activities have large differences: \n', 
      supply_use_results[2], '\n')

#%% To do
# Still check if the FD shouldnt be used, and what the boundary conditions for the bigdifs should be.

