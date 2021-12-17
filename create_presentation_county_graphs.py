"""
Authors:        Seun Eisape & Victor Nault
Description:    This file creates the two Delaware DSCI graphs used in our
                presentation
                presentation
Date:           12/17/21
"""
from DsciDataset import *
import json

def main():
    """
    This function creates DSCI graphs for the counties of Delaware
    """
    all_counties_dict = json.load(open("all_counties.json"))
    for county in all_counties_dict:
        if county[0:2] == "DE":
            DE_county = DsciDataset(all_counties_dict[county], \
            int(len(all_counties_dict[county])/2), county)
            DE_county.export_prediction_plot()
    pass

if __name__ == '__main__':
    main()
