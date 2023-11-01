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
    
    # drop 'of-which' rows
        # is this necessary for now?
        # yes, otherwise the wrong column gets dropped in the logic of dropping an intermediate column
        # if need, reattach by concatenation.
    if OECD_table_nr == 43:
        
        # then drop column with '..'; of which: Domestic purchases by non-residents
        # it contains a portion of the column to the left, so not necessary.
        
        iloc_owdpbnr = np.where(transactions.columns.get_loc_level('of which: Domestic purchases by non-residents', level=2)[0] == True)[0][0]
        transactions.drop(transactions.columns[iloc_owdpbnr], axis=1, inplace=True)
        # drops the column, but intermediate totals of the upper levels are not dropped
        
        # dropping the re-export column
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

#%% Check for negative values
# dataframe should not have entries with strings instead of floats (floats include NaNs)

def neg_check(dataframe, OECD_table_nr):
    # varname = 'neg_dict' + str(OECD_table_nr)     # not necessary if assigning outcome of function to variable

    neg_df = dataframe[dataframe < 0].notna()      # returns True when values are neg, and False otherwise (instead of nan otherwise)

    neg_df_np = np.array(neg_df)

    true_ilocs = np.where(neg_df_np == True)

    if len(true_ilocs[0]) > 0:
        neg_dict = {}
        for i in np.arange(len(true_ilocs[0])):
            # print(i)
            child_dict = 'neg_' + str(i)
            neg_dict.update({
                child_dict: {
                'negative value' : dataframe.iloc[true_ilocs[0][i],true_ilocs[1][i]],
                'source table': 'table_'+ str(OECD_table_nr),
                'row iloc': true_ilocs[0][i],
                'col iloc': true_ilocs[1][i],
                'index location': dataframe.index[true_ilocs[0][i]],
                'columns location': dataframe.columns[true_ilocs[1][i]]
                }
                })
        print('Negative values were found in table: ', OECD_table_nr)
        print('See dictionary "neg_dict" corresponding to this table for details on locations. \n')
        
    else: 
        print('No negatives were found in the considered table: ', OECD_table_nr)
        print('The returned variable by this function is of type "None". \n')
        # return
    
    return neg_dict if 'neg_dict' in locals() else None


#%% GDP calculations with CSV file input (as opposed to xls(x) files)

# import & prep
def csv_input(path_var, table_nr):
    t_csv = pd.read_csv(path_var, header=0)
    if table_nr == 30:
        for row in t_csv.index:  # not specifying .index results in iteration over every field instead of the row nr.
            t_csv.loc[row, 'Transaction'] = t_csv.loc[row, 'Transaction'].strip()
            t_csv.loc[row, 'Product'] = t_csv.loc[row, 'Product'].strip()
            
        transactions = t_csv.loc[:,'Transaction'].unique()
        products = t_csv.loc[:,'Product'].unique()

        t_df = pd.DataFrame(np.full((len(products),len(transactions)), np.nan), index=products, columns=transactions)
        t_df.sort_index(inplace=True)
        t_df.sort_index(axis=1, inplace=True)

        for row in t_csv.index:
            # print(row) # --> gives index as integer now
            t_df.loc[t_csv.loc[row,'Product'], t_csv.loc[row,'Transaction']] = t_csv.loc[row,'Value']
            
    elif table_nr == 43:
        for row in t_csv.index:  # not specifying .index results in iteration over every field instead of the row nr.
            t_csv.loc[row, 'Transaction'] = t_csv.loc[row, 'Transaction'].strip()
            t_csv.loc[row, 'Product'] = t_csv.loc[row, 'Product'].strip(', bp')
            t_csv.loc[row, 'Product'] = t_csv.loc[row, 'Product'].strip()
            
        transactions = t_csv.loc[:,'Transaction'].unique()
        products = t_csv.loc[:,'Product'].unique()

        t_df = pd.DataFrame(np.full((len(products),len(transactions)), np.nan), index=products, columns=transactions)
        t_df.sort_index(inplace=True)
        t_df.sort_index(axis=1, inplace=True)

        for row in t_csv.index:
            t_df.loc[t_csv.loc[row,'Product'], t_csv.loc[row,'Transaction']] = t_csv.loc[row,'Value']

    elif table_nr == 41:
        for row in t_csv.index:  # not specifying .index results in iteration over every field instead of the row nr.
            t_csv.loc[row, 'Transaction'] = t_csv.loc[row, 'Transaction'].strip()
            t_csv.loc[row, 'Activity'] = t_csv.loc[row, 'Activity'].strip()
            
        transactions = t_csv.loc[:,'Transaction'].unique()
        activities = t_csv.loc[:,'Activity'].unique()

        t_df = pd.DataFrame(np.full((len(transactions),len(activities)), np.nan), index=transactions, columns=activities)
        t_df.sort_index(inplace=True)
        t_df.sort_index(axis=1, inplace=True)

        for row in t_csv.index:
            # only use the rows with current prices, not constant prices from last year.
            if t_csv.loc[row,'MEASURE'] == 'C':
                t_df.loc[t_csv.loc[row,'Transaction'], t_csv.loc[row,'Activity']] = t_csv.loc[row,'Value']
    
    else: 
        print('This table is not included in gdp calculations: ', table_nr)
    
    return t_df # dataframe


