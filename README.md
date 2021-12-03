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
