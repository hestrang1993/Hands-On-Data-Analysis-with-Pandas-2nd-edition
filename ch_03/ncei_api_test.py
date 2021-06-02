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


# Run the code above directly (no import needed)
if __name__ == '__main__':
    response = make_request(request_endpoint, test_payload)
    if response.ok:
        print(response.ok)
    else:
        print('Nothing was retrieved.')