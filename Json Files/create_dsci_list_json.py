"""
Author:
Description:
Date:
"""

import csv
import pandas
import json

def main():
    """
    This function
    """

    drought_data_frame = read_in_data()
    all_county_dict = create_all_county_dict(drought_data_frame)
    save_dict_to_json(all_county_dict, "all_counties.json", 1)

def read_in_data():
    return pandas.read_csv("county_drought_data_2000-2021_dsci.csv", header=0)

def create_all_county_dict(input_df):
    """
    This function reads over the State and county columns within the DSCI
    drought data set and creates a dictionary holding each time a county appears

    input_df: drought datatset
    return: dictionary with keys representing each county and values being each
    instance that county appears
    """
    county_data_frame = input_df[["State", "County"]]
    county_df_no_dupes = county_data_frame.drop_duplicates()
    all_county_dict = {}
    for i in range(len(county_df_no_dupes)):
        this_row = county_df_no_dupes.iloc[i]
        this_county = this_row["County"]
        this_state = this_row["State"]
        key_name = this_state + " " + this_county
        state_df = input_df[input_df["State"].isin([this_state])]
        county_df = state_df[state_df["County"].isin([this_county])]
        all_county_dict[key_name] = create_dsci_list(county_df)

    return all_county_dict

def create_dsci_list(county_data_frame):
    """
    This function
    """

    dsci_by_week = len(county_data_frame) * [0]
    reverse_counter = len(county_data_frame)
    for i in range(len((county_data_frame))):
        # Conversion to int here because the default data type returned by
        # county_data_frame["DSCI"].iloc[i] is "int64", which breaks the dump
        # to json
        dsci_by_week[i] = int(county_data_frame["DSCI"].iloc[i])
    return dsci_by_week

def save_dict_to_json(input_dict, file_name_str, indent_int):
    """
    This function
    """
    
    with open(file_name_str, "w") as fp:
        json.dump(input_dict, fp, indent=indent_int)


if __name__ == "__main__":
    main()
