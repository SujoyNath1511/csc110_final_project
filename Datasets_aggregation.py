"""
Dummy functions that read csv datasets
Datasets Aggregations

CSC110 Final Project

These are the functions that I came up with so far. If you guys have any suggestion or anything you want to point out,
please do so.

I did not find it necessary to apply classes here.
If you guys think it is better, feel free to tell me and I will re-edit
"""
from typing import List, Dict
import csv
from dataclasses import dataclass
# I made these two functions specifically for the datasets that Benjamin Suggested


@dataclass
class TempWaterInfo:
    """A dataclass that gives the temperature in celsius and average water level in meters for a specific year

    Instance Attributes:
    - year: The year that the data was recorded for
    - temp: The mean temperature for that given year
    - sea_level: The average sea level for that given year in meters in different places
    - location: The location where the temperature was located
    """
    year: int
    temp: float
    sea_level: float


def read_annual_mean_sea_level_new_zealand(filename: str, temp_info: Dict[int, float])\
        -> Dict[str, List[TempWaterInfo]]:
    """
    This function reads the csv file that stores the mean sea level relative to the land in New Zealand

    This function returns a list of lists that store all the rows in the csv file excluding the first row
    """
    dict_so_far = {}
    with open(filename) as file:
        reader = csv.reader(file)
        next(reader)    # Skip the first row
        for row in reader:
            year = int(row[0])
            if row[2] == 'no_data' or year not in temp_info:
                continue
            elif row[1] in dict_so_far:
                dict_so_far[row[1]].append(TempWaterInfo(year, temp_info[year], float(row[2])))
            else:
                dict_so_far[row[1]] = [TempWaterInfo(year, temp_info[year], float(row[2]))]

    return dict_so_far


def read_global_temp_new_zealand(filename: str) -> Dict[int, float]:
    """
    This function reads the csv file that contains the New Zealand temperatures.
    It returns a list of lists that contain all the rows that have "NZ_7_Stn_Composite_Temp" excluding the first row
    """
    data = {}
    with open(filename) as file:
        reader = csv.reader(file)
        next(reader)  # skip the first row

        for row in reader:
            if "NZ_7_Stn_Composite_Temp" in row:
                year = int(row[0])
                temp = float(row[2])
                data[year] = temp

    return data
