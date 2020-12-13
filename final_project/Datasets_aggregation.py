"""
Datasets Aggregations

CSC110 Final Project
"""
from typing import List, Dict
import csv
from dataclasses import dataclass


@dataclass
class TempWaterInfo:
    """A dataclass that gives the temperature in celsius and average water level in meters for a specific year

    Instance Attributes:
        - years: A list of years that the data was recorded for
        - temps: A list of temperatures in Celsius. The temperature at index i
                 is the mean temperature for years[i]
        - sea_levels: A list of average sea levels in meters. The sea level at index i is the mean temperature for
                      years[i]

    Representation Invariant:
        - len(self.years) == len(self.temps) == len(self.sea_levels)
    """
    years: List[int]
    temps: List[float]
    sea_levels: List[float]


def read_global_temp_new_zealand(filename: str) -> Dict[int, float]:
    """
    Returns a dictionary mapping years to temperatures for that year in New Zealand.
    Reads the csv file temp_new_zealand.csv and filters out all the rows that don't have
    'NZ_7_Stn_Composite_Temp' in the second column. Takes the first column as year and the 
    third column as temperature.
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


def read_annual_mean_sea_level_new_zealand(filename: str, temp_info: Dict[int, float]) \
        -> Dict[str, TempWaterInfo]:
    """
    Returns a dictionary with the location as the key and maps to TempWaterInfo, which stores the
    temperature and sea level for that location for the given years. Reads the csv file
    'annual-mean-sea-level-relative-to-land-19002013.csv'. It filters out years where there is no sea level
    or temperature data for that given year. For the data not filtered out, it uses the second row as the
    location and takes the sea level from the file. Uses temp_info to access the temperature for a given year.
    
    """
    dict_so_far = {}
    with open(filename) as file:
        reader = csv.reader(file)
        next(reader)  # Skip the first row
        for row in reader:
            year = int(row[0])
            if row[2] == 'no_data' or year not in temp_info:
                continue
            if row[1] in dict_so_far:
                dict_so_far[row[1]].years.append(year)
                dict_so_far[row[1]].temps.append(temp_info[year])
                dict_so_far[row[1]].sea_levels.append(float(row[2]))
            else:
                dict_so_far[row[1]] = TempWaterInfo([year], [temp_info[year]], [float(row[2])])

    return dict_so_far
