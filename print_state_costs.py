"""
Authors:
Description:
Date:
"""
import json

def main():
    three_quarters_state_avg_rss_dict = \
    json.load(open("Json_Files/three_quarters_state_avg_rss_dict.json"))
    for state in three_quarters_state_avg_rss_dict:
        if (three_quarters_state_avg_rss_dict[state] < 50000):
            print("50000 > Cost, ", state)
        if ((three_quarters_state_avg_rss_dict[state] >= 50000) and \
        (three_quarters_state_avg_rss_dict[state] <= 100000)):
            print("50000 <= Cost <= 100000, ", state)
        if (three_quarters_state_avg_rss_dict[state] > 100000):
            print("Cost > 100000, ", state)

if __name__ == "__main__":
    main()
