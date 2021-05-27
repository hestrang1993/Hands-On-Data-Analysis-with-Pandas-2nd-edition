"""
The :module:`ch01.exercises` module is meant to test my ability to use Python to perform important statistical operations.
"""
# Imports
import random

import numpy as np
from scipy import stats

# Setting the random seed
seed_value = 0
"""
int: The seed to use for random.seed()
"""
random.seed(seed_value)

# Variables to help build the salaries list
N_salaries = 100  # Number of salaries in thSe salaries list
"""
int: The number of salaries to randomly generate for this exercise.

Adjust this to adjust the number of elements in the exercise list.
"""
max_salary = 100000  # Maximum potential salary
"""
int: The maximum possible salary.

Use this as the ceiling for any randomly generated list.
"""
salaries = []
"""
list[float]: The list to use for this exercise.
"""
for i in range(0, N_salaries):
    salary = round(random.random() * max_salary, -3)
    salaries.append(salary)

# Get the mean salary
mean = np.mean(salaries)

# Get the median salary
median = np.median(salaries)

# Get the most common salary (mode salary)
mode = stats.mode(salaries)

# Get the statistical variance of the salaries
statistical_variance = np.var(salaries, ddof=1)


class BasicStatisticsCalculator:
    """
    The :class:`BasicStatisticsCalculator` class will automatically calculate several statistical values from a given
    1-dimensional :type:`list` of :type:`float` values.
    """

    def __init__(self, list_in=None):
        """
        __init__ Create an instance of :class:`BasicScienceCalculator`.

        [extended_summary]

        Args:
            list_in (list[float], optional): [description]. Defaults to None.
        """
        if list_in is None:
            list_in = []
        self.list_in = list_in
        self._np = np
        self._stats = stats
        self._number_of_values = len(self.list_in)
        self._mean = self.np.mean(self.list_in)
        self._median = self.np.median(self.list_in)
        self._mode = self.stats.mode(self.list_in)
        self._statistical_variance = self.np.var(self, ddof=1)

    @property
    def np(self):
        """
        numpy: The NumPy package.
        """
        return self._np

    @property
    def stats(self):
        """
        scipy.stats: The statistics module from SciPy.
        """
        return self._stats

    @property
    def number_of_values(self):
        """
        int: The number of elements in the list to analyze.
        """
        return self._number_of_values

    @property
    def mean(self):
        """
        int or dtype or ndarray or float64: The mean value from the list to analyze.
        """
        return self._mean

    @property
    def median(self):
        """
        numpy.median: The median value in the list to analyze.
        """
        return self._median

    @property
    def mode(self):
        """
        scipy.stats.mode: The most common value in the list to analyze.
        """
        return self._mode

    @property
    def statistical_variance(self):
        """
        numpy.var: The statistical variance of the list to analyze.

        Includes a Bessel's correction.
        """
        return self._statistical_variance

    @property
    def test(self):
        """
        test [summary]

        [extended_summary]
        """


if __name__ == '__main__':
    print(f"Salaries: {salaries}")
    print(f"Mean Salary: {mean}")
    bsc = BasicStatisticsCalculator(list_in=salaries)
    print(f"Mean Salary: {bsc.mean}")
