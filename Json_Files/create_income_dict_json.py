"""
Authors:        Seun Eisape & Victor Nault
Description:
Date:
"""
import pandas
import json

def main():
    """
    This function
    """

    unemployment_data_df = read_in_data()
    income_dict = make_income_dict(unemployment_data_df)
    save_to_json(income_dict, "income_dict.json", 1)


def make_income_dict(input_df):
    """
    This function
    """

    unemployment_info = input_df[["Area_name", "Attribute", "Value"]]
    #print(unemployment_info)
    income_dict = {}
    for i in range(len(unemployment_info)):
        this_row = unemployment_info.iloc[i]
        #print(this_row)
        #print(this_row[0])
        #print(this_row[0][-4])
        if (this_row[0][-4] == ","):
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
                #print(this_key)
                income_dict[this_key] = this_row[2]
    return income_dict
                #income_dict
        #counties = unemploment_info.contains(",")
        #unemploment_info[unemploment_info["Area_name"]]
    #print(counties)
    #county_to_unemployment = {}

def save_to_json(input, file_name_str, indent_int):
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
        json.dump(input, fp, indent=indent_int)

def read_in_data():
    return pandas.read_csv("Unemployment.csv", header=0)

if __name__ == "__main__":
    main()