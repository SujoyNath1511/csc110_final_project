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
import statistics
from Datasets_aggregation import read_annual_mean_sea_level_new_zealand, read_global_temp_new_zealand


if __name__ == '__main__':
    dict_info = read_global_temp_new_zealand(
        'mfe-global-and-new-zealand-temperatures-five-year-running-averag-CSV/'
        'global-and-new-zealand-temperatures-five-year-running-averag.csv')
    read_annual_mean_sea_level_new_zealand(
        'mfe-annual-mean-sea-level-relative-to-land-19002013-CSV/'
        'annual-mean-sea-level-relative-to-land-19002013.csv',
        dict_info)
    time = [year for year in dict_info]
    temperature = [dict_info[year].temp for year in time]
    sea_level = [statistics.mean(dict_info[year].sea_level) for year in time]
    max_time = max(time)
    time2 = [i + max_time for i in range(1, 41)]
    # Predicted outcome is the list that would be the line of best fit.
    # Predicted temperature depends on time, and predicted sea level depends on predicted temperature.
    temp_time_intercept, temp_time_slope = one_pred_reg_cofficients(time, temperature)
    predicted_temperature = one_predictor_linear_regression(time, temperature) + \
        [temp_time_intercept + temp_time_slope * i for i in time2]
    sl_temp_intercept, sl_temp_slope = one_pred_reg_cofficients(temperature, sea_level)
    predicted_sea_level = one_predictor_linear_regression(temperature, sea_level) + \
        [sl_temp_intercept + sl_temp_slope * predicted_temperature[i] for i in range(len(time), len(time) + 40)]
    trace_temperature = get_trace_all_points(time, temperature, mode='markers',
                                             name='temperature', color='#636EFA')
    trace_sea_level = get_trace_all_points(time, sea_level, mode='markers',
                                           name='sea level', color='#00CC96')
    trace_predicted_temp = get_trace_first_point(time + time2, predicted_temperature, mode='lines',
                                                 name='predicted temperature', color='#EF553B')
    trace_predicted_sl = get_trace_first_point(time + time2, predicted_sea_level, mode='lines',
                                               name='predicted sea level', color='#AB63FA')

    frames = get_frames(time + time2, [predicted_temperature, predicted_sea_level],
                        mode=['lines', 'lines'], indexes=[1, 3])

    layout = get_layout(frames, len(temperature), xrange=[min(time), max_time + 40],
                        yrange1=[min(predicted_temperature) * .9,
                                 max(predicted_temperature) * 1.1],
                        yrange2=[min(predicted_sea_level) * .9,
                                 max(predicted_sea_level) * 1.1])
    line_chart = go.Figure(
        data=[trace_temperature, trace_predicted_temp, trace_sea_level, trace_predicted_sl],
        frames=frames,
        layout=layout
    )
    line_chart.update_traces(visible='legendonly')
    line_chart.show()
