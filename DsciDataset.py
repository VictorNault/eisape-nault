"""
Authors: Seun Eisape & Victor Nault
Description: This file contains the DsciDataset class. Created using a list of
DSCI per week for a region, a week to divide the list between, and the name of
the region, it contains class variables for all of these things, as well as
derived data. It also contains functions that can show a graph of the linear
prediction for the first part of the data alongside the linear prediction for
the full data, export this same graph to the figures folder as a .pdf file,
return the RSS for the two linear predictions, and return the difference
between the average value of the two linear predictions.
Date: 12/17/21
"""

import numpy
import csv
import matplotlib.pyplot as pyplot

class DsciDataset:

    def __init__(self, input_dsci_list, input_boundary_week, region_name):
        self.real_dsci_list = input_dsci_list
        self.region_name = region_name
        self.boundary_week = input_boundary_week
        self.train_dsci_list = self.real_dsci_list[:self.boundary_week]
        # Below is never actually used in class functions, but could be helpful
        # for external functions
        self.test_dsci_list = self.real_dsci_list[self.boundary_week:]
        self.train_data_pred_dsci_list  = \
        self.create_lin_pred_dsci_list(self.train_dsci_list)
        self.full_data_pred_dsci_list = \
        self.create_lin_pred_dsci_list(self.real_dsci_list)
        self.train_data_after_boundary = \
        self.train_data_pred_dsci_list[self.boundary_week:]
        self.full_data_pred_dsci_list_after_boundary_week = \
        self.full_data_pred_dsci_list[self.boundary_week:]

    def create_lin_pred_dsci_list(self, dsci_list):
        """
        Creates a plot of the actual dsci data, as well as a linear
        approximation of the dsci data BEFORE the week boundary, but extended
        to encompass every week in the full dsci data.
        Parameters: dsci_list - A list of every dsci in the data per week. The
                    index of the dsci is the week it's for.
                    week_boundary - The week at which to separate the dsci list
                    into testing and training data.
        """
        dsci_X = numpy.array(range(len(dsci_list)))
        dsci_X_with_ones = self.add_ones_column_to_axis_0(dsci_X)
        predicted_dsci_weights = self.fit(dsci_X_with_ones, dsci_list)
        predicted_dsci = []
        # For a linear model: y-hat at every x is equal to w0 + (w1 * x)
        for i in range(len(self.real_dsci_list)):
            predicted_dsci.append(predicted_dsci_weights[0] + \
            (i * predicted_dsci_weights[1]))
        return predicted_dsci

    def show_prediction_plot(self):
        """
        Exports the plot of both linear predictions, alongside the actual data,
        to a .pdf file in the figures folder.
        """
        self.create_prediction_plot()
        pyplot.show()
        # pyplot.show() automatically clears the graph. No pyplot.clf needed!

    def export_prediction_plot(self):
        """
        Shows the plot of both linear predictions, alongside the actual data, in
        a separate window.
        """
        self.create_prediction_plot()
        pyplot.savefig(self.region_name + ".pdf", format="pdf")
        pyplot.clf()

    def create_prediction_plot(self):
        """
        Creates a plot of the two linear predictions, one for the first part of
        the data, one for the full data, with appropriate labels and a legend.
        """
        pyplot.title(f"Real DSCI Over Time for {self.region_name} Overlayed " +
        f"by Predicted DSCI Based on Data before Week {self.boundary_week}", \
        fontsize = "small")
        pyplot.xlabel("Weeks since January 2nd, 2000")
        pyplot.ylabel("DSCI")
        pyplot.plot(self.real_dsci_list)
        pyplot.plot(self.train_data_pred_dsci_list )
        pyplot.plot(self.full_data_pred_dsci_list)
        pyplot.legend(["Real DSCI Data", \
        "Predicted DSCI from Data Before Cutoff", \
        "Predicted DSCI from All Data"])
        # Creates an infinitely long straight line at x = boundary_week
        pyplot.axline((self.boundary_week, 0), (self.boundary_week, 1), \
        color="black")

    def fit(self, X, y) :
        """
        Uses the closed-form solution to linear regression to compute weights
        for a model.
        Parameters: X - a matrix of all the features of a data set, y - a
        vector / single column matrix of the responses / outputs of a data set
        Returns: A weight vector, representing a linear model.
        """

        """
        This is the below code written much more understandably and slightly
        less memory-efficently (I think):
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

    def add_ones_column_to_axis_0(self, input_array):
        """
        Concatenates a column consisting solely of ones to the front of a
        matrix.
        Parameter: A numpy array
        Returns: The input numpy array, but modified as described
        """
        if (input_array.ndim == 1):
            midput_array = numpy.expand_dims(input_array, axis=1)
        else:
            midput_array = input_array
        output_array = numpy.concatenate(((numpy.ones( \
        (midput_array.shape[0], 1)), midput_array)), axis=1)
        return output_array

    def calc_rss(self, array1, array2):
        """
        Calculates the reduced sum of squares for a given set of features, outputs,
        and weights. The RSS is, more verbosely, the sum of the differences of each
        predicted y value and the real y value, squared and halved.
        Parameters: X - A matrix of feature values
        y - A vector of predetermined output values
        w - Weights to multiply X by to get predicted y-values
        """

        """
        Below is the code of this function written more understandably, but to my
        knowledge slightly less efficently
        predicted_y_vals = predict(X, w)
        difference_between_predicted_and_real_output = numpy.subtract( \
        predicted_y_vals, y)
        reduced_sum_of_squares = 0.5 * (numpy.sum( \
        difference_between_predicted_and_real_output)**2)
        return reduced_sum_of_squares
        """
        return (0.5 * numpy.sum((numpy.subtract(array1, array2))**2))

    def calc_diff_of_list_avgs(self, list1, list2):
        """
        Finds the average values for two lists consisting of numerical values.
        Then, returns the difference between the average of the first list and
        the average of the second list.
        Parameters: list1 - The first list to be averaged, and the minuend of
                    the return value
                    list2 - The second list to be averaged, and the subtrahend
                    of the return value
        Returns:    The difference between the average of the first list and
                    the average of the second list
        """
        counter1 = 0
        list1_avg = 0
        for i in list1:
            list1_avg += i
            counter1 += 1
        list1_avg = list1_avg / counter1
        counter2 = 0
        list2_avg = 0
        for i in list2:
            list2_avg += i
            counter2 += 1
        list2_avg = list2_avg / counter2
        return list1_avg - list2_avg
