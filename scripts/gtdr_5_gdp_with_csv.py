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

#%% Construction of table --> less detail, so onlyh global calcs? 

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

# select & drop int. totals manually? 
#%% MI via excel (not preferred, needs excel file in addition to CSV)
t_30_xlsx = pd.read_excel('OECD_Data_downloads\Table_30.xlsx', engine="openpyxl", skipfooter=3)

row_names = np.array(t_30_xlsx.iloc[11:,0:3])
col_names = np.array(t_30_xlsx.iloc[5:10,5:])

r0 = row_names[:,0]
r1 = row_names[:,1]
r2 = row_names[:,2]
index = [r0, r1, r2]

# build col index of Table 30
c0 = col_names[0,:]
c1 = col_names[1,:]
c2 = col_names[2,:]
c3 = col_names[3,:]
c4 = col_names[4,:]
columns = [c0,c1,c2,c3,c4]

index_clean = []
i = 0
for array in index:
    index_clean.append([])    # works but a np array is necessary for a multiindex.from_arrays
    # t30_index.append(np.array()) # does not work
    # print(array[0])
    for value in array:
        if type(value) == float:
            # print(value)
            index_clean[i].append(value)
        elif type(value) == str:
            # print(value.strip())
            index_clean[i].append(value.strip())
        else:
            print('Error: value type: ', type(value))
            
    # t30_index[i] = np.array(t30_index[i])
    index_clean[i] = np.array(index_clean[i], dtype=object)   # works, but nan floats are converted to numpy_str_ type
    i += 1
    
# index_clean_mi = pd.MultiIndex.from_arrays(index_clean, names=('Products', 'Sub-Products')) 
index_clean_mi = pd.MultiIndex.from_arrays(index_clean)
                                           
columns_clean = []
i = 0
for array in columns:
    columns_clean.append([])    # works but a np array is necessary for a multiindex.from_arrays
    # t30_index.append(np.array()) # does not work
    # print(array[0])
    for value in array:
        if type(value) == float:
            # print(value)
            columns_clean[i].append(value)
        elif type(value) == str:
            # print(value.strip())
            columns_clean[i].append(value.strip())
        else:
            print('Error: value type: ', type(value))
            
    # t30_index[i] = np.array(t30_index[i])
    columns_clean[i] = np.array(columns_clean[i], dtype=object)   # works, but nan floats are converted to numpy_str_ type
    i += 1

columns_clean_mi = pd.MultiIndex.from_arrays(columns_clean)

# create placeholder df and combine with MI:

row_size = index_clean_mi.shape[0]
col_size = columns_clean_mi.shape[0]
t_30 = pd.DataFrame(np.full((row_size,col_size),np.nan), index=index_clean_mi, columns=columns_clean_mi)

t_30.iloc[0][0] = 111
