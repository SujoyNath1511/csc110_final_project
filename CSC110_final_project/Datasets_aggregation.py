"""
Dummy functions that read csv datasets
Datasets Aggregations

CSC110 Final Project

These are the functions that I came up with so far. If you guys have any suggestion or anything you want to point out,
please do so.

I did not find it necessary to apply classes here.
If you guys think it is better, feel free to tell me and I will re-edit
"""
from typing import List, Tuple, Set, Any, Dict
import csv
from dataclasses import dataclass


@dataclass
class TempWaterInfo:
    """A dataclass that gives the temperature in celsius and average water level in meters for a specific year
    Instance Attributes:
    - year: The year that the data was recorded for
    - temp: The mean temperature for that given year
    - sea_level: The average sea level for that given year in meters in different places
    """
    year: int
    temp: float
    sea_level: List[float]


def read_annual_mean_sea_level_new_zealand(filename: str, temp_info: Dict[int, TempWaterInfo]) -> None:
    """
    This function reads the csv file that stores the mean sea level relative to the land in New Zealand
    This function returns a list of lists that store all the rows in the csv file excluding the first row
    """
    with open(filename) as file:
        reader = csv.reader(file)
        next(reader)  # Skip the first row
        for row in reader:
            if row[2] == 'no_data' or int(row[0]) not in temp_info:
                continue

            else:
                year = int(row[0])
                water_level = float(row[2])
                temp_info[year].sea_level.append(water_level)


def read_global_temp_new_zealand(filename: str) -> Dict[int, TempWaterInfo]:
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
                data[year] = TempWaterInfo(year, temp, [])

    return data


def read_general_csv_files(filename: str) -> List[List[Any]]:
    """
    This function is a dummy version that reads the datasets "globl_temp" and "monthly_GMSL(the global sea levels)
    This function returns a list of lists that contain the rows for the dataset excluding the first row
    """
    data = []
    with open(filename) as file:
        reader = csv.reader(file)
        next(reader)  # Skip the first row

        for row in reader:
            data.append(row)

    return data
