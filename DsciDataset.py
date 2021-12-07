
# hello

import numpy
import csv
import matplotlib.pyplot as pyplot

class DsciDataset:

    def __init__(self, input_dsci_list, input_boundary_week, region_name):
        self.real_dsci_list = input_dsci_list
        self.region_name = region_name
        self.boundary_week = input_boundary_week
        self.train_dsci_list = self.real_dsci_list[:self.boundary_week]
        self.test_dsci_list = self.real_dsci_list[self.boundary_week:]
        self.train_data_pred_dsci_list  = self.create_lin_pred_dsci_list(self.train_dsci_list)
        self.full_data_pred_dsci_list = self.create_lin_pred_dsci_list(self.real_dsci_list)
        self.train_data_pred_dsci_list_after_boundary_week = self.train_data_pred_dsci_list[self.boundary_week:]
        self.full_data_pred_dsci_list_after_boundary_week = self.full_data_pred_dsci_list[self.boundary_week:]

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
        self.create_prediction_plot()
        pyplot.show()
        # pyplot.show() automatically clears the graph. No pyplot.clf needed!

    def export_prediction_plot(self):
        self.create_prediction_plot()
        pyplot.savefig(self.region_name + ".pdf", format="pdf")
        pyplot.clf()

    def create_prediction_plot(self):
        pyplot.title(f"Real DSCI Over Time for {self.region_name} Overlayed " +
        f"by Predicted DSCI Based on Data before Week {self.boundary_week}")
        pyplot.xlabel("Weeks since January 2nd, 2000")
        pyplot.ylabel("DSCI")
        pyplot.plot(self.real_dsci_list)
        pyplot.plot(self.train_data_pred_dsci_list )
        pyplot.plot(self.full_pred_dsci_list)
        pyplot.legend(["Real DSCI Data", "Predicted DSCI from Data Before Cutoff", "Predicted DSCI from All Data"])
        # Creates an infinitely long straight line at x = boundary_week
        pyplot.axline((self.boundary_week, 0), (self.boundary_week, 1), \
        color="black")

    # Not how RSS works. Whoops!
    """
    def show_rss_plot(self, dsci_list1, dsci_list2, dsci_list1_name_str, dsci_list2_name_str):
        self.create_rss_plot(dsci_list1, dsci_list2, dsci_list1_name_str, dsci_list2_name_str)
        pyplot.show()
        # pyplot.show() automatically clears the graph. No pyplot.clf needed!

    def export_rss_plot(self, dsci_list1, dsci_list2, dsci_list1_name_str, dsci_list2_name_str):
        self.create_rss_plot(dsci_list1, dsci_list2, dsci_list1_name_str, dsci_list2_name_str)
        pyplot.savefig()
        pyplot.clf()

    def create_rss_plot(self, dsci_list1, dsci_list2, dsci_list1_name_str, dsci_list2_name_str):
        pyplot.title(f"RSS Over Time for {self.region_name} between " +
        f"{dsci_list1_name_str} and {dsci_list2_name_str}")
        pyplot.xlabel("Weeks since January 2nd, 2000")
        pyplot.ylabel(f"RSS between {dsci_list1_name_str} and {dsci_list2_name_str}")
        pyplot.plot(self.calc_rss(dsci_list1, dsci_list2))

    def repartition(self, new_boundary_week):
        self.boundary_week = input_boundary_week
        self.region_name = region_name
        self.train_dsci_list = self.real_dsci_list[:self.boundary_week]
        self.test_dsci_list = self.real_dsci_list[self.boundary_week:]
        self.train_data_pred_dsci_list  = self.create_lin_pred_dsci_list(self.train_dsci_list)
        self.full_data_pred_dsci_list = self.create_lin_pred_dsci_list(self.real_dsci_list)
    """

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
