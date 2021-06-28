"""
import this module in feature extraction script using

from preprocessing import temporary_df_read

logic for reading D0 dataframe is hard coded for now; control to be given to the user later. This module will be depreacted in our final version.
the try block is for 170619a2-delim-whitespace.csv
the except block is for test1-delim-line.csv

to test it from the feature extraction directory, use
python feature_extractor.py ../test_data/170619a2-delim-whitespace.csv from the feature extraction directory

This module will give you access to a dataframe with sorted out column headers and delimiters. 

Using the naming convention
d0-for the raw dataframe with correct tried encoding
d1- for the dataframe with correct delimiter
.
.
.
df- for the final dataframe with correct delimiter, skipped rows, column_headers, index_columns, correct number of columns

"""

import pandas as pd 
import numpy as np
import sys

filename = sys.argv[1]



try:
	df = pd.read_csv(filename, encoding = 'utf-16', skiprows=16, delimiter='\t', index_col='Scan') 
	print(df.head())
except:
	df = pd.read_csv(filename, encoding = 'utf-8', skiprows=0, delimiter='|', index_col=0) ## for
	print(df.head())