def gdp_csv(t_30, t_43, t_41, ignore_list_path, t_30_csv_path):  
    # the 3 created DFs
    # the path to the ignore list
    # the path to the csv file of t_30 (for ciffob adj value)
    
    ignore_ = open(ignore_list_path, "r")
    ignore = ignore_.read().split('\n')
    ignore_list = []
    for line in ignore:
        if line != '':
            ignore_list.append(line.strip())
    
    table_list = [
        t_30,
        t_43,
        t_41
        ]        
    
    for df in table_list:
        for entry in df.index: 
            if entry in ignore_list:
                df.drop(index = entry, inplace=True) 
        for entry in df.columns: 
            if entry in ignore_list:
                df.drop(columns = entry, inplace=True)
    
    SU_GDP_approaches_results = {"income": None, "expenditure": None, "production": None}
    
    # Production approach 
    t_30_drop_for_production = pd.concat([
        t_30.loc[:,'Imports, cif'],
        t_30.loc[:,'Taxes less subsidies on products'],
        t_30.loc[:,'Trade and transport margins']
        ], axis=1)

    # actually output at bp, not supply.
    total_supply_bp = t_30.sum().sum() - t_30_drop_for_production.sum().sum()

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

    gross_va = total_supply_bp - intermediate_consumption

    tls_op = t_30.loc[:,'Taxes less subsidies on products'].sum()

    gdp_production = gross_va + tls_op
    
    SU_GDP_approaches_results["production"] = gdp_production
    
    # income approach
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

    gdp_income = gross_va_bp_sum + tls_op
    
    SU_GDP_approaches_results["income"] = gdp_income
    
    # expenditure approach
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

    necessary_columns_neg = pd.concat([
        t_30.loc[:,'Imports, cif']
        ], axis=1)

    # either include t_30 csv in the function input, or just hardcode the ciffob correction here
    # hardcoding seems error prone.
    t_30_csv = pd.read_csv(t_30_csv_path, header=0)
    ciffob_adj = t_30_csv.loc[5228, 'Value']    # t_30 row 5228 = ciffob correction (= -2267 for NL 2019)

    # imports minus adjustments
    gdp_expenditure_supply_sum = necessary_columns_neg.sum().sum() - np.abs(ciffob_adj)

    gdp_expenditure = gdp_expenditure_use_sum - gdp_expenditure_supply_sum  

    SU_GDP_approaches_results["expenditure"] = gdp_expenditure
    
    return SU_GDP_approaches_results # GDP_vals


