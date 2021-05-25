"""
The :py:mod:`ch_02.inspecting_a_dataframe_object` will show me how to get basic information about my
:pandas.core.frame.DataFrame:`DataFrame` instance.
"""
from ch_02.dataframe_test_instance import df_csv

var = df_csv.empty
"""
bool: A Boolean value that tells me whether the DataFrame instance is empty or not
"""

if __name__ == '__main__':
    print(var)

