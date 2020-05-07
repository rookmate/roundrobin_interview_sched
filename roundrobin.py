import argparse
import itertools
import pandas as pd

import sys

if __name__ == "__main__":
    # Doodle needs to be exported to xls
    # Parse xls to csv
    read_file = pd.read_excel(r'Doodle.xls', sheet_name='Poll', encoding='utf-8')
    read_file.to_csv(r'Doodle.csv', encoding='utf-8', index=None, header=True)

    doodle = pd.read_csv("Doodle.csv",
                         skiprows=3,
                         skip_blank_lines=True,
                         header=None,
                         encoding='utf-8',
                         squeeze=True,
                         keep_default_na=False
                         )[:-1]

    interviewers = {}
    patch_date = True
    ym = '' # Stores year/month
    wd = '' # Stores week/day
    for index, row in doodle.iterrows():
        if index == 0:
            # Get year and month in variables
            year_month = row.to_dict()
            continue
        if index == 1:
            # Get days
            week_day = row.to_dict()
            continue
        if index == 2:
            # If empty match cycle with index 1, to add the date
            hour_segments = row.to_dict()
            continue

        if patch_date:
            for key, value in year_month.items():
                # Stores the year/month to use later
                if value != '':
                    ym = value
                # Stores week/day to use later
                if week_day[key] != '':
                    wd = week_day[key]
                else:
                    week_day[key] = wd
                hour_segments[key] = wd + ' ' + ym + ' ' + hour_segments[key]
            patch_date = False

        if row[0] == '':
            continue
        availabilities = row[1:].to_dict()
        for key, value in availabilities.items():
            if value == '':
                continue
            availabilities[key] = hour_segments[key]

        interviewers[row[0]] = availabilities

    for e in interviewers.items():
        print(e)

    print(hour_segments)
    #print(interviewers)
    #print(doodle)




    sys.exit()
    # Generate one dict with names as keys and availabilities as values
    # Number of interviews per candidate
    # TODO: need to be argument for argparse
    num_int_cand = 2
    # Pair up the interviewers
    roundrobin = list(itertools.combinations(interviewers.keys(), num_int_cand))
    print(roundrobin)
    # Match roundrobin with possible calendar availability
    for pair in roundrobin:
        calendar_intersect = list(set(interviewers[pair[0]])
                                  .intersection(interviewers[pair[1]])
                                  )
        print(pair, calendar_intersect)
