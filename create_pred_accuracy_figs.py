"""
Authors:        Seun Eisape & Victor Nault
Description:
Date:
"""

import json
from DsciDataset import *
import matplotlib.pyplot as pyplot
from random import random

def main():
    """
    This function
    """
    all_counties_dict = json.load(open("all_counties.json"))
    state_list = []
    rss_list_half_boundary_week = []
    avg_diff_list_half_boundary_week = []
    rss_list_three_quarters_boundary_week = []
    avg_diff_list_three_quarters_boundary_week = []
    for i in all_counties_dict:
        state_list.append(i[:2])
        half_dsci_dataset = DsciDataset(all_counties_dict[i], int(len(all_counties_dict[i]) / 2) , i)
        three_quarters_dsci_dataset = DsciDataset(all_counties_dict[i], int((3 * len(all_counties_dict[i])) / 4) , i)
        rss_list_half_boundary_week.append(half_dsci_dataset.calc_rss(half_dsci_dataset.train_data_pred_dsci_list_after_boundary_week, half_dsci_dataset.full_data_pred_dsci_list_after_boundary_week))
        avg_diff_list_half_boundary_week.append(half_dsci_dataset.calc_diff_of_list_avgs(half_dsci_dataset.train_data_pred_dsci_list_after_boundary_week, half_dsci_dataset.full_data_pred_dsci_list_after_boundary_week))
        rss_list_three_quarters_boundary_week.append(three_quarters_dsci_dataset.calc_rss(three_quarters_dsci_dataset.train_data_pred_dsci_list_after_boundary_week, three_quarters_dsci_dataset.full_data_pred_dsci_list_after_boundary_week))
        avg_diff_list_three_quarters_boundary_week.append(three_quarters_dsci_dataset.calc_diff_of_list_avgs(three_quarters_dsci_dataset.train_data_pred_dsci_list_after_boundary_week, three_quarters_dsci_dataset.full_data_pred_dsci_list_after_boundary_week))

    state_color_dict = create_state_color_dict(state_list)
    color_list = create_color_list(state_list, state_color_dict)

    state_names_list = []
    for i in state_color_dict:
        state_names_list.append(i)

    export_rss_plot(rss_list_half_boundary_week, state_names_list, state_color_dict, color_list, "figures/rss_plot_half_boundary_week.pdf", "RSS between DSCI Models for all Counties with 1/2 Training Data")
    export_avg_diff_plot(avg_diff_list_half_boundary_week, state_names_list, state_color_dict, color_list, "figures/avg_diff_plot_half_boundary_week.pdf", "Difference between Averages of DSCI Models for all Counties with 1/2 Training Data")
    export_rss_plot(rss_list_three_quarters_boundary_week, state_names_list, state_color_dict, color_list, "figures/rss_plot_three_quarters_boundary_week.pdf", "RSS between DSCI Models for all Counties with 3/4 Training Data")
    export_avg_diff_plot(avg_diff_list_three_quarters_boundary_week, state_names_list, state_color_dict, color_list, "figures/avg_diff_plot_three_quarters_boundary_week.pdf", "Difference between Averages of DSCI Models for all Counties with 3/4 Training Data")

    half_state_avg_rss_list = create_state_avg_rss_list(rss_list_half_boundary_week, state_list, state_names_list)
    three_quarters_state_avg_rss_list = create_state_avg_rss_list(rss_list_three_quarters_boundary_week, state_list, state_names_list)

    half_state_avg_rss_dict = create_state_avg_rss_dict(state_names_list, half_state_avg_rss_list)
    three_quarters_state_avg_rss_dict = create_state_avg_rss_dict(state_names_list, three_quarters_state_avg_rss_list)
    save_to_json(half_state_avg_rss_dict, "half_state_avg_rss_dict.json", 1)
    save_to_json(three_quarters_state_avg_rss_dict, "three_quarters_state_avg_rss_dict.json", 1)

    export_state_avg_rss_plot(half_state_avg_rss_list, state_names_list, state_color_dict, "figures/state_avg_rss_plot_half_boundary_week.pdf", "Statewide Average RSS between DSCI Models for all Counties with 1/2 Training Data")
    export_state_avg_rss_plot(three_quarters_state_avg_rss_list, state_names_list, state_color_dict, "figures/state_avg_rss_plot_three_quarters_boundary_week.pdf", "Statewide Average RSS between DSCI Models for all Counties with 3/4 Training Data")

