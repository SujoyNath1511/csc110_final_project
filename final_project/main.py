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
from final_project.Datasets_aggregation import *

if __name__ == '__main__':
    temp_info = read_global_temp_new_zealand(
        'temp/temp_new_zealand.csv')

    data_for_region = read_annual_mean_sea_level_new_zealand(
        'sea_level/annual-mean-sea-level-relative-to-land-19002013.csv',
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

    # Create the Scatter objects for the time and temperature
    trace_temp = get_trace_all_points(time, temperature, mode='markers',
                                      name='Temperature', color='blue')
    trace_pred_temp = get_trace_first_point(time2, pred_temp, mode='lines',
                                            name='Predicted Temperature', color='red')
    # ---------------------------------------------------------------------------------------------

    traces_so_far = [trace_temp, trace_pred_temp]

    visible = {'Temperature vs Sea Level': [False, False],
               'Temperature vs Time': [True, True],
               'Sea Level vs Time': [False, False]}

    colors = {'Auckland': 'orange', 'Wellington': 'blue', 'Dunedin': 'red', 'Lyttleton': 'green',
              'New_Plymouth': 'brown'}

    for location in data_for_region:
        temp = data_for_region[location].temps
        sea_level = data_for_region[location].sea_levels
        year = data_for_region[location].years

        # Create linear regression model of sea-level and temperature
        pred_sl, temp2 = one_predictor_linear_regression(
            predictor=temp, response=sea_level, forecast=True,
            forecast_end_time=round(max(pred_temp)))

        # Create linear regression model of sea-level and time
        pred_sl_2, year2 = one_predictor_linear_regression(
            predictor=year, response=sea_level, forecast=True, forecast_end_time=max(time2))

        # Visualization part

        # Get traces for temperature-sea level data
        trace_sl_vs_temp = get_trace_all_points(temp, sea_level, mode='markers',
                                                name='Sea Levels vs Temperature in ' + location.rstrip('_MSL'),
                                                color=colors[location.rstrip('_MSL')])

        # Scatterplot of the predicted temperature-sea level (regression line)
        trace_linear_reg = get_trace_all_points(temp2, pred_sl, mode='lines',
                                                name='Linear Regression Line for ' + location.rstrip('_MSL'),
                                                color=colors[location.rstrip('_MSL')])

        # Scatterplot of sea level-time data
        trace_sl = get_trace_all_points(year, sea_level, mode='markers',
                                        name='Sea Levels in ' + location.rstrip('_MSL'),
                                        color=colors[location.rstrip('_MSL')])

        # Scatterplot of predicted sea level-time data (regression line)
        trace_pred_sl = get_trace_all_points(year2, pred_sl_2, mode='lines',
                                             name='Predicted Sea Levels in ' + location.rstrip('_MSL'),
                                             color=colors[location.rstrip('_MSL')])

        traces_so_far.extend([trace_sl_vs_temp, trace_linear_reg, trace_sl, trace_pred_sl])
        visible['Temperature vs Sea Level'].extend([True, True, False, False])
        visible['Temperature vs Time'].extend([False, False, False, False])
        visible['Sea Level vs Time'].extend([False, False, True, True])

    # Add a new trace in which all values are None, so that every non-animated traces do not disappear
    trace_none = get_trace_first_point([None], [None], 'lines', ' ', 'black')
    trace_none.update(dict(showlegend=False))  # let the legend of this trace be invisible
    traces_so_far.append(trace_none)
    for option in visible:
        visible[option].append(True)

    # Get frames for line chart animation
    frames = get_frames(time2, [pred_temp, [None] * len(pred_temp)], indexes=[1, len(traces_so_far) - 1])

    # Get layout for setting interface
    sea_level = [sea_lvl for region in data_for_region for sea_lvl in data_for_region[region].sea_levels]
    layout = get_layout(frames, len(temperature),
                        xrange=[[min(temperature) * 0.98, max(temperature) * 1.02],
                                [min(time2) - 5, max(time2) + 5]],
                        yrange=[[min(sea_level) * 0.85, max(sea_level) * 1.05],
                                [min(temperature) * 0.95, max(temperature) * 1.05],
                                [min(sea_level) * 0.85, max(sea_level) * 1.05]],
                        visible=visible)

    line_chart = go.Figure(
        data=traces_so_far,
        frames=frames,
        layout=layout
    )

    # Update traces so that the traces of sea levels versus temperature are the only visible traces at
    # the beginning
    for title in {'Temperature', 'Predicted Temperature'}:
        line_chart.update_traces(visible=False, selector=dict(name=title))
    for location in data_for_region:
        for title in {'Sea Levels in ' + location.rstrip('_MSL'),
                      'Predicted Sea Levels in ' + location.rstrip('_MSL')}:
            line_chart.update_traces(visible=False, selector=dict(name=title))

    # Display the figure
    line_chart.show()
