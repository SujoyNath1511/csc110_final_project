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
from final_project.linear_regression_v2 import *
from final_project.visualization import *
import random
from typing import List, Dict
from final_project.Datasets_aggregation import *

if __name__ == '__main__':
    temp_info = read_global_temp_new_zealand(
        'temp/temp_new_zealand.csv')

    data_for_region = read_annual_mean_sea_level_new_zealand(
        'sea_level/annual-mean-sea-level-relative-to-land-19002013.csv',
        temp_info)

    time = []
    temperature = []
    sea_level = []
    for location in data_for_region:
        for sea_temp_data in data_for_region[location]:
            time.append(sea_temp_data.year)
            temperature.append(sea_temp_data.temp)
            sea_level.append(sea_temp_data.sea_level)

    # Predicted outcome is the list that would be the line of best fit.
    # Predicted temperature depends on time, and predicted sea level depends on predicted temperature.

    predicted_temperature, time2 = one_predictor_linear_regression(predictor=time, response=temperature,
                                                                   forecast=True,
                                                                   forecast_end_time=max(time) + 40)

    predicted_sea_level, temp2 = one_predictor_linear_regression(
        predictor=temperature, response=sea_level, forecast=True,
        forecast_end_time=round(max(temperature)) + round(max(predicted_temperature)))

    trace_temperature = get_trace_all_points(time, temperature, mode='markers',
                                             name='temperature', color='#636EFA')
    trace_sea_level = get_trace_all_points(time, sea_level, mode='markers',
                                           name='sea level', color='#00CC96')
    trace_predicted_temp = get_trace_first_point(time2, predicted_temperature, mode='lines',
                                                 name='predicted temperature', color='#EF553B')
    trace_predicted_sl = get_trace_first_point(time2, predicted_sea_level, mode='lines',
                                               name='predicted sea level', color='#AB63FA')

    frames = get_frames(time2, [predicted_temperature, predicted_sea_level],
                        mode=['lines', 'lines'], indexes=[1, 3])

    layout = get_layout(frames, len(temperature), xrange=[time[0], time[-1]],
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
