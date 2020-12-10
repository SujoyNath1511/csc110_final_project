"""CSC110 Fall 2020 Final Project, Visualization: Scatter Plot and Line Chart Animation with Plotly
This module contains functions that are required to generate scatter plot and animate lines
in one graph object figure.
"""

import plotly.graph_objects as go
from typing import List


def get_trace_first_point(x_value: list, y_value: list, mode: str, name: str, color: str) -> go.Scatter():
    """Return a go.Scatter object that only includes the first (x, y) point of given data.
       Set type (i.e. line or scatters) of the trace by the given string - mode.
       Set name, which will be shown in the legend, by the given string - name.
       Set color of the trace by the given string - color.
       Result that is obtained by calling this function can be used for line chart animation.

       Preconditions:
           - x_value != []
           - y_value != []
           - mode in {'lines', 'markers', 'lines+markers'}
           - name != ''
    """
    return go.Scatter({'x': x_value[:1], 'y': y_value[:1], 'mode': mode, 'name': name,
                       (mode[:-1] + '_color'): color})


def get_trace_all_points(x_value: list, y_value: list, mode: str, name: str, color: str) -> go.Scatter():
    """Return a go.Scatter object that includes all points of given data.
       Set type (i.e. line or scatters) of the trace by the given string - mode.
       Set name, which will be shown in the legend, by the given string - name.
       Set color of the trace by the given string - color.

       Preconditions:
           - x_value != []
           - y_value != []
           - len(x_value) == len(y_value)
           - mode in {'lines', 'markers', 'lines+markers'}
           - name != ''
    """
    return go.Scatter({'x': x_value, 'y': y_value, 'mode': mode, 'name': name,
                       (mode[:-1] + '_color'): color})


def get_frames(x_value: list, y_value: List[list], mode: List[str], indexes: List[int]) -> list:
    """Return a list of dictionaries that each of them is a frame. The k-th frame contains data
       points from the first one to the (k - 1)-th one, where k is between 1 and len(x_value),
       inclusive.
       Set type (i.e. line or scatters) of each frame by corresponding given mode.
       The list indexes contains integers that are indexes of every the traces that need to be
       updated.

       Preconditions:
           - x_value != []
           - y_value != []
           - all(y_value[i] != [] for i in range(0, len(y_value)))
           - all(len(x_value) == len(y_value[i]) for i in range(0, len(y_value)))
           - len(y_value) == len(mode) == len(index)
           - all(mode[i] in {'lines', 'markers', 'lines+markers'} for i in range(0, len(mode)))
    """
    frames = []
    for k in range(1, len(x_value) + 1):
        frame_so_far = dict(data=[go.Scatter(x=x_value[:k],
                                             y=y_value[i][:k],
                                             mode=mode[i])
                                  for i in range(0, len(y_value))],
                            traces=indexes
                            )
        frames.append(frame_so_far)

    return frames


def get_layout(frames: list, split_point: int, xrange: List[float], yrange1: List[float], yrange2: List[float]) \
        -> go.Layout():
    """Return a go.Layout object, which can be passed to the attribute 'layout' of a go.Figure object.
       Through layout we can set interface arrangement and intersections for a graphic figure.
       The variable updatemenus in the function body is a list that can be passed to the attribute
       'updatemenus' for a go.Layout object.

       The use for the given integer split_point is to divide analysis for previous data and prediction
       for future data. So it should be equal to the length of every aggregated dataset.
       Each of the two given lists xrange and yrange should be a list containing two float values.
       set range of xaxis and yaxis

       In updatemenus, we set:
       (i) Two buttons on the top:
         - 'Temperature vs Time': to show the plot of temperature versus time.
         - 'Sea Level vs Time': to show the plot of sea level versus time.
       (ii) Three buttons on the right:
         - 'Clear': can be clicked to clear regression line(s) has been generated.
         - 'Analyze': can be clicked to show our animated regression line(s).
         - 'Predict': can be clicked to show our predicted data for future time, i.e. extended
                      regression line(s).

    Preconditions:
        - breakpoint > 0
        - len(frames) >= breakpoint
        - len(xrange) == len(yrange1) == len(yrange2) == 2
        - all(range[0] < range[1] for range in [xrange, yrange1, yrange2])
    """
    updatemenus = [dict(type='buttons',  # set the two buttons on the top
                        direction='right',
                        showactive=False,
                        x=0.8,
                        y=1.11,
                        xanchor='center',
                        yanchor='top',
                        buttons=[dict(label='Temperature vs Time',
                                      method='update',
                                      args=[dict(visible=[True, True, False, False]),
                                            dict(title="Plot of Temperature versus Time",
                                                 yaxis=dict(title='temperature (degree)',
                                                            range=yrange1))]
                                      ),
                                 dict(label='Sea Level vs Time',
                                      method='update',
                                      args=[dict(visible=[False, False, True, True]),
                                            dict(title="Plot of Sea Level versus Time",
                                                 yaxis=dict(title='sea level (m)',
                                                            range=yrange2))]
                                      )
                                 ]
                        ),
                   dict(type='buttons',  # set the three buttons on the right
                        showactive=False,  # not highlight the button
                        x=1.09,  # set the position of the button
                        y=0.8,
                        xanchor='right',
                        yanchor='top',
                        buttons=[dict(label='Analyze',  # show our animated regression line(s)
                                      method='animate',
                                      args=[frames[:split_point],
                                            dict(frame=dict(duration=20,
                                                            redraw=False),
                                                 transition=dict(duration=0))]
                                      ),
                                 dict(label='Predict',  # show predicted data for future time
                                      method='animate',
                                      args=[frames[split_point - 1:],
                                            dict(frame=dict(duration=8,
                                                            redraw=False),
                                                 transition=dict(duration=0))]
                                      ),
                                 dict(label='Clear',  # clear regression line(s) that has been generated
                                            method='animate',
                                            args=[frames[:1]]
                                      )
                                 ]
                        )
                   ]

    layout = go.Layout(title="Plots of Temperature/Sea Level versus Time",  # title
                       hovermode='x unified',  # the mode of hover interactions
                       updatemenus=updatemenus,
                       xaxis=dict(title='time (year)',  # the label of x-axis
                                  range=xrange),  # fix the range of x-axis
                       yaxis=dict(range=[-10, 10])  # fix the range of x-axis
                       )
    return layout
