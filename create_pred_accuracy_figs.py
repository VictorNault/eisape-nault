"""
Authors:       Seun Eisape & Victor Nault
Description:   This file holds functions necessary for creating graphs that show
prediciton acuracy of predicted trends of DSCI
Date:           12/17/21
"""

import json
from DsciDataset import *
import matplotlib.pyplot as pyplot
from random import random

def main():
    """
    This function is responsible for saving, exporting, and getting necessary
    data to create prediction accuracy graphs
    """
    all_counties_dict = json.load(open("Json_Files/all_counties.json"))
    state_list = []
    rss_list_half_boundary_week = []
    avg_diff_list_half_boundary_week = []
    rss_list_three_quarters_boundary_week = []
    avg_diff_list_three_quarters_boundary_week = []
    for i in all_counties_dict:
        # Adds Residual sum values for different partitions of DSCI dataset
        state_list.append(i[:2])
        half_dsci_dataset = DsciDataset(all_counties_dict[i], \
        int(len(all_counties_dict[i]) / 2) , i)
        three_quarters_dsci_dataset = DsciDataset(all_counties_dict[i], \
        int((3 * len(all_counties_dict[i])) / 4) , i)
        rss_list_half_boundary_week.append(half_dsci_dataset.calc_rss \
        (half_dsci_dataset.train_data_after_boundary, \
        half_dsci_dataset.full_data_pred_dsci_list_after_boundary_week))
        avg_diff_list_half_boundary_week.append(\
        half_dsci_dataset.calc_diff_of_list_avgs(half_dsci_dataset. \
        train_data_after_boundary, half_dsci_dataset. \
        full_data_pred_dsci_list_after_boundary_week))
        rss_list_three_quarters_boundary_week.append( \
        three_quarters_dsci_dataset.calc_rss( \
        three_quarters_dsci_dataset. \
        train_data_after_boundary, \
        three_quarters_dsci_dataset. \
        full_data_pred_dsci_list_after_boundary_week))
        avg_diff_list_three_quarters_boundary_week.append( \
        three_quarters_dsci_dataset.calc_diff_of_list_avgs( \
        three_quarters_dsci_dataset. \
        train_data_after_boundary, \
        three_quarters_dsci_dataset.\
        full_data_pred_dsci_list_after_boundary_week))
    # Colors for each sate
    state_color_dict = create_state_color_dict(state_list)
    color_list = create_color_list(state_list, state_color_dict)

    state_names_list = []
    for i in state_color_dict:
        state_names_list.append(i)

    #exporting and saving created plots
    export_rss_plot(rss_list_half_boundary_week, state_names_list, \
    state_color_dict, color_list, "figures/rss_plot_half_boundary_week.pdf", \
    "RSS between DSCI Models for all Counties with 1/2 Training Data")
    export_avg_diff_plot(avg_diff_list_half_boundary_week, state_names_list, \
    state_color_dict, color_list, "figures/avg_diff_plot_half_boundary_week.pdf"\
    , "Difference between Averages of DSCI Models for all Countieswith 1/2" + \
    "Training Data")
    export_rss_plot(rss_list_three_quarters_boundary_week, state_names_list, \
    state_color_dict, color_list, "figures/rss_plot_three_quarters_boundary_w"+\
    "eek.pdf", "RSS between DSCI Models for all Counties with 3/4 Training Data")
    export_avg_diff_plot(avg_diff_list_three_quarters_boundary_week, \
    state_names_list, state_color_dict, color_list, \
    "figures/avg_diff_plot_three_quarters_boundary_week.pdf", \
    "Difference between Averages of DSCI Models for all Counties with 3/4 " + \
    "Training Data")

    #average resdidual sums values
    half_state_avg_rss_list = create_state_avg_rss_list( \
    rss_list_half_boundary_week, state_list, state_names_list)
    three_quarters_state_avg_rss_list = create_state_avg_rss_list( \
    rss_list_three_quarters_boundary_week, state_list, state_names_list)
    half_state_avg_rss_dict = create_state_avg_rss_dict(state_names_list, \
    half_state_avg_rss_list)
    three_quarters_state_avg_rss_dict = create_state_avg_rss_dict( \
    state_names_list, three_quarters_state_avg_rss_list)
    save_to_json(half_state_avg_rss_dict, "half_state_avg_rss_dict.json", 1)
    save_to_json(three_quarters_state_avg_rss_dict, "three_quarters_state_" + \
    "avg_rss_dict.json", 1)

    export_state_avg_rss_plot(half_state_avg_rss_list, state_names_list, \
    state_color_dict, "figures/state_avg_rss_plot_half_boundary_week.pdf", \
    "Statewide Average RSS between DSCI Models for all Counties with 1/2 " + \
    "Training Data")
    export_state_avg_rss_plot(three_quarters_state_avg_rss_list, \
    state_names_list, state_color_dict, \
    "figures/state_avg_rss_plot_three_quarters_boundary_week.pdf", \
    "Statewide Average RSS between DSCI Models for all Counties with 3/4 " + \
    "Training Data")

def create_state_avg_rss_dict(state_names_list, state_avg_rss_list):
    """
    This function creates a dictionary mapping states to their average RSS
    county value
    Parameters: states_names_list - list of all state names
    state_avg_rss_list - avg Residual sums value for each state
    """

    output_dict = {}
    for i in range(len(state_names_list)):
        output_dict[state_names_list[i]] = state_avg_rss_list[i]
    return output_dict


