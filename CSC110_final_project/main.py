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
from CSC110_final_project.linear_regression import *
from CSC110_final_project.visualization import *
import random
from typing import List, Dict
from CSC110_final_project.Datasets_aggregation import *


def create_dataset() -> List[List[float]]:
    """Creates a random dataset for testing purposes.
    """
    time_column = list(range(1900, 2071))
    temperature_column = [random.uniform(-10, 10) + i * 1.8 for i in range(0, 120)]
    sea_level_column = [random.uniform(-15, 15) + j * 1.5 for j in range(0, 120)]

    return [time_column, temperature_column, sea_level_column]


if __name__ == '__main__':
    dataset = create_dataset()

    # time = dataset[0]
    # temperature = dataset[1]
    # sea_level = dataset[2]

    temperature_data = read_global_temp_new_zealand('temp/temp_new_zealand.csv')
    read_annual_mean_sea_level_new_zealand('sea_level/annual-mean-sea-level-relative-to-land-19002013.csv', temperature_data)

    year = [year for year in temperature_data]
    temperature = [temperature_data[temp].temp for temp in temperature_data]
    sea_levels = [sum(temperature_data[year].sea_level) / len(temperature_data[year].sea_level)
                  for year in temperature_data]

    # Predicted outcome is the list that would be the line of best fit.
    # Predicted temperature depends on time, and predicted sea level depends on predicted temperature.
    temp_time_intercept, temp_time_slope = one_pred_reg_cofficients(year[:120], temperature)
    predicted_temperature = one_predictor_linear_regression(year[:120], temperature) + \
        [temp_time_intercept + temp_time_slope * year[i] for i in range(120, len(year))]
    sl_temp_intercept, sl_temp_slope = one_pred_reg_cofficients(temperature, sea_levels)
    predicted_sea_level = one_predictor_linear_regression(temperature, sea_levels) + \
        [sl_temp_intercept + sl_temp_slope * predicted_temperature[i] for i in range(120, len(year))]

    trace_temperature = get_trace_all_points(year[:120], temperature, mode='markers',
                                             name='temperature', color='#636EFA')
    trace_sea_level = get_trace_all_points(year[:120], sea_levels, mode='markers',
                                           name='sea level', color='#00CC96')
    trace_predicted_temp = get_trace_first_point(year, predicted_temperature, mode='lines',
                                                 name='predicted temperature', color='#EF553B')
    trace_predicted_sl = get_trace_first_point(year, predicted_sea_level, mode='lines',
                                               name='predicted sea level', color='#AB63FA')

    frames = get_frames(year, [predicted_temperature, predicted_sea_level],
                        mode=['lines', 'lines'], indexes=[1, 3])

    layout = get_layout(frames, len(temperature), xrange=[year[0], year[-1]],
                        yrange1=[min(predicted_temperature) - 10,
                                 max(predicted_temperature) + 10],
                        yrange2=[min(predicted_sea_level) - 10,
                                 max(predicted_sea_level) + 10])
    line_chart = go.Figure(
        data=[trace_temperature, trace_predicted_temp, trace_sea_level, trace_predicted_sl],
        frames=frames,
        layout=layout
    )
    line_chart.update_traces(visible='legendonly')
    line_chart.show()
