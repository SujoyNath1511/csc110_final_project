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

from linear_regression import *
from visualization import *
import random
from typing import List


def create_dataset() -> List[List[float]]:
    """Creates a random dataset for testing purposes.
    """
    time_column = list(range(1900, 2071))
    sea_level_column = [random.uniform(-5.00, 5.00) for _ in range(0, 120)]
    temperature_column = [random.uniform(-3, 5) for _ in range(0, 120)]

    return [time_column, temperature_column, sea_level_column]


if __name__ == '__main__':
    dataset = create_dataset()

    time = dataset[0]
    temperature = dataset[1]
    sea_level = dataset[2]

    # Predicted outcome is the list that would be the line of best fit.
    # Predicted temperature depends on time, and predicted sea level depends on predicted temperature.
    temp_time_intercept, temp_time_slope = one_pred_reg_cofficients(time[:120], temperature)
    predicted_temperature = one_predictor_linear_regression(time[:120], temperature) + \
        [temp_time_intercept + temp_time_slope * time[i] for i in range(120, 171)]
    sl_temp_intercept, sl_temp_slope = one_pred_reg_cofficients(temperature, sea_level)
    predicted_sea_level = one_predictor_linear_regression(temperature, sea_level) + \
        [sl_temp_intercept + sl_temp_slope * predicted_temperature[i] for i in range(120, 171)]

    trace_temperature = get_trace_all_points(time[:120], temperature, mode='markers',
                                             name='temperature')
    trace_sea_level = get_trace_all_points(time[:120], sea_level, mode='markers',
                                           name='sea level')
    trace_predicted_temp = get_trace_first_point(time, predicted_temperature, mode='lines',
                                                 name='predicted temperature')
    trace_predicted_sl = get_trace_first_point(time, predicted_sea_level, mode='lines',
                                               name='predicted sea level')

    frames = get_frames(time, [predicted_temperature, predicted_sea_level],
                        mode=['lines', 'lines'], indexes=[1, 3])

    layout = get_layout(frames, len(temperature), xrange=[1900, 2070], yrange=[-10, 10])

    line_chart = go.Figure(
        data=[trace_temperature, trace_predicted_temp, trace_sea_level, trace_predicted_sl],
        frames=frames,
        layout=layout
    )

    line_chart.show()
