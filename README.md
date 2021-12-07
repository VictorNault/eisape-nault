# eisape-nault

Victor and Seun: 11-18-21 (1 hour)
- Downloaded drought dataset as .csv, cumulative area for all 3006 US Counties, by State
- Uploaded drought dataset to google drive because it was over 300 mb and github will not accept files over 25 mb
- Made Github repositiory
- Downloaded median income by county dataset as .csv, and found that it only had median income data for 2019, crisis ensued

Victor and Seun: 11-23-21 (2 hours)
- Downloaded drought dataset containing only DSCI data
- crated functions to locate a single county than create list of DSCI values and graphed them

Victor: 11-30-21 (1.5 hours)
- Created a function to create a linear model of the DSCI data based on the DSCI data before a specified week cutoff point
- Copied over helper functions from previous labs that were necessary to achieve this
- Renamed "d0_by_week" to "dsci_by_week" to reflect that we are using dsci as our metric, not d0.

Seun and Victor: 12-2-21 (4 hours)
- modularized the process_data function to read over all counties rather than the deleware test case
- commented some functions
- Changed most code that used dsci_list into calls to create and use DsciDataset.py
- Renamed create_county_plot() to create_dsci_list()), make it return the dsci_list, and moved the functionality for actual plotting into main
- made linear graphs for model

Victor: 12-03-21 (0.5 hours)
- fixed broken dictionary code

Victor: 12-04-21 (5 hours)
- Made the dictionary of all counties map to lists of dscis instead of pandas dataframes
- Exported the dictionary of all counties to all_counties.json so we didn't need to wait 5 minutes for the program to make said dictionary every time it ran
- Moved functionality for creating and exporting said dictionary to a separate file
- Ran said file and then added all_counties.json to the repository
- Created new instance variables in DsciDataset to record the predicted dscis using an earlier partition of the full dsci list and the total full dsci list, as these are what we are comparing
- Created a new function in DsciDataset to recalculate the dataset partitions with a new week to divide the full dsci list by
- Created new functions in DsciDataset to calculate the rss for two arrays and to calculate the sum of differences for two arrays
- Created a new file to plot the rss and sum of differences between the two new instance variables in DsciDataset, and then color each point by state
- Used said file to make said plots
- Added said plots to the repository
- Felt great pain at trying to get pyplot to do what I wanted4

Victor and Seun: 12-05-21 (4.5 hours)
- created files to make dictionaries mapping: State-County-DSCI values (all-time) & county-DSCI (2019) & county-median household income (2019)
- read in median household avgs for counties in 2019  
- un-reversed data sets that were being read in backwards
- some comments for functions

Victor and Seun: 12-06-21 (7.5 hours)
- Discretized our DSCI data into "Above Average DSCI" and "Below Average DSCI", and discretized our median income data to "Low Income" and "Not Low Income" (based on the US legal definition of low income as below $51852 a year for a family of three)
- Wrote this to a csv file
- Shuffled and then randomly divided the contents of this csv file into training and testing partitions 20 times
- Did a Naive Bayes analysis on all of these paired partitions
- Averaged the resulting accuracy to get a final result of about 55%
- Fixed broken code for making county-level graphs in DsciDataset
- Exported two example graphs to demonstrate how we got our linear models
- Replaced sum of differences graphs with difference between average DSCI graphs
- Made RSS and difference between averages graphs for models of three-quarters of the original data
- Made graphs for the average RSS and average difference between averages for entire states
- Changed the color dictionary for all scatterplot graphs to no longer be random
- Exported the average cost/RSS of every state to a .json file
- Discretized this data into cost below 50000, cost between 50000 and 100000, and cost above 100000
- Manually made a map of the US states and territories colored based on this using GIMP