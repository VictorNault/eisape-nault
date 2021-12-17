"""
Authors:        Seun Eisape & Victor Nault
Description:    This script creates a .csv file containing the discretized
                DSCI data and income data for the counties in
                counties_2019.json and med_income_dict. The DSCI data is
                discretized by averaging the average DSCIs for each county,
                then if the average for any given county is at or above this
                value, it is classifed as "Above Average", and if it is below,
                "Below Average". Then, if the median income, as found in
                med_income_dict, is at or above the low income cutoff, it is
                classified as "Not low income", and if it is below, "Low
                income". Finally these values are written to "naive_bayes.csv".
Date: 12/17/21
"""

import json
import csv

def main():
    """
    This function loads the dictionaries found in the .json files containing
    median income and average DSCI for every county, then passes them to
    helper functions to discretize them, then passes the discretized values to
    a helper function to export them.
    """
    counties_2019 = json.load(open("counties_2019.json"))
    discrete_dsci_dict = discretize_dsci_dict(counties_2019)
    med_income_dict = json.load(open("income_dict.json"))
    discrete_med_income_dict = discretize_med_income_dict(med_income_dict)
    create_csv(discrete_dsci_dict, discrete_med_income_dict)

def discretize_dsci_dict(dsci_dict):
    """
    This function discretizes the continuous average DSCI data by averaging the
    average DSCIs for each county, then if the average for any given county is
    at or above this value, classifying it as "Above Average", and if it is
    below, "Below Average". Each value is linked to its county via a dictionary.
    Parameter:  A dictionary with states as keys to dictionaries with counties
    as keys and average DSCI (single numerical value) as values.
    Returns: A dictionary with the same keys and structure as the parameter but
    discretized values.
    """

    avg_dsci = 0
    county_counter = 0
    for state in dsci_dict:
        for county in dsci_dict[state]:averaging
    said median income for each count, then
            avg_dsci += dsci_dict[state][county]
            county_counter += 1
    avg_dsci = avg_dsci / county_counter
    discrete_dsci_dict = {}
    for state in dsci_dict:
        this_state_county_dict = {}
        for county in dsci_dict[state]:
            if (dsci_dict[state][county] >= avg_dsci):
                this_state_county_dict[county] = "Above average DSCI"
            else:
                this_state_county_dict[county] = "Below average DSCI"
        discrete_dsci_dict[state] = this_state_county_dict
    return discrete_dsci_dict

def discretize_med_income_dict(med_income_dict):
    """
    This function discretizes the continuous median income data by comparing
    the median income of the county to a hardcoded cutoff value. If the median
    income is at or above the low income cutoff, it is classified as "Not low
    income", and if it is below, "Low income". Each value is linked to its
    county via a dictionary.
    Parameter:  A dictionary with counties as keys and median income (single
    numerical value) as values.
    Returns: A dictionary with the same keys as the parameter but discretized
    values.
    """

    # based on the National Center for Children in Poverty definition of low
    # income as below $51852 a year for a family of three
    low_income_cutoff = 51852
    discrete_med_income_dict = {}
    for county in med_income_dict:
        if (med_income_dict[county] >= low_income_cutoff):
            discrete_med_income_dict[county] = "Not low income"
        else:
            discrete_med_income_dict[county] = "Low income"
    return discrete_med_income_dict

def create_csv(dsci_dict, med_income_dict):
    """
    This function writes all the DSCI values in a dictionary of states to
    counties to DSCI values, and all the median income values in a dictionary
    of counties to median incomes, to a .csv file, where the columns are these
    two values and the rows are each county.
    Parameters: dsci_dict - A dictionary with counties as keys and median income
                (single numerical value) as values.
                med_income_dict - A dictionary with counties as keys and median
                income (single numerical value) as values.
    """
    with open("naive_bayes.csv", "w", newline="") as naive_bayes_csv:
        headers = ["DSCI", "Income"]
        writer = csv.writer(naive_bayes_csv)
        writer.writerow(headers)
        for state in dsci_dict:
            for county in dsci_dict[state]:
                try:
                    writer.writerow([dsci_dict[state][county], \
                    med_income_dict[county]])
                # If a county exists in the dsci_dict but not the
                # med_income_dict, ignore it
                except KeyError:
                    pass

if __name__ == "__main__":
    main()
