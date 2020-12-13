"""CSC110 Fall 2020 Final Project, Main File

This file is used to run the main program, by calling in functions to load in the datasets,
perform the necessary computations and visualizing the results.

Copyright and Usage Information
===============================
This file is provided solely for the personal and private use of students
taking CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited.
This file is Copyright (c) 2020 Sujoy Deb Nath, Yunjia Guo, Benjamin Lee and Mohamed Abdullahi.
"""

from final_project.linear_regression_v2 import *
from final_project.visualization import *
from final_project.datasets_aggregation import *

if __name__ == '__main__':

    # =============================================================================================
    # Load in the datasets
    # =============================================================================================
    temp_info = read_global_temp_new_zealand(
        'temp_new_zealand.csv')

    data_for_region = read_mean_sea_level_new_zealand(
        'annual-mean-sea-level-relative-to-land-19002013.csv',
        temp_info)

    # Turn the temperature data into 2 list, each a column from the dataset
    time = []               # The year column
    temperature = []        # The temperature column
    for year in temp_info:
        time.append(year)
        temperature.append(temp_info[year])

    # =============================================================================================
    # Computations
    # =============================================================================================

    # Create a linear model for Temperature vs Time
    pred_temp, time2 = one_predictor_linear_regression(
        predictor=time, response=temperature,
        forecast=True,
        forecast_end_time=max(time) + 40)

    # Create a scatter plot that plots time on the x-axis and temperature on the y-axis
    trace_temp = get_trace_all_points(time, temperature, mode='markers',
                                      name='Temperature', color='blue')

    # Create a line graph for the linear model of Temperature vs Time
    trace_pred_temp = get_trace_first_point(time2, pred_temp, mode='lines',
                                            name='Predicted Temperature', color='red')

    # Add the two scatterplots to a list of scatter plots that we will use later to plot all
    # graphs. Scatter plots are called traces in Plotly.
    traces_so_far = [trace_temp, trace_pred_temp]

    # This dictionary will be used later to define which graphs are visible based on which
    # option was picked on the drop down menu. Will be more obvious when you see the actual
    # graphs.
    visible = {'Temperature vs Sea Level': [False, False],
               'Temperature vs Time': [True, True],
               'Sea Level vs Time': [False, False]}

    # Colors for each coastal city in New Zealand in the dataset
    colors = {'Auckland': 'orange', 'Wellington': 'blue', 'Dunedin': 'red', 'Lyttleton': 'black',
              'New_Plymouth': 'green'}

    # For each city from the data set:
    for location in data_for_region:

        # Get the data for the temperatures, sea levels and years.
        temp = data_for_region[location].temps
        sea_level = data_for_region[location].sea_levels
        year = data_for_region[location].years

        # Create linear regression model of sea-level and temperature
        pred_sl, temp2 = one_predictor_linear_regression(
            predictor=temp, response=sea_level, forecast=True,
            forecast_end_time=round(max(pred_temp)))

        # Create linear regression model of sea-level and time (in years)
        pred_sl_2, year2 = one_predictor_linear_regression(
            predictor=year, response=sea_level, forecast=True, forecast_end_time=max(time2))

        # Scatter plot of the Sea level and Temperature from the dataset
        trace_sl_vs_temp = get_trace_all_points(temp, sea_level, mode='markers',
                                                name='Sea Levels vs Temperature in ' + location.rstrip('_MSL'),
                                                color=colors[location.rstrip('_MSL')])

        # Scatter plot of the predicted sea level and temperature (regression line)
        trace_linear_reg = get_trace_all_points(temp2, pred_sl, mode='lines',
                                                name='Linear Regression Line for ' + location.rstrip('_MSL'),
                                                color=colors[location.rstrip('_MSL')])

        # Scatter plot of Sea level and Time from the sea
        trace_sl = get_trace_all_points(year, sea_level, mode='markers',
                                        name='Sea Levels in ' + location.rstrip('_MSL'),
                                        color=colors[location.rstrip('_MSL')])

        # Scatter plot of predicted Sea level and Time data (regression line)
        trace_pred_sl = get_trace_all_points(year2, pred_sl_2, mode='lines',
                                             name='Predicted Sea Levels in ' + location.rstrip('_MSL'),
                                             color=colors[location.rstrip('_MSL')])

        # Add the scatter plots to the list of scatter plots.
        traces_so_far.extend([trace_sl_vs_temp, trace_linear_reg, trace_sl, trace_pred_sl])

        # Set the visibility of each graph so that only certain ones are shown based on which
        # graph the user wants to see. This is based on the graph drop down menu in the
        # visualization.
        visible['Temperature vs Sea Level'].extend([True, True, False, False])
        visible['Temperature vs Time'].extend([False, False, False, False])
        visible['Sea Level vs Time'].extend([False, False, True, True])

        # Underneath, we print the correlation and RMSE values for each regression line
        # created per iteration/per city.
        print('Correlation between Sea Level and Temperature for ' + location.rstrip('_MSL')
              + ': ' + str(correlation(temp, sea_level)))

        print('RMSE of Sea Level vs Temperature %s linear model: %0.2f'
              % (location.rstrip('_MSL'), calculate_rmse(sea_level, pred_sl[: len(sea_level)])))

        print('\n')  # print a new line

        print('Correlation between Sea Level and Time for ' + location.rstrip('_MSL')
              + ': ' + str(correlation(year, sea_level)))

        print('RMSE of Sea Level vs Time %s linear model: %0.2f'
              % (location.rstrip('_MSL'), calculate_rmse(sea_level, pred_sl_2[: len(sea_level)])))

        print('\n')

    # Print the RMSE and correlation values for the Temperature and Time linear model.
    print('Correlation of Average Temperature in New Zealand vs Time: %0.2f'
          % correlation(time, temperature))
    print('RMSE of Average Temperature in New Zealand vs Time: %0.2f'
          % calculate_rmse(temperature, pred_temp[: len(temperature)]))

    # Add a new trace in which all values are None, so that every non-animated traces do not disappear
    trace_none = get_trace_first_point([None], [None], 'lines', ' ', 'black')
    trace_none.update(dict(showlegend=False))  # let the legend of this trace be invisible
    traces_so_far.append(trace_none)

    # Let trace_none be visible in every graph that we can select from the drop down menu in the
    # visualization. This is so that when we animate the line, the other graphs don't become
    # invisible. Before when we animated the line, the other scatter plots became invisible,
    # this is to fix that.
    for option in visible:
        visible[option].append(True)

    # Get frames for Temperature vs Time line chart animation
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

    # Create the final graphs for visualization
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

    # Display the visualization of the graph.
    line_chart.show()
