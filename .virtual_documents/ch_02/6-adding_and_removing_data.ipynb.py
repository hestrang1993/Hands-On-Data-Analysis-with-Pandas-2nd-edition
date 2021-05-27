import pandas as pd

df = pd.read_csv(
    'data/earthquakes.csv', 
    usecols=['time', 'title', 'place', 'magType', 'mag', 'alert', 'tsunami']
)


df['source'] = 'USGS API'
df.head()


df['mag_negative'] = df.mag < 0
df.head()


df.place.str.extract(r', (.*$)')[0].sort_values().unique()


df['parsed_place'] = df.place.str.replace(
    r'.* of ', '', regex=True # remove anything saying <something> of <something>
).str.replace(
    'the ', '' # remove "the "
).str.replace(
    r'CA$', 'California', regex=True # fix California
).str.replace(
    r'NV$', 'Nevada', regex=True # fix Nevada
).str.replace(
    r'MX$', 'Mexico', regex=True # fix Mexico
).str.replace(
    r' region$', '', regex=True # chop off endings with " region"
).str.replace(
    'northern ', '' # remove "northern "
).str.replace(
    'Fiji Islands', 'Fiji' # line up the Fiji places
).str.replace(
    r'^.*, ', '', regex=True # remove anything else extraneous from the beginning
).str.strip() # remove any extra spaces


df.parsed_place.sort_values().unique()


df.assign(
    in_ca=df.parsed_place.str.endswith('California'),
    in_alaska=df.parsed_place.str.endswith('Alaska')
).sample(5, random_state=0)


df.assign(
    in_ca=df.parsed_place == 'California',
    in_alaska=df.parsed_place == 'Alaska',
    neither=lambda x: ~x.in_ca & ~x.in_alaska
).sample(5, random_state=0)


tsunami = df[df.tsunami == 1]
no_tsunami = df[df.tsunami == 0]

tsunami.shape, no_tsunami.shape


pd.concat([tsunami, no_tsunami]).shape


tsunami.append(no_tsunami).shape


additional_columns = pd.read_csv(
    'data/earthquakes.csv', usecols=['tz', 'felt', 'ids']
)
pd.concat([df.head(2), additional_columns.head(2)], axis=1)


additional_columns = pd.read_csv(
    'data/earthquakes.csv', usecols=['tz', 'felt', 'ids', 'time'], index_col='time'
)
pd.concat([df.head(2), additional_columns.head(2)], axis=1)


pd.concat(
    [tsunami.head(2), no_tsunami.head(2).assign(type='earthquake')], join='inner'
)


pd.concat(
    [tsunami.head(2), no_tsunami.head(2).assign(type='earthquake')], join='inner', ignore_index=True
)


del df['source']
df.columns


try:
    del df['source']
except KeyError:
    # handle the error here
    print('not there anymore')


mag_negative = df.pop('mag_negative')
df.columns


mag_negative.value_counts()


df[mag_negative].head()


df.drop([0, 1]).head(2)


cols_to_drop = [
    col for col in df.columns
    if col not in ['alert', 'mag', 'title', 'time', 'tsunami']
]
df.drop(columns=cols_to_drop).head()


df.drop(columns=cols_to_drop).equals(
    df.drop(cols_to_drop, axis=1)
)


df.drop(columns=cols_to_drop, inplace=True)
df.head()
