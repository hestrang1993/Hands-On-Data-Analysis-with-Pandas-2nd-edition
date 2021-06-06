"""
The :mod:`ch03.ncei_api_test` module is meant to test getting data using :mod:`requests`.
"""
# Key import
import requests

# Key variables for my request.
api_token_dict = {'token': 'ysVIqRTQlsItJQPLcOelgYbIIxPancXx'}
"""
dict[str, str]: A dictionary for accessing NCEI API.
"""
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


def make_request(endpoint, payload_in = None):
    """
    Makes a request to a specific endpoint on the weather API
    passing headers and optional payload.

    Parameters
    ----------
    endpoint : str
        The endpoint of the API I want to make a GET request to.
    payload_in : dict[str, str]
        A dictionary of data to pass along with the request.

    Returns
    -------
    requests.Response
        A response object.
    """
    return requests.get(
            f'{api_website}{endpoint}',
            headers = api_token_dict,
            params = payload_in
    )


# Call the NCEI API and get a JSON response.
response = make_request(request_endpoint, test_payload)
"""
requests.Response: The NCEI GET request object with the data I need.

This request is a JSON payload. Thus, it needs to be converted into a dictionary in the future.
"""

# Convert the JSON into a dictionary.
payload = response.json()
"""
dict: The dictionary version of the JSON response.
"""


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


list_comprehension = parse_payload('id', 'name', 'results', payload)


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


def look_left(what, endpoint_in, start, mid):
    """
    If the name I want comes before the current name, then this function will search to the left of the last search.

    Parameters
    ----------
    what : dict[str, str]
        A dictionary specifying
    endpoint_in : str
        The name of the location I want to look in.
    start : int, optional
        The position to start looking at.
    mid : int
        The midpoint for the dataset.

    Returns
    -------
    requests.Response
        The API request in a JSON file format.
    """
    payload_left = get_response_out(what, endpoint_in, start, mid - 1)
    return payload_left


def look_right(what, endpoint_in, start, mid):
    """
    If the name I want comes after the current name, then this function will search to the right of the last search.

    Parameters
    ----------
    what : dict[str, str]
        A dictionary specifying
    endpoint_in : str
        The name of the location I want to look in.
    start : int, optional
        The position to start looking at.
    mid : int
        The midpoint for the dataset.

    Returns
    -------
    requests.Response
        The API request in a JSON file format.
    """
    payload_right = get_response_out(what, endpoint_in, start, mid + 1)
    return payload_right


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
    name = name.lower()

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


# Run the code above directly (no import needed)
if __name__ == '__main__':
    name_nyc = 'New York'
    what_nyc = {
            'locationcategoryid': 'CITY'
    }
    endpoint_nyc = 'locations'
    nyc = get_item(name_nyc, what_nyc, endpoint_nyc)
    print(nyc)
