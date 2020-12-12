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
from final_project.Datasets_aggregation import read_annual_mean_sea_level_new_zealand, read_global_temp_new_zealand

if __name__ == '__main__':
    temp_info = read_global_temp_new_zealand(
        'mfe-global-and-new-zealand-temperatures-five-year-running-averag-CSV/'
        'global-and-new-zealand-temperatures-five-year-running-averag.csv')
    data_for_region = read_annual_mean_sea_level_new_zealand(
        'mfe-annual-mean-sea-level-relative-to-land-19002013-CSV/'
        'annual-mean-sea-level-relative-to-land-19002013.csv',
        temp_info)

    time = []
    temperature = []
    for year in temp_info:
        time.append(year)
        temperature.append(temp_info[year])

    # ---------------------------------------------------------------------------------------------
    # Predicted outcome is the list that would be the line of best fit.
    # Predicted temperature depends on time, and predicted sea level depends on predicted temperature.
    pred_temp, time2 = one_predictor_linear_regression(
        predictor=time, response=temperature,
        forecast=True,
        forecast_end_time=max(time) + 40)

    # Creates the Scatter objects for the time and temperature
    trace_temp = get_trace_all_points(time, temperature, mode='markers',
                                      name='temperature', color='#636EFA')
    trace_pred_temp = get_trace_first_point(time2, pred_temp, mode='lines',
                                            name='predicted temperature', color='#EF553B')
    # ---------------------------------------------------------------------------------------------

    traces_so_far = [trace_temp, trace_pred_temp]

    frames_so_far = []
    frames = []

    for location in data_for_region:

        temp = data_for_region[location].temp
        sea_level = data_for_region[location].sea_level
        year = data_for_region[location].year

        # Create linear regression model of sea-level and temperature
        pred_sl, temp2 = one_predictor_linear_regression(
            predictor=temp, response=sea_level, forecast=True,
            forecast_end_time=round(max(data_for_region[location].temp)) + round(max(pred_temp)))

        pred_sl_2, year2 = one_predictor_linear_regression(
            predictor=year, response=sea_level, forecast=True, forecast_end_time=max(year) + 40)

        # visualization part

        # get traces for temperature-sea level data
        trace_sl_vs_temp = get_trace_all_points(temp, sea_level, mode='markers',
                                                name='Sea Levels vs. Temperature in ' + location.strip('_MLS'),
                                                color='orange')

        # Scatterplot of the predicted temperature vs sea level values (regression line)
        trace_linear_reg = get_trace_all_points(temp2, pred_sl, mode='lines',
                                                name='linear regression', color='orange')

        # Scatterplot of sea level-time data
        trace_sl = get_trace_all_points(year, sea_level, mode='markers',
                                        name='sea levels in ' + location.strip('_MLS'), color='#00CC96')

        # Scatterplot of predicted sea level-time data (regression line)
        trace_pred_sl = get_trace_first_point(year2, pred_sl_2, mode='lines',
                                              name='predicted sea level', color='#AB63FA')

        traces_so_far.append(trace_sl_vs_temp)
        traces_so_far.append(trace_linear_reg)
        traces_so_far.append(trace_sl)
        traces_so_far.append(trace_pred_sl)

        # get frames for line chart animation
        frames = get_frames(time2, [pred_temp, pred_sl],
                            mode=['lines', 'lines'], indexes=[3, 5])

        # frames_so_far.append(frames)

    # get frames for line chart animation
    frames = get_frames(time2, [pred_temp, pred_sl],
                        mode=['lines', 'lines'], indexes=[3, 5])

    # get layout for setting interface
    sea_level = [sea_lvl for region in data_for_region for sea_lvl in data_for_region[region].sea_level]
    layout = get_layout(frames_so_far, len(temperature),
                        xrange=[[min(temperature) * 0.98, max(temperature) * 1.02],
                                [min(time2) - 5, max(time2) + 5]],
                        yrange=[[min(sea_level) * 0.95, max(sea_level) * 1.05],
                                [min(temperature) * 0.95, max(temperature) * 1.05],
                                [min(sea_level) * 0.95, max(sea_level) * 1.05]])

    line_chart = go.Figure(
        data=traces_so_far,
        frames=frames_so_far,
        layout=layout
    )

    # update traces so that the traces of regression models are the only visible traces at the beginning
    for title in ['temperature', 'predicted temperature', 'sea level', 'predicted sea level']:
        line_chart.update_traces(visible=False, selector=dict(name=title))

    # display the figure
    line_chart.show()
