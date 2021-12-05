import json
from DsciDataset import *
import matplotlib.pyplot as pyplot
from random import random

def main():
    all_counties_dict = json.load(open("all_counties.json"))
    state_list = []
    rss_list = []
    sum_diff_list = []
    for i in all_counties_dict:
        state_list.append(i[:2])
        this_dsci_dataset = DsciDataset(all_counties_dict[i], int(len(all_counties_dict[i]) / 2) , i)
        rss_list.append(this_dsci_dataset.calc_rss(this_dsci_dataset.train_data_pred_dsci_list_after_boundary_week, this_dsci_dataset.full_data_pred_dsci_list_after_boundary_week))
        sum_diff_list.append(this_dsci_dataset.calc_sum_diff(this_dsci_dataset.train_data_pred_dsci_list_after_boundary_week, this_dsci_dataset.full_data_pred_dsci_list_after_boundary_week))

    state_color_dict = create_state_color_dict(state_list)
    color_list = create_color_list(state_list, state_color_dict)

    state_names_list = []
    for i in state_color_dict:
        state_names_list.append(i)

    export_rss_plot(rss_list, state_names_list, state_color_dict, color_list)
    export_sum_diff_plot(sum_diff_list, state_names_list, state_color_dict, color_list)


def export_rss_plot(rss_list, state_names_list, state_color_dict, color_list):
    pyplot.xlim(-100, 3600)
    leg_objects = []
    for i in state_color_dict:
        circle, = pyplot.plot([], 'o', markerfacecolor="none", markeredgecolor=state_color_dict[i], alpha = 0.9)
        leg_objects.append(circle)
    pyplot.legend(leg_objects, state_names_list, loc=(0.93, 0.08), ncol=2, fontsize="xx-small")
    pyplot.scatter(range(len(rss_list)), rss_list, facecolors="none", edgecolors=color_list, alpha=0.9, s=5)
    pyplot.savefig("figures/rss_plot.pdf", format="pdf")
    pyplot.clf()

def export_sum_diff_plot(sum_diff_list, state_names_list, state_color_dict, color_list):
    pyplot.xlim(-100, 3600)
    leg_objects = []
    for i in state_color_dict:
        circle, = pyplot.plot([], 'o', markerfacecolor="none", markeredgecolor=state_color_dict[i], alpha = 0.9)
        leg_objects.append(circle)
    pyplot.legend(leg_objects, state_names_list, loc=(0.93, 0.08), ncol=2, fontsize="xx-small")
    pyplot.scatter(range(len(sum_diff_list)), sum_diff_list, facecolors="none", edgecolors=color_list, alpha=0.9, s=5)
    pyplot.savefig("figures/sum_diff_plot.pdf", format="pdf")
    pyplot.clf()

def create_state_color_dict(state_list):
    state_color_dict = {}
    for i in state_list:
        r = random()
        b = random()
        g = random()
        state_color_dict[i] = (r, g, b)
    return state_color_dict

def create_color_list(state_list, state_color_dict):
    color_list = []
    for i in state_list:
        color_list.append(state_color_dict[i])
    return color_list

def create_legend(names, color_dict):
    leg_objects = []
    for i in color_dict:
        circle, = pyplot.plot([], 'o', c=color_dict[i])
        leg_objects.append(circle)
    pyplot.legend(leg_objects, names, loc=(0.85, 0.2), ncol=2)

if __name__ == "__main__":
    main()
