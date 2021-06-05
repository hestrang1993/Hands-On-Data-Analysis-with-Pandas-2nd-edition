import requests

def make_request(endpoint, payload=None):
    """
    Make a request to a specific endpoint on the weather API
    passing headers and optional payload.
    
    Parameters:
        - endpoint: The endpoint of the API you want to 
                    make a GET request to.
        - payload: A dictionary of data to pass along 
                   with the request.
    
    Returns:
        A response object.
    """
    return requests.get(
        f'https://www.ncdc.noaa.gov/cdo-web/api/v2/{endpoint}',
        headers={
            'token': 'PASTE_TOKEN_HERE'
        },
        params=payload
    )


response = make_request('datasets', {'startdate': '2018-10-01'})


response.status_code


response.ok


payload = response.json()
payload.keys()


payload['metadata']


payload['results'][0].keys()


[(data['id'], data['name']) for data in payload['results']]


# get data category id
response = make_request(
    'datacategories', payload={'datasetid': 'GHCND'}
)
response.status_code


response.json()['results']


# get data type id
response = make_request(
    'datatypes',
    payload={
        'datacategoryid': 'TEMP', 
        'limit': 100
    }
)
response.status_code


[(datatype['id'], datatype['name']) for datatype in response.json()['results']][-5:] # look at the last 5


# get location category id 
response = make_request(
    'locationcategories', 
    payload={'datasetid': 'GHCND'}
)
response.status_code


import pprint
pprint.pprint(response.json())


def get_item(name, what, endpoint, start=1, end=None):
    """
    Grab the JSON payload for a given field by name using binary search.

    Parameters:
        - name: The item to look for.
        - what: Dictionary specifying what the item in `name` is.
        - endpoint: Where to look for the item.
        - start: The position to start at. We don't need to touch this, but the
                 function will manipulate this with recursion.
        - end: The last position of the items. Used to find the midpoint, but
               like `start` this is not something we need to worry about.

    Returns:
        Dictionary of the information for the item if found otherwise 
        an empty dictionary.
    """
    # find the midpoint which we use to cut the data in half each time
    mid = (start + (end or 1)) // 2
    
    # lowercase the name so this is not case-sensitive
    name = name.lower()
    
    # define the payload we will send with each request
    payload = {
        'datasetid': 'GHCND',
        'sortfield': 'name',
        'offset': mid, # we will change the offset each time
        'limit': 1 # we only want one value back
    }
    
    # make our request adding any additional filter parameters from `what`
    response = make_request(endpoint, {**payload, **what})
    
    if response.ok:
        payload = response.json()

        # if response is ok, grab the end index from the response metadata the first time through
        end = end or payload['metadata']['resultset']['count']
        
        # grab the lowercase version of the current name
        current_name = payload['results'][0]['name'].lower()
        
        # if what we are searching for is in the current name, we have found our item
        if name in current_name:
            return payload['results'][0] # return the found item
        else:
            if start >= end: 
                # if our start index is greater than or equal to our end, we couldn't find it
                return {}
            elif name < current_name:
                # our name comes before the current name in the alphabet, so we search further to the left
                return get_item(name, what, endpoint, start, mid - 1)
            elif name > current_name:
                # our name comes after the current name in the alphabet, so we search further to the right
                return get_item(name, what, endpoint, mid + 1, end)    
    else:
        # response wasn't ok, use code to determine why
        print(f'Response not OK, status: {response.status_code}')


# get NYC id 
nyc = get_item('New York', {'locationcategoryid': 'CITY'}, 'locations')
nyc


central_park = get_item('NY City Central Park', {'locationid': nyc['id']}, 'stations')
central_park


# get NYC daily summaries data 
response = make_request(
    'data', 
    {
        'datasetid': 'GHCND',
        'stationid': central_park['id'],
        'locationid': nyc['id'],
        'startdate': '2018-10-01',
        'enddate': '2018-10-31',
        'datatypeid': ['TAVG', 'TMAX', 'TMIN'], # average, max, and min temperature
        'units': 'metric',
        'limit': 1000
    }
)
response.status_code


import pandas as pd

df = pd.DataFrame(response.json()['results'])
df.head()


df.datatype.unique()


if get_item(
    'NY City Central Park', {'locationid': nyc['id'], 'datatypeid': 'TAVG'}, 'stations'
):
    print('Foundget_ipython().getoutput("')")


laguardia = get_item(
    'LaGuardia', {'locationid': nyc['id']}, 'stations'
)
laguardia


# get NYC daily summaries data 
response = make_request(
    'data', 
    {
        'datasetid': 'GHCND',
        'stationid': laguardia['id'],
        'locationid': nyc['id'],
        'startdate': '2018-10-01',
        'enddate': '2018-10-31',
        'datatypeid': ['TAVG', 'TMAX', 'TMIN'], # temperature at time of observation, min, and max
        'units': 'metric',
        'limit': 1000
    }
)
response.status_code


df = pd.DataFrame(response.json()['results'])
df.head()


df.datatype.value_counts()


df.to_csv('data/nyc_temperatures.csv', index=False)
