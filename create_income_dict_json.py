"""
Authors:        Seun Eisape & Victor Nault
Description:    This file holds necessary functions to create an income
                which maps a county to their median household income
Date:           12/17/21
"""
import pandas
import json

def main():
    """
    This function reads in data and is what ultimately creates the income
    dictionary
    """

    unemployment_data_df = read_in_data()
    income_dict = make_income_dict(unemployment_data_df)
    save_dict_to_json(income_dict, "Json_Files/income_dict.json", 1)


def make_income_dict(input_df):
    """
    This function creates a dictionary that takes the state county dictionary,
    and will map the county values to their respective median household income
    Parameters: input_df - unemploment data frame
    """

    unemployment_info = input_df[["Area_name", "Attribute", "Value"]]
    # returns area name, attribute, and value from household income data set
    income_dict = {}
    for i in range(len(unemployment_info)):
        this_row = unemployment_info.iloc[i]
        if (this_row[0][-4] == ","):
            # renames problematic county names from Alaska to match the format
            # of other data
            if (this_row[1] == "Median_Household_Income_2019"):
                this_key = this_row[0][-2:] + " " + this_row[0][:-4]
                if (this_key == "AK Anchorage Borough/municipality"):
                    this_key = "AK Anchorage Municipality"
                if (this_key == "AK Juneau Borough/city"):
                    this_key = "AK Juneau City and Borough"
                if (this_key == "AK Sitka Borough/city"):
                    this_key = "AK Sikta City and Borough"
                if (this_key == "AK Wrangell Borough/city"):
                    this_key = "AK Wrangell City and Borough"
                if (this_key == "AK Yakutat Borough/city"):
                    this_key = "AK Yakutat City and Borough"
                income_dict[this_key] = this_row[2]
    return income_dict

def save_dict_to_json(input_dict, file_name_str, indent_int):
    """
    Creates a Json file containing a single data structure of the type of input.
    Parameters: input - data structure to be saved to .json
                file_name_str - name of the new .json file, including the .json
                extension at the end
                indent_int - changes how spread out the elements of the data
                structure are visually in the .json file, must be positive and
                greater than 0
    """

    with open(file_name_str, "w") as fp:
        json.dump(input_dict, fp, indent=indent_int)

def read_in_data():
    return pandas.read_csv("starting_csv_data/Unemployment.csv", header=0)

if __name__ == "__main__":
    main()
