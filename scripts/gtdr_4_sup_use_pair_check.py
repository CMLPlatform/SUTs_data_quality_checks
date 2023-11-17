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

#%% Check supply-use pairs --> works, but turns out not to be the objective.

t_30_zeros = t_30_transactions[t_30_transactions == 0].notna()  # mask zeros as True, nonzeros False
t_43_zeros = t_43_transactions[t_43_transactions == 0].notna()

# t_30_zeros = t_30_transactions[t_30_transactions == 0]    # masks nonzeros as nans. Nans give difficulty in further comparison
# t_43_zeros = t_43_transactions[t_43_transactions == 0]

# equality_check = t_30_zeros.compare(t_43_zeros)     # does not work because col labels are not the same.
t_43_zeros.columns = t_30_zeros.columns     # making equal columns index, now for 43 does not hold, but only the P2 turned into P1 in the names

t_30_43_comp = t_30_zeros[t_30_zeros == t_43_zeros]  # masking matching Trues 'True', Falses 'False', and non-matches 'nan'
                                                # non-matches are zeros that match a nonzero entry in the other df
t_30_43_discrepancies = t_30_43_comp[t_30_43_comp != np.nan].notna() # non-zero matches are masked as False. True or False masked as True
# t_30_43_2 = t_30_43[t_30_43 == np.nan].notna()  # does not work: everything masked as False

# create dict of the zero-nonzero matches found in t_30_43_1

#%% Check supply 0's, and index magnitude of the main products on the diagonal

# start with getting lowest level names of the square table: products and industries.

# t_30
t_30_main_products = t_30_transactions.index.get_level_values(0)
t_30_products = t_30_transactions.index.get_level_values(1)
t_30_main_industries = t_30_transactions.columns.get_level_values(2)
t_30_industries = t_30_transactions.columns.get_level_values(3)

t_30_product_list = []
t_30_industry_list = []

for i in np.arange(0, len(t_30_products)):
    if type(t_30_products[i]) == float:
        # print(i, t_30_main_products[i], t_30_products[i])
        t_30_product_list.append(t_30_main_products[i])
    else:
        t_30_product_list.append(t_30_products[i])
        
    if type(t_30_industries[i]) == float:
        t_30_industry_list.append(t_30_main_industries[i])
    else:
        t_30_industry_list.append(t_30_industries[i])
        
# t_43
# start with getting lowest level names of the square table: products and industries.
t_43_main_products = t_43_transactions.index.get_level_values(0)
t_43_products = t_43_transactions.index.get_level_values(1)
t_43_main_industries = t_43_transactions.columns.get_level_values(1)
t_43_industries = t_43_transactions.columns.get_level_values(2)

t_43_product_list = []
t_43_industry_list = []

for i in np.arange(0, len(t_43_products)):
    if type(t_43_products[i]) == float:
        # print(i, t_30_main_products[i], t_30_products[i])
        t_43_product_list.append(t_43_main_products[i])
    else:
        t_43_product_list.append(t_43_products[i])
        
    if type(t_43_industries[i]) == float:
        t_43_industry_list.append(t_43_main_industries[i])
    else:
        t_43_industry_list.append(t_43_industries[i])
        
# test = t_30_transactions.loc[[t_30_product_list[3]],[t_30_industry_list[3]]]
# test_1 = t_30_transactions.loc[[t_30_product_list[3]]]
# test_2 = t_30_transactions.loc[[t_30_product_list[3]], [3]]
# test_3 = t_30_transactions.loc[[t_30_product_list[3]],[t_30_industry_list[3]]]
# test_4 = t_30_transactions.loc[[t_30_industry_list[3]]]
# # test_5 = t_30_transactions.loc[('nan', [t_30_product_list[1]]),('nan', 'nan', 'nan', [t_30_industry_list[1]])]
# test_6 = t_30_transactions.iloc[[3],[3]]    # returns df of size (1,1)
# test_6_a = test_6.iloc[0]                   # returns series
# test_6_b = test_6.iloc[0][0]                # returns int (value)
# test_7 = t_30_transactions.iloc[1],[1]      # returns tuple of size 2
#                                             # first series of row [1], then [1] (so the given [1] instead of a value)
# test_8 = t_30_transactions.iloc[1][1]       # returns int (value) --> use for diagonal