def export_state_avg_rss_plot(state_avg_rss_list, state_names_list, \
state_color_dict, export_name, title):
    """
    This function creates a graph showing a states avg RSS value and exports it
    Parameters: state_names_list - state_list with all state duplicates removed
    state_avg_rss_list - avg Residual sums value for each state
    state_color_dict - maps each state to a color to be visualized
    export_name - will be name of exported graphs
    title - title of plot
    """

    pyplot.xlim(-1, 58)
    leg_objects = []
    for i in state_color_dict:
        circle, = pyplot.plot([], 'o', c=state_color_dict[i], alpha = 0.9)
        leg_objects.append(circle)
    #creating plot
    pyplot.legend(leg_objects, state_names_list, loc=(0.93, 0.08), ncol=2, \
    fontsize="xx-small")
    color_list = create_color_list(state_names_list, state_color_dict)
    pyplot.scatter(range(len(state_avg_rss_list)), state_avg_rss_list, \
    c=color_list, alpha=0.9)
    pyplot.title(title, fontsize="xx-small")
    pyplot.ylabel("RSS")
    pyplot.savefig(export_name, format="pdf")
    pyplot.clf()

def create_state_avg_rss_list(rss_list, state_list, state_names_list):
    """
    This function adds a states RSS avg value to a list so that it can later be
    mapped to a state
    Parameters: rss_list - list of RSS values
    state_list - every instance of a state appearing in DSCI dataset
    state_names_list - state_list with all state duplicates removed
    """

    num_counties = len(rss_list)
    state_avg_rss_list = []
    for state in state_names_list:
        this_state_avg = 0
        counter = 0
        for j in range(num_counties):
            #accesses counties to see what state they are in
            if (state_list[j] == state): #Finds correct state to add RSS val to
                this_state_avg += rss_list[j]
                counter += 1
        this_state_avg = this_state_avg / counter
        state_avg_rss_list.append(this_state_avg)
    return state_avg_rss_list

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

def export_rss_plot(rss_list, state_names_list, state_color_dict, color_list, \
export_name, title):
    """
    This function creates exports a RSS value for a state
    Parameters: rss_list - list of all RSSS values per state
    state_names_list - state_list with all state duplicates removed
    state_color_dict - dictionary mapping states with visualized color
    color list - list of all colors for states, in state order
    export_name: name of file to be exported
    title: title of graph

    """

    pyplot.xlim(-100, 3600)
    leg_objects = []
    for i in state_color_dict:
        circle, = pyplot.plot([], 'o', markerfacecolor="none", \
        markeredgecolor=state_color_dict[i], alpha = 0.9)
        leg_objects.append(circle)
    pyplot.legend(leg_objects, state_names_list, loc=(0.93, 0.08), ncol=2, \
    fontsize="xx-small")
    pyplot.scatter(range(len(rss_list)), rss_list, facecolors="none", \
    edgecolors=color_list, alpha=0.9, s=5)
    pyplot.title(title, fontsize="small")
    pyplot.ylabel("RSS")
    pyplot.savefig(export_name, format="pdf")
    pyplot.clf()

def export_avg_diff_plot(avg_diff_list, state_names_list, state_color_dict, color_list, export_name, title):
    """
    This function creates and exports plots for the difference of averages
    between states
    Parameters: avg_diff_list - list of average differences for state
    state_names_list - state_list with all state duplicates removed
    state_color_dict - dictionary mapping states to their visualized colors
    color_list - list of all colors to be visualized for states in state order
    export_name - name of file to be exported
    title: title of graph
    """

    pyplot.xlim(-100, 3600)
    leg_objects = []
    for i in state_color_dict:
        circle, = pyplot.plot([], 'o', markerfacecolor="none", \
        markeredgecolor=state_color_dict[i], alpha = 0.9)
        leg_objects.append(circle)
    pyplot.legend(leg_objects, state_names_list, loc=(0.93, 0.08), ncol=2, fontsize="xx-small")
    pyplot.scatter(range(len(avg_diff_list)), avg_diff_list, facecolors="none", edgecolors=color_list, alpha=0.9, s=5)
    pyplot.title(title, fontsize="small")
    pyplot.ylabel("Difference of Averages")
    pyplot.savefig(export_name, format="pdf")
    pyplot.clf()

def create_state_color_dict(state_list):
    """
    This function maps a State to a color to be visualized in a plot
    Parameters: state_list - list of every state form DSCI dataset
    """

    state_color_dict = {}
    counter = 0
    for i in state_list:
        try:
            state_color_dict[i]
        except KeyError:
            if (counter == 0):
                state_color_dict[i] = "Orange"
            if (counter == 1):
                state_color_dict[i] = "Blue"
            if (counter == 2):
                state_color_dict[i] = "Yellow"
            if (counter == 3):
                state_color_dict[i] = "Purple"
            if (counter == 4):
                state_color_dict[i] = "Green"
            if (counter == 5):
                state_color_dict[i] = "Red"
            if (counter == 6):
                state_color_dict[i] = "Black"
            counter = (counter + 1) % 7
    return state_color_dict

def create_color_list(state_list, state_color_dict):
    """
    This function creates a list of colors for every instance of a state in the
    DSCI dataset
    Parameters: state_list - list of every instance of a state that appears in
    DSCI dataset
    state_color_dict - dictionary mapping a state to a color to be visualized
    """

    color_list = []
    for i in state_list:
        color_list.append(state_color_dict[i])
    return color_list


if __name__ == "__main__":
    main()
