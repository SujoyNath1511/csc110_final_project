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

    pred_temp, time2 = one_predictor_linear_regression(
        predictor=time, response=temperature,
        forecast=True,
        forecast_end_time=max(time) + 40)

    pred_sl, temp2 = one_predictor_linear_regression(
        predictor=temperature, response=sea_level, forecast=True,
        forecast_end_time=round(max(temperature)) + round(max(pred_temp)))

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
    trace_pred_temp = get_trace_first_point(time2, pred_temp, mode='lines',
                                            name='predicted temperature', color='#EF553B')
    trace_pred_sl = get_trace_first_point(time2, pred_sl, mode='lines',
                                          name='predicted sea level', color='#AB63FA')

    # get frames for line chart animation
    frames = get_frames(time2, [pred_temp, pred_sl],
                        mode=['lines', 'lines'], indexes=[3, 5])

    # get layout for setting interface
    layout = get_layout(frames, len(temperature),
                        xrange=[[min(temperature) * 0.98, max(temperature) * 1.02],
                                [min(time2) - 5, max(time2) + 5]],
                        yrange=[[min(sea_level) * 0.95, max(sea_level) * 1.05],
                                [min(temperature) * 0.95, max(temperature) * 1.05],
                                [min(sea_level) * 0.95, max(sea_level) * 1.05]])
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
