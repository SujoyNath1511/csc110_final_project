"""CSC110 Fall 2020 Final Project, Computational Model: Linear Regression

This module contains the functions required to perform Linear Regression on
one predictor, including calculating the correlation and RMSE values for the
models.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited.

This file is Copyright (c) 2020 Sujoy Deb Nath, Yunjia Guo, Benjamin Lee and Mohamed Abdullahi.
"""
from typing import List, Tuple, Optional


def correlation(x_val: List[float], y_val: List[float]) -> float:
    """
    Returns the float value for the correlation between the predictor (x)
    and the response (y) variable. The correlation is the strength of the
    association between the two variables.

    correlation > 0: Positive association (are proportional)
    correlation < 0: Negative association (are inversely proportional)

    The domain of the correlation values is between -1 to 1, the closer the
    value is to 1 or -1, the more linear the association. A correlation value
    of 1 or -1  indicates a perfect linear relationship.

    Preconditions:
        - len(x_val) == len(y_val)
        - len(x_val) != 0
        - len(y_val) != 0

    >>> lst = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    >>> lst2 = lst
    >>> correlation(lst, lst2)
    1.0

    >>> lst = [0, 1, 2, 3, 4, 5, 6, 8]
    >>> lst2 = [0, 1, 4, 9, 16, 25, 36, 64]
    >>> abs(correlation(lst, lst2) - 0.9543246) <= 0.0000001
    True
    """
    x_avg = sum(x_val) / len(x_val)
    y_avg = sum(y_val) / len(y_val)

    # sum((x_i - x_avg)(y_i - y_avg))
    numerator = sum((x_val[i] - x_avg) * (y_val[i] - y_avg) for i in range(0, len(x_val)))

    # sum((x_i - x_avg)^2) * sum((y_i - y_avg)^2)
    denominator = sum((x_i - x_avg) ** 2 for x_i in x_val) * sum((y_i - y_avg) ** 2
                                                                 for y_i in y_val)

    # The denominator has to be square rooted to get the proper value.
    return numerator / (denominator ** 0.5)


def one_pred_reg_cofficients(x_val: List[float], y_val: List[float]) -> Tuple[float, float]:
    """
    Returns the slope and intercept coefficients for the simple linear regression formula.
    The first value in the tuple is the intercept parameter and the second is the slope parameter.

    Preconditions:
        - len(x_val) == len(y_val)
        - len(x_val) != 0
        - len(y_val) != 0

    >>> x_coords = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    >>> y_coords = [x * 2 for x in x_coords]
    >>> one_pred_reg_cofficients(x_coords, y_coords)
    (0.0, 2.0)

    >>> x_coords = [x for x in range(0, 10)]
    >>> y_coords = [2 for _ in range(0, 10)]
    >>> one_pred_reg_cofficients(x_coords, y_coords)
    (2.0, 0.0)
    """
    x_avg = sum(x_val) / len(x_val)
    y_avg = sum(y_val) / len(y_val)
    beta_1 = estimate_slope(x_val, y_val, y_avg, x_avg)
    beta_0 = estimate_intercept(y_avg, beta_1, x_avg)

    return (beta_0, beta_1)


def forecast_regression(est_inter: float, est_slope: float, starting_x: int,
                        end_time: int) -> List[float]:
    """Return a list of y coordinates generated from the estimated y-intercept
    and the estimated slope given.

    The domain is starting_x + 1 <= x <= end_time.

    Preconditions:
        - end_time >= starting_x
        - len(x_val) != 0

    >>> lst = forecast_regression(2, 4, 10, 50)
    >>> lst2 = [2 + 4 * x for x in range(11, 51)]
    >>> lst == lst2
    True
    """
    return [est_inter + est_slope * x for x in range(starting_x + 1, end_time + 1)]


def estimate_intercept(y_avg: float, beta_1: float, x_avg: float) -> float:
    """Return the estimated y-intercept for the simple linear regression model.

    >>> x_values = [x for x in range(0, 10)]
    >>> y_values = [x * 2 + 4for x in range(0, 10)]
    >>> avg_y = sum(y_values) / len(y_values)
    >>> avg_x = sum(x_values)/ len(x_values)
    >>> estimate_intercept(avg_y, 2, avg_x)
    4.0
    """
    return y_avg - beta_1 * x_avg


