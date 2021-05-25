# Necessary imports
import pandas as pd
import numpy as np


csv_file_path = 'data/earthquakes.csv'
"""
str: The path to the earthquake data from September 18, 2018 - October 13, 2018

Obtained from the US Geological Survey (USGS) using the USGS API
"""

df_csv = pd.read_csv(csv_file_path)
"""
pandas.dataframe: The DataFrame we will examine in this notebook.

It will be the test DataFrame used in this notebook.
The DataFrame is built on the CSV file I loaded in before.
"""

df_csv


# Checks to see if DataFrame object is empty or not
df_csv.empty


# Get the shape of the DataFrame object
df_csv.shape


df_csv.columns

# Test to see if this returns an iterable item
test = df_csv.columns
for col in test:
    print(col)

# See the original return of df_csv.columns
test


# Get the head of the DataFrame object
df_csv.head()


# Get the tail of the DataFrame object
df_csv.tail(2)


# Get the data types in each column of the DataFrame object
df_csv.dtypes


# Get a lot of information about the DataFrame object
df_csv.info()


# Base describe() method
df_csv.describe()


floor = 0.05
"""
float: The lowest percentile to look at
"""
ceiling = 0.95
"""
float: The highest percentile to look at
"""
percentile_range = [floor, ceiling]
"""
list(float, float): The floor and ceiling to use for our example percentile range
"""

# Describe the DataFrame object within a given range
df_csv.describe(percentiles=percentile_range)


data_type = object
"""
object: The data type to test the include argument with
"""
df_csv.describe(include = data_type)


data_type = "all"
"""
str: The data type to test the include argument with
"""
df_csv.describe(include = data_type)


df_csv.felt.describe()


# Retrieve a column using attributes
df_csv.time


# Retrieve a column using dictionaries
first_column_to_get = 'time'
"""
str: A unique column header from my DataFrame instance.

Used to test getting one or more columns from a pandas DataFrame.
"""
df_csv[first_column_to_get]


# Retrieving more than one column using dictionaries
second_column_to_get = 'title'
"""
str: A unique column header from my DataFrame instance.

Used to test getting one or more columns from a pandas DataFrame.
"""
columns_dictionary = [first_column_to_get, second_column_to_get]
"""
list(str, str): A dictionary containing two or more column headings from my DataFrame instance.
"""
df_csv[columns_dictionary]


# Create a new columns dictionary using list comprehension and string operations
columns_dictionary = columns_dictionary + [column for column in df_csv.columns if column.startswith('mag')]
columns_dictionary


df_csv[columns_dictionary]


row_start = 101
"""
int: The row to start the slice at.

This is an inclusive value.
"""
row_stop = 104
"""
int: The row I need to stop.

This is an exclusive value.
"""
df_csv[row_start: row_stop]


df_csv[columns_dictionary][row_start: row_stop]


# Indexing with loc
df_csv.loc[row_start:row_stop, columns_dictionary]


# Indexing with iloc
first_column_to_get_index = 18
second_column_to_get_index = 19
columns_to_get_indices = [first_column_to_get_index, second_column_to_get_index]
df_csv.iloc[row_start: row_stop + 1, columns_to_get_indices]


# Scalars with at
test_row = 10
"""
int: A random row to test at and iat with.
"""
test_column_title = 'mag'
"""
str: A random column heading to test at with.
"""
df_csv.at[test_row, test_column_title]


# Scalars with iat
test_column_index = 8
"""
int: A random column index to test iat with.
"""
df_csv.iat[test_row, test_column_index]


# Boolean mask on a column
bool_mag_value = 7.0
"""
float: The magnitude of the earthquake I want to filter for.
"""
df_csv.mag > bool_mag_value


# Boolean mask on a selection
df_csv[df_csv.mag >= bool_mag_value]


# Boolean mask + loc
df_csv.loc[
    df_csv.mag >= bool_mag_value,
    columns_dictionary
]


bool_alert_value = 'red'
"""
str: The boolean value for the alert I want to filter for.

This argument can either be ``red`` or ``green``.
"""
## Using & with Boolean masks.
df_csv.loc[
    (df_csv.tsunami >= 1) & (df_csv.alert == bool_alert_value),
    columns_dictionary
]


## Using | with Boolean masks.
df_csv.loc[
    (df_csv.tsunami >= 1) | (df_csv.alert == bool_alert_value),
    columns_dictionary
]


location_to_check = 'Alaska'
"""
str: A location I want to see whether they've had earthquakes or not.
"""
# Filtering for all earthquakes occurring in Alaska.
# Use the notnull() method to return instances of earthquakes that triggered alerts.
columns_dictionary = [
    'alert',
    'mag',
    'magType',
    'title',
    'tsunami',
    'type'
]
df_csv.loc[(df_csv.place.str.contains(location_to_check)) & (df_csv.alert.notnull()), columns_dictionary]


mag_filter = 3.8
"""
float: The magnitude to use for this filter test.
"""
df_csv.loc[(df_csv.place.str.contains(r'CA|California$')) & (df_csv.mag > mag_filter), columns_dictionary]


min_mag = 6.5
"""
float: The minimum magnitude to include in the filter.
"""
max_mag = 7.5
"""
float: The maximum magnitude to include in the filter.
"""
df_csv.loc[df_csv.mag.between(min_mag, max_mag), columns_dictionary]


isin_dict = ['mw', 'mwb']
"""
list(str, str): The items to use as a filter for a column.

I'll use this dictionary to return rows with either a `mw` element or a `mwb` element in the `magType` column.
"""
df_csv.loc[df_csv.magType.isin(isin_dict), columns_dictionary]


mag_min_max_dict = [df_csv.mag.idxmin(), df_csv.mag.idxmax()]
"""
[int, int]: The index for the minimum and maximum values in the `mag` column.
"""
df_csv.loc[mag_min_max_dict, columns_dictionary]


items_list = ['mag', 'magType']
"""
[str, str]: The columns to get from my DataFrame instance.
"""
df_csv.filter(items_list).head()


df_csv.filter(like = 'mag').head()


df_csv.filter(regex = r'^t').head()


index_to_set = 'place'
df_csv.set_index(index_to_set).filter(like = 'Japan', axis = 0).filter(items = columns_dictionary).head()



