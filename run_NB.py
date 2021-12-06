"""
CS260 Lab 4: This script reads in the data from two csv files - one for
training, another for testing, that have column headers, with one of the
headers being 'sex' and the only values in the column being 'Male' and
'Female'. It converts this data into two 'Partition' classes - one for the
training data and another for the testing data. It then uses the training data
to train a Naive Bayes algorithm, which attempts to map the likelyhoods of
a row having a given sex feature value given its other feature values. Finally
it uses the algorithm it just trained to classify the test data, checks the
predicted values to the actual values, and prints out the corresponding
confusion matrix and accuracy.
Author: Victor Nault
Date: 10/21/21
"""

# Below is the command to run the script from the console
# python3 run_NB.py -r data/1994_census_cleaned_train.csv -e data/1994_census_cleaned_test.csv

from NaiveBayes import NaiveBayes
import optparse
import sys
from collections import OrderedDict
import csv

################################################################################
# CLASSES
################################################################################

class Example:

    def __init__(self, features, label):
        """Helper class (like a struct) that stores info about each example."""
        # dictionary. key=feature name: value=feature value for this example
        self.features = features
        self.label = label # in {0, 1}

class Partition:

    def __init__(self, data, F, K):
        """Store information about a dataset"""
        # list of Examples
        self.data = data
        self.n = len(self.data)

        # dictionary. key=feature name: value=list of possible values
        self.F = F

        # number of classes
        self.K = K

################################################################################
# MAIN
################################################################################

def main():
    """
    Uses helper functions to parse the command line arguments and read in the
    corresponding csv files, makes a NaiveBayes class with the training data,
    then calls a helper function to make a confusion matrix and accuracy for
    the testing data set using the model it just made.
    """
    for i in range(0, 20):
        train_partition = read_csv("train_nb_" + str(i) + ".csv")
        test_partition = read_csv("test_nb_" + str(i) + ".csv")
        #print(train_partition.data)
        #print(train_partition.n)
        #print(train_partition.F)
        #print(train_partition.K)
        nb_model = NaiveBayes(train_partition)
        print_confusion_matrix(test_partition, nb_model)


################################################################################
# HELPER FUNCTIONS
################################################################################

"""
Calculates the information for a confusion matrix (the amount of examples
classified correctly and incorrectly for each class) and the accuracy of the
model. Then prints both a confusion matrix and the accuracy.
Parameters: partition - An instance of the Partition class with testing data
            NaiveBayes - An instance of the NaiveBayes class
"""
def print_confusion_matrix(partition, NaiveBayes):
    true_not_low_income = 0
    true_low_income = 0
    false_not_low_income = 0
    false_low_income = 0
    for i in partition.data:
        if (i.label == 0):
            # Model predicts male, is actually male
            if (NaiveBayes.classify(i.features) == 0):
                true_not_low_income += 1
            # Model predicts female, is actually male
            if (NaiveBayes.classify(i.features) == 1):
                false_low_income += 1
        if (i.label == 1):
            # Model predicts male, is actually female
            if (NaiveBayes.classify(i.features) == 0):
                false_not_low_income += 1
            # Model predicts female, is actually female
            if (NaiveBayes.classify(i.features) == 1):
                true_low_income += 1
    num_correct_preds = true_not_low_income + true_low_income
    print("\n")
    print("\tPrediction")
    print("\tNot Low Income\tLow Income\n")
    print("  Not Low Income\t", true_not_low_income, "\t", false_not_low_income)
    print("Low Income\t", false_low_income, "\t", true_low_income)
    # Accuracy = correctly predicted examples / all examples
    print("\nAccuracy:", num_correct_preds / partition.n, " (",
    num_correct_preds, " out of ", partition.n, " correct )")

def read_csv(filename):
    """
    Uses csv reader to import csv data, then goes through each row in the given
    csv file. If it's at the 1st (header) row, it creates a list with each
    header to use as features, except the 'sex' column, since it's the class.
    Afterwards it creates an instance of the Example class to hold the features
    and class for each row, and if it finds a feature value that is not already
    mapped to a feature, it does so.
    Parameter: String that is the path to a csv file
    Output: The data in the csv file, in the form of an instance of the
    Partition class
    """
    input_data = csv.reader(open(filename, 'r'), delimiter=',')
    # F maps the feature names to a list of all the possible values for that
    # feature
    F = OrderedDict()
    lst_of_features = []
    data = []
    num_of_class_features = 2
    class_index = None
    passed_first_row = False
    for row in input_data:
        # If it's the header row
        if (passed_first_row == False):
            passed_first_row = True
            # Start at -1 so when it increments at the start of the first loop
            # it's at index 0
            element_index = -1
            for element in row:
                element_index += 1
                # Single out the class index so it isn't included in the
                # features used to calculate the probability of the class
                if (element == "Income"):
                    class_index = element_index
                else:
                    lst_of_features.append(element)
                    F[element] = []
        else:
            # Start at -1 so when it increments at the start of the first loop
            # it's at index 0 (again)
            element_index = -1
            row_label = None
            row_features = {}
            past_class_index = False
            for element in row:
                element_index += 1
                ################################################################
                # Between these lines: for loop code for creating Examples
                if (element_index == class_index):
                    past_class_index = True
                    if (element == 'Not low income'):
                        row_label = 0
                    if (element == 'Low income'):
                        row_label = 1
                else:
                    if (past_class_index == False):
                        row_features[lst_of_features[element_index]] = element
                        ########################################################
                        # Between these lines: for loop code for adding feature
                        # values to dictionary of features
                        element_present = False
                        for i in F[lst_of_features[element_index]]:
                            if (i == element):
                                element_present = True
                                break
                        if (element_present == False):
                            F[lst_of_features[element_index]].append(element)
                        ########################################################
                    else:
                        row_features[lst_of_features[element_index-1]] = element
                        ########################################################
                        # Between these lines: for loop code for adding feature
                        # values to dictionary of features
                        element_present = False
                        # Here the element index is decremented by one because
                        # each row has a class column that is skipped over,
                        # so the index of the following columns in the list of
                        # features is one less than its place in the row
                        for i in F[lst_of_features[element_index-1]]:
                            if (i == element):
                                element_present = True
                                break
                        if (element_present == False):
                                F[lst_of_features[element_index-1]].append(\
                                element)
                        ########################################################
            data.append(Example(row_features, row_label))
    return Partition(data, F, num_of_class_features)

if __name__ == "__main__":
    main()
