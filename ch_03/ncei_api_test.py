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

# Run the code above directly (no import needed)
if __name__ == '__main__':
    print(list_comprehension)
