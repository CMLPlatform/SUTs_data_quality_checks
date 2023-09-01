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
To do: Remove hardcoding as much as possible






"""
#%% Import packages

import pandas as pd
import numpy as np

#%% Data import/read + checks


table_30_excel_ = pd.read_excel('OECD_Data_downloads\Table_30.xlsx', engine="openpyxl", skipfooter=3)

"""
Can I build a new dataframe with a MultiIndex comprising the slices of columns and rows already here.
And then iterate over the index and column names, eg: if index ['1'] = nan, check index['0'].
Where 0 and 1 are the names or indices of the index columns, not rows and columns as used in axis=...
"""

# get labels for multi index
col_names = table_30_excel_.iloc[6:10,7:]   # changed col from 6 to 7
col_names_np = np.array(table_30_excel_.iloc[6:10,7:])  # changed col from 6 to 7
row_names = table_30_excel_.iloc[12:,1:3]
row_names_np = np.array(table_30_excel_.iloc[12:,1:3])

col_lists = col_names.values.tolist()
for column_list in col_lists:
    # print(type(column_list))
    for entry in column_list:
        if type(entry) == str:
            # print(entry)
            entry = entry.strip()
            # print(entry)


# slice the appropriate data
# example: df = pd.DataFrame(np.random.randn(3, 8), index=["A", "B", "C"], columns=index)

table_30_excel_clean = pd.DataFrame(table_30_excel_.iloc[12:,7:])   # changed col from 6 to 7 onwards
# print('Columns: ', col_names.shape, 'Rows: ', row_names.shape, 'Data: ', table_30_excel_clean.shape)
# table_30_excel_clean_mi = pd.DataFrame(table_30_excel_.iloc[12:,6:], index=row_names_np, columns=col_names_np)
# # does not work because levels have to be created (at least in the case of np.arrays; so an array of arrays)
# # creating a multiindex needs list of arrays or tuples.
# # alternatively: df as multiindex source not possible? check docs: pandas.MultiIndex.from_frame()
# # multiindex.from_frame not useful, as the index and columns should be constructed first, and it 
# # uses and empty data table (only the index rows and columns are created)
# # create multiindex first, assign to clean df later.


# multi_index_T = pd.MultiIndex(row_names_np, col_names_np.T) # transpose gives same error as this line above
# multi_index_T = pd.MultiIndex(row_names_np, names=('Industry', 'Sub-Industry'))
# does not work; one row of the multi index needs to have the format ([0,0,0],[1,1,1])
# row_names_np has (0,1,2), [0A, 1A, 2A]
# multi_index_tuples = pd.MultiIndex.from_tuples(row_names) # also does not work because takes tuples (0,1) for every row

# to do: write loops to create the seperate arrays: strip names first.
# one for each column of the index, one for each row(?) of the column index
# use these arrays with pd.MultiIndex.from_arrays()

# a slice of an array in a variable = an array

'''
The underneath code works, but turns the string into a np array.
Probably, the stripping needs to happen directly when obtaining the columns from the original dataframe/file.
 Then turn into a np array for index

col_index[0][0] = np.char.strip(col_index[0][0])

col_index[0][0]
Out[129]: array('Total supply at basic prices', dtype='<U30')

print(col_index[0][0])
Total supply at basic prices
-------------------------------------
In dataframe col_names:
    col_names.iloc[0][0]
    Out[137]: '  Total supply at basic prices'
    col_names.iloc[0][0].strip()
    Out[139]: 'Total supply at basic prices'
    
    
Park the white spaces for later. maybe doable by creating a new list and appending in a for loop.
'''
# build row index of Table 30
t30_r0 = row_names_np[:,:1]
# pd.MultiIndex_from_arrays() only accepts flat arrays, not 1 dimensional (i.e. (78,), not (78,1))
t30_r0.resize(78)
t30_r1 = row_names_np[:,1]
# a2.resize(78,1)
t30_index = [t30_r0,t30_r1]

# build col index of Table 30
t30_c0 = col_names_np[0,:]
t30_c1 = col_names_np[1,:]
t30_c2 = col_names_np[2,:]
t30_c3 = col_names_np[3,:]
t30_col_index = [t30_c0,t30_c1,t30_c2,t30_c3]

t30_index_clean = []
i = 0
for array in t30_index:
    t30_index_clean.append([])    # works but a np array is necessary for a multiindex.from_arrays
    # t30_index_clean.append(np.array()) # does not work
    # print(array[0])
    for value in array:
        if type(value) == float:
            # print(value)
            t30_index_clean[i].append(value)
        elif type(value) == str:
            # print(value.strip())
            t30_index_clean[i].append(value.strip())
        else:
            print('Error: value type: ', type(value))
            
    # t30_index_clean[i] = np.array(t30_index_clean[i])
    t30_index_clean[i] = np.array(t30_index_clean[i], dtype=object)   # works, but nan floats are converted to numpy_str_ type
    i += 1
    


t30_mi_index = pd.MultiIndex.from_arrays(t30_index_clean, names=('Products', 'Sub-Products')) 
# works, needs to be type multiindex of size (78,), later is converted
# t30_mi_index = pd.MultiIndex.from_tuples(np.array(t30_index).T)

t30_col_index_clean = []
i = 0
for array in t30_col_index:
    t30_col_index_clean.append([])    # works but a np array is necessary for a multiindex.from_arrays
    # t30_index.append(np.array()) # does not work
    # print(array[0])
    for value in array:
        if type(value) == float:
            # print(value)
            t30_col_index_clean[i].append(value)
        elif type(value) == str:
            # print(value.strip())
            t30_col_index_clean[i].append(value.strip())
        else:
            print(type('Error: value type: ', value))
            
    t30_col_index_clean[i] = np.array(t30_col_index_clean[i], dtype=object)   # works: dtype needs to be specified here
    i += 1

t30_mi_columns = pd.MultiIndex.from_arrays(t30_col_index_clean)

t30_table_30_mi = pd.DataFrame(np.array(table_30_excel_clean), index=t30_mi_index, columns=t30_mi_columns)


## Table 43
table_43_excel_ = pd.read_excel('OECD_Data_downloads\Table_43.xlsx', engine="openpyxl", skipfooter=3)
table_43_excel_clean = pd.DataFrame(table_43_excel_.iloc[12:,6:])   
#check if table 43 is sliced correctly
row_names_43 = np.array(table_43_excel_.iloc[12:,1:3])
col_names_43 = np.array(table_43_excel_.iloc[7:10,6:])  # might be better to make 43 and 30 the same size index

t43_r0 = row_names_43[:,0]
t43_r1 = row_names_43[:,1]
t43_index = [t43_r0, t43_r1]

t43_c0 = col_names_43 [0,:]
t43_c1 = col_names_43 [1,:]
t43_c2 = col_names_43 [2,:]

t43_columns = [t43_c0, t43_c1, t43_c2]

t43_index_clean = []
i = 0
for array in t43_index:
    t43_index_clean.append([])    # works but a np array is necessary for a multiindex.from_arrays
    # t30_index.append(np.array()) # does not work
    # print(array[0])
    for value in array:
        if type(value) == float:
            # print(value)
            t43_index_clean[i].append(value)
        elif type(value) == str:
            # print(value.strip())
            t43_index_clean[i].append(value.strip())
        else:
            print('Error: value type: ', type(value))
            
    # t30_index[i] = np.array(t30_index[i])
    t43_index_clean[i] = np.array(t43_index_clean[i], dtype=object)   # works, but nan floats are converted to numpy_str_ type
    i += 1
    



t43_index_clean_mi = pd.MultiIndex.from_arrays(t43_index_clean, names=('Products', 'Sub-Products')) 

t43_columns_clean = []
i = 0
for array in t43_columns:
    t43_columns_clean.append([])    # works but a np array is necessary for a multiindex.from_arrays
    # t30_index.append(np.array()) # does not work
    # print(array[0])
    for value in array:
        if type(value) == float:
            # print(value)
            t43_columns_clean[i].append(value)
        elif type(value) == str:
            # print(value.strip())
            t43_columns_clean[i].append(value.strip())
        else:
            print('Error: value type: ', type(value))
            
    # t30_index[i] = np.array(t30_index[i])
    t43_columns_clean[i] = np.array(t43_columns_clean[i], dtype=object)   # works, but nan floats are converted to numpy_str_ type
    i += 1

t43_columns_clean_mi = pd.MultiIndex.from_arrays(t43_columns_clean)


t43_clean_mi = pd.DataFrame(np.array(table_43_excel_clean), index=t43_index_clean_mi, columns=t43_columns_clean_mi)


#%% Check if table at base prices are balanced (inputs = outputs)

# remove intermediate totals --> Temporarily mask or drop (so either just for this calc, or new df)


# table 30
t30_transactions = t30_table_30_mi.copy()   # create deep copy
t30_transactions = t30_transactions.iloc[:,0:78]    # drop the columns at the end that do not contain activities

# test for future use of multiindex in for loops: 
# list of values within level 0 of the index
t30_index_l0 = t30_transactions.index.get_level_values(0)
# t30_index = t30_transactions.index.get_level_values(0,1)    # does not work: only takes 1 level
# how to handle the duplicate values? with an extra counter or with a more elegant solution?

# slice only the transactions and their intermediate totals first (so drop e.g. columns from 'Imports, cif')

# return np series of True/False of a matched key in a index' level
# this works but on a whole multiindes, not on a specified level
# t30_np_key_locs = t30_mi_index.get_loc('Products of agriculture, forestry and fishing')
# t30_itemindex = np.where(t30_np_key_locs == True)   # returns list where the keys are found 
# (= list of indices with True)
# count Trues --> if 1 True keep, if >1 drop the row associated with the first one
# loc_series_test = t30_mi_index.get_loc_level('Products of agriculture, forestry and fishing')
# try: mi.get_loc_level('e', level='B')
# t30_np_key_locs_test = t30_mi_index.get_loc_level('Products of agriculture, hunting and related services', level=1)
# t30_np_key_locs_test = t30_mi_index.get_loc_level('Products of agriculture, hunting and related services', level=0)


# drop all rows where: intermediate totals are shown
for tuple_entry in t30_transactions.index:    # t30_mi_index is a multiindex, so it is a 
                                    # list of tuples with as many entries as there are levels
    for value in tuple_entry: 

        # if value == np.NaN:   # apparently this will always render false.
        if type(value) == float:    # cannot compare a string to nan; check float first
            if np.isnan(value):      # necessary method to check for NaN (or math.isnan)
                # print("nan is found at if statement")
                pass
        else: 
        # print(value)
        # loc_series = t30_mi_index.get_loc(value)  # get an array of booleans per index (by place in array) of specified key (value) 
            try:
                loc_series = t30_transactions.index.get_loc_level(value, level=0)     # specified level 0
            except KeyError:
                # print('Only exists in level 1: ', value)
                pass
            else:
                loc_series = t30_transactions.index.get_loc_level(value, level=0)     # returns tuple
            # print('previous done')
            # key error happens because it tries to find a key that does not exist in level 0
            # maybe use .get_loc_level instead
            true_ilocs = np.where(loc_series[0] == True)  # select all True value from the array at place 0
            if len(true_ilocs[0]) > 1:     # check if there's more than 1 entry of this sort
                                            # the first row is then an intermediate totals row
                # print('Occurs more than once on level 0: ', value)
                iloc = true_ilocs[0][0]     # select the first True value
                # t30_transactions.drop([iloc])    # drops row with nr 'iloc'; [] is necessary, otherwise uses label
                # dropping does not yet work
                t30_transactions.drop(t30_transactions.index[iloc], inplace=True)   # dropping by mi TUPLE of row 
                                                                                    # --> really a tuple?  actually just row number  
                # only works one time if it refers to a not-mutating object.
                # so entire loop has to be written while referring to self.mi
                # instead of the mi that was used initially.

# drop all columns where: intermediate totals are shown: same but for columns instead of index

# t30_cols_l_2= t30_transactions.columns.get_level_values(level=2)
# t30_cols = t30_transactions.columns
# t30_cols_l_2_3 = t30_cols.droplevel([0,1])

for tuple_entry in t30_transactions.columns:    # should just be working on levels 2 and 3 of the columns mi
                                                # but later apply to whole multiiindex tuple for dropping
                                                # better to apply this to the df.mi directly so it can manipulate in place
    for value in tuple_entry:
        if type(value) == float:
            if np.isnan(value):
                pass
        else:
            # print(value)
            try:
                # check for level 2 in the columns (index was level 0)
                loc_series = t30_transactions.columns.get_loc_level(value, level=2)
            except KeyError:
                pass
            else:
                loc_series = t30_transactions.columns.get_loc_level(value, level=2)
            true_ilocs = np.where(loc_series[0] == True)
            if len(true_ilocs[0]) > 1:
                # print('duplicate found!', true_ilocs[0])
                iloc = true_ilocs[0][0]
                t30_transactions.drop(t30_transactions.columns[iloc], axis = 1, inplace=True)   # need to specify axis here
        

# sum remaining in dataframe
t30_total_inputs = t30_transactions.sum()
# t30_total_inputs_1 = t30_transactions.cumsum()  # does not work!
# to do: replace '..' earlier
# t30_total_inputs.drop(t30_total_inputs.index[66], inplace=True) # contains the .., to do: drop earlier
t30_total_inputs_result = t30_total_inputs.sum()
total_supply_bp = t30_total_inputs_result   # rewrite as function
# Hard coded, revise: 
t30_total_inputs_difference = t30_total_inputs_result - 1569815 # = output at basic prices total in excel
# was because of wrongly sliced t30_transactions in columns direction: 
    # based on itself after in place testing instead of original
print('T30: There is a difference in calculated total activity at basic prices, of: ', t30_total_inputs_difference)


# table 43
t43_transactions = t43_clean_mi.copy()   # create deep copy
t43_transactions = t43_transactions.iloc[:,0:78]    # until Final demand begins

# drop all rows where: intermediate totals are shown
for tuple_entry in t43_transactions.index:    
    for value in tuple_entry: 
        if type(value) == float:    # cannot compare a string to nan; check float first
            if np.isnan(value):      # necessary method to check for NaN (or math.isnan)
                # print("nan is found at if statement")
                pass
        else: 
        # print(value)
        
            try:
                loc_series = t43_transactions.index.get_loc_level(value, level=0)     # specified level 0
            except KeyError:
                # print('Only exists in level 1: ', value)
                pass
            else:
                loc_series = t43_transactions.index.get_loc_level(value, level=0)     # returns tuple
           
            true_ilocs = np.where(loc_series[0] == True)  # select all True value from the array at place 0
            if len(true_ilocs[0]) > 1:     # check if there's more than 1 entry of this sort
                                            # the first row is then an intermediate totals row
                # print('Occurs more than once on level 0: ', value)
                iloc = true_ilocs[0][0]     # select the first True value
                t43_transactions.drop(t43_transactions.index[iloc], inplace=True) 
        
for tuple_entry in t43_transactions.columns:    
    for value in tuple_entry:
        if type(value) == float:
            if np.isnan(value):
                pass
        else:
            # print(value)
            try:
                # 1 less level in columns compared to table 30
                # check for level 1 in the columns (index was level 0)
                loc_series = t43_transactions.columns.get_loc_level(value, level=1)
            except KeyError:
                pass
            else:
                loc_series = t43_transactions.columns.get_loc_level(value, level=1)
            true_ilocs = np.where(loc_series[0] == True)
            if len(true_ilocs[0]) > 1:
                # print('duplicate found!', true_ilocs[0])
                iloc = true_ilocs[0][0]
                t43_transactions.drop(t43_transactions.columns[iloc], axis = 1, inplace=True)   # need to specify axis here
                
# sum remaining in dataframe
t43_total_inputs = t43_transactions.sum()

t43_total_inputs_result = t43_total_inputs.sum()
intermediate_consumption = t43_total_inputs_result # rewrite as function
t43_total_intermediate_plus_FD_GCf = t43_total_inputs_result + 554921 + 179656
t43_total_inputs_difference = t43_total_inputs_result - 844855  # = intermediate consuption at basic prices total in excel

print('T43: There is a difference in calculated total activity at basic prices, of: ', t43_total_inputs_difference)

# comparing outputs and inputs: 
print('The balance difference at basic prices between tables 30 and 43 is: ',
      t30_total_inputs_result - t43_total_inputs_result)
# actually these are two different things. Making sure it's balanced probably concerns
# comparing the sum of both the entire tables. But still without the (intermediate) totals rows/cols
# --> extra info: check eurostat manuals to see what to include to balance the two tables. 

# output and fabricated inputs difference:
   # recalculate
print('t30(total outputs) - t43(intermediate consumption, FD, GCf) = ', 
      t30_total_inputs_result - t43_total_intermediate_plus_FD_GCf)

#%% GDP by income approach - Leave to last
# GDP = Gross VA at BP (other table) + taxes less subsidies on products (ST)
# Gross VA at BP = compensation of employees + other net taxes on production + consumption of fixed capital + net operating surplus
# use table 41

# create dictionary for storing results of GDP calcs
SU_GDP_approaches_results = {"income": None, "expenditure": None, "production": None}

# load and compile workable table 41 (Value Added and its components --> wages etc.)
table_41_excel_ = pd.read_excel('OECD_Data_downloads\Table_41.xlsx', engine="openpyxl", skipfooter=1)
table_41_excel_clean = table_41_excel_.iloc[10:,6:]
row_names_41 = np.array(table_41_excel_.iloc[10:,1:4])
col_names_41 = np.array(table_41_excel_.iloc[6:8,6:])
t41_r0 = row_names_41[:,0]
t41_r1 = row_names_41[:,1]
t41_r2 = row_names_41[:,2]
t41_index = [t41_r0, t41_r1, t41_r2]
t41_c0 = col_names_41[0,:]
t41_c1 = col_names_41[1,:]
t41_columns = [t41_c0, t41_c1]

## below is a copied piece of code, and it works with only adjusting the names:
# potential to make this a function easily.
t41_index_clean = []
i = 0
for array in t41_index:
    t41_index_clean.append([])    # works but a np array is necessary for a multiindex.from_arrays
    for value in array:
        if type(value) == float:
            t41_index_clean[i].append(value)
        elif type(value) == str:
            t41_index_clean[i].append(value.strip())
        else:
            print('Error: value type: ', type(value))
    t41_index_clean[i] = np.array(t41_index_clean[i], dtype=object)   # works, but nan floats are converted to numpy_str_ type
    i += 1

t41_index_clean_mi = pd.MultiIndex.from_arrays(t41_index_clean) 

t41_columns_clean = []
i = 0
for array in t41_columns:
    t41_columns_clean.append([])    # works but a np array is necessary for a multiindex.from_arrays
    for value in array:
        if type(value) == float:
            t41_columns_clean[i].append(value)
        elif type(value) == str:
            t41_columns_clean[i].append(value.strip())
        else:
            print('Error: value type: ', type(value))

    t41_columns_clean[i] = np.array(t41_columns_clean[i], dtype=object)   # works, but nan floats are converted to numpy_str_ type
    i += 1
    # maybe select 'the last list in the created list of lists?
    # to eliminate need for counter i
    # as a new list is being appended at every loop iteration, the one for the current operation is always the last one
t41_columns_last = t41_columns_clean[-1]
t41_columns_clean_mi = pd.MultiIndex.from_arrays(t41_columns_clean)


t41_clean_mi = pd.DataFrame(np.array(table_41_excel_clean), index=t41_index_clean_mi, columns=t41_columns_clean_mi)

## now drop intermediate totals
#compare levels to previous tables 30 and 43
#check what's the best thing to do: slice more accurately for the next loop (create new df, like t##_transactions)
#or adjust logic on the rows (index) to compare both levels 0 and 1 and 1 and 2

t41_transactions = t41_clean_mi.copy()   # create deep copy
t41_transactions = t41_transactions.iloc[2:,:]
t41_transactions.index = t41_transactions.index.droplevel(0)

# only necesessary to drop columns. Will pick specific rows to compile gdp later
for tuple_entry in t41_transactions.columns:    
    for value in tuple_entry:
        if type(value) == float:
            if np.isnan(value):
                pass
        else:
            # print(value)
            try:
                
                loc_series = t41_transactions.columns.get_loc_level(value, level=0)
            except KeyError:
                pass
            else:
                loc_series = t41_transactions.columns.get_loc_level(value, level=0)
            true_ilocs = np.where(loc_series[0] == True)
            if len(true_ilocs[0]) > 1:
                # print('duplicate found!', true_ilocs[0])
                iloc = true_ilocs[0][0]
                t41_transactions.drop(t41_transactions.columns[iloc], axis = 1, inplace=True)

# Calculate gdp

gross_va_bp = [
    t41_transactions.iloc[t41_transactions.index.get_level_values(1)=='of which: Wages and salaries',:],
    t41_transactions.iloc[t41_transactions.index.get_level_values(0)=='Other taxes less other subsidies on production',:],
    t41_transactions.iloc[t41_transactions.index.get_level_values(1)=='Consumption of fixed capital',:],
    # not sure if the below one is really only the 'net operating surplus'
    t41_transactions.iloc[t41_transactions.index.get_level_values(1)=='Operating surplus and mixed income, net',:]
    ]

gross_va_bp = pd.concat(gross_va_bp, axis=0)
gross_va_bp_sum = gross_va_bp.sum().sum()
# gdp calc and input into dict after the production approach 
# because they both use taxes less subsidies on products: tls_op



#%% GDP by expenditure approach
# GDP = FCE (UT) + GCF (UT) + exports of goods and services (UT) - imports of goods and services (ST)
# FCE = Household fce + NIPSH fce + govt ce
# GFC = GFCF + acquisistions less disposals of valuables + changes in inventories
# + acquisistions less disposals of valuables + changes in inventories + exports of goods and services (UT)

# no need for dropping columns and loops, if just using the names based on the manual for GDP calc from SUTs
# however, a solution needs to be found for the 'of which: Domestic purchases by non-residents' column (level 2)

# fce_h_nr = t43_clean_mi['Final consumption expenditure by households, domestic concept']['of which: Domestic purchases by non-residents']
# does not work, instead see below combining .iloc and get_level_values:
fce_h_nr = t43_clean_mi.iloc[:, t43_clean_mi.columns.get_level_values(2)=='of which: Domestic purchases by non-residents']
# in this case, because the overal totals row is not included in the original slice.
# this column ONLY contains '..' in the intermediate fields, while still contributing.

# will fd_hh yield a dataframe of 2 columns? --> YES
fd_hh = t43_clean_mi.iloc[:, t43_clean_mi.columns.get_level_values(1)=='Final consumption expenditure by households, domestic concept']
exports = t43_clean_mi.iloc[:, t43_clean_mi.columns.get_level_values(0)=='Exports']
exports_simple = exports.iloc[:,0]  # important: in absence of unique names for levels, slice resulting df.
necessary_columns_pos = [
    t43_clean_mi.iloc[:, t43_clean_mi.columns.get_level_values(1)=='Final consumption expenditure by households, domestic concept'].iloc[:,0],
    # t43_clean_mi.iloc[:, t43_clean_mi.columns.get_level_values(2)=='of which: Domestic purchases by non-residents'],
    t43_clean_mi.iloc[:, t43_clean_mi.columns.get_level_values(1)=='Final consumption expenditure by NIPSH'],
    t43_clean_mi.iloc[:, t43_clean_mi.columns.get_level_values(1)=='Final consumption expenditure by government'],
    t43_clean_mi.iloc[:, t43_clean_mi.columns.get_level_values(1)=='Gross fixed capital formation'],
    t43_clean_mi.iloc[:, t43_clean_mi.columns.get_level_values(1)=='Changes in inventories'],
    t43_clean_mi.iloc[:, t43_clean_mi.columns.get_level_values(1)=='Acquisitions less disposals of valuables'],
    # t43_clean_mi.iloc[:, t43_clean_mi.columns.get_level_values(0)=='Exports'].iloc[:,0] # works, but dim 78, instead of 78,1
    # additional slicing creates a series instead of a df. If this is a problem: resize
    t43_clean_mi.iloc[:, t43_clean_mi.columns.get_level_values(0)=='Exports'].iloc[:,0] - t43_clean_mi.iloc[:, t43_clean_mi.columns.get_level_values(0)=='Exports'].iloc[:,1]
    ]

exports_net = t43_clean_mi.iloc[:, t43_clean_mi.columns.get_level_values(0)=='Exports'].iloc[:,0] - t43_clean_mi.iloc[:, t43_clean_mi.columns.get_level_values(0)=='Exports'].iloc[:,1]
gdp_expenditure_use = pd.concat(necessary_columns_pos, axis=1)
gdp_expenditure_use_sum = gdp_expenditure_use.sum().sum()  # first sum creates a series, 2nd creates a float or int
# gdp_expenditure_use_sumsum = gdp_expenditure_use_sum.sum()
# imports = t30_table_30_mi.iloc[:, t30_table_30_mi.columns.get_level_values(1)=='Imports, cif']
# gdp_expenditure_supply_sum = imports.sum().sum()
necessary_columns_neg = [
    t30_table_30_mi.iloc[:, t30_table_30_mi.columns.get_level_values(1)=='Imports, cif']
    ]
gdp_expenditure_supply_sum = necessary_columns_neg[0].sum().sum()

gdp_expenditure = gdp_expenditure_use_sum - gdp_expenditure_supply_sum  # too high: mistake in exports? 

SU_GDP_approaches_results["expenditure"] = gdp_expenditure
#%% GDP by production approach
# GDP = Gross VA (BP) + Taxes less subsidies on products (ST)
# Gross VA = Total output at BP (ST) - Intermediate consumption (UT)
gross_va = total_supply_bp - intermediate_consumption
tls_op = t30_table_30_mi.iloc[:, t30_table_30_mi.columns.get_level_values(0)=='Taxes less subsidies on products'].sum().sum()
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
# - drop .. columns? 
