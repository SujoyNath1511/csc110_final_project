"""
Dummy functions that read csv datasets
Datasets Aggregations

CSC110 Final Project

These are the functions that I came up with so far. If you guys have any suggestion or anything you want to point out,
please do so.

I did not find it necessary to apply classes here.
If you guys think it is better, feel free to tell me and I will re-edit
"""
from typing import List, Tuple, Set, Any
import csv


# I made these two functions specifically for the datasets that Benjamin Suggested
def read_annual_mean_sea_level_new_zealand(filename: str) -> List[List[Any]]:
    """
    This function reads the csv file that stores the mean sea level relative to the land in New Zealand

    This function returns a list of lists that store all the rows in the csv file excluding the first row
    """
    data = []
    with open(filename) as file:
        reader = csv.reader(file)
        next(reader)    # Skip the first row
        for row in reader:
            data.append(row)

    return data


def read_global_temp_new_zealand(filename: str) -> List[List[Any]]:
    """
    This function reads the csv file that contains the New Zealand temperatures.

    It returns a list of lists that contain all the rows that have "NZ_7_Stn_Composite_Temp" excluding the first row
    """
    data = []
    with open(filename) as file:
        reader = csv.reader(file)
        next(reader)    # skip the first row

        for row in reader:
            if "NZ_7_Stn_Composite_Temp" in row:
                data.append(row)

    return data


def read_general_csv_files(filename: str) -> List[List[Any]]:
    """
    This function is a dummy version that reads the datasets "globl_temp" and "monthly_GMSL(the global sea levels)

    This function returns a list of lists that contain the rows for the dataset excluding the first row
    """
    data = []
    with open(filename) as file:
        reader = csv.reader(file)
        next(reader)    # Skip the first row

        for row in reader:
            data.append(row)

    return data
