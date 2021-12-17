"""
Authors:
Description:
Date:
"""
import json

def main():
    """
    This function
    """

    all_counties_dict = json.load(open("all_counties.json"))
    all_states_list = []
    for i in all_counties_dict:
        if (all_states_list.count(i[:2]) == 0):
            all_states_list.append(i[:2])

    state_dict_all_for_2019 =  {}
    for i in all_states_list:
        this_state_dict = {}
        for j in all_counties_dict:
            if (j[:2] == i):
                this_state_dict[j] = all_counties_dict[j][991:1044]
            """
            try:
                #print(state_dict[i[:2]])
                #a_list = state_dict[i[:2]]
                #print(a_list)
                #print("RE")
                #a_nother_list = [all_counties_dict[i]]
                #print(a_nother_list)
                #print("RAA")
                #state_
                state_dict_all[i[:2]] = state_dict_all[i[:2]] + [all_counties_dict[i][991:1044]]
                #print(state_dict[i[:2]])
                #print("AAA")
            except KeyError:
                state_dict_all[i[:2]] = [all_counties_dict[i][991:1044]]
                #print(state_dict[i[:2]])
                #print(state_dict[i[:2]])
                #print("REE")\
            """
        state_dict_all_for_2019[i] = this_state_dict
    state_dict_avg_for_2019 = calc_state_avg(state_dict_all_for_2019)
    save_to_json(state_dict_avg_for_2019, "counties_2019.json", 1)



def calc_state_avg(dsci_dict_2019):
    """
    This function
    """
    
    output_dict_of_dicts = {}
    for state in dsci_dict_2019:
        counties_dict = {}
        for county in dsci_dict_2019[state]:
            counties_dict[county] = None
        output_dict_of_dicts[state] = counties_dict

    for state in dsci_dict_2019:
        for county in dsci_dict_2019[state]:
            avg_tracker = 0
            for week in dsci_dict_2019[state][county]:
                #print(week)
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

if __name__ == "__main__":
    main()
