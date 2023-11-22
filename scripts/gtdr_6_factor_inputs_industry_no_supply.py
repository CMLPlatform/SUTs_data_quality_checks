# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 12:39:03 2023

@author: Horsting

GTDR: Assignment 6 - Factor input into industry, but no supply

Factor inputs:
    - Taxes
    - Subsidies
    - Wages
    
"""

#%% import packages & function file
import pandas as pd
import numpy as np

import gtdr_functions as functions

#%% Import files
table_30 = "OECD_Data_downloads\Table_30.xlsx"  # supply
table_41 = "OECD_Data_downloads\Table_41.xlsx"  # factor inputs (VA)

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

#%% create industries and products lists

t_30_indices_tuple = functions.indices_lists(t_30_transactions, 30)
t_30_product_list = t_30_indices_tuple[0]
t_30_industry_list = t_30_indices_tuple[1]

t_41_indices_tuple = functions.indices_lists(t_41_wo_totals, 41)
t_41_fi_list = t_41_indices_tuple[0]
t_41_activity_list = t_41_indices_tuple[1]


#%% check industries with 0 supply, and then if there're fi in that industry (activity)

no_sup_with_fi = functions.fi_in_industry_no_supply(t_30_transactions, t_41_wo_totals, 
                                                    t_30_product_list, t_30_industry_list, 
                                                    t_41_fi_list, t_41_activity_list)

print('the following', len(no_sup_with_fi), 
      'industries have no supply, but there are nonzero factor inputs: \n',
      no_sup_with_fi, '\n')
#%% Find industries with no supply (colsums t_30 transactions): create dict
# # --> not necessary: just know where to find it in the table
# # need to find an industry's supply and if that's 0, check against the VARIOUS factor inputs (not totals).

# t_30_totals_cols = t_30_transactions.sum(axis=0)
# zero_sup_ind = {}
# for i in np.arange(0, len(t_30_transactions)):
#     if t_30_totals_cols.iloc[i] == 0:
#         child_dict = t_30_industry_list[i]
#         zero_sup_ind.update({
#             child_dict: {
#                 'Industry': t_30_industry_list[i], 
#                 'row': i, 
#                 'column': i, 
#                 'value': t_30_transactions.iloc[i][i]
#                 }
#             })

#%% For the industries with no supply, check all factor inputs for nonzeros.

# total_factor_input = {}
# for item in zero_sup_ind:
#     # print(item)
    
#     # what is j, and should it not be less hard-coded? 
#     j = zero_sup_ind['P1, Activities of extraterritorial organizations and bodies']['column']   # correct?
    
#     for i in np.arange(0,len(t_41_wo_totals.index)):
#         if t_41_wo_totals.iloc[i][j] != 0:
#             child_dict = t_41_fi_list[i]
#             total_factor_input.update({
#                 child_dict: {
#                     'Industry': item, 
#                     'row': i, 
#                     'column': j, 
#                     'value': t_41_wo_totals.iloc[i][j]
#                     }
#                 })
            
# print('the following', len(total_factor_input), 
#       'industries have no supply, but there are nonzero factor inputs: \n',
#       total_factor_input, '\n')