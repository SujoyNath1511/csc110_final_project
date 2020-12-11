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
import plotly
import plotly.io as pio
from typing import List, Dict
from CSC110_final_project.Datasets_aggregation import *
import dash
import dash_core_components as dcc
import dash_html_components as html
if __name__ == '__main__':
    temp_info = read_global_temp_new_zealand(
        'temp/temp_new_zealand.csv')

    data_for_region = read_annual_mean_sea_level_new_zealand(
        'sea_level/annual-mean-sea-level-relative-to-land-19002013.csv',
        temp_info)

    temperature = data_for_region['Auckland_MSL'].temp
    time = data_for_region['Auckland_MSL'].year
    sea_level = [sea_lvl for region in data_for_region for sea_lvl in data_for_region[region].sea_level]


    Auckland = data_for_region['Auckland_MSL']
    Wellington = data_for_region['Wellington']
    Dunedin = data_for_region['Dunedin_MSL']
    Lyttleton = data_for_region['Lyttleton_MSL']
    New_Plymouth = data_for_region['New_Plymouth_MSL']

    # Predicted outcome is the list that would be the line of best fit.
    # Predicted temperature depends on time, and predicted sea level depends on predicted temperature.

    pred_temp, time2 = one_predictor_linear_regression(
        predictor=time, response=temperature,
        forecast=True,
        forecast_end_time=max(time) + 40)

    # Version 1
    # Using a for loop to implement one_predictor_linear_regression and append the tuples into the list
    one_predictor_linear_reg = []
    for region in data_for_region:
        one_predictor_linear_reg.append(one_predictor_linear_regression(
            predictor=data_for_region[region].temp, response=data_for_region[region].sea_level, forecast=True,
            forecast_end_time=round(max(data_for_region[region].temp)) + round(max(pred_temp))))

    # Version 2
    # Using Variables which leads to more clarity in code

    # Linear regression for each city sea_level vs temperature
    # Auckland_lin_reg = one_predictor_linear_regression(
    #     predictor=Auckland.temp, response=Auckland.sea_level, forecast=True,
    #     forecast_end_time=round(max(Auckland.temp)) + round(max(pred_temp)))
    #
    # Wellington_lin_reg = one_predictor_linear_regression(
    #     predictor=Wellington.temp, response=Wellington.sea_level, forecast=True,
    #     forecast_end_time=round(max(Wellington.temp)) + round(max(pred_temp)))
    #
    # Dunedin_lin_reg = one_predictor_linear_regression(
    #     predictor=Dunedin.temp, response=Dunedin.sea_level, forecast=True,
    #     forecast_end_time=round(max(Dunedin.temp)) + round(max(pred_temp)))
    #
    # Lyttleton_lin_reg = one_predictor_linear_regression(
    #     predictor=Lyttleton.temp, response=Lyttleton.sea_level, forecast=True,
    #     forecast_end_time=round(max(Lyttleton.temp)) + round(max(pred_temp)))
    #
    # New_Plymouth_lin_reg = one_predictor_linear_regression(
    #     predictor=New_Plymouth.temp, response=New_Plymouth.sea_level, forecast=True,
    #     forecast_end_time=round(max(New_Plymouth.temp)) + round(max(pred_temp)))

    pred_sl, temp2 = one_predictor_linear_regression(
        predictor=temperature, response=sea_level, forecast=True,
        forecast_end_time=round(max(temperature)) + round(max(pred_temp)))

    # visualization part
    # get traces for temperature-sea level data and regression lines

    # For Auckland
    Auckland_trace_sl_vs_temp = get_trace_all_points(Auckland.temp, Auckland.sea_level, mode='markers',
                                                     name='Sea levels vs temperature in Auckland', color='orange')
    Auckland_trace_linear_reg = get_trace_all_points(Auckland.temp, one_predictor_linear_reg[0][0][:len(Auckland.temp)],
                                                     mode='lines', name='Auckland linear regression', color='orange')

    # For Wellington
    Wellington_trace_sl_vs_temp = get_trace_all_points(Wellington.temp, Wellington.sea_level, mode='markers',
                                                       name='Sea levels vs temperature in Wellington', color='blue')
    Wellington_trace_linear_reg = get_trace_all_points(Wellington.temp,
                                                       one_predictor_linear_reg[1][0][:len(Wellington.temp)],
                                                       mode='lines', name='Wellington Line regression', color='blue')

    # For Dunedin
    Dunedin_trace_sl_vs_temp = get_trace_all_points(Dunedin.temp, Dunedin.sea_level, mode='markers',
                                                    name='Sea levels vs temperature for Dunedin',
                                                    color='red')
    Dunedin_trace_linear_reg = get_trace_all_points(Dunedin.temp, one_predictor_linear_reg[2][0][:len(Dunedin.temp)],
                                                    mode='lines',
                                                    name='Dunedin Line regression', color='red')

    # For Lyttleton
    Lyttleton_trace_sl_vs_temp = get_trace_all_points(Lyttleton.temp, Lyttleton.sea_level, mode='markers',
                                                      name='Sea levels vs Temperatures in Lyttleton', color='green')
    Lyttleton_trace_linear_reg = get_trace_all_points(Lyttleton.temp,
                                                      one_predictor_linear_reg[3][0][:len(Lyttleton.temp)],
                                                      mode='lines', name='Lyttleton Line regression', color='green')

    # For New_Plymouth
    New_Plymouth_trace_sl_vs_temp = get_trace_all_points(New_Plymouth.temp, New_Plymouth.sea_level, mode='markers',
                                                         name='Sea levels vs Temperatures in New Plymouth',
                                                         color='black')
    New_Plymouth_trace_linear_reg = get_trace_all_points(New_Plymouth.temp,
                                                         one_predictor_linear_reg[4][0][:len(New_Plymouth.temp)],
                                                         mode='lines',
                                                         name='New Ploymouth linear regression', color='black')

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
        # Plug in the traces and the linear regressions lines for the 5 cities
        data=[Auckland_trace_sl_vs_temp, Wellington_trace_sl_vs_temp, Dunedin_trace_sl_vs_temp,
              Lyttleton_trace_sl_vs_temp, New_Plymouth_trace_sl_vs_temp, Auckland_trace_linear_reg,
              Wellington_trace_linear_reg, Dunedin_trace_linear_reg, Lyttleton_trace_linear_reg,
              New_Plymouth_trace_linear_reg, trace_temp, trace_pred_temp, trace_sl, trace_pred_sl],
        frames=frames,
        layout=layout
    )
    
    # update traces so that the traces of regression models are the only visible traces at the beginning
    for title in ['temperature', 'predicted temperature', 'sea level', 'predicted sea level']:
        line_chart.update_traces(visible=False, selector=dict(name=title))

    # Use this if it works for you
    # line_chart.show()

    line_chart.show(renderer='browser')