def create_state_avg_rss_dict(state_names_list, state_avg_rss_list):
    """
    This function
    """

    output_dict = {}
    for i in range(len(state_names_list)):
        output_dict[state_names_list[i]] = state_avg_rss_list[i]
    return output_dict


def export_state_avg_rss_plot(state_avg_rss_list, state_names_list, state_color_dict, export_name, title):
    """
    This function
    """

    pyplot.xlim(-1, 58)
    leg_objects = []
    for i in state_color_dict:
        circle, = pyplot.plot([], 'o', c=state_color_dict[i], alpha = 0.9)
        leg_objects.append(circle)
    pyplot.legend(leg_objects, state_names_list, loc=(0.93, 0.08), ncol=2, fontsize="xx-small")
    color_list = create_color_list(state_names_list, state_color_dict)
    pyplot.scatter(range(len(state_avg_rss_list)), state_avg_rss_list, c=color_list, alpha=0.9)
    pyplot.title(title, fontsize="xx-small")
    pyplot.ylabel("RSS")
    pyplot.savefig(export_name, format="pdf")
    pyplot.clf()

def create_state_avg_rss_list(rss_list, state_list, state_names_list):
    """
    This function
    """

    num_counties = len(rss_list)
    state_avg_rss_list = []
    for state in state_names_list:
        this_state_avg = 0
        counter = 0
        for j in range(num_counties):
            if (state_list[j] == state):
                this_state_avg += rss_list[j]
                counter += 1
        this_state_avg = this_state_avg / counter
        state_avg_rss_list.append(this_state_avg)
    return state_avg_rss_list

def save_to_json(input, file_name_str, indent_int):
    """
    This function
    """

    with open(file_name_str, "w") as fp:
        json.dump(input, fp, indent=indent_int)

def export_rss_plot(rss_list, state_names_list, state_color_dict, color_list, export_name, title):
    """
    This function
    """

    pyplot.xlim(-100, 3600)
    leg_objects = []
    for i in state_color_dict:
        circle, = pyplot.plot([], 'o', markerfacecolor="none", markeredgecolor=state_color_dict[i], alpha = 0.9)
        leg_objects.append(circle)
    pyplot.legend(leg_objects, state_names_list, loc=(0.93, 0.08), ncol=2, fontsize="xx-small")
    pyplot.scatter(range(len(rss_list)), rss_list, facecolors="none", edgecolors=color_list, alpha=0.9, s=5)
    pyplot.title(title, fontsize="small")
    pyplot.ylabel("RSS")
    pyplot.savefig(export_name, format="pdf")
    pyplot.clf()

def export_avg_diff_plot(avg_diff_list, state_names_list, state_color_dict, color_list, export_name, title):
    """
    This function
    """

    pyplot.xlim(-100, 3600)
    leg_objects = []
    for i in state_color_dict:
        circle, = pyplot.plot([], 'o', markerfacecolor="none", markeredgecolor=state_color_dict[i], alpha = 0.9)
        leg_objects.append(circle)
    pyplot.legend(leg_objects, state_names_list, loc=(0.93, 0.08), ncol=2, fontsize="xx-small")
    pyplot.scatter(range(len(avg_diff_list)), avg_diff_list, facecolors="none", edgecolors=color_list, alpha=0.9, s=5)
    pyplot.title(title, fontsize="small")
    pyplot.ylabel("Difference of Averages")
    pyplot.savefig(export_name, format="pdf")
    pyplot.clf()

def create_state_color_dict(state_list):
    """
    This function
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
    This function
    """

    color_list = []
    for i in state_list:
        color_list.append(state_color_dict[i])
    return color_list

def create_legend(names, color_dict):
    """
    This function
    """
    
    leg_objects = []
    for i in color_dict:
        circle, = pyplot.plot([], 'o', c=color_dict[i])
        leg_objects.append(circle)
    pyplot.legend(leg_objects, names, loc=(0.85, 0.2), ncol=2)

if __name__ == "__main__":
    main()
