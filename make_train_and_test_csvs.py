"""
Authors:
Description:
Date:
"""

import csv
import random

def main():
    """
    This function
    """

    input_data = csv.reader(open("naive_bayes.csv", 'r'), delimiter=',')
    list_of_rows, header_list = read_in_csv_to_list(input_data)
    for i in range(0, 20):
        create_new_partition_csvs(list_of_rows, "train_nb_" + str(i) + ".csv", \
        "test_nb_" + str(i) + ".csv", header_list)

def read_in_csv_to_list(input_data):
    """
    This function
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
    This function
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
    This function
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
