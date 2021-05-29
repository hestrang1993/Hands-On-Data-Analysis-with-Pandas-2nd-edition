"""
The :mod:`ch_02.dataframe_test_instance` contains the :obj:`DataFrame` object I will use to
learn about
:obj:`DataFrame` objects in this chapter.

The object in question is :obj:`df_csv`.
"""

# Key Imports
import pandas as pd

path_to_csv_file = 'data/earthquakes.csv'
"""
str: The path to the file with earthquake data.
"""

df_csv = pd.read_csv(path_to_csv_file)
"""
pandas.core.frame.DataFrame: The DataFrame instance 
"""


if __name__ == '__main__':
    print(type(df_csv))
    print(df_csv)
