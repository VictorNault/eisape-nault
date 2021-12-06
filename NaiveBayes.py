"""
This script takes the necessary steps to turn an instance of class Partition,
which contains training data, into a Naive Bayes Algorithm. The classify method
within the class can be used to predict what class label a dictionary of
feature values likely has, based on the training data fed into the algorithm
upon the creation of the class. Completely general - can be used with any
features or class labels as long as the training and test partitions are in the
correct formats.
Author: Victor Nault
Date: 10/21/21
"""

from math import log
from copy import deepcopy

class NaiveBayes:

    def __init__(self, partition):
        """
        Creates all the instance variables necessary to classify a test
        partition using a Naive Bayes algorithm.
        Parameter: An instance of class Partition used to train the algorithm.
        """
        self.partition = partition
        self.num_classes = self.partition.K
        # Is a list of the total number of examples that have a given class
        # label in the partition
        self.num_class_instances_lst = \
        self.count_num_of_class_instances()
        # Is a list of dictionaries, of dictionaries. Each index in the list is
        # a class label. The first dictionary maps feature names to dictionaries
        # for each feature value. The second dictionary maps feature values to
        # the number of times they appear with the label that is the top
        # dictionary's index in the top list
        self.feature_vals_per_class_lst = \
        self.fill_feature_vals_per_class_lst()
        # Is a list of dictionaries, of dictionaries. Each index in the list is
        # a class label. The first dictionary maps feature names to dictionaries
        # for each feature value. The second dictionary maps feature values to
        # their theta for the class label that is the top dictionary's index in
        # the top list
        self.thetas_dict_of_feature_dicts = self.compute_thetas()
        # Is a list. Each element is the natural log of the prior probability
        # of the class label that is the index of the element
        self.log_prior_probs = self.compute_log_prior_probs()

    """
    Computes the prior probabilities of any example having each class label.
    Then it takes the natural log of this.
    Returns: A list of the logs of the prior probabilities for each class
    label. The index of the element is the class label it corresponds to.
    """
    def compute_log_prior_probs(self):
        log_prior_probs = []
        for i in self.num_class_instances_lst:
            log_prior_probs.append(log((i + 1) / (self.partition.n +
            self.num_classes)))
        return log_prior_probs

    """
    Computes the thetas for each feature value for each class label. These
    estimate the probability of a feature having a given value given that the
    class label is a given value.
    Returns: A list of dictionaries of dictionaries. Each index in the list is
    a class label. Each key in the first dictionary is a feature name. It
    corresponds to a dictionary where each key is a feature value. These keys
    correspond to the theta for the feature value and the class label.
    """
    def compute_thetas(self):
        theta_for_each_class_feature_val_lst = \
        self.initialize_feature_vals_per_class_lst()
        for k in range(self.num_classes):
            for i in self.partition.F:
                for j in self.partition.F[i]:
                    # + 1 to the numerator and + number of possible values for
                    # the feature to the denominator are the LaPlace values.
                    # these prevent the result being 0, which would cause an
                    # error when the log is taken, but do not affect the
                    # accuracy of the prediction
                    theta_for_each_class_feature_val_lst[k][i][j] = \
                    log((self.feature_vals_per_class_lst[k][i][j] + 1) / \
                    (self.num_class_instances_lst[k] + \
                    len(self.partition.F[i])))
        return theta_for_each_class_feature_val_lst

    """
    Counts the number of times each example in the training partition has each
    class label.
    Returns: A list of integers. Each element is the count for the class label
    equal to its index.
    """
    def count_num_of_class_instances(self):
        class_instances_list = [0] * self.num_classes
        for i in self.partition.data:
            class_instances_list[i.label] += 1
        return class_instances_list

    """
    Creates a dictionary of dictionaries. Each key in the first
    dictionary is a feature, it corresponds to a dictionary where each key is a
    feature value. The feature values all correspond to a 0.
    Returns: A list of dictionaries of dictionaries, ultimately filled with
    zeroes
    """
    def initialize_dict_of_feature_dicts(self):
        double_dict_of_features = {}
        for j in self.partition.F:
            dict_of_feature_vals_for_feature = {}
            for k in self.partition.F[j]:
                dict_of_feature_vals_for_feature[k] = 0
            double_dict_of_features[j] = dict_of_feature_vals_for_feature
        return double_dict_of_features

    """
    Creates a list of dictionaries of dictionaries. Each key in the first
    dictionary is a feature, it corresponds to a dictionary where each key is a
    feature value. The feature values, at this point, all correspond to 0.
    The index of the first dictionary in the top list is the class label it
    is for.
    Returns: A list of dictionaries of dictionaries.
    """
    def initialize_feature_vals_per_class_lst(self):
        feature_vals_per_class_lst = [None] * self.num_classes
        dict_of_feature_dicts = self.initialize_dict_of_feature_dicts()
        for i in range(self.num_classes):
            # Deepcopy so each class has its own double dictionary
            feature_vals_per_class_lst[i] = deepcopy(dict_of_feature_dicts)
        # My therapist: Python list of double dictionaries isn't real, Python
        # list of double dictionaries can't hurt you
        # Python list of double dictionaries:
        return feature_vals_per_class_lst

    """
    Loops through the training data and counts each feature value for the class
    label of the row.
    Returns: A list of dictionaries of dictionaries. Each index in the list is
    a class label. Each key in the first dictionary is a feature name. It
    corresponds to a dictionary where each key is a feature value. These keys
    correspond to the number of times that feature value is in a row with the
    class label that is the index of the top list.
    """
    def fill_feature_vals_per_class_lst(self):
        feature_vals_per_class_lst = \
        self.initialize_feature_vals_per_class_lst()
        for i in self.partition.data:
            for j in i.features:
                feature_vals_per_class_lst[i.label][j][i.features[j]] += 1
        return feature_vals_per_class_lst

    """
    For a given class label and dictionary of features, computes the product of
    the natural logs of all of the thetas for that class and each feature in
    the dictionary
    Parameters: class_label - An integer corresponding to one of the classes
                              to be predicted
                features - A dictionary, where each key is a feature that
                           corresponds to one feature value
    Returns: The product of every theta log for each feature value + the class
             label
    """
    def compute_product_of_theta_logs(self, class_label, features):
        product_of_theta_logs = 0
        for i in features:
            # This is addition because the natural log of everything has been
            # taken, so the product of all the thetas becomes the sum of all
            # the theta logs
            product_of_theta_logs += \
            self.thetas_dict_of_feature_dicts[class_label][i][features[i]]
        return product_of_theta_logs

    def classify(self, x_test):
        """
        Classifies a given set of feature values to have a class label. This is
        done by multiplying (the log of) the prior likelyhood of any example
        having a class label by (the log of) the product of all of the theta
        values for each of the feature values for the class label. After a
        posterior is calculated for each class label, the one with the greatest
        value is used to indicate that the set of features likely have that
        class label.
        Parameter: A dictionary of feature values
        Returns: An integer, representing the likeliest class label for the
                 input features.
        """
        posteriors_list = []
        for k in range(self.num_classes):
            this_theta_product = self.compute_product_of_theta_logs(k, x_test)
            # This is addition because the natural log of everything has been
            # taken, so all multiplications become addition
            posteriors_list.append(self.log_prior_probs[k] + this_theta_product)
        likeliest_class_label = 0
        prior_likeliest_posterior = -float('inf')
        for k in range(self.num_classes):
            if (posteriors_list[k] > prior_likeliest_posterior):
                likeliest_class_label = k
                prior_likeliest_posterior = posteriors_list[k]
        return likeliest_class_label
