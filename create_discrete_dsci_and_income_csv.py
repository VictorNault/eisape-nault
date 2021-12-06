# kello
import json
import csv

def main():
    counties_2019 = json.load(open("counties_2019.json"))
    discrete_dsci_dict = discretize_dsci_dict(counties_2019)
    #print(discrete_dsci_dict)
    med_income_dict = json.load(open("income_dict.json"))
    discrete_med_income_dict = discretize_med_income_dict(med_income_dict)
    #print(discrete_med_income_dict)
    create_csv(discrete_dsci_dict, discrete_med_income_dict)

def discretize_dsci_dict(dsci_dict):
    avg_dsci = 0
    county_counter = 0
    for state in dsci_dict:
        for county in dsci_dict[state]:
            avg_dsci += dsci_dict[state][county]
            county_counter += 1
    avg_dsci = avg_dsci / county_counter
    #print(avg_dsci)
    discrete_dsci_dict = {}
    for state in dsci_dict:
        this_state_county_dict = {}
        #discrete_dsci_dict[state]
        for county in dsci_dict[state]:
            if (dsci_dict[state][county] >= avg_dsci):
                this_state_county_dict[county] = "Above average DSCI"
            else:
                this_state_county_dict[county] = "Below average DSCI"
        discrete_dsci_dict[state] = this_state_county_dict
    return discrete_dsci_dict

def discretize_med_income_dict(med_income_dict):
    low_income_cutoff = 51852
    discrete_med_income_dict = {}
    for county in med_income_dict:
        if (med_income_dict[county] >= low_income_cutoff):
            discrete_med_income_dict[county] = "Not low income"
        else:
            discrete_med_income_dict[county] = "Low income"
    return discrete_med_income_dict

def create_csv(dsci_dict, med_income_dict):
    with open("naive_bayes.csv", "w", newline="") as naive_bayes_csv:
        headers = ["DSCI", "Income"]
        writer = csv.writer(naive_bayes_csv)
        writer.writerow(headers)
        for state in dsci_dict:
            for county in dsci_dict[state]:
                try:
                    writer.writerow([dsci_dict[state][county], med_income_dict[county]])
                except KeyError:
                    pass




if __name__ == "__main__":
    main()
