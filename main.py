"""CSC110 Fall 2020 Final Project, Computational Model: Linear Regression

This module contains the functions required to perform Linear Regression on
one predictor, including calculating the correlation and RMSE values for the
models.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC110 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2020 Sujoy Deb Nath, Yunjia Guo, Benjamin Lee and Mohamed Abdullahi.
"""

from final_project.linear_regression import *
import random
from typing import List, Tuple


def create_dataset() -> List[List[float]]:
    """Creates a random dataset for testing purposes.
    """
    time_column = [random.randint(1900, 2020) for i in range(0, 1000)]
    sea_level_column = [random.uniform(-5.00, 5.00) for j in range(0, 1000)]
    temperature_column = [random.uniform(-3, 5) for k in range(0, 1000)]

    return [time_column, temperature_column, sea_level_column]


if __name__ == '__main__':
    dataset = create_dataset()

    # You can change which column for your own purposes.
    column_a = dataset[0]
    column_b = dataset[1]

    # Predicted outcome is the list that would be the line of best fit
    predicted_outcome = one_predictor_linear_regression(column_a, column_b)

    # Continue the work below
    ...
