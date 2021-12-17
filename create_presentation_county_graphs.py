"""
Authors:        Seun Eisape & Victor Nault
Description:    This file creates the two deleware DSCI graphs used in our
                presentation
Date:
"""
from DsciDataset import *
import json

def main():
    """
    This function creates DSCI graphs for the counties of Deleware
    """
    all_counties_dict = json.load(open("all_counties.json"))
    for county in all_counties_dict:
        if county[0:2] == "DE":
            #print(all_counties_dict[county])
            DE_county = DsciDataset(all_counties_dict[county], int(len(all_counties_dict[county])/2), county)
            DE_county.export_prediction_plot()
            #print(DE_county)
    pass

if __name__ == '__main__':
    main()
