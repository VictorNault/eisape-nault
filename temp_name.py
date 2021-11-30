# hello

import numpy
import csv
import pandas
import matplotlib.pyplot as pyplot

def main():
    drought_data_frame = read_in_data()
    de_test = process_data(drought_data_frame)
    create_county_plot(de_test["Kent County"])
    create_county_plot(de_test["Sussex County"])
    create_county_plot(de_test["New Castle County"])


def read_in_data():
    return pandas.read_csv("county_drought_data_2000-2021_dsci.csv", header=0)


def process_data(input_df):
    de_data_frame = input_df[input_df["State"].isin(["DE"])]
    #print(de_data_frame)

    de_county_data_frame = (de_data_frame["County"])
    de_county_df_no_dupes = de_county_data_frame.drop_duplicates()
    #print(de_county_df_no_dupes)

    de_county_dict = {}
    for county in de_county_df_no_dupes:
        de_county_dict[county]= de_data_frame[de_data_frame["County"].isin([county])]
    #print(de_county_dict)\

    return de_county_dict


def create_county_plot(county_data_frame):
    dsci_by_week = len(county_data_frame) * [0]
    reverse_counter = len(county_data_frame)
    #print(county_data_frame)

    for i in range(len((county_data_frame))):
        dsci_by_week[reverse_counter - i - 1] = county_data_frame["DSCI"].iloc[i]
        #print(county_data_frame[reverse_counter - i - 1])
    #print(dsci_by_week)
    create_linear_prediction_plot(dsci_by_week, int(len(dsci_by_week) / 2))
    #pyplot.plot(dsci_by_week)
    #pyplot.show()

def create_linear_prediction_plot(dsci_list, week_boundary):
    """
    Creates a plot of the actual dsci data, as well as a linear approximation
    of the dsci data BEFORE the week boundary, but extended to encompass
    every week in the full dsci data.
    Parameters: dsci_list - A list of every dsci in the data per week. The
                index of the dsci is the week it's for.
                week_boundary - The week at which to separate the dsci list
                into testing and training data.
    """
    train_dsci_list = dsci_list[:week_boundary]
    test_dsci_list = dsci_list[week_boundary:]
    dsci_X = numpy.array(range(len(train_dsci_list)))
    dsci_X_with_ones = add_ones_column_to_axis_0(dsci_X)
    predicted_dsci_weights = fit(dsci_X_with_ones, train_dsci_list)
    predicted_dsci = []
    # For a linear model: y-hat at every x is equal to w0 + (w1 * x)
    for i in range(len(dsci_list)):
        predicted_dsci.append(predicted_dsci_weights[0] + \
        (i * predicted_dsci_weights[1]))
    pyplot.plot(dsci_list)
    pyplot.plot(predicted_dsci)
    # Creates an infinitely long straight line at x = week_boundary
    pyplot.axline((week_boundary, 0), (week_boundary, 1), color="black")
    pyplot.show()


def fit(X, y) :
    """
    Uses the closed-form solution to linear regression to compute weights for a
    model.
    Parameters: X - a matrix of all the features of a data set, y - a vector /
    single column matrix of the responses / outputs of a data set
    Returns: A weight vector, representing a linear model.
    """

    """
    This is the below code written much more understandably and slightly less
    memory-efficently (I think):

    variance_of_X_inverted = numpy.matmul(X.transpose(), X)
    variance_of_X = numpy.linalg.inv(variance_of_X_inverted)
    covariance_of_X_and_y = numpy.matmul(X.transpose(), y)
    weights_vector = numpy.matmul(variance_of_X, covariance_of_X_and_y)
    return weights_vector

    NOTE: In the code variance_of_X is directly multiplied by X.transpose(),
    which is subsequently multipled by y. If it's done as in the descriptive
    way, the result should be the exact same.
    """

    # All hail the line
    return numpy.matmul(numpy.matmul(numpy.linalg.inv( \
    (numpy.matmul(X.transpose(), X))), X.transpose()), y)

def add_ones_column_to_axis_0(input_array):
    """
    Concatenates a column consisting solely of ones to the front of a matrix.
    Parameter: A numpy array
    Returns: The input numpy array, but modified as described
    """
    if (input_array.ndim == 1):
        midput_array = numpy.expand_dims(input_array, axis=1)
    else:
        midput_array = input_array
    output_array = numpy.concatenate(((numpy.ones((midput_array.shape[0], 1)), \
    midput_array)), axis=1)
    return output_array

if __name__ == "__main__":
    main()
