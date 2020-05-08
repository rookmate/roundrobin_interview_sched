import argparse
import itertools
import pandas as pd


def read_xls_to_dataframe(fp):
    read_file = pd.read_excel(fp, sheet_name='Poll', encoding='utf-8')
    read_file.to_csv(r'Doodle.csv', encoding='utf-8', index=None, header=True)

    doodle = pd.read_csv("Doodle.csv",
                         skiprows=3,
                         skip_blank_lines=True,
                         header=None,
                         encoding='utf-8',
                         squeeze=True,
                         keep_default_na=False
                         )[:-1]
    return doodle


def clean_date_data(df):
    patch_date = True
    ym = '' # Stores year/month
    wd = '' # Stores week/day
    for index, row in df.iterrows():
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

        # Patches the date to have the week/day and year/month
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
            break;
    # Creates new row to add
    new_row = pd.DataFrame(hour_segments, index=[0])
    # Deletes the previous split dates
    df = df.drop([0, 1, 2])
    # Concatenates at the top
    df = pd.concat([new_row, df]).reset_index(drop=True)
    return df


def get_interviewers_available(df):
    interviewers = {}
    for index, row in df.iterrows():
        # Skips empty lines of interviewers
        if row[0].strip() == '':
            continue
        # Stores availabilities for each user
        availabilities = {}
        for key, value in row[1:].to_dict().items():
            if value.strip() == '':
                continue
            availabilities[key] = df.iloc[0][key]

        availabilities = [(value) for key, value in availabilities.items()]
        interviewers[row[0]] = availabilities
    return interviewers


def get_cal_robin_dict(fp):
    # Doodle needs to be exported to xls
    # Parse xls to csv
    # TODO: need to be argument for argparse
    doodle = read_xls_to_dataframe(fp)
    doodle = clean_date_data(doodle)
    # Matches interviewers with available dates
    # Generate one dict with names as keys and availabilities as values
    interviewers = get_interviewers_available(doodle)
    # Number of interviews per candidate
    # TODO: need to be argument for argparse
    int_per_cand = 2
    # Pair up the interviewers
    roundrobin = list(itertools.combinations(interviewers.keys(), int_per_cand))
    # Match roundrobin with possible calendar availability
    robin_cal = {}
    for pair in roundrobin:
        calendar_intersect = list(set(interviewers[pair[0]])
                                  .intersection(interviewers[pair[1]])
                                  )
        robin_cal[pair] = calendar_intersect
    return robin_cal


if __name__ == "__main__":
    robin_cal = get_cal_robin_dict(r'Doodle.xls')
    # TODO: need to be argument for argparse
    # Number of Candidates
    num_candidates = 10
    for elem in robin_cal.items():
        print(elem)
    # TODO: Find a pretty way to display this info
