# Set how Python handles rendering code cells, particularly HTML
from IPython.core.display import display, HTML
display(HTML("<style>.container { width:100% get_ipython().getoutput("important; }</style>"))")


get_ipython().run_cell_magic("html", "", """<style>
/*Make a 16:9 container*/
.container {
    position: relative;
    overflow: hidden;
    width: 100%;
    padding-top: 56.25%;
}
/*Make the iframe responsive*/
.responsive-iframe {
    position: absolute;
    top: 0;
    left: 0;
    bottom: 0;
    right: 0;
    width: 100%;
    height: 100%;
    border: none;
}
</style>
<!--Create the div-->
<div class="container">
    <!--Create the iframe-->
    <iframe src="https://www.ncdc.noaa.gov/cdo-web/webservices/v2" class="responsive-iframe"><iframe>
</div>""")


# Necessary imports
from matplotlib import pyplot as plt
import pandas as pd
from pprint import pprint
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


payload = response.json()['results']
"""
dict: The payload with the results I want.
"""
payload


limit = 100
"""
int: The number of datatypes I want to get.
"""
endpoint_in = 'datatypes'
payload_in = {'datacategoryid': 'TEMP', 'limit': limit}
response = make_request(endpoint_in, payload_in)
response.ok


payload = response.json()
list_comprehension = parse_payload('id', 'name', 'results', payload)
list_comprehension


# Get the location category ID.
endpoint_in = 'locationcategories'
payload_in = {'datasetid': 'GHCND'}
response = make_request(endpoint_in, payload_in)
payload = response.json()


pprint(payload)


def get_data_midpoint(start = 1, end = None):
    """
    Get the midpoint of the data set.

    I will use this midpoint to cut the data in half after each search.

    Parameters
    ----------
    start : int, optional
        The index to start the search at.

        I don't need to touch this.
        The functions I plan to make will update this through recursion.
    end : int or None, optional
        The last index.

        I use this to find the midpoint.
        The functions I plan to make will update this through recursion.

    Returns
    -------
    int
        The midpoint for the dataset.
    """
    mid = (start + (end or 1)) // 2
    return mid


def to_lower(name):
    """
    Make a name lowercase.

    I make the name lowercase so any search won't run into case-sensitivity issues.

    Parameters
    ----------
    name : str
        The name of the item I want to look for.

    Returns
    -------
    str
        The name of the item I want to look for in lowercase font.
    """
    name = name.lower()
    return name


def define_payload(mid):
    """
    Define the payload to send with each request.

    Parameters
    ----------
    mid : int
        The midpoint of the dataset I want to search through.

    Returns
    -------
    dict[str: str, str: str, str: int, str: int]
        The payload I want to get with each NCEI API request.
    """
    payload_to_get = {
            "datasetid": "GHCND",
            "sortfield": "name",
            "offset": mid,
            "limit": 1
    }
    return payload_to_get


def get_response_out(what, endpoint_in, start = 1, end = None):
    """
    Get the NCEI GET request instance.

    Parameters
    ----------
    what : dict[str, str]
        A dictionary specifying
    endpoint_in : str
        The name of the location I want to look in.
    start : int, optional
        The position to start looking at.
    end : int or None, optional
        The last position to look at.

    Returns
    -------
    requests.Response
        The API request in a JSON file format.
    """
    mid = get_data_midpoint(start, end)
    payload_to_get = define_payload(mid)
    response_out = make_request(endpoint_in, {**payload_to_get, **what})
    return response_out


def get_payload_out(response_to_convert):
    """
    Get a dictionary version of the JSON response.

    Parameters
    ----------
    response_to_convert : requests.Response
        The GET request I want to convert into a dictionary.

    Returns
    -------
    dict
        A dictionary version of the JSON response I want.
    """
    payload_out = response_to_convert.json()
    return payload_out


def get_the_end_index(end, payload_in):
    """
    Return the end index

    Parameters
    ----------
    end : int
        The old end index.
    payload_in : dict
        A JSON Response instance that has been converted into a dictionary.

    Returns
    -------
    int
        The new end index to use.
    """
    m = 'metadata'
    r = 'resultset'
    c = 'count'
    end_index = end or payload_in[m][r][c]
    return end_index


