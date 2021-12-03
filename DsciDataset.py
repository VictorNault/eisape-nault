# hello

import numpy
import csv
import matplotlib.pyplot as pyplot

class DsciDataset:

    def __init__(self, input_dsci_list, input_boundary_week, region_name):
        self.real_dsci_list = input_dsci_list
        self.boundary_week = input_boundary_week
        self.region_name = region_name
        self.train_dsci_list = self.real_dsci_list[:self.boundary_week]
        self.test_dsci_list = self.real_dsci_list[self.boundary_week:]
        self.pred_dsci_list = self.create_lin_pred_dsci_list(self.train_dsci_list)
        self.full_pred_dsci_list = self.create_lin_pred_dsci_list(self.real_dsci_list)

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
        pyplot.title(f"Real DSCI Over Time for {self.region_name} Overlayed " +
        f"by Predicted DSCI Based on data before Week {self.boundary_week}")
        pyplot.xlabel("Weeks since January 2nd, 2000")
        pyplot.ylabel("DSCI")
        pyplot.plot(self.real_dsci_list)
        pyplot.plot(self.pred_dsci_list)
        pyplot.plot(self.full_pred_dsci_list)
        pyplot.legend(["Real DSCI Data", "Predicted DSCI from Data Before Cutoff", "Predicted DSCI from All Data"])
        # Creates an infinitely long straight line at x = boundary_week
        pyplot.axline((self.boundary_week, 0), (self.boundary_week, 1), \
        color="black")
        pyplot.show()

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