supply_diagonal_zeros = {}
for i in np.arange(0, len(t_30_transactions)):
    if t_30_transactions.iloc[i][i] == 0:
        child_dict = t_30_product_list[i]
        supply_diagonal_zeros.update({
            child_dict: {
                'Industry': t_30_industry_list[i], 
                'row': i, 
                'column': i, 
                'value': t_30_transactions.iloc[i][i]
                }
            })
        
use_diagonal_zeros = {}
for i in np.arange(0, len(t_43_transactions)):
    if t_43_transactions.iloc[i][i] == 0:
        child_dict = t_43_product_list[i]
        use_diagonal_zeros.update({
            child_dict: {
                'Industry': t_43_industry_list[i], 
                'row': i, 
                'column': i, 
                'value': t_43_transactions.iloc[i][i]
                }
            })

# use_zeros.update({'Product name': t_43_product_list[63],'row':63, 'column': 63})

# need a nested dictionary instead to keep from overwriting last value.

#%% Check use but no supply 
#Check against per product use in every industry: is total use either 0 or <50% of supply?

supply_zero_use_nonzero = {}

for item in supply_diagonal_zeros:
    child_dict = item
    if t_43_transactions.iloc[supply_diagonal_zeros[item]['row']][:].sum() != 0:
        supply_zero_use_nonzero.update({
            child_dict: {
                'Product' : item,
                'Supply' : 0,
                'Use': t_43_transactions.iloc[supply_diagonal_zeros[item]['row']][:].sum()
                }
            })

print('The following products do not have supply while being used:\n', supply_zero_use_nonzero)

supply_diagonal = {}

for i in np.arange(0, len(t_30_transactions)):
# if t_30_transactions.iloc[i][i] == 0:
    child_dict = t_30_product_list[i]
    supply_diagonal.update({
        child_dict: {
            'Industry': t_30_industry_list[i], 
            'row': i, 
            'column': i, 
            'value': t_30_transactions.iloc[i][i]
            }
        })
    
supply_use_bigdif = {}

for item in supply_diagonal:
    child_dict = item
    if t_43_transactions.iloc[supply_diagonal[item]['row']][:].sum() >= 2 * (supply_diagonal[item]['value']):
        supply_use_bigdif.update({
            child_dict: {
                'Supply': supply_diagonal[item]['value'],
                'Use': t_43_transactions.iloc[supply_diagonal[item]['row']][:].sum()
                }
            })
    
    elif t_43_transactions.iloc[supply_diagonal[item]['row']][:].sum() <= 0.5 * supply_diagonal[item]['value']:
        supply_use_bigdif.update({
            child_dict: {
                'Supply': supply_diagonal[item]['value'],
                'Use': t_43_transactions.iloc[supply_diagonal[item]['row']][:].sum()
                }
            })

print('The following products have large differences between supply and use:\n', supply_use_bigdif)

# to do: 
    # - alter the boundaries based on what Franco says are large differences.

"""
Supply/use pairs:
	- Chosen parameters:
		○ Take the diagonals in the t_30 supply matrix as the main supply/products.
			§ Can also take row sum of t_30 as supply per product, just like now row sum of t_43
Is that what Franco meant when he said 'column by column comparison'. During one of the previous meetings?

"""

# supply_diagonal = {}

# for item in supply_diagonal:
#     child_dict = item
#     if t_43_transactions.iloc[supply_diagonal_zeros[item]['row']][:].sum() != 0:
#         supply_zero_use_nonzero.update({
#             child_dict: {
#                 'Product' : item,
#                 'Supply' : 0,
#                 'Use': t_43_transactions.iloc[supply_diagonal_zeros[item]['row']][:].sum()
#                 }
#             })

# test_list = [1,2,3,4,5]
# test_array = np.array(test_list)
# test_array_sum = test_array.sum()
# test_slice = t_43_transactions.iloc[supply_diagonal_zeros[item]['row']][:]
# test_slice_sum = test_slice.sum()

#%% Check use but no supply
