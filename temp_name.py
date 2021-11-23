# hello

import numpy
import csv
import pandas
import matplotlib.pyplot as pyplot

def main():
    drought_data_frame = read_in_data()
    de_test = process_data(drought_data_frame)
    create_county_plot(de_test["Kent County"])
    create_county_plot(de_test["Sussex County"])
    create_county_plot(de_test["New Castle County"])


def read_in_data():
    return pandas.read_csv("county_drought_data_2000-2021_dsci.csv", header=0)


def process_data(input_df):
    de_data_frame = input_df[input_df["State"].isin(["DE"])]
    #print(de_data_frame)

    de_county_data_frame = (de_data_frame["County"])
    de_county_df_no_dupes = de_county_data_frame.drop_duplicates()
    #print(de_county_df_no_dupes)

    de_county_dict = {}
    for county in de_county_df_no_dupes:
        de_county_dict[county]= de_data_frame[de_data_frame["County"].isin([county])]
    #print(de_county_dict)\

    return de_county_dict


def create_county_plot(county_data_frame):
    d0_by_week = len(county_data_frame) * [0]
    reverse_counter = len(county_data_frame)
    #print(county_data_frame)

    for i in range(len((county_data_frame))):
        d0_by_week[reverse_counter - i - 1] = county_data_frame["DSCI"].iloc[i]
        #print(county_data_frame[reverse_counter - i - 1])
    #print(d0_by_week)
    pyplot.plot(d0_by_week)
    pyplot.show()


if __name__ == "__main__":
    main()
