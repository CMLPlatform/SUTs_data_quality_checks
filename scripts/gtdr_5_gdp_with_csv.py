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

# t_30_csv = pd.read_csv('OECD_Data_downloads\SNA_TABLE30_25052023111909457.csv', header=0)
# t_43_csv = pd.read_csv('OECD_Data_downloads\SNA_TABLE43_25052023114840741.csv', header=0)
# t_41_csv = pd.read_csv('OECD_Data_downloads\SNA_TABLE41_25052023114000008.csv', header=0)

t_30_csv_path = 'OECD_Data_downloads\SNA_TABLE30_25052023111909457.csv'
t_43_csv_path = 'OECD_Data_downloads\SNA_TABLE43_25052023114840741.csv'
t_41_csv_path = 'OECD_Data_downloads\SNA_TABLE41_25052023114000008.csv'
total_rows_ignore = 't_30_total_cols_rows.txt'

#%% GDP calc with functions

t_30 = functions.csv_input(t_30_csv_path, 30)
t_43 = functions.csv_input(t_43_csv_path, 43)
t_41 = functions.csv_input(t_41_csv_path, 41)

gdp_values = functions.gdp_csv(t_30, t_43, t_41, total_rows_ignore, t_30_csv_path)

print('The calculated GDP values are as follows: \n', gdp_values)

