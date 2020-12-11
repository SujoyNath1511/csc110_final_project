"""
Polynomial regression model
"""
from CSC110_final_project.Datasets_aggregation import *
from numpy import *
from scipy.interpolate import *
from matplotlib.pyplot import *
from typing import *
import chart_studio.plotly as py
import plotly.graph_objs as go
# Scientific libraries
import numpy as np


def get_coordinates() -> List[List[Any]]:
    """
    This function returns a List of lists that contain the years, temperature and sea levels
    """
    temperature_data = read_global_temp_new_zealand('temp/temp_new_zealand.csv')
    read_annual_mean_sea_level_new_zealand('sea_level/annual-mean-sea-level-relative-to-land-19002013.csv',
                                           temperature_data)

    year = [year for year in temperature_data]
    temperature = [temperature_data[temp].temp for temp in temperature_data]
    sea_levels = [sum(temperature_data[year].sea_level) / len(temperature_data[year].sea_level)
                  for year in temperature_data]

    return [year, temperature, sea_levels]


def plot_poly(data: List[List[Any]]) -> None:
    """
    Plots the data points using numpy
    """
    year = data[0]
    temperature = data[1]
    sea_levels = data[2]
    x_vals = array(year)
    y_vals = array(temperature)
    p2 = polyfit(x_vals, y_vals, 2)
    plot(x_vals, y_vals, "o")
    plot(x_vals, polyval(p2, x_vals), "r-")
    show()


if __name__ == "__main__":
    coordinates = get_coordinates()
    # plot_poly(coordinates)
    points = np.array([(1, 1), (2, 4), (3, 1), (9, 3)])

    # get x and y vectors
    x = coordinates[0]
    y = coordinates[1]

    # calculate polynomial
    z = np.polyfit(x, y, 2)
    f = np.poly1d(z)
    print(f)

    # calculate new x's and y's
    x_new = np.linspace(x[0], x[-1], 50)
    y_new = f(x_new)

    # Creating the dataset, and generating the plot
    trace1 = go.Scatter(
        x=x,
        y=y,
        mode='markers',
        marker=go.scatter.Marker(color='rgb(255, 127, 14)'),
        name='Data'
    )

    trace2 = go.Scatter(
        x=x_new,
        y=y_new,
        mode='lines',
        marker=go.scatter.Marker(color='rgb(31, 119, 180)'),
        name='Fit'
    )

    annotation = go.layout.Annotation(
        x=x,
        y=y,
        showarrow=False
    )
    layout = go.Layout(
        title='Polynomial Fit in Python',
        plot_bgcolor='rgb(229, 229, 229)',
        xaxis=go.layout.XAxis(zerolinecolor='rgb(255,255,255)', gridcolor='rgb(255,255,255)'),
        yaxis=go.layout.YAxis(zerolinecolor='rgb(255,255,255)', gridcolor='rgb(255,255,255)'),
        annotations=[annotation]
    )

    data = [trace1, trace2]
    fig = go.Figure(data=data, layout=layout)
    # fig.show()
    fig.update_layout(barmode='stack',
                      title='Polynomial regression for temperature change over the years in New Zealand',
                      xaxis_title='Years',
                      yaxis_title='Temperature')
    fig.write_image('POLY.png', width=1000)
