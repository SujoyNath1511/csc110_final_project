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
    max_time = max(time)
    time2 = [i + max_time for i in range(1, 41)]
    temperature = [dict_info[year].temp for year in time]
    sea_level = [statistics.mean(dict_info[year].sea_level) for year in time]
    
    # Predicted outcome is the list that would be the line of best fit.
    # Predicted temperature depends on time, and predicted sea level depends on predicted temperature.
    temp_time_intercept, temp_time_slope = one_pred_reg_cofficients(time, temperature)
    pred_temp = one_predictor_linear_regression(time, temperature) + \
        [temp_time_intercept + temp_time_slope * i for i in time2]
    sl_temp_intercept, sl_temp_slope = one_pred_reg_cofficients(temperature, sea_level)
    pred_sl = one_predictor_linear_regression(temperature, sea_level) + \
        [sl_temp_intercept + sl_temp_slope * pred_temp[i] for i in range(len(time), len(time) + 40)]
    
    # visualization part
    # get traces for temperature-sea level data and regression lines
    trace_sl_vs_temp = get_trace_all_points(temperature, sea_level, mode='markers', name='sl vs temp', color='orange')
    trace_linear_reg = get_trace_all_points(temperature, pred_sl[:len(temperature)], mode='lines',
                                            name='linear regression', color='orange')
    
    # get traces for temperature/sea level versus time data
    trace_temp = get_trace_all_points(time, temperature, mode='markers',
                                      name='temperature', color='#636EFA')
    trace_sl = get_trace_all_points(time, sea_level, mode='markers',
                                    name='sea level', color='#00CC96')
    trace_pred_temp = get_trace_first_point(time + time2, pred_temp, mode='lines',
                                            name='predicted temperature', color='#EF553B')
    trace_pred_sl = get_trace_first_point(time + time2, pred_sl, mode='lines',
                                          name='predicted sea level', color='#AB63FA')

    # get frames for line chart animation
    frames = get_frames(time + time2, [pred_temp, pred_sl],
                        mode=['lines', 'lines'], indexes=[3, 5])
    
    # get layout for setting interface
    layout = get_layout(frames, len(temperature),
                        xrange=[[min(temperature) * 0.98, max(temperature) * 1.02],
                                [min(time) - 5, max_time + 45]],
                        yrange=[[min(sea_level) * 0.95, max(sea_level) * 1.05],
                                [min(temperature) * 0.95, max(temperature) * 1.05],
                                [min(sea_level) * 0.95, max(sea_level) * 1.05]])
    
    # generate the graphic object
   line_chart = go.Figure(
        data=[trace_sl_vs_temp, trace_linear_reg, trace_temp, trace_pred_temp, trace_sl, trace_pred_sl],
        frames=frames,
        layout=layout
    )

    # update traces so that the traces of regression models are the only visible traces at the beginning
    for title in ['temperature', 'predicted temperature', 'sea level', 'predicted sea level']:
        line_chart.update_traces(visible=False, selector=dict(name=title))

    # display the figure
    line_chart.show()
