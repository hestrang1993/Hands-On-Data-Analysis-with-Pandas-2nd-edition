# Necessary imports
from matplotlib import pyplot as plt
import pandas as pd
import requests
import seaborn as sns

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


# Get the first x number of columns from the wide DataFrame instance
number_of_rows_to_get = 6
"""
int: The number of rows to display.
"""
wide_df.head(number_of_rows_to_get)


wide_df.describe(include = 'all', datetime_is_numeric = True)


long_df.head(number_of_rows_to_get)


# Seaborn variables
y_label = 'Temperature in Celsius'
"""
str: The y-axis label for this seaborn plot.
"""
title = 'Temperature in NYC (October 2018)'
"""
str: The title for the seaborn plot.
"""
rc_dict = {'figure.figsize': (15, 5)}
"""
{str: (int, int)}: A dictionary defining the seaborn figure size.
"""
style_str = 'white'
"""
str: The style argument for the seaborn plot.
"""

# Drawing the plot
sns.set_theme(rc = rc_dict, style = style_str)
ax = sns.lineplot(
    data = long_df,
    x = 'date',
    y = 'value',
    hue = 'datatype'
)
ax.set_ylabel(y_label)
ax.set_title(title)
plt.show()


# Plot variables
rc_dict = {'figure.figsize': (20, 10)}
"""
{str: (int, int)}: A dictionary defining the seaborn figure size.
"""
font_scl = 2
"""
int: The scaling for fonts in the faceted plots.
"""
title_size = 25
"""
str: The size of the title for the facet plots.
"""
x_label_rotation = 90
"""
int: The degree of rotation for the x-labels.
"""
plot_height = 10
"""
int: The height of the faceted plots.
"""
col_key = 'datatype'
"""
str: The key to facet out the datatype.
"""

# Drawing the plots
sns.set(rc = rc_dict, style = style_str, font_scale = font_scl)
g = sns.FacetGrid(long_df, col = col_key, height = plot_height)
g = g.map(plt.plot, 'date', 'value')
g.set_titles(size = title_size)
g.set_xticklabels(rotation = x_label_rotation)
plt.show()


# The token dictionary I need to access the NCEI data.
api_token_dict = {'token': 'ysVIqRTQlsItJQPLcOelgYbIIxPancXx'}
"""
{str: str}: The NCEI API token key I need to access the data.
"""

# Variables that will help my GET request.
api_website = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/'
"""
str: The website I'll use for the NCEI API.
"""
request_endpoint = 'datasets'
"""
str: The name of the endpoint I want to get.
"""
test_payload = {'startdate': '2018-10-01'}
"""
dict[str, str]: The payload I want to retrieve.
"""


# Defining the function that will make my GET request.
def make_request(endpoint, payload = None):
    """
    Make a request to a specific endpoint on the weather API
    passing headers and optional payload.

    Parameters
    ----------
    endpoint: str
        The endpoint of the API I want to make a GET request to.
    payload: dict[str, str]
        A dictionary of data to pass along with the request.

    Returns
    -------
    requests.Response
        A response object.
    """
    return requests.get(
            f'{api_website}{endpoint}',
            headers = api_token_dict,
            params = payload
    )


# Create the Response instance.
response = make_request(request_endpoint, test_payload)

# If the function worked, calling response.ok will return True
response.ok


# Access the JSON payload
payload = response.json()

# Return the keys of the JSON payload
payload.keys()


# Returning the metadata of the JSON instance.
meta_key = 'metadata'
"""
str: The key I need to access the metadata of the JSON payload. 
"""
payload[meta_key]


# Return what kind of data I got
results_key = 'results'
"""
str: The key I need to access what kind of data I got from the JSON payload.
"""
row_headings_index = 0
"""
int: The index for the row headings.

By default, this will be 0.
"""
payload[results_key][row_headings_index].keys()


def parse_payload(field_1, field_2, key_1, payload_in):
    """
    Perform a list comprehension on a dictionary payload.

    Parameters
    ----------
    field_1 : str
        The key for the first field I want to get.
    field_2 : str
        The key for the second field I want to get.
    key_1 : str
        The key where I can find field_1 and field_2.
    payload_in: dict
        The

    Returns
    -------
    list[tuple[str, str]]
        The list comprehension I want to get.

    Note
    ----
    The :param:`payload_in` will be the parent for all other arguments in this function.
    Both :param:`field_1` and :param:`field_2` are keys within the :param:`key_1` dictionary.
    """
    return [(data[field_1], data[field_2]) for data in payload_in[key_1]]

# Create list comprehension to get the information within the id key and name key
list_comprehension = parse_payload('id', 'name', 'results', payload)
"""list[tuple[str, str]]: A list comprehension of the names and IDs for data in my NCEI GET instance.
"""

# Display the results.
list_comprehension


endpoint_in = 'datacategories'
"""
str: The endpoint I want to return.

In this case, it will be the data categories from the GHCND dataset.
"""
payload_in = {'datasetid': 'GHCND'}
"""
dict[str, str]: The payload I want to load for this request.

In this case, I want to use the ``datasetid`` key to return values from the ``GHCND`` dataset.
"""
response = make_request(endpoint_in, payload_in)

# Check to see if the response went through.
response.ok



