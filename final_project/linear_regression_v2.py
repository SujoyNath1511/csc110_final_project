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

This file is Copyright (c) 2020 Sujoy Deb Nath.
"""
from typing import List, Tuple, Optional


def correlation(x_val: List[float], y_val: List[float]) -> float:
    """
    Returns the float value for the correlation between the predictor (x)
    and the response (y) variable.

    Preconditions:
        - len(x_val) == len(y_val)
        - len(x_val) != 0
        - len(y_val) != 0
    """
    x_avg = sum(x_val) / len(x_val)
    y_avg = sum(y_val) / len(y_val)

    numerator = sum((x_val[i] - x_avg) * (y_val[i] - y_avg) for i in range(0, len(x_val)))
    denominator = sum((x_i - x_avg) ** 2 for x_i in x_val) * \
                  sum((y_i - y_avg) ** 2 for y_i in y_val)

    return numerator / (denominator ** 0.5)


def one_pred_reg_cofficients(x_val: List[float], y_val: List[float]) -> Tuple[float, float]:
    """
    Returns the slope coefficients and intercept for the simple linear regression formula.
    The first value in the tuple is the intercept parameter and the second is the slope parameter.

    Preconditions:
        - len(x_val) == len(y_val)
        - len(x_val) != 0
        - len(y_val) != 0
    """
    x_avg = sum(x_val) / len(x_val)
    y_avg = sum(y_val) / len(y_val)
    beta_1 = estimate_slope(x_val, y_val, y_avg, x_avg)
    beta_0 = estimate_intercept(y_avg, beta_1, x_avg)

    return (beta_0, beta_1)


def forecast_regression(est_inter: float, est_slope: float, starting_x: int,
                        end_time: int) -> List[float]:
    """Return a list of predicted y values based on the linear regression model and x values
    outside of the range of data. The x values are greater than the x values in the data.

    Preconditions:
        - end_time >= starting_x
        - len(x_val) != 0
    """
    return [est_inter + est_slope * x for x in range(starting_x, end_time + 1)]


def estimate_intercept(y_avg: float, beta_1: float, x_avg: float) -> float:
    """Returns the intercept parameter for simple linear regression
    """
    return y_avg - beta_1 * x_avg


def estimate_slope(x_val: List[float], y_val: List[float], y_avg: float, x_avg: float) -> float:
    """Returns the slope parameter for simple linear regression.

    Preconditions:
        - len(x_val) == len(y_val)
        - len(x_val) != 0
        - len(y_val) != 0
        - all((x_i - x_avg) ** 2 != 0 for x_i in x_val)
    """
    numerator = sum((x_val[i] - x_avg) * (y_val[i] - y_avg) for i in range(0, len(x_val)))
    denominator = sum((x_i - x_avg) ** 2 for x_i in x_val)

    return numerator / denominator


def calculate_rmse(actual_y_val: List[float], predicted_y_val: List[float]) -> float:
    """Return the Root Mean Squared Error for the predictions made by the regression
    model.

    Preconditions:
        - len(predicted_y_val) != 0
        - len(actual_y_val) != 0
        - len(actual_y_val) == len(predicted_y_val)
    """
    n = len(actual_y_val)
    mean_squared_error = sum((actual_y_val[i] - predicted_y_val[i]) ** 2 for i in range(0, n)) * \
                         (1 / n)
    return mean_squared_error ** 0.5


def one_predictor_linear_regression(predictor: List[float], response: List[float],
                                    forecast: Optional[bool] = False,
                                    forecast_end_time: Optional[int] = 0) -> \
        Tuple[List[float], List[int]]:
    """NEEDS CORRECTION ASAP!!!!!!!

    The first list is the list of y values created using the values in the predictor variable.

    The second list is the list of generated x values that correspond to the extrapolated
    y-values.

    Preconditions:
        - len(predictor) == len(response)
        - forecast_end_time >= 0
    """

    estimated_intercept, estimated_slope = one_pred_reg_cofficients(predictor, response)

    predicted_forecast_vals = []
    forecast_x_vals = []
    if forecast:
        starting_x = round(max(predictor))
        predicted_forecast_vals = forecast_regression(estimated_intercept, estimated_slope,
                                               starting_x, forecast_end_time)

        forecast_x_vals = predictor + [x for x in range(starting_x, forecast_end_time + 1)]

    return ([estimated_intercept + estimated_slope * x for x in predictor] + predicted_forecast_vals,
            forecast_x_vals)
