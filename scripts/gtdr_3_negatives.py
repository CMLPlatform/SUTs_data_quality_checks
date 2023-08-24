# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 17:13:06 2023

@author: Horsting

GTDR: Assignment 3 - Check for negatives

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

#%% Checking for negatives and add to dictionary

neg_dict = {
    'neg_dict_t_30_wo_totals': functions.neg_check(t_30_wo_totals, 30),

    'neg_dict_t_43_wo_totals': functions.neg_check(t_43_wo_totals, 43),

    'neg_dict_t_41_wo_totals': functions.neg_check(t_41_wo_totals, 41),

    'neg_dict_t_30_transactions': functions.neg_check(t_30_transactions, 30),

    'neg_dict_t_43_transactions': functions.neg_check(t_43_transactions, 43),

    'neg_dict_t_41_transactions': functions.neg_check(t_41_transactions, 41)
    }

#%% testing

# # Create a sample dataframe
# df = pd.DataFrame({
#     'A': [1, 2, 3],
#     'B': [4, 5, 6],
#     'C': [7, 8, 9]
# })

# df1 = pd.DataFrame({
#     'A': [True, True, True],
#     'B': [True, True, False],
#     'C': [True, True, True]
# })

# print(df)
        
# # for col in df:
# #     print(col)
    
# for index, row in df.iterrows():
#     print(index,row)
#     # print(row)
    
# for row in neg_df_30.itertuples():
#     print(row)
#     i=0
#     for entry in row:
#         print(i, entry)
#         i+=1
