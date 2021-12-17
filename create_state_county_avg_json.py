"""
Authors:        Seun Eisape & Victor Nault
Description:    This file holds the necessary funcitons to create a file with
                state mapped to counties mapped to average Dsci values for 2019
Date:           12/17/21
"""
import json

def main():
    """
    This function runs all code to create the one year average of DSCI values
    """

    all_counties_dict = json.load(open("Json_Files/all_counties.json"))
    all_states_list = []
    for i in all_counties_dict:
        if (all_states_list.count(i[:2]) == 0):
            all_states_list.append(i[:2])

    state_dict_all_for_2019 =  {}
    for i in all_states_list:
        #finds the values for counties only in the year 2019
        this_state_dict = {}
        for j in all_counties_dict:
            if (j[:2] == i):
                this_state_dict[j] = all_counties_dict[j][991:1044]

        state_dict_all_for_2019[i] = this_state_dict
    state_dict_avg_for_2019 = calc_state_avg(state_dict_all_for_2019)
    save_dict_to_json(state_dict_avg_for_2019, \
    "Json_Files/counties_2019.json", 1)



def calc_state_avg(dsci_dict_2019):
    """
    This function finds all values and returns average for the year 2019
    Parameters: dsci_dict_2019 dictionary of states counties mapped to average
    dsci value for 2019
    """

    output_dict_of_dicts = {}
    for state in dsci_dict_2019:
        counties_dict = {}
        for county in dsci_dict_2019[state]:
            counties_dict[county] = None
        output_dict_of_dicts[state] = counties_dict

    for state in dsci_dict_2019:#iterate through states
        for county in dsci_dict_2019[state]: #iterate through counties
            avg_tracker = 0
            for week in dsci_dict_2019[state][county]: #calculate average
                avg_tracker += week
            avg_tracker = avg_tracker/len(dsci_dict_2019[state][county])
            output_dict_of_dicts[state][county] = avg_tracker

    return output_dict_of_dicts

    """
    state_to_county_avg_dict = {}
    for key in dsci_dict_2019:
        state_list_of_list_dsci = dsci_dict_2019[key]
        list_of_avgs = []
        for list in state_list_of_list_dsci:
            avg_tracker = 0
            for i in list:
                avg_tracker += i
            avg_tracker = avg_tracker/len(list)
            list_of_avgs.append(avg_tracker)
        state_to_county_avg_dict[key] = list_of_avgs
    return state_to_county_avg_dict
    """

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

if __name__ == "__main__":
    main()
