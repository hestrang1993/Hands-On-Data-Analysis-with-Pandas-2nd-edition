"""
The :py:mod:`ch_02.inspecting_a_dataframe_object` will show me how to get basic information about my
:pandas.core.frame.DataFrame:`DataFrame` instance.
"""
from ch_02.dataframe_test_instance import df_csv

is_empty = df_csv.empty
"""
bool: A Boolean value that tells me whether the DataFrame instance is empty or not
"""

dimensions = df_csv.shape
"""
(int, int): The dimensions of my :obj:`DataFrame` instance.
"""

if __name__ == '__main__':
    print(is_empty)
    print(dimension)
    print(type(dimension))