def estimate_slope(x_val: List[float], y_val: List[float], y_avg: float, x_avg: float) -> float:
    """Return the estimated slope for the simple linear regression model.

    Preconditions:
        - len(x_val) == len(y_val)
        - len(x_val) != 0
        - len(y_val) != 0
        - all((x_i - x_avg) ** 2 != 0 for x_i in x_val)

    >>> x_values = [x for x in range(0, 10)]
    >>> y_values = [x * 2 for x in range(0, 10)]
    >>> y_avg = sum(y_values) / len(y_values)
    >>> x_avg = sum(x_values)/ len(x_values)
    >>> estimate_slope(x_values, y_values, y_avg, x_avg)
    2.0
    """
    # sum((x_i - x_avg)(y_i - y_avg))
    numerator = sum((x_val[i] - x_avg) * (y_val[i] - y_avg) for i in range(0, len(x_val)))

    # sum((x_i - x_avg)^2)
    denominator = sum((x_i - x_avg) ** 2 for x_i in x_val)

    return numerator / denominator


def calculate_rmse(actual_y_val: List[float], predicted_y_val: List[float]) -> float:
    """Return the Root Mean Squared Error for the predictions made by the regression
    model.

    The RMSE of regression model calculates the accuracy of the model by finding how
    close the predicted values are to the real values. The close the RMSE is to 0,
    the more accurate the model and it's predictions.

    Preconditions:
        - len(predicted_y_val) != 0
        - len(actual_y_val) != 0
        - len(actual_y_val) == len(predicted_y_val)

    >>> x_coords = [x for x in range(0, 10)]
    >>> y_coords = [x * 2 for x in x_coords]
    >>> predicted_y_coords, pred_x_coords = one_predictor_linear_regression(x_coords, y_coords)
    >>> calculate_rmse(y_coords, predicted_y_coords)
    0.0
    """
    n = len(actual_y_val)

    # 1/n * sum((y_i - y_hat_i)^2)
    mean_squared_error = sum((actual_y_val[i] - predicted_y_val[i]) ** 2
                             for i in range(0, n)) * (1 / n)

    # Since its ROOT mean squared error, we need to square root it.
    return mean_squared_error ** 0.5


def one_predictor_linear_regression(predictor: List[float], response: List[float],
                                    forecast: Optional[bool] = False,
                                    forecast_end_time: Optional[int] = None) -> \
        Tuple[List[float], List[int]]:
    """Returns a tuple of two lists, the first is predicted y-coordinates based on the regression
    model and the second list is a list of x-coordinates that were to used to create a forecast.

    Forecasting is a technique used to try and predict future values using current trends, and
    this function creates forecasted coordinates if forecast is True.

    If the forecast variable is false, the second list is empty as no forecast was generated. Then
    the returned list of predicted y-coordinates will be the same length as the predictor variable.

    If the forecast variable is true, then the second list has x-coordinates greater than the
    x-coordinates in the predictor list. The predicted y-coordinates extend beyond the range
    of the provided data.

    Preconditions:
        - len(predictor) == len(response)
        - len(predictor) != 0
        - len(response) != 0
        - forecast_end_time >= starting_x

    >>> x_coords = [x for x in range(0, 100)]
    >>> y_coords = [x * 5.0 for x in x_coords]
    >>> pred_coords = one_predictor_linear_regression(x_coords, y_coords)
    >>> pred_coords[0] == y_coords     # The second list is empty since forecast is False
    True

    >>> x_coords = [x for x in range(0, 100)]
    >>> y_coords = [x * 5.0 for x in x_coords]
    >>> pred_coords = one_predictor_linear_regression(x_coords, y_coords, True, 200)
    >>> expected_y_coords = [x * 5.0 for x in range(0, 201)]
    >>> pred_coords[0] == expected_y_coords
    True
    """

    # Get the regression coefficients.
    estimated_intercept, estimated_slope = one_pred_reg_cofficients(predictor, response)

    predicted_forecast_vals = []
    forecast_x_vals = []
    if forecast:                         # If forecast is true, then create forecasted coordinates.

        starting_x = round(max(predictor))

        # Create forecasted y-coordinates
        predicted_forecast_vals = forecast_regression(
            estimated_intercept, estimated_slope, starting_x, forecast_end_time)

        # Create forecasted x-coordinates
        forecast_x_vals = predictor + list(range(starting_x + 1, forecast_end_time + 1))

    # Return both the predicted y-coordinates and the forecasted x-coordinates, even if no
    # forecast was created.
    return ([estimated_intercept + estimated_slope * x
             for x in predictor] + predicted_forecast_vals, forecast_x_vals)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    from python_ta.contracts import check_all_contracts
    import python_ta
    check_all_contracts()
    python_ta.check_all(config={
        'extra-imports': ['typing', 'python_ta.contracts', 'python_ta', 'doctest'],
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })
