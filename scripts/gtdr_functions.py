# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 12:16:15 2023

@author: Horsting

GTDR Functions
"""
#%% Import packages

import pandas as pd
import numpy as np
import sys

#%% Importing and slicing

def excel_df(filename, OECD_table_nr, footer):
    
    table_list = [30,43,41]
    if OECD_table_nr in table_list:
        pass
    else:
        raise ValueError("This function has not been tested with the specified table")

  

    excel_ = pd.read_excel(filename, engine="openpyxl", skipfooter=footer)  # footer = 3 for transaction tables
    
    # Table 30
    if OECD_table_nr == 30:
        excel_clean = pd.DataFrame(excel_.iloc[12:,7:])
        row_names = np.array(excel_.iloc[12:,1:3])
        col_names = np.array(excel_.iloc[6:10,7:])
        
        r0 = row_names[:,0]
        r1 = row_names[:,1]
        index = [r0, r1]
        
        # build col index of Table 30
        c0 = col_names[0,:]
        c1 = col_names[1,:]
        c2 = col_names[2,:]
        c3 = col_names[3,:]
        columns = [c0,c1,c2,c3]
    
    # Table 43
    if OECD_table_nr == 43:
        excel_clean = pd.DataFrame(excel_.iloc[12:,6:])   
        #check if table 43 is sliced correctly
        row_names = np.array(excel_.iloc[12:,1:3])
        col_names = np.array(excel_.iloc[7:10,6:])  # might be better to make 43 and 30 the same size index
    
    # add a loop that adds variables as much as there are names/levels specified.
    # or use partially hard-coded for now
        r0 = row_names[:,0]
        r1 = row_names[:,1]
        index = [r0, r1]
    
        c0 = col_names[0,:]
        c1 = col_names[1,:]
        c2 = col_names[2,:]
    
        columns = [c0, c1, c2]
        
    if OECD_table_nr == 41:
        excel_clean = pd.DataFrame(excel_.iloc[10:,6:])
        row_names = np.array(excel_.iloc[10:,1:4])
        col_names = np.array(excel_.iloc[6:8,6:])
        
        r0 = row_names[:,0]
        r1 = row_names[:,1]
        r2 = row_names[:,2]
        index = [r0, r1, r2]
        
        c0 = col_names[0,:]
        c1 = col_names[1,:]
    
        columns = [c0, c1]

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


    clean_mi = pd.DataFrame(np.array(excel_clean), index=index_clean_mi, columns=columns_clean_mi)
    return clean_mi


#%% Dropping intermediate totals
def drop_int_totals(dataframe, OECD_table_nr, collevel):    # collevel is the level at which 
                                                            # duplicate check needs to happen 
    table_list = [30,43,41]
    if OECD_table_nr in table_list:
        pass
    else:
        raise ValueError("This function has not been tested with the specified table")


    transactions = dataframe.copy()   # create deep copy
    
    # drop rows with '..' entries and estimates
    if OECD_table_nr == 30:
        iloc_dpabr = np.where(transactions.columns.get_loc_level('Direct purchases abroad by residents', level=1)[0] == True)[0][0]
        # gives error because using this function it appears on level 0 (so what is dropped?)
        # fault in excel_df function: should specify table, and slice columns accordingly
        transactions.drop(transactions.columns[iloc_dpabr], axis=1, inplace=True)
        
        iloc_ciffob = np.where(transactions.columns.get_loc_level('cif/fob adjustment on imports', level=1)[0] == True)[0][0]
        transactions.drop(transactions.columns[iloc_ciffob], axis=1, inplace=True)
    
    if OECD_table_nr == 43:
        
        # turn off as test: 
        # t43_transactions = t43_transactions.iloc[:,0:78]    # until Final demand begins
    
        # then drop column with '..'; of which: Domestic purchases by non-residents
        # it contains a portion of the column to the left, so not necessary.
        
        iloc_owdpbnr = np.where(transactions.columns.get_loc_level('of which: Domestic purchases by non-residents', level=2)[0] == True)[0][0]
        transactions.drop(transactions.columns[iloc_owdpbnr], axis=1, inplace=True)
        # drops the column, but intermediate totals of the upper levels are not dropped
        
        # droping the re-export column
        # it contains a portion of the column to the left, so not necessary.
        iloc_eowre = np.where(transactions.columns.get_loc_level('of which: Re-export', level=1)[0] == True)[0][0]
        transactions.drop(transactions.columns[iloc_eowre], axis=1, inplace=True)
    


    # drop all rows where: intermediate totals are shown
    for tuple_entry in transactions.index:    
        for value in tuple_entry: 
            if type(value) == float:    # cannot compare a string to nan; check float first
                if np.isnan(value):      # necessary method to check for NaN (or math.isnan)
                    # print("nan is found at if statement")
                    pass
            else: 
            # print(value)
            
                try:
                    loc_series = transactions.index.get_loc_level(value, level=0)     # specified level 0
                except KeyError:
                    # print('Only exists in level 1: ', value)
                    pass
                else:
                    loc_series = transactions.index.get_loc_level(value, level=0)     # returns tuple
               
                true_ilocs = np.where(loc_series[0] == True)  # select all True value from the array at place 0
                if len(true_ilocs[0]) > 1:     # check if there's more than 1 entry of this sort
                                                # the first row is then an intermediate totals row
                    # print('Occurs more than once on level 0: ', value)
                    iloc = true_ilocs[0][0]     # select the first True value
                    transactions.drop(transactions.index[iloc], inplace=True) 
            
    for tuple_entry in transactions.columns:    
        for value in tuple_entry:
            if type(value) == float:
                if np.isnan(value):
                    pass
            else:
                
                
                # print(value)
                try:
                    # 1 less level in columns compared to table 30
                    # check for level 1 in the columns (index was level 0)
                    loc_series = transactions.columns.get_loc_level(value, level=collevel)
                except KeyError:
                    pass
                else:
                    loc_series = transactions.columns.get_loc_level(value, level=collevel)
                    #no indent after theis else? --> this is the fix to let the second try-except-else work with the same variable names
                    true_ilocs = np.where(loc_series[0] == True)
                    if len(true_ilocs[0]) > 1:
                        # print('duplicate found!', true_ilocs[0])
                        iloc = true_ilocs[0][0]
                        transactions.drop(transactions.columns[iloc], axis = 1, inplace=True)   # need to specify axis here
                    
                # the below is a test to drop intermediate total columns based on level 1 (non-transactions)
                # it drops ALL columns. Syntax does not seem different from the one above. only difference is the level indication.
                try:
                    loc_series = transactions.columns.get_loc_level(value, level=0)
                except KeyError:
                    pass
                else:
                    # print(value)    # prints every name in level 1
                    loc_series = transactions.columns.get_loc_level(value, level=0)
                    #indented below as test: was running also when the conditions above for level 1 were running.
                    true_ilocs = np.where(loc_series[0] == True)
                    if len(true_ilocs[0]) > 1:
                        # print('duplicate found!', true_ilocs[0])
                        iloc = true_ilocs[0][0]
                        #test
                        # print(iloc)
                        transactions.drop(transactions.columns[iloc], axis = 1, inplace=True)   # need to specify axis here
        
    return transactions

#%% VA without of-which rows
def VA_of_which_strip(transactions, OECD_table_nr):
    if OECD_table_nr == 41:
        transactions = transactions.iloc[1:,:]
        transactions.index = transactions.index.droplevel(0)
        
        gross_va_bp = [
            transactions.iloc[transactions.index.get_level_values(0)=='Compensation of employees',:].iloc[0,:].to_frame().T,
            # all compensation instead of only wages and salaries.
            # makes gdp by income and production the same.
            transactions.iloc[transactions.index.get_level_values(0)=='Other taxes less other subsidies on production',:],
            transactions.iloc[transactions.index.get_level_values(1)=='Consumption of fixed capital',:],
            # not sure if the below one is really only the 'net operating surplus'
            transactions.iloc[transactions.index.get_level_values(1)=='Operating surplus and mixed income, net',:]
            ]

        gross_va_bp = pd.concat(gross_va_bp, axis=0)
        
        transactions = gross_va_bp
    else:
        print("This function is exclusively for use with table 41: Value Added")
    return transactions

