"""
Authors: Victor Nault and Seun Eisape
Description: This script takes in a .csv of discretized DSCI and median income
data per county. It then shuffles the data, splits it in half, and exports both,
one being the training partition for naive bayes, and one being the testing
partition. It then does this 20 more times.
Date: 12/17/21
"""

import csv
import random

def main():
    """
    This function reads in the .csv file of discretized data, turns them into
    lists, then shuffles, splits, and exports them 20 times.
    """

    input_data = csv.reader(open("NB_Data/naive_bayes.csv", 'r'), delimiter=',')
    list_of_rows, header_list = read_in_csv_to_list(input_data)
    for i in range(0, 20):
        create_new_partition_csvs(list_of_rows, "NB_Data/train_nb_" + str(i) \
        + ".csv", "NB_Data/test_nb_" + str(i) + ".csv", header_list)

def read_in_csv_to_list(input_data):
    """
    This function reads in a csv file into two separate lists, one with the
    rows and one with the headers.
    Parameter:  A csv file that has been opened by csv.reader
    Returns:    A list of all of the rows, a list of all of the headers
    """

    list_of_rows = []
    passed_first_row = False
    header_list = None
    for row in input_data:
        if (passed_first_row == False):
            header_list = row
            passed_first_row = True
        else:
            list_of_rows.append(row)
    return list_of_rows, header_list


def create_new_partition_csvs(input_list, csv_name1, csv_name2, header_list):
    """
    This function shuffles a given list in place, then divides it in half and
    creates new .csv files for both halves.
    Parameters: input_list - A list
                csv_name1 - A string value to use as the first csv file name.
                Include .csv file ending
                csv_name1 - A string value to use as the second csv file name.
                Include .csv file ending
                header_list - A list of column headers to use for both csv files
    """

    shuffle_in_place(input_list)
    #print(list_of_rows)
    list_midpoint = int(len(input_list) / 2)
    list1 = input_list[:list_midpoint]
    list2 = input_list[list_midpoint:]
    create_csv(list1, csv_name1, header_list)
    create_csv(list2, csv_name2, header_list)

def create_csv(input_list, csv_name, headers):
    """
    This function exports a list of csv rows and a list of csv headers to a new
    csv file.
    Parameters: input_list - A list of csv rows
                csv_name - A string value to use as the name of the file,
                include .csv file ending
                headers - A list of strings to use as the column headers
    """

    #print(input_list)
    with open(csv_name, "w", newline="") as new_csv:
        writer = csv.writer(new_csv)
        writer.writerow(headers)
        for element in input_list:
            writer.writerow(element)

def shuffle_in_place(lst):
    '''
    Shuffles a list in place by taking the initial list length, randomly
    choosing an index within the range of the list, and removing the element
    there and putting it at the end of the list, decreasing the index of every
    other element by one (except the one that was just swapped). This iterates
    until every element has been moved, although the range of the index that
    can be chosen decreases by one every iteration, so the already moved
    elements are not disturbed.
    '''

    assert(type(lst) is list), """Error in shuffle_in_place(): Non-lists are not
valid input"""

    unswapped_list_length = len(lst)

    if (unswapped_list_length > 0):
        index_to_swap = random.randrange(0, unswapped_list_length)

    while (unswapped_list_length > 0):
        random_element = lst.pop(index_to_swap)
        lst.append(random_element)
        unswapped_list_length -= 1
        try:
            index_to_swap = random.randrange(0, unswapped_list_length)
        except:
            pass

if __name__ == "__main__":
    main()
