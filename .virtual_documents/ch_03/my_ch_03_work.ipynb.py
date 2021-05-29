# Necessary imports
from matplotlib import pyplot as plt
import pandas as pd

# File paths
wide_data_file_path = 'data/wide_data.csv'
"""
str: The relative pathway to the wide data format CSV.
"""
long_data_file_path = 'data/long_data.csv'
"""
str: The relative pathway to the long data format CSV.
"""

# Variables for building the DataFrame instances
use_columns_long = ['date', 'datatype', 'value']
"""
list of str: The column headings for the columns I want to use for the long data format DataFrame instance.
"""
parse_date_arg = ['date']
"""
[str]: This variable will be used to tell pandas to parse the DataFrame instances along the date format.
"""

# Creating the DataFrame instances: wide & long
wide_df = pd.read_csv(wide_data_file_path, parse_dates = parse_date_arg)
print(type(wide_df))
"""
pandas.core.frame.DataFrame: The wide format DataFrame instance.
"""
long_df = pd.read_csv(long_data_file_path, parse_dates = parse_date_arg, usecols = use_columns_long)
"""
pandas.core.frame.DataFrame: The long format DataFrame instance.
"""

# Sort columns in the long DataFrame instance
long_df = long_df[use_columns_long]



