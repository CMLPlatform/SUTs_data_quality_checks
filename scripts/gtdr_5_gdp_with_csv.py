# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 16:31:41 2023

@author: Horsting

GTDR: Assignment 5 - GDP Calc using CSV files
"""
#%% import packages & function file
import pandas as pd
import numpy as np

import gtdr_functions as functions

#%% Import files

# Table 30 | Supply
t_30_csv = pd.read_csv('OECD_Data_downloads\SNA_TABLE30_25052023111909457.csv', header=0)
t_43_csv = pd.read_csv('OECD_Data_downloads\SNA_TABLE43_25052023114840741.csv', header=0)
t_41_csv = pd.read_csv('OECD_Data_downloads\SNA_TABLE41_25052023114000008.csv', header=0)

#%% Construction of table --> less detail, so only global calcs? 

# table 30

# removing leading and trailing white spaces
for row in t_30_csv.index:  # not specifying .index results in iteration over every field instead of the row nr.
    t_30_csv.loc[row, 'Transaction'] = t_30_csv.loc[row, 'Transaction'].strip()
    t_30_csv.loc[row, 'Product'] = t_30_csv.loc[row, 'Product'].strip()
    
transactions = t_30_csv.loc[:,'Transaction'].unique()
# cols = transactions.unique()
products = t_30_csv.loc[:,'Product'].unique()
# rows = products.unique()

t_30 = pd.DataFrame(np.full((len(products),len(transactions)), np.nan), index=products, columns=transactions)
t_30.sort_index(inplace=True)
t_30.sort_index(axis=1, inplace=True)

for row in t_30_csv.index:
    # print(row) # --> gives index as integer now
    t_30.loc[t_30_csv.loc[row,'Product'], t_30_csv.loc[row,'Transaction']] = t_30_csv.loc[row,'Value']
# Q: What do 'Product' and 'Transaction' do in the line above? 
# A: They are the column names in the csv file. no need to adjust them with the numbers of the table name.

# table 43
# transactions_43 = t_43_csv.loc[:,'Transaction'].unique()
# products_43 = t_43_csv.loc[:,'Product'].unique()

# t_43 = pd.DataFrame(np.full((len(products_43),len(transactions_43)), np.nan), index=products_43, columns=transactions_43)
# t_43.sort_index(inplace=True)
# t_43.sort_index(axis=1, inplace=True)

# for row in t_43_csv.index:
#     t_43.loc[t_43_csv.loc[row,'Product'], t_43_csv.loc[row,'Transaction']] = t_43_csv.loc[row,'Value']



# testing how to remove white spaces here so the ignore list will work, without
# messing up the keys to match the csv values in the df positions. 
# index 126 = 'P2, Manufacturing ', so with a trailing whitespace
for row in t_43_csv.index:  # not specifying .index results in iteration over every field instead of the row nr.
    t_43_csv.loc[row, 'Transaction'] = t_43_csv.loc[row, 'Transaction'].strip()
    # t_43_csv.loc[row, 'Product'] = t_43_csv.loc[row, 'Product'].strip('bp')
    # t_43_csv.loc[row, 'Product'] = t_43_csv.loc[row, 'Product'].strip(', ')     # because trailing ',' was not removed in form of .strip(',bp') 
    t_43_csv.loc[row, 'Product'] = t_43_csv.loc[row, 'Product'].strip(', bp')
    t_43_csv.loc[row, 'Product'] = t_43_csv.loc[row, 'Product'].strip()
    
# print(t_43_csv.loc[126,'Transaction'])

transactions_43 = t_43_csv.loc[:,'Transaction'].unique()
products_43 = t_43_csv.loc[:,'Product'].unique()

t_43 = pd.DataFrame(np.full((len(products_43),len(transactions_43)), np.nan), index=products_43, columns=transactions_43)
t_43.sort_index(inplace=True)
t_43.sort_index(axis=1, inplace=True)

for row in t_43_csv.index:
    t_43.loc[t_43_csv.loc[row,'Product'], t_43_csv.loc[row,'Transaction']] = t_43_csv.loc[row,'Value']

# table 41

for row in t_41_csv.index:  # not specifying .index results in iteration over every field instead of the row nr.
    t_41_csv.loc[row, 'Transaction'] = t_41_csv.loc[row, 'Transaction'].strip()
    t_41_csv.loc[row, 'Activity'] = t_41_csv.loc[row, 'Activity'].strip()
    
transactions_41 = t_41_csv.loc[:,'Transaction'].unique()
activities_41 = t_41_csv.loc[:,'Activity'].unique()

t_41 = pd.DataFrame(np.full((len(transactions_41),len(activities_41)), np.nan), index=transactions_41, columns=activities_41)
t_41.sort_index(inplace=True)
t_41.sort_index(axis=1, inplace=True)


for row in t_41_csv.index:
    # only use the rows with current prices, not constant prices from last year.
    if t_41_csv.loc[row,'MEASURE'] == 'C':
        # print(entry)
        # t_41.drop(index = row, inplace=True)  # drops row and messes up index.
        t_41.loc[t_41_csv.loc[row,'Transaction'], t_41_csv.loc[row,'Activity']] = t_41_csv.loc[row,'Value']

#%% select & drop int. totals manually? 

t_30_ignore_ = open("t_30_total_cols_rows.txt", "r")
t_30_ignore = t_30_ignore_.read().split('\n')
t_30_ignore_list = []
for line in t_30_ignore:
    if line != '':
        t_30_ignore_list.append(line.strip())

for entry in t_30.index: 
    if entry in t_30_ignore_list:
        # print(entry)
        t_30.drop(index = entry, inplace=True) 
        
# Manual drops because for some reason they're not picked up
# see also at table 43, consider fix mentioned there
# t_30.drop(index='Wholesale&retail trade serv., repair serv. of motor vehicles & motorcycles', inplace=True)

for entry in t_30.columns: 
    if entry in t_30_ignore_list:
        t_30.drop(columns = entry, inplace=True) 
# what to do with the Direct purchases abroad by residents and the cif/fob adjustment columsn? 
# only used for corrections, possible to retreive these numbers later.

# table 43
for entry in t_43.index: 
    if entry in t_30_ignore_list:
        # print(entry)
        t_43.drop(index = entry, inplace=True) 

# manually drop taxes less subsidies row, which is there for no apparent reason in the csv
# and necessary as a column from other tables later on
# nicer fix: make txt files for every table.

# check value of the tls on products first: 
tls_on_products = t_43.loc['Taxes less subsidies on products',:].sum()

t_43.drop(index='Taxes less subsidies on products', inplace=True)
# t_43.drop(index='Wholesale&retail trade serv., repair serv. of motor vehicles & cycles', inplace=True)

for entry in t_43.columns: 
    if entry in t_30_ignore_list:
        t_43.drop(columns = entry, inplace=True) 

# STILL CHECK ALL POSSIBLE COLUMN/ROW NAMES IN THE CSV FILES AND DETERMINE NO TOTAL ROWS ARE LEFT 
# AND ARE ALL ROWS ACCOUNTED FOR? WHAT DO THE ONES NOT PRESENT IN XLSX FILES MEAN? 

t_30_index_check = t_30.index
# index check passed
t_30_columns_check = t_30.columns
# from check: manually drop additionally:
# 1	Output at basic prices (P1), Total activity
# 68	Total supply at basic prices
# 69	Total supply at purchasers' prices


t_43_index_check = t_43.index
# check result: no filter applied, possibly because of ', bp' after the match
t_43_columns_check = t_43.columns
# some dropped, some not dropped even though they look exactly the same, e.g.:
    # P2, Agriculture, forestry and fishing
t_30_ignore_list[29]
t_43.columns[18]
# these two have the same length, and same type
if t_30_ignore_list[29] == t_43.columns[18]:
    print('SAME, WTF?!')
    # result: same
# and 'P2, Manufacturing'
t_30_ignore_list[30]
t_43.columns[58]
if t_30_ignore_list[30] == t_43.columns[58]:
    print('SAME, WTF?!')
    #result: not same
# these two differ in length


# table 41
for entry in t_41.index: 
    if entry in t_30_ignore_list:
        # print(entry)
        t_41.drop(index = entry, inplace=True) 

for entry in t_41.columns: 
    if entry in t_30_ignore_list:
        t_41.drop(columns = entry, inplace=True) 
        

#%% calc gdp 3 ways:

# create dictionary for storing results of GDP calcs
SU_GDP_approaches_results = {"income": None, "expenditure": None, "production": None}

#%% GDP by production approach
# GDP = Gross VA (BP) + Taxes less subsidies on products (ST)
# Gross VA = Total output at BP (ST) - Intermediate consumption (UT)

t_30_drop_for_production = pd.concat([
    t_30.loc[:,'Imports, cif'],
    t_30.loc[:,'Taxes less subsidies on products'],
    t_30.loc[:,'Trade and transport margins']
    ], axis=1)

# t_30_transactions = t_30

# actually output at bp, not supply.
total_supply_bp = t_30.sum().sum() - t_30_drop_for_production.sum().sum()
# correct value: 1,569,815 
# here: 1569815.0

t_43_drop_for_production = pd.concat([
    t_43.loc[:,'Acquisitions less disposals of valuables'],
    t_43.loc[:,'Changes in inventories'],
    t_43.loc[:,'Exports'],
    t_43.loc[:,'Final consumption expenditure by NIPSH'],
    t_43.loc[:,'Final consumption expenditure by government'],
    t_43.loc[:,'Final consumption expenditure by households, domestic concept'],
    t_43.loc[:,'Gross fixed capital formation'],
    ],axis=1)

intermediate_consumption = t_43.sum().sum() - t_43_drop_for_production.sum().sum()
# correct value: 844855.0
# here: 822209.0

gross_va = total_supply_bp - intermediate_consumption
# correct value: 724960
# here: 747606.0

tls_op = t_30.loc[:,'Taxes less subsidies on products'].sum()
# correct value: 88095
# here: 88095.0

gdp_production = gross_va + tls_op
SU_GDP_approaches_results["production"] = gdp_production

# total_supply_bp = t_30_transactions.sum().sum()

# intermediate_consumption = t_43_transactions.sum().sum()

# gross_va = total_supply_bp - intermediate_consumption
# tls_op = t_30_wo_totals.iloc[:, t_30_wo_totals.columns.get_level_values(0)=='Taxes less subsidies on products'].sum().sum()
# # tls_op calculation is FAULTY, taxes less subsidies should be 88095, instead of 154731
# # not because a totals row is included
# # t30_table_30_mi STILL CONTAINS THE INTERMEDIATE TOTALS ROWS (AND COLS?)
# gdp_production = gross_va + tls_op
# SU_GDP_approaches_results["production"] = gdp_production

#%% GDP by income approach - Leave to last
# GDP = Gross VA at BP (other table) + taxes less subsidies on products (ST)
# Gross VA at BP = compensation of employees + other net taxes on production + consumption of fixed capital + net operating surplus
# use table 41

# A LOT OF VALUES ARE OFF. 
# IN THE CSV, EVERY TRANSACTION EXISTS TWICE. ONCE WITH MEASURE 'C', AND ONCE WITH 'VP'
# LOOKS LIKE IT SCHOULD BE THE MEASURE 'C'
# THE COLUMNS 'MEASURE' WITH VALUE 'C' ARE CURRENT PRICES (COLUMN: 'Measure')
# THE COLUMNS 'MEASURE' with value 'VP 'ARE CONSTANT PRICES, PREVIOUS YEAR PRICES (COLUMN: 'Measure')
# DROP THESE FROM THE CSV BEFORE CONSTRUCTING THE DF

gross_va_bp = [
    t_41.loc['Compensation of employees',:],
    # all compensation instead of only wages and salaries.
    # makes gdp by income and production the same.
    t_41.loc['Other taxes less other subsidies on production',:],
    t_41.loc['Consumption of fixed capital',:],
    # not sure if the below one is really only the 'net operating surplus'
    t_41.loc['Operating surplus and mixed income, net',:]
    ]

gross_va_bp = pd.concat(gross_va_bp, axis=0)
gross_va_bp_sum = gross_va_bp.sum().sum()
# correct value: 724960
# here: 774635.0

# gdp calc and input into dict after the production approach 
# because they both use taxes less subsidies on products: tls_op

gdp_income = gross_va_bp_sum + tls_op
SU_GDP_approaches_results["income"] = gdp_income

#%% GDP by expenditure approach
# GDP = FCE (UT) + GCF (UT) + exports of goods and services (UT) - imports of goods and services (ST)
# FCE = Household fce + NIPSH fce + govt ce
# GFC = GFCF + acquisistions less disposals of valuables + changes in inventories
# + acquisistions less disposals of valuables + changes in inventories + exports of goods and services (UT)

necessary_columns_pos = pd.concat([
    t_43.loc[:,'Final consumption expenditure by households, domestic concept'],
    t_43.loc[:,'Final consumption expenditure by NIPSH'],
    t_43.loc[:,'Final consumption expenditure by government'],
    t_43.loc[:,'Gross fixed capital formation'],
    t_43.loc[:,'Acquisitions less disposals of valuables'],
    t_43.loc[:,'Changes in inventories'],
    t_43.loc[:,'Exports']
    ], axis=1)

gdp_expenditure_use_sum = necessary_columns_pos.sum().sum()
# correct value: 1389061.0
# here: 1323612.0 --> most column sums are off. Especially for the bigger values like GFCF, this adds up

necessary_columns_neg = pd.concat([
    t_30.loc[:,'Imports, cif']
    ], axis=1)
# correct values: 578273
# here: 578273.0

ciffob_adj = t_30_csv.loc[5228, 'Value']
# correct value: -2267
# here: -2267

# imports minus adjustments
gdp_expenditure_supply_sum = necessary_columns_neg.sum().sum() - np.abs(ciffob_adj)
# correct value: 576006
# here: 576006.0

gdp_expenditure = gdp_expenditure_use_sum - gdp_expenditure_supply_sum  

SU_GDP_approaches_results["expenditure"] = gdp_expenditure

print(SU_GDP_approaches_results)
print("The correct values are: \n {'income': 813055, 'expenditure': 813055.0, 'production': 813055}")
#%% MI via excel (not preferred, needs excel file in addition to CSV)

# t_30_xlsx = pd.read_excel('OECD_Data_downloads\Table_30.xlsx', engine="openpyxl", skipfooter=3)

# row_names = np.array(t_30_xlsx.iloc[11:,0:3])
# col_names = np.array(t_30_xlsx.iloc[5:10,5:])

# r0 = row_names[:,0]
# r1 = row_names[:,1]
# r2 = row_names[:,2]
# index = [r0, r1, r2]

# # build col index of Table 30
# c0 = col_names[0,:]
# c1 = col_names[1,:]
# c2 = col_names[2,:]
# c3 = col_names[3,:]
# c4 = col_names[4,:]
# columns = [c0,c1,c2,c3,c4]

# index_clean = []
# i = 0
# for array in index:
#     index_clean.append([])    # works but a np array is necessary for a multiindex.from_arrays
#     # t30_index.append(np.array()) # does not work
#     # print(array[0])
#     for value in array:
#         if type(value) == float:
#             # print(value)
#             index_clean[i].append(value)
#         elif type(value) == str:
#             # print(value.strip())
#             index_clean[i].append(value.strip())
#         else:
#             print('Error: value type: ', type(value))
            
#     # t30_index[i] = np.array(t30_index[i])
#     index_clean[i] = np.array(index_clean[i], dtype=object)   # works, but nan floats are converted to numpy_str_ type
#     i += 1
    
# # index_clean_mi = pd.MultiIndex.from_arrays(index_clean, names=('Products', 'Sub-Products')) 
# index_clean_mi = pd.MultiIndex.from_arrays(index_clean)
                                           
# columns_clean = []
# i = 0
# for array in columns:
#     columns_clean.append([])    # works but a np array is necessary for a multiindex.from_arrays
#     # t30_index.append(np.array()) # does not work
#     # print(array[0])
#     for value in array:
#         if type(value) == float:
#             # print(value)
#             columns_clean[i].append(value)
#         elif type(value) == str:
#             # print(value.strip())
#             columns_clean[i].append(value.strip())
#         else:
#             print('Error: value type: ', type(value))
            
#     # t30_index[i] = np.array(t30_index[i])
#     columns_clean[i] = np.array(columns_clean[i], dtype=object)   # works, but nan floats are converted to numpy_str_ type
#     i += 1

# columns_clean_mi = pd.MultiIndex.from_arrays(columns_clean)

# # create placeholder df and combine with MI:

# row_size = index_clean_mi.shape[0]
# col_size = columns_clean_mi.shape[0]
# t_30 = pd.DataFrame(np.full((row_size,col_size),np.nan), index=index_clean_mi, columns=columns_clean_mi)


#%% testing
# t_30.iloc[0][0] = 111

# the products that are spelled marginally different between the tables: 
    
# print('t30 \n')

# for name in t_30_index_check:
#     if name not in t_43_index_check:
#         print(name, '\n')
        
# print('t43 \n')

# for name in t_43_index_check:
#     if name not in t_30_index_check:
#         print(name, '\n')