def get_current_name(payload_in):
    """
    Grab the lowercase version of the current name.

    Parameters
    ----------
    payload_in : dict
        A JSON Response instance that has been converted into a dictionary.

    Returns
    -------
    str
        The lowercase version of the string found at a particular index in the dictionary I loaded in.
    """
    r = 'results'
    n = 'name'
    index = 0
    current_name = payload_in[r][index][n]
    current_name = to_lower(current_name)
    return current_name


def get_item(name, what, endpoint, start = 1, end = None):
    """
    Grab the JSON payload for a given field by name using binary search.

    Parameters
    ----------
    name : str
        The item to look for.
    what: dict[str, str]
        Dictionary specifying what the item in ``name`` is.
    endpoint : str
        Where to look for the item.
    start : int, optional
        The position to start at.

        We don't need to touch this, but the function will manipulate this with recursion.
    end : int or None, optional
        The last position of the items.

        Used to find the midpoint, but like ``start`` this is not something we need to worry about.

    Returns
    -------
    dict
        Dictionary of the information for the item if found otherwise
        an empty dictionary.
    """
    # Get the midpoint of the data set.
    mid = get_data_midpoint(start, end)

    # Make our request adding any additional filter parameters from ``what``.
    response_to_get = get_response_out(what, endpoint, start, end)

    # Make the name lowercase.
    name = to_lower(name)

    # Check the response, if it went through.
    if response.ok:

        # Convert the JSON response into a dictionary.
        payload_i_got = response_to_get.json()

        # Find the end index of the dictionary.
        end = get_the_end_index(end, payload_i_got)

        # Get the string item at the end of the dictionary.
        current_name = get_current_name(payload_i_got)

        # Return the found item.
        if name in current_name:
            return payload_i_got['results'][0]
        else:
            # If our start index is greater than or equal to our end, we couldn't find it
            if start >= end:
                return {}
            # Our name comes before the current name in the alphabet, so we search further to the left
            elif name < current_name:
                return get_item(name, what, endpoint, start, mid - 1)
            # Our name comes after the current name in the alphabet, so we search further to the right
            elif name > current_name:
                return get_item(name, what, endpoint, mid + 1, end)
    else:
        # The response wasn't ok, use code to determine why
        print(f'Response not OK, status: {response.status_code}')


# Get NYC's ID
nyc_name = "New York"
"""
str: The item to look for.

In this case, it will be NYC.
"""
nyc_what = {"locationcategoryid": "CITY"}
"""
dict[str: str]: Dictionary specifying what the item in ``nyc_name`` is.
"""
nyc_endpoint = "locations"
"""
str: Where to look for the NYC ID.
"""
nyc = get_item(nyc_name, nyc_what, nyc_endpoint)
nyc


central_park_name = 'NY City Central Park'
"""
str: The item to look for.

In this case, it is the station at NYC Central Park.
"""
central_park_what = {
    'locationid': nyc['id']
}
"""
dict[str: dict]: Dictionary specifying what the item in ``central_park_name`` is.
"""
central_park_endpoint = 'stations'
"""
str: Where to look for the NYC Central Park ID.
"""
central_park = get_item(central_park_name, central_park_what, central_park_endpoint)
central_park


central_park_endpoint = 'data'
"""
str: The endpoint for where I the temperature data for NYC Central Park is.
"""
central_park_payload_in = {
        'datasetid': 'GHCND',
        'stationid': central_park['id'],
        'locationid': nyc['id'],
        'startdate': '2018-10-01',
        'enddate': '2018-10-31',
        'datatypeid': [
                'TAVG',
                'TMAX',
                'TMIN'
        ],
        'units': 'metric',
        'limit': 1000
}
"""
dict: The payload I need to submit to get the temperature data for NYC Central Park.
"""
central_park_response = make_request(central_park_endpoint, central_park_payload_in)
central_park_response.ok


# Convert the Response instance into a dictionary
grab = 'results'
"""
str: The part of the Response instance to grab.
"""
central_park_response = central_park_response.json()[grab]
"""
dict: A dictionary with all the temperatures from NYC Central Park.
"""

# Create the DataFrame instance
df_central_park = pd.DataFrame(central_park_response)
"""
pandas.core.frame.DataFrame: The DataFrame with the daily minimum and maximum temperatures from NYC Central Park during October, 2018.
"""
df_central_park.head